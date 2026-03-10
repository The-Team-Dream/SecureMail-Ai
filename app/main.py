import sys
import os
import grpc
import json
from concurrent import futures
from dotenv import load_dotenv

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
sys.path.append(os.path.join(current_dir, 'protos'))

import protos.secure_mail_pb2 as pb2
import protos.secure_mail_pb2_grpc as pb2_grpc

from agent.brain import analyze_email

load_dotenv()

class AIAgentService(pb2_grpc.AIAgentServiceServicer):
    def GenerateReport(self, request, context):
        print(f"\n[*] 📥 Received new analysis request for Email ID: {request.email_id}")
        
        try:
            # تحويل البيانات لقاموس Dictionary
            rule_hits_list = [
                {"rule": rh.rule, "score": rh.score, "description": rh.description} 
                for rh in request.rule_hits
            ]
            
            payload_dict = {
                "email_id": request.email_id,
                "subject": request.subject,
                "from_addr": request.from_addr,
                "from_name": request.from_name,
                "body_text": request.body_text,
                "spam_score": request.spam_score,
                "phishing_score": request.phishing_score,
                "is_spam": request.is_spam,
                "is_phishing": request.is_phishing,
                "rule_hits": rule_hits_list,
                "has_attachment": request.has_attachment,
                "malware_verdict": request.malware_verdict,
                "malware_score": request.malware_score,
                "malware_severity": request.malware_severity,
                "mailbox_id": request.mailbox_id,
                "previous_email_count": request.previous_email_count,
                "sender_typical_topic": request.sender_typical_topic
            }

            
            # استدعاء الـ Agent
            ai_result = analyze_email(payload_dict)
            
            # التأكد من تحويل النتيجة لـ dict لو كانت Object
            if hasattr(ai_result, 'model_dump'):
                ai_result = ai_result.model_dump()
            elif hasattr(ai_result, 'dict'):
                ai_result = ai_result.dict()
            # بناء الرد النهائي للتيم ليدر
            return pb2.AnalysisReport(
                email_id=request.email_id,
                verdict=str(ai_result.get("verdict", "UNKNOWN")),
                severity=str(ai_result.get("severity", "UNKNOWN")),
                confidence=float(ai_result.get("confidence", 0.0)),
                explanation=str(ai_result.get("explanation", "")),
                summary=str(ai_result.get("summary", "")),
                reply_suggestions=list(ai_result.get("reply_suggestions", [])),
                is_campaign=bool(ai_result.get("is_campaign", False)),
                campaign_description=str(ai_result.get("campaign_description", "")),
                priority=str(ai_result.get("priority", "NORMAL")),
                priority_reason=str(ai_result.get("priority_reason", "")),
                behavioral_anomaly=bool(ai_result.get("behavioral_anomaly", False)),
                anomaly_description=str(ai_result.get("anomaly_description", "")),
                recommendation=str(ai_result.get("recommendation", ""))
            )
            
        except Exception as e:
            print(f"[!] ❌ Error: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return pb2.AnalysisReport()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_AIAgentServiceServicer_to_server(AIAgentService(), server)
    server.add_insecure_port("0.0.0.0:50051")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()