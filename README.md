# 🛡️ SecureMail AI Agent (gRPC Microservice)

## 📌 Overview
The SecureMail AI Agent is a highly deterministic, containerized microservice built to analyze email telemetry and heuristical data. Powered by Groq LLMs (Llama-3) and LangChain, it acts as a core security analyst engine. It ingests static analysis data, threat scores, and backend rule hits, then maps them strictly to an actionable security report with predefined tiers (SAFE, SUSPICIOUS, DANGEROUS).

## 🏗️ Tech Stack
- **Language:** Python 3.11
- **Framework:** gRPC / Protobuf
- **AI Engine:** LangChain, Groq API (`llama-3.3-70b-versatile` / `llama-3.1-8b-instant`)
- **Infrastructure:** Docker & Docker Compose
- **Data Validation:** Pydantic (Structured Output)

## ⚙️ Prerequisites
To run this microservice, you need:
- Docker & Docker Compose installed.
- A valid [Groq API Key](https://console.groq.com/).

## 🚀 Quick Start (Deployment)

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd <your-repo-folder>
