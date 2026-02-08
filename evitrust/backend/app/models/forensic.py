from pydantic import BaseModel, Field


class ForensicNoteCreate(BaseModel):
    note_text: str = Field(min_length=5)
    recommendation: str
