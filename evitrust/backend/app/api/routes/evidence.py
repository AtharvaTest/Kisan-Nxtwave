from datetime import datetime, timezone

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile

from app.deps import ROLE_ADMIN, ROLE_FORENSIC, ROLE_JUDGE, ROLE_POLICE, assert_case_access, require_roles
from app.repositories.audit_repo import audit_repo
from app.repositories.case_repo import case_repo
from app.repositories.evidence_repo import evidence_repo
from app.services.audit_service import audit_service
from app.services.hashing_service import sha256_bytes
from app.services.merkle_service import update_case_merkle
from app.services.storage_service import storage_service
from app.utils.ids import new_id

router = APIRouter(tags=["evidence"])


@router.post("/cases/{case_id}/evidence/upload")
async def upload_evidence(
    case_id: str,
    type: str = Form(...),
    uploaded_by_name: str | None = Form(None),
    uploaded_by_email: str | None = Form(None),
    file: UploadFile = File(...),
    user=Depends(require_roles(ROLE_POLICE, ROLE_ADMIN)),
):
    c = case_repo.get(case_id)
    if not c:
        raise HTTPException(404, "Case not found")
    assert_case_access(case_id, user, write=True)

    blob = await file.read()
    digest = sha256_bytes(blob)
    dup_case = evidence_repo.find_duplicate_in_case(case_id, digest)
    dup_global = evidence_repo.find_duplicate_global(digest)
    if dup_case:
        audit_service.append_event(
            case_id,
            dup_case["_id"],
            "DUPLICATE_UPLOAD_ATTEMPT",
            {
                "sha256": digest,
                "existing_evidence_id": dup_case["_id"],
                "duplicate_global": bool(dup_global and dup_global["_id"] != dup_case["_id"]),
                "actor_user_id": user["_id"],
                "actor_role": user["role"],
                "actor_name": user["name"],
                "actor_email": user["email"],
            },
        )
        response = {"duplicate": True, "existing_evidence_id": dup_case["_id"]}
        if dup_global and dup_global["case_id"] != case_id and user["role"] in {ROLE_POLICE, ROLE_ADMIN}:
            response.update({"duplicate_global": True, "matched_case_id": dup_global["case_id"]})
        return response

    eid = new_id()
    ext = file.filename.split(".")[-1] if "." in file.filename else "bin"
    key = f"{case_id}/{eid}/original.{ext}"
    storage_service.upload_bytes(key, blob, file.content_type or "application/octet-stream")
    doc = {
        "_id": eid,
        "case_id": case_id,
        "type": type,
        "filename_original": file.filename,
        "mime_type": file.content_type,
        "file_size": len(blob),
        "storage": {"provider": "minio", "bucket": storage_service.bucket, "key": key},
        "sha256": digest,
        "uploaded_by": {"name": uploaded_by_name or user["name"], "email": uploaded_by_email or user["email"]},
        "uploaded_at": datetime.now(timezone.utc).isoformat(),
        "status": "UPLOADED",
        "analysis_version": "v1",
    }
    evidence_repo.create(doc)
    audit_service.append_event(
        case_id,
        eid,
        "UPLOAD",
        {
            "sha256": digest,
            "actor_user_id": user["_id"],
            "actor_role": user["role"],
            "actor_name": user["name"],
            "actor_email": user["email"],
        },
    )
    merkle_root, leaf_count = update_case_merkle(case_id, eid)
    audit_service.append_event(
        case_id,
        eid,
        "MERKLE_ROOT_UPDATED",
        {"merkle_root": merkle_root, "leaf_count": leaf_count, "changed_evidence_id": eid, "actor": "SYSTEM"},
    )
    return doc


@router.get("/evidence/{evidence_id}")
def get_evidence(evidence_id: str, user=Depends(require_roles(ROLE_POLICE, ROLE_FORENSIC, ROLE_JUDGE, ROLE_ADMIN))):
    d = evidence_repo.get(evidence_id)
    if not d:
        raise HTTPException(404, "Evidence not found")
    assert_case_access(d["case_id"], user)
    return d


@router.get("/evidence/{evidence_id}/download")
def get_download(evidence_id: str, user=Depends(require_roles(ROLE_POLICE, ROLE_FORENSIC, ROLE_JUDGE, ROLE_ADMIN))):
    d = evidence_repo.get(evidence_id)
    if not d:
        raise HTTPException(404, "Evidence not found")
    assert_case_access(d["case_id"], user)
    return {"url": storage_service.presigned_get(d["storage"]["key"])}


@router.get("/cases/{case_id}/evidence")
def list_case_evidence(case_id: str, user=Depends(require_roles(ROLE_POLICE, ROLE_FORENSIC, ROLE_JUDGE, ROLE_ADMIN))):
    assert_case_access(case_id, user)
    return evidence_repo.list_by_case(case_id)


@router.get("/evidence/{evidence_id}/verify")
def verify_evidence(evidence_id: str, user=Depends(require_roles(ROLE_POLICE, ROLE_FORENSIC, ROLE_JUDGE, ROLE_ADMIN))):
    ev = evidence_repo.get(evidence_id)
    events = audit_repo.by_evidence(evidence_id)
    if not ev or not events:
        raise HTTPException(404, "Verification data unavailable")
    assert_case_access(ev["case_id"], user)

    latest = events[-1]["entry_hash"]
    code = f"EVT-{ev['sha256'][:12].upper()}-{latest[-6:].upper()}"
    from app.db.mongo import db

    merkle = db.case_merkle.find_one({"_id": ev["case_id"]}) or {}
    return {
        "sha256": ev["sha256"],
        "latest_audit_hash": latest,
        "verification_code": code,
        "case_merkle_root": merkle.get("merkle_root"),
    }
