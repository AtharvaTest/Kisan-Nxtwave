import json
from datetime import datetime, timezone
from app.utils.ids import new_id
from app.services.hashing_service import sha256_text
from app.services.signing_service import signing_service
from app.repositories.audit_repo import audit_repo

class AuditService:
    def append_event(self, case_id: str, evidence_id: str | None, event_type: str, payload: dict):
        now = datetime.now(timezone.utc).isoformat()
        prev = audit_repo.latest_by_case(case_id)
        prev_hash = prev["entry_hash"] if prev else None
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        entry_hash = sha256_text((prev_hash or "") + event_type + canonical + now)
        sig = signing_service.sign_hex_hash(entry_hash)
        doc = {
            "_id": new_id(),
            "case_id": case_id,
            "evidence_id": evidence_id,
            "event_type": event_type,
            "event_payload": payload,
            "prev_hash": prev_hash,
            "entry_hash": entry_hash,
            "signature": sig,
            "created_at": now,
        }
        return audit_repo.append(doc)

audit_service = AuditService()
