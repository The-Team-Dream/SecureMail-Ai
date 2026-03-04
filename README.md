# SecureMail-Ai
# 🛡️ SecureMail-Ai: AI-Powered Email Security Microservice

SecureMail-Ai is a containerized gRPC service designed to analyze potentially malicious emails. It leverages **LangGraph**, **Llama 3 (via Groq)**, and automated **DNS Analysis** to distinguish between genuine threats (Phishing, Typosquatting) and legitimate marketing communications.

---

## 🌟 Key Features
- **AI-Driven Analysis**: Uses a Senior SOC Analyst persona to evaluate email intent.
- **Infrastructure Validation**: Automated DNS lookups for SPF, MX, and TXT records via the `check_domain` tool.
- **Typosquatting Detection**: Identifies lookalike domains (e.g., `micros0ft.com`).
- **gRPC Interface**: High-performance communication for seamless integration into larger systems.
- **Dockerized Architecture**: Simplified deployment with one command.

## 🛠️ Tech Stack
- **AI/LLM**: LangGraph, LangChain-Groq (Llama-3.3-70b).
- **Framework**: Python 3.10-slim.
- **Communication**: gRPC & Protocol Buffers.
- **Deployment**: Docker & Docker Compose.

---

## 🚀 Getting Started

### Prerequisites
- Docker & Docker Compose.
- A Groq API Key.

### Installation
1. Clone the repository.
2. Create a `.env` file in the root directory:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
