#!/bin/bash

# ═══════════════════════════════════════════════════════════════
# SecureMail-Ai — Standalone Setup Script (Mac/Linux)
# Usage: chmod +x setup.sh && ./setup.sh
# ═══════════════════════════════════════════════════════════════

REPO_URL="https://github.com/The-Team-Dream/SecureMail-Ai"

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║       SecureMail-Ai Setup                ║"
echo "╚══════════════════════════════════════════╝"
echo ""

# ── 1. Check Docker ─────────────────────────────────────────────
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop first."
    exit 1
fi
echo "✅ Docker is running"
echo ""

# ── 2. Create .env.standalone from example ──────────────────────
if [ ! -f .env.standalone ]; then
    cp .env.standalone.example .env.standalone
    echo "✅ Created .env.standalone"
else
    echo "ℹ️  .env.standalone already exists — skipping copy"
fi
echo ""

# ── 3. Ask for Groq API Key ─────────────────────────────────────
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  GROQ API KEY SETUP"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  The AI service requires a Groq API key."
echo "  Get one free at: https://console.groq.com/keys"
echo ""
echo "  Press Enter to skip (service will start"
echo "  but analysis will fail without a key)"
echo ""
read -s -p "  Groq API Key: " groq_key
echo ""

if [ -z "$groq_key" ]; then
    echo "  ⚠️  No key provided — AI analysis will not work"
    echo "      Fill GROQ_API_KEY in .env.standalone later"
else
    sed -i "s/^GROQ_API_KEY=.*/GROQ_API_KEY=${groq_key}/" .env.standalone
    echo "  ✅ Groq API key written to .env.standalone"
fi
echo ""

# ── 4. Optional config reminder ─────────────────────────────────
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  ℹ️  OPTIONAL CONFIG (defaults are fine)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  AI_MAX_CONCURRENT=4    Max parallel analyses"
echo "  AI_MAX_BODY_CHARS=120000  Max email body size"
echo "  LOG_LEVEL=INFO"
echo ""
echo "  Edit .env.standalone to change these."
echo ""
echo "  📖 Full guide: $REPO_URL#readme"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
read -p "  Press Enter to start Docker..." _

# ── 5. Start Docker Compose ─────────────────────────────────────
echo ""
echo "🚀 Starting SecureMail-Ai..."
echo ""
docker compose down > /dev/null 2>&1
docker compose up --build -d

# ── 6. Wait for service to be healthy ───────────────────────────
echo ""
echo "⏳ Waiting for AI service to be ready..."
RETRIES=20
until docker compose logs ai 2>&1 | grep -q "gRPC listening"; do
    RETRIES=$((RETRIES - 1))
    if [ $RETRIES -eq 0 ]; then
        echo ""
        echo "❌ AI service failed to start. Check logs with:"
        echo "   docker compose logs ai"
        exit 1
    fi
    sleep 3
    echo "   still waiting..."
done

# ── 7. Done ─────────────────────────────────────────────────────
echo ""
echo "╔══════════════════════════════════════════╗"
echo "║       ✅ AI Service is running!          ║"
echo "╠══════════════════════════════════════════╣"
echo "║  gRPC: localhost:50051                   ║"
echo "╠══════════════════════════════════════════╣"
echo "║  Logs:  docker compose logs -f ai       ║"
echo "║  Stop:  docker compose down             ║"
echo "╚══════════════════════════════════════════╝"
echo ""
