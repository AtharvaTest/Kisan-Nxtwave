from pydantic import BaseModel

class AuditEventOut(BaseModel):
    event_type: str
    created_at: str
    entry_hash: str
