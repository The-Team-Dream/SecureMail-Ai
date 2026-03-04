import json
from langchain_core.messages import HumanMessage
import grpc
from concurrent import futures
import time 
from app.graph import app 
import secure_mail_pb2
import secure_mail_pb2_grpc

class Email_anaylis(secure_mail_pb2_grpc.EmailGuardServicer):
    
    def ScanEmail(self, request, context):
        print("\n📥 Received email for analysis...")
        
        # 1. تشغيل الـ AI Agent
        inputs = {"messages": [HumanMessage(content=request.email_json)]}
        final_state = app.invoke(inputs)
        
        # 2. الحصول على كلام الـ AI مباشرة (من آخر رسالة في المحادثة)
        last_message_content = final_state["messages"][-1].content
        
        # 3. صائد الـ JSON: هنستخرج التقرير من النص غصب عن LangGraph
        final_verdict = {}
        try:
            start_idx = last_message_content.find('{')
            end_idx = last_message_content.rfind('}')
            
            if start_idx != -1 and end_idx != -1:
                clean_json_str = last_message_content[start_idx:end_idx+1]
                final_verdict = json.loads(clean_json_str)
                print("✅ JSON Extracted Successfully in Server!")
            else:
                print("⚠️ No JSON found in the final message.")
                final_verdict["Recommendation"] = last_message_content
        except Exception as e:
            print(f"⚠️ Parsing Error in Server: {e}")
            final_verdict["Recommendation"] = last_message_content

        # 4. تنظيف وتأكيد الأنواع (عشان الـ gRPC)
        title_safe = str(final_verdict.get("Title", "Analysis Completed (Text Only)"))
        verdict_safe = str(final_verdict.get("verdict", "Unknown"))
        severity_safe = str(final_verdict.get("severity", "Unknown"))
        recommendation_safe = str(final_verdict.get("Recommendation", "No specific recommendation."))
        
        try:
            confidence_safe = float(final_verdict.get("confidence", 0.0))
        except (ValueError, TypeError):
            confidence_safe = 0.0

        print("📤 Sending Full Report to Client...")
        
        # 5. إرسال التقرير للعميل
        return secure_mail_pb2.ScanResponse(
            Title=title_safe,
            verdict=verdict_safe,
            severity=severity_safe,
            confidence=confidence_safe,
            Recommendation=recommendation_safe
        )

def server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    secure_mail_pb2_grpc.add_EmailGuardServicer_to_server(Email_anaylis(), server)
    server.add_insecure_port('[::]:50051')
    print("Starting gRPC server on port 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    server()