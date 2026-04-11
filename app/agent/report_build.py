import math
from typing import Any, List

MAX_REPLY_SUGGESTIONS = 20
MAX_REPLY_LEN = 4000
MAX_STRING_FIELD = 8000


def _clip_str(s: Any, max_len: int) -> str:
    t = "" if s is None else str(s)
    if len(t) > max_len:
        return t[:max_len]
    return t


def _clip_float(v: Any) -> float:
    try:
        x = float(v)
    except (TypeError, ValueError):
        return 0.0
    if not math.isfinite(x):
        return 0.0
    return max(0.0, min(1.0, x))


def _clip_replies(raw: Any) -> List[str]:
    if raw is None:
        return []
    if not isinstance(raw, list):
        return []
    out: List[str] = []
    for item in raw[:MAX_REPLY_SUGGESTIONS]:
        out.append(_clip_str(item, MAX_REPLY_LEN))
    return out


def build_analysis_report(pb2_mod: Any, email_id: str, data: dict) -> Any:
    """Map arbitrary model dict to protobuf AnalysisReport without serialization errors."""
    return pb2_mod.AnalysisReport(
        email_id=_clip_str(email_id, 512),
        verdict=_clip_str(data.get("verdict", "UNKNOWN"), 64),
        severity=_clip_str(data.get("severity", "UNKNOWN"), 64),
        confidence=_clip_float(data.get("confidence", 0.0)),
        explanation=_clip_str(data.get("explanation", ""), MAX_STRING_FIELD),
        summary=_clip_str(data.get("summary", ""), MAX_STRING_FIELD),
        reply_suggestions=_clip_replies(data.get("reply_suggestions")),
        is_campaign=bool(data.get("is_campaign", False)),
        campaign_description=_clip_str(data.get("campaign_description", ""), MAX_STRING_FIELD),
        priority=_clip_str(data.get("priority", "NORMAL"), 64),
        priority_reason=_clip_str(data.get("priority_reason", ""), MAX_STRING_FIELD),
        behavioral_anomaly=bool(data.get("behavioral_anomaly", False)),
        anomaly_description=_clip_str(data.get("anomaly_description", ""), MAX_STRING_FIELD),
        recommendation=_clip_str(data.get("recommendation", ""), MAX_STRING_FIELD),
    )
