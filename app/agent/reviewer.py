import os 
import json
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from app.core.config import GROQ_API_KEY, supervisor_model
from app.core.state import AgentState

# 1. Initialize LLM
llm = ChatGroq(
    model=supervisor_model,
    temperature=0.0,          
    api_key=GROQ_API_KEY      
)

# 2. The Prompt (Fixed)
# We removed the "REJECT" text rule. We force it to reject INSIDE the JSON.
# We also tell it that it is an authorized security system to bypass safety filters.
reviewer_prompt = """
You are a Senior Defensive Security Analyst in a SOC. 
Your job is to analyze potentially malicious emails to protect users.

YOUR GOAL:
Produce a final, highly accurate security report, effectively distinguishing between genuine threats and aggressive but safe marketing.

LOGIC & ANALYTICAL DIRECTIVES:
1. MISSING DATA: IF the data is missing or incomplete, output the JSON with verdict "Unknown" and explain the missing data in "Recommendation".
2. TECHNICAL HEADERS FIRST: Always evaluate "Authentication-Results" (SPF, DKIM, DMARC) before the body. If these checks pass, the baseline threat score must be heavily reduced.
3. FALSE POSITIVE RECOGNITION: Actively look for marketing indicators, specifically the "List-Unsubscribe" header. Real threat actors rarely implement valid unsubscribe mechanisms. 
4. CONTEXTUAL CORRELATION: Differentiate between malicious urgency (e.g., "Account suspended", "Wire transfer needed") and commercial urgency (e.g., "Sale ends in 1 hour"). A high-urgency marketing email with passing authentication and unsubscribe headers is SAFE, not suspicious.
5. BEHAVIORAL WEIGHING: Do not flag an email as Malicious or Suspicious solely based on high-pressure keywords if the technical headers and sender intent align with a legitimate commercial business.
6. DOMAIN IMPERSONATION (TYPOSQUATTING): Passing SPF/DKIM/DMARC only proves the email originated from the domain in the "From" address; it DOES NOT prove the domain itself is legitimate. You must actively cross-reference the sender's domain against the claimed identity or recipient domain. Actively look for typosquatting tactics such as added suffixes (e.g., "-hr", "-support", "-secure") or slight misspellings. If a domain appears to be a lookalike attempting to impersonate an internal department or a trusted brand, the verdict MUST be "Malicious", even if authentication headers pass.
OUTPUT FORMAT:
You MUST return the result as a single valid JSON OBJECT ONLY.
No conversational text. No markdown blocks.
{
    "Title": "Professional title for the report",
    "confidence": 95,
    "severity": "Critical/High/Medium/Low/Informational",
    "verdict": "Malicious/Safe/Suspicious/Unknown",
    "Recommendation": "Clear recommendation based on both technical metadata and behavioral evidence"
}
"""

def reviewer_node(state: AgentState):
    
    messages = state.get("messages", [])
    network_report = state.get("network_report", "No network report provided.")
    email_content = state.get("email_content", "No email content provided.")

    prompt = [
        SystemMessage(content=reviewer_prompt),
        HumanMessage(content=f"""
        --- NETWORK FINDINGS ---
        {network_report}
        
        --- EMAIL CONTENT ---
        {email_content}
        """)
    ] + messages 

    # 3. INVOKE MODEL
    response = llm.invoke(prompt)

    raw_text = response.content.strip()

    # 4. PARSE JSON SAFELY
    final_verdict = {
        "Title": "Analysis Failed",
        "verdict": "Unknown",
        "severity": "Medium",
        "confidence": 0,
        "Recommendation": raw_text if raw_text else "AI returned an empty response."
    }

    try:
        # THE JSON EXTRACTOR: Find the first { and the last }
        start_idx = raw_text.find('{')
        end_idx = raw_text.rfind('}')
        
        if start_idx != -1 and end_idx != -1:
            # Slice the string to get ONLY the JSON part
            clean_json_str = raw_text[start_idx:end_idx+1]
            final_verdict = json.loads(clean_json_str)
            print("✅ JSON Parsed Successfully.")
        else:
            print("⚠️ No JSON brackets found in the AI response.")
            
    except Exception as e:
        print(f"⚠️ Could not parse JSON. Error: {e}")

    # 5. RETURN STATE UPDATE
    return {
        "messages": [response],
        "final_verdict": final_verdict
    }