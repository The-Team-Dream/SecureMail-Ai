# SecureMail AI (gRPC service)

Python microservice that exposes **gRPC** method `GenerateReport` for email security analysis. It consumes structured telemetry from the Nest backend (rule hits, scores, body text, etc.), calls **Groq** via LangChain with structured output, and returns a protobuf **AnalysisReport**.

## Tech stack

- Python **3.11**
- **gRPC** + protobuf (generated stubs from repo root `contracts/ai-agent.proto`)
- **LangChain** + **ChatGroq**
- **Pydantic** (structured LLM output)
- **Docker** (see repo root `docker-compose.yml`)

## Ports

| Variable / default | Port |
|--------------------|------|
| `GRPC_PORT` (default `50051`) | gRPC listen port |

Inside Docker Compose the service is reachable as **`ai:50051`** from the backend.

## Environment variables

| Variable | Required | Purpose |
|----------|----------|---------|
| `GROQ_API_KEY` | **Yes** (for real analysis) | Groq API key |
| `GRPC_PORT` | No | Listen port (default `50051`) |
| `AI_MAX_BODY_CHARS` | No | Max `body_text` length accepted |
| `AI_MAX_CONCURRENT` | No | Concurrent analyses (semaphore) |
| `AI_SLOT_ACQUIRE_TIMEOUT_S` | No | Wait for a free slot |
| `AI_GRPC_MAX_MSG_MB` | No | gRPC max message size |

## Regenerating protobuf stubs

When `contracts/ai-agent.proto` changes, regenerate Python files from the **monorepo root**:

```bash
python -m grpc_tools.protoc -I contracts \
  --python_out=SecureMail-Ai/app/protos \
  --grpc_python_out=SecureMail-Ai/app/protos \
  contracts/ai-agent.proto
```

(On Windows you can use `SecureMail-Ai/tools/regen_proto.ps1` if present.)

## Run locally (step-by-step)

1. Python 3.11+, `pip`.
2. Create a virtualenv (recommended):
   ```bash
   cd SecureMail-Ai
   python -m venv .venv
   .venv\Scripts\activate   # Windows
   # source .venv/bin/activate  # macOS/Linux
   ```
3. Install deps:
   ```bash
   pip install -r requirements.txt
   ```
4. Set `GROQ_API_KEY` in `.env` or environment.
5. From `SecureMail-Ai/app`:
   ```bash
   python main.py
   ```
6. gRPC listens on `0.0.0.0:50051` by default.

Point the backend at `AI_AGENT_GRPC_URL=localhost:50051`.

## Run with Docker

From **monorepo root**:

```bash
docker compose up --build ai
```

Or full stack: see root [README.md](../README.md).

**Dockerfile path:** `SecureMail-Ai/Dockerfile` (context = repo root).

## API (gRPC — not HTTP)

This service does **not** expose Swagger. Contract is defined in:

- **`contracts/ai-agent.proto`** (shared with Nest gRPC client)

Package: `aiagent`  
Service: `AIAgentService`  
RPC: `GenerateReport(EmailAnalysisRequest) returns (AnalysisReport)`

Backend developers document REST; AI contract is the `.proto` file and generated stubs.

## Troubleshooting

| Issue | What to check |
|-------|----------------|
| `GROQ_API_KEY` errors | Key set in env; quota / network. |
| `RESOURCE_EXHAUSTED` from gRPC | Too many concurrent requests; raise `AI_MAX_CONCURRENT` or scale. |
| `INVALID_ARGUMENT` on body | Email body exceeds `AI_MAX_BODY_CHARS`. |
| Version mismatch warnings | Align `grpcio` / `grpcio-tools` with generated code (see `requirements.txt` / Dockerfile). |

## Related docs

- [Monorepo README](../README.md) — full stack, ports, Compose
- [Backend README](../SecureMail-Backend/README.md) — REST + Swagger URLs
