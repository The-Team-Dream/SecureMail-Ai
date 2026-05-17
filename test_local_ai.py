import sys
import os
import json

# Add the 'app' directory to the path so we can import modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from agent.brain import analyze_email

dummy_payload = {
    "email_id": "test-local-123",
    "subject": "Urgent: Reset your password",
    "from_addr": "security@paypal-update.com",
    "from_name": "PayPal Support",
    "body_text": "Dear customer, your account has been locked. Click here to reset your password and OTP immediately.",
    "spam_score": 0.9,
    "phishing_score": 0.95,
    "is_spam": True,
    "is_phishing": True,
    "rule_hits": ["credential_harvesting_attempt", "lookalike_domain_attack"],
    "has_attachment": False,
    "malware_verdict": "clean",
    "mailbox_id": 1,
    "previous_email_count": 0,
    "sender_typical_topic": "none"
}

print("Sending test payload to local Llama 3.1:8b model via Ollama...")
try:
    result = analyze_email(dummy_payload)
    print("\n[SUCCESS] AI responded:")
    # Handle pydantic model output or dict
    if hasattr(result, 'model_dump_json'):
        print(result.model_dump_json(indent=2))
    elif hasattr(result, 'json'):
        print(result.json(indent=2))
    else:
        print(json.dumps(result, indent=2, default=str))
except Exception as e:
    print(f"\n[FAILED] {e}")
