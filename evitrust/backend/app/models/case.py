from pydantic import BaseModel, Field


class Actor(BaseModel):
    name: str
    email: str


class CaseCreate(BaseModel):
    title: str = Field(min_length=3)
    description: str | None = None


class CaseOut(BaseModel):
    id: str = Field(alias="_id")
    title: str
    description: str | None = None
    created_by: Actor
    created_at: str
    status: str

    class Config:
        populate_by_name = True
