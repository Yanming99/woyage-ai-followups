from typing import List, Optional, Literal
from pydantic import BaseModel, constr, field_validator

class GenerateFollowupsRequest(BaseModel):
    question: constr(strip_whitespace=True, min_length=3)
    answer: constr(strip_whitespace=True, min_length=3)
    role: Optional[constr(strip_whitespace=True, min_length=2)] = None
    interview_type: Optional[List[constr(strip_whitespace=True, min_length=2)]] = None

    @field_validator("interview_type", mode="before")
    @classmethod
    def normalize_interview_type(cls, v):
        if v is None:
            return None
        if isinstance(v, str):
            return [v]
        return v

class FollowupItem(BaseModel):
    question: str
    rationale: Optional[str] = None

class GenerateFollowupsResponseData(BaseModel):
    followup_questions: List[FollowupItem]

class Envelope(BaseModel):
    result: Literal["success", "error"]
    message: str
    data: Optional[GenerateFollowupsResponseData] = None
