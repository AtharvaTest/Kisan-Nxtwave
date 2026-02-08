from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    name: str = Field(min_length=2)
    email: EmailStr
    password: str = Field(min_length=6)
    role: str
    department: str = ""
