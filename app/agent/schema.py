from typing import List

from pydantic import BaseModel, ConfigDict, Field


class EmailAnalysisReport(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    email_id: str = Field(
        ...,
        description="The exact email_id extracted from the input payload.",
    )
    verdict: str = Field(
        ...,
        description="The final decision. MUST be exactly one of: 'SAFE', 'SUSPICIOUS', or 'DANGEROUS'.",
    )
    severity: str = Field(
        ...,
        description="The threat level. MUST be exactly one of: 'LOW', 'MEDIUM', 'HIGH', or 'CRITICAL'.",
    )
    confidence: float = Field(
        ...,
        description="Confidence 0.0–1.0.",
    )
    explanation: str = Field(
        ...,
        description="Why this verdict was reached, based on rule_hits and scores.",
    )
    summary: str = Field(
        ...,
        description="A short 1–2 sentence summary of the email's core intent.",
    )
    reply_suggestions: List[str] = Field(
        ...,
        description="Exactly 2 drafted replies; defensive if threat, professional if safe.",
    )
    priority: str = Field(
        ...,
        description="One of: 'LOW', 'NORMAL', 'HIGH', 'URGENT'.",
    )
    priority_reason: str = Field(
        ...,
        description="Short reason for the assigned priority.",
    )
    behavioral_anomaly: bool = Field(
        ...,
        description="Native boolean per behavioral rules.",
    )
    anomaly_description: str = Field(
        ...,
        description="If anomaly is false, use: No behavioral anomalies detected.",
    )
    recommendation: str = Field(
        ...,
        description="Actionable recommendation for the user.",
    )
    is_campaign: bool = Field(
        ...,
        description="True if mass phishing/spam/marketing campaign patterns.",
    )
    campaign_description: str = Field(
        ...,
        description="Campaign description or 'Not applicable' if is_campaign is false.",
    )
