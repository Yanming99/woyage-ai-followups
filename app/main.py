from fastapi import FastAPI
from openai import OpenAI, RateLimitError

app = FastAPI(title="Woyage Followups API")

@app.get("/health", tags=["System"])
async def health_check():
    """Check OpenAI connectivity and quota status."""
    try:
        client = OpenAI()
        r = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Reply ONLY JSON: {\"ping\": \"pong\"}"}],
            temperature=0.1,
            max_tokens=20,
            timeout=10,
        )
        return {
            "status": "ok",
            "message": "√ OpenAI API test successful!",
            "model_reply": r.choices[0].message.content,
        }

    except RateLimitError:
        return {
            "status": "ok",
            "message": "√ OpenAI API reachable, but usage quota exceeded.",
            "note": "💡 Please add a payment method or recharge your account to continue using the API.",
            "billing_url": "https://platform.openai.com/account/billing",
        }

    except Exception:
        return {
            "status": "ok",
            "message": "√ OpenAI API reachable, Verify your billing and API key settings.",
            "note": "💡 Verify your billing and API key settings.",
            "billing_url": "https://platform.openai.com/account/billing",
        }
