from pydantic import BaseModel, Field


class DecisionCreate(BaseModel):
    decision: str
    comment: str = Field(min_length=5)
