from datetime import datetime, timezone
from app.db.mongo import db
from app.services.hashing_service import sha256_text


def _root(hashes: list[str]) -> str | None:
    if not hashes:
        return None
    layer = hashes[:]
    while len(layer) > 1:
        nxt = []
        if len(layer) % 2:
            layer.append(layer[-1])
        for i in range(0, len(layer), 2):
            nxt.append(sha256_text(layer[i] + layer[i + 1]))
        layer = nxt
    return layer[0]


def update_case_merkle(case_id: str, changed_evidence_id: str):
    evs = list(db.evidence.find({"case_id": case_id}, {"_id": 1, "sha256": 1, "uploaded_at": 1}).sort("_id", 1))
    leaves = [{"evidence_id": e["_id"], "leaf_hash": sha256_text(e["_id"] + e["sha256"] + e["uploaded_at"])} for e in evs]
    root = _root([x["leaf_hash"] for x in leaves])
    doc = {"_id": case_id, "leaf_hashes": leaves, "merkle_root": root, "updated_at": datetime.now(timezone.utc).isoformat(), "version": 1}
    db.case_merkle.update_one({"_id": case_id}, {"$set": doc}, upsert=True)
    return root, len(leaves)
