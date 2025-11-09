import os
from openai import OpenAI, RateLimitError

print("Has KEY:", bool(os.getenv("OPENAI_API_KEY")))

try:
    client = OpenAI()
    r = client.chat.completions.create(
        model=os.getenv("MODEL_NAME", "gpt-4o-mini"),
        messages=[{"role": "user", "content": "Reply ONLY JSON: {\"ping\": \"pong\"}"}],
        temperature=0.1,
        max_tokens=20,
        timeout=12,
    )
    print("√ OpenAI API test successful!")
    print("Model says:", r.choices[0].message.content)

except RateLimitError:
    print("√ OpenAI API reachable, but usage quota exceeded.")
    print("💡 Please add a payment method or recharge your account to continue using the API.")
    print("👉 Visit: https://platform.openai.com/account/billing")

except Exception:
    print("√ OpenAI API reachable, but an unknown error occurred.")
    print("💡 If this persists, please verify your billing and API key settings.")
    print("👉 Visit: https://platform.openai.com/account/billing")
