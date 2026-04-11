import json
import logging
import os
import sys
import threading
from concurrent import futures

import grpc
from dotenv import load_dotenv

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, "protos"))

import ai_agent_pb2 as pb2
import ai_agent_pb2_grpc as pb2_grpc

from agent.brain import analyze_email
from agent.report_build import build_analysis_report

load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

MAX_BODY_CHARS = max(4096, int(os.getenv("AI_MAX_BODY_CHARS", "120000")))
MAX_CONCURRENT = max(1, int(os.getenv("AI_MAX_CONCURRENT", "4")))
ACQUIRE_TIMEOUT_S = float(os.getenv("AI_SLOT_ACQUIRE_TIMEOUT_S", "30"))

_GRPC_MAX_MB = int(os.getenv("AI_GRPC_MAX_MSG_MB", "8"))
_GRPC_OPTIONS = [
    ("grpc.max_send_message_length", _GRPC_MAX_MB * 1024 * 1024),
    ("grpc.max_receive_message_length", _GRPC_MAX_MB * 1024 * 1024),
]

_slot = threading.BoundedSemaphore(MAX_CONCURRENT)


class AIAgentService(pb2_grpc.AIAgentServiceServicer):
    def GenerateReport(self, request, context):
        eid = request.email_id
        logger.info("AI GenerateReport email_id=%s", eid)

        if len(request.body_text) > MAX_BODY_CHARS:
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                f"body_text exceeds {MAX_BODY_CHARS} characters",
            )

        if not _slot.acquire(timeout=ACQUIRE_TIMEOUT_S):
            context.abort(
                grpc.StatusCode.RESOURCE_EXHAUSTED,
                "AI analysis capacity saturated; retry later",
            )

        try:
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
                "sender_typical_topic": request.sender_typical_topic,
            }

            ai_result = analyze_email(payload_dict)

            if hasattr(ai_result, "model_dump"):
                ai_result = ai_result.model_dump()
            elif hasattr(ai_result, "dict"):
                ai_result = ai_result.dict()

            if not isinstance(ai_result, dict):
                raise TypeError("analyze_email must return dict or Pydantic model")

            return build_analysis_report(pb2, request.email_id, ai_result)

        except grpc.RpcError:
            raise
        except Exception as e:
            logger.exception("AI GenerateReport failed email_id=%s", eid)
            context.abort(grpc.StatusCode.INTERNAL, str(e)[:2000])
        finally:
            _slot.release()


def serve():
    pool = futures.ThreadPoolExecutor(max_workers=max(4, MAX_CONCURRENT * 2))
    server = grpc.server(pool, options=_GRPC_OPTIONS)
    pb2_grpc.add_AIAgentServiceServicer_to_server(AIAgentService(), server)
    port = os.getenv("GRPC_PORT", "50051")
    bind = f"0.0.0.0:{port}"
    server.add_insecure_port(bind)
    server.start()
    logger.info("AI gRPC listening on %s (max concurrent analyses=%s)", bind, MAX_CONCURRENT)
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
