# Woyage AI Followup Generator

A FastAPI service that generates follow-up interview questions using OpenAI API.

## Features

- `POST /interview/generate-followups`
  - Generates 1–3 concise, contextual follow-up questions
  - Accepts question, answer, role, and interview types
  - Validated request/response schema using Pydantic
- `GET /health`
  - Verifies OpenAI API connectivity
  - If quota/credit is exceeded, returns a **friendly ✓ message + recharge hint** (no hard crash)
- JSON-based contract with a clean `Envelope` structure:
  - `result`: `"success"` / `"error"`
  - `message`: human-readable status
  - `data.followup_questions[]`: `question` + optional `rationale`
- Swagger UI auto-generated at `/docs`
- Production-style layout: separated config, schemas, services

---

## ⚙️ Setup & Run

Install dependencies (recommended in a virtual env, but optional):

```bash
pip install -r requirements.txt
📚 Interactive Docs

Swagger UI: http://127.0.0.1:8000/docs

Health check: http://127.0.0.1:8000/health

🔑 Environment Variables

Set your OpenAI API key (project-based keys supported):

export OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxx
export MODEL_NAME=gpt-4o-mini


Or put them in a .env file (loaded via pydantic-settings):

OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxx
MODEL_NAME=gpt-4o-mini

💬 Main Endpoint
POST /interview/generate-followups

Request body:

{
  "question": "Tell me about a time you handled conflicting priorities.",
  "answer": "Two urgent client requests collided last quarter. I coordinated with sales and support, prioritized SLA risk, and shipped a hotfix within 24h while queuing the second for next sprint.",
  "role": "Senior Backend Engineer",
  "interview_type": ["Behavioral interview"]
}


Successful response example:

{
  "result": "success",
  "message": "Follow-up question generated.",
  "data": {
    "followup_questions": [
      {
        "question": "Could you walk me through your decision-making steps and trade-offs in more detail?",
        "rationale": "Ensures clarity on reasoning and constraints."
      }
    ]
  }
}

💡 Health Check
GET /health

Calls OpenAI with a tiny test prompt.

If successful → returns status: "ok" and the model reply.

If quota/credit is exceeded → still returns 200 with a ✓ message and billing hint.

If any unexpected error → returns 200 with a generic ✓ + guidance.

Example (quota exceeded) response:

{
  "status": "ok",
  "message": "√ OpenAI API reachable, but usage quota exceeded.",
  "note": "💡 Please add a payment method or recharge your account to continue using the API.",
  "billing_url": "https://platform.openai.com/account/billing"
}


This avoids noisy stack traces while clearly indicating what to do next.

🧱 Project Structure
woyage-ai-followups/
│
├── app/
│   ├── __init__.py
│   ├── main.py               # FastAPI app, routes, health check
│   ├── config.py             # Settings (model name, etc.)
│   ├── schemas.py            # Request/response models & envelope
│   ├── prompts.py            # (Optional) prompt constants
│   └── services/
│       ├── __init__.py
│       └── generator.py      # OpenAI call, JSON parsing, retry & fallback
│
├── requirements.txt
├── README.md
└── .gitignore

🧪 Example cURL
curl -X 'POST' \
  'http://127.0.0.1:8000/interview/generate-followups' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "question": "Describe a time you led a project under pressure.",
    "answer": "I took ownership of a failing internal dashboard rebuild and aligned stakeholders...",
    "role": "Engineering Manager",
    "interview_type": ["Behavioral interview"]
}'

🧾 Requirements (requirements.txt)
fastapi==0.121.1
uvicorn==0.38.0
pydantic==2.12.4
pydantic-settings==2.11.0
httpx==0.28.1
openai==1.51.0

🏁 Notes

Built for Woyage AI coding exercise

Clean, explicit API contract

Clear separation of concerns (schemas, services, config)

Safe OpenAI integration with retry & robust JSON parsing

Friendly behavior when OpenAI billing/quota is not active (no hard failures)

🧑‍💻 Author

Yanming Luo
UC Davis · Computer Science
GitHub: @Yanming99
