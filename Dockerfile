# ════════════════════════════════════════════════════════════════════════════
# SecureMail-Ai — Multi-stage Dockerfile
# Service: AI Agent gRPC Server (Python 3.11)
# Port:    50051
# ════════════════════════════════════════════════════════════════════════════

# ── Stage 1: Install Python dependencies into an isolated layer ──────────────
FROM python:3.11-slim AS builder

WORKDIR /install

# Copy only requirements for cache efficiency
COPY requirements.txt .

# Install all deps into /install/packages (no cache to keep image lean)
RUN pip install --no-cache-dir --target /install/packages -r requirements.txt


# ── Stage 2: Minimal production runtime ─────────────────────────────────────
FROM python:3.11-slim AS runtime

WORKDIR /app

# Copy installed packages from builder stage
COPY --from=builder /install/packages /usr/local/lib/python3.11/site-packages/

# Copy application source code
# Note: app/protos/ contains pre-generated gRPC stubs — no protoc needed at runtime
COPY app/ ./app/

# Copy proto contracts (source of truth, for reference)
COPY contracts/ ./contracts/

# Non-root user for security
RUN addgroup --system grpcgroup && adduser --system --ingroup grpcgroup grpcuser
USER grpcuser

# gRPC port
EXPOSE 50051

# Environment defaults (overridden by .env.standalone or .env.docker)
ENV AI_PORT=50051 \
    AI_MAX_CONCURRENT=4 \
    AI_MAX_BODY_CHARS=120000 \
    LOG_LEVEL=INFO \
    PYTHONUNBUFFERED=1

CMD ["python", "app/main.py"]
