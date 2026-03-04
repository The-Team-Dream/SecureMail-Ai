import os 
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent 
from app.tools.check_domain import check_domain
from app.core.config import GROQ_API_KEY,WORK_Model

llm = ChatGroq(
    model=WORK_Model,
    temperature=0.0,          
    api_key=GROQ_API_KEY      
)

system_prompt = """
You are a Network Security Specialist.
Your task is to validate the sender's domain using the `check_domain` tool.
Analyze the SPF and DMARC records strictly.

IMPORTANT:
At the end of your analysis, you MUST provide a "Technical Verdict" based on your findings.
- If records are missing/failed -> Verdict: Malicious/Suspicious
- If records are valid -> Verdict: Safe
"""

network_agent=create_react_agent(
    model=llm,
    tools=[check_domain],
    prompt=system_prompt
)

def network_node(state):
    result=network_agent.invoke(state)

    return{
        "messages":[result["messages"][-1]]
    }