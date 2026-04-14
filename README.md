# SecureMail AI (Python)

A gRPC microservice providing email security analysis using LangChain and Groq.

## ✅ Run Options

### 1. Via Turborepo (Root)
Run this service along with the Backend:
```bash
npm run dev:api
```

### 2. Manual Execution
Requires Python 3.14+ (compatible with 3.11+).

1. **Environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Or .venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```
2. **Settings**: Create a `.env` file and add your `GROQ_API_KEY`.
3. **Run**:
   ```bash
   python app/main.py
   ```

## ⚙️ Configuration
- **Port**: `50051` (gRPC)
- **Key**: `GROQ_API_KEY` is required for analysis to succeed.

---

## 🏗️ Synchronization
This service uses Protobuf stubs generated from `contracts/ai-agent.proto`. To regenerate stubs after a contract change:
```bash
# From root
npx turbo run dev --filter=ai
```
(Or use the local `tools/regen_proto.ps1` on Windows).
