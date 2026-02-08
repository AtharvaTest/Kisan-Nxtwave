from pydantic import BaseModel, Field


class EvidenceOut(BaseModel):
    id: str = Field(alias="_id")
    case_id: str
    type: str
    filename_original: str
    mime_type: str | None = None
    file_size: int
    sha256: str
    status: str
    analysis_version: str

    class Config:
        populate_by_name = True


class VerifyOut(BaseModel):
    sha256: str
    latest_audit_hash: str
    verification_code: str
    case_merkle_root: str | None = None
