from pydantic import BaseModel


class CaseAssignCreate(BaseModel):
    assigned_to_user_id: str
    role_in_case: str
