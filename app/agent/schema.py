from pydantic import BaseModel, Field
from typing import List

class EmailAnalysisReport(BaseModel):
    email_id: str = Field(...,
        description="The exact email_id extracted from the input payload."
    )
    verdict: str = Field(
        description="The final decision. MUST be exactly one of: 'SAFE', 'SUSPICIOUS', or 'DANGEROUS'."
    )
    severity: str = Field(...,
        description="The threat level. MUST be exactly one of: 'LOW', 'MEDIUM', 'HIGH', or 'CRITICAL'."
    )
    confidence: float = Field(...,
        description="The model's confidence in its verdict, represented as a float between 0.0 and 1.0 (e.g., 0.93)."
    )
    explanation: str = Field(...,
        description="A clear, user-friendly explanation of WHY this verdict was reached, based on the 'rule_hits' and scores"
    )
    summary: str = Field(
        description="A short 1-2 sentence summary of the email's core intent."
    )
    reply_suggestions: List[str] = Field(...,
        description="An array of 1-2 suggested replies . If verdict is SAFE, suggest normal replies. If DANGEROUS/SUSPICIOUS, suggest ONLY defensive replies (e.g., contacting official support) or leave empty."
    )
    priority: str = Field(...,
        description="Action priority. MUST be exactly one of: 'LOW', 'NORMAL', 'HIGH', or 'URGENT'."
    )
    priority_reason: str = Field(...,
        description="A short reason for the assigned priority level."
    )
    behavioral_anomaly: bool = Field(...,
        description="MUST be a native JSON boolean (true or false). Do NOT use strings like 'true' or 'false'. ")
    anomaly_description: str = Field(...,
        description="An explanation of the behavioral anomaly analysis. If anomaly is true, explain why. If false, state that behavior is normal."
    )
    recommendation: str = Field(...,
        description="A direct, actionable recommendation for the user (e.g., 'Do not click links', 'Safe to reply')."
    )
    is_campaign: bool = Field(...,
        description="MUST be a native JSON boolean. Set to true if the email looks like a mass phishing, spam, or marketing campaign."
    )
    campaign_description: str = Field(...,
        description="Briefly describe the campaign (e.g., 'Mass credential harvesting campaign'). If is_campaign is false, output 'Not applicable'."
    )