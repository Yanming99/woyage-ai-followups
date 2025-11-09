from __future__ import annotations
from typing import List, Optional
import json, os, re, time
from openai import OpenAI, APIError, RateLimitError, APITimeoutError
from app.schemas import FollowupItem

MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
TIMEOUT_SECS = 12
MAX_RETRIES = 3

SYSTEM_PROMPT = """
You are a senior interview coach. Based on the given interview question and candidate answer,
produce 1–3 concise follow-up questions (<=140 chars each). Each may include an optional one-sentence rationale.
Avoid sensitive or discriminatory topics (e.g., age, religion, family, health).
Output strictly JSON:
{
  "followup_questions": [
    {"question": "...", "rationale": "..."},
    ...
  ]
}
"""

def _build_user_prompt(question: str, answer: str, role: Optional[str], interview_type: Optional[list[str]]) -> str:
    role_line = f"Role: {role}\n" if role else ""
    it_line = f"Interview Types: {', '.join(interview_type)}\n" if interview_type else ""
    return (
        f"{role_line}{it_line}"
        f"Original Question:\n{question}\n\n"
        f"Candidate Answer:\n{answer}\n\n"
        "Requirements:\n"
        "- Ask 1–3 specific, actionable follow-ups.\n"
        "- Focus on ambiguities, risks, or quantifiable outcomes.\n"
        "- Keep each question <= 140 chars; rationale <= 120 chars.\n"
        "- Return STRICT JSON only (no markdown or prose).\n"
    )

def _parse_json_strict(s: str) -> list[FollowupItem]:
    try:
        obj = json.loads(s)
        items = obj.get("followup_questions", [])
        return [
            FollowupItem(
                question=(it.get("question") or "").strip()[:140],
                rationale=(it.get("rationale") or "").strip()[:120] if it.get("rationale") else None,
            )
            for it in items if (it.get("question") or "").strip()
        ]
    except Exception:
        pass

    m = re.search(r"\{.*\}", s, re.DOTALL)
    if m:
        try:
            obj = json.loads(m.group(0))
            items = obj.get("followup_questions", [])
            return [
                FollowupItem(
                    question=(it.get("question") or "").strip()[:140],
                    rationale=(it.get("rationale") or "").strip()[:120] if it.get("rationale") else None,
                )
                for it in items if (it.get("question") or "").strip()
            ]
        except Exception:
            pass

    lines = [ln.strip("-• ").strip() for ln in s.splitlines() if ln.strip()]
    return [FollowupItem(question=ln[:140]) for ln in lines if ln.endswith("?")][:3]

def _call_openai(messages: list[dict]) -> str:
    client = OpenAI()
    last_err = None
    for i in range(MAX_RETRIES):
        try:
            resp = client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
                temperature=0.4,
                max_tokens=400,
                timeout=TIMEOUT_SECS,
            )
            return resp.choices[0].message.content or ""
        except (RateLimitError, APITimeoutError, APIError) as e:
            last_err = e
            time.sleep(0.5 * (2**i))
        except Exception as e:
            last_err = e
            break
    raise RuntimeError(f"OpenAI call failed after retries: {last_err}")

def generate_followups(
    question: str,
    answer: str,
    role: Optional[str],
    interview_type: Optional[list[str]],
) -> List[FollowupItem]:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": _build_user_prompt(question, answer, role, interview_type)},
    ]
    try:
        content = _call_openai(messages)
        items = _parse_json_strict(content)
        if items:
            seen, out = set(), []
            for it in items:
                key = it.question.lower().strip(" ?.!，。！？")
                if key and key not in seen:
                    seen.add(key)
                    out.append(it)
                if len(out) >= 3:
                    break
            if out:
                return out
    except Exception:
        pass

    return [
        FollowupItem(
            question="Could you walk me through your decision-making steps and trade-offs in more detail?",
            rationale="Ensures clarity on reasoning and constraints."
        )
    ]
