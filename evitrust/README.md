# EviTrust — Digital Evidence Integrity & Trustworthiness Pipeline

EviTrust is a demo-ready, trust-first digital evidence platform focused on:
- Explainability (XAI)
- Human-in-the-loop workflows
- Accountability via signed, hash-chained audit logs

## Stack
- FastAPI API + Celery worker
- MongoDB for metadata
- MinIO for binary media/artifacts/reports
- Redis as Celery broker/result backend
- React (Vite) frontend

## One-command startup
```bash
docker compose up --build
```

## Services
- `frontend`: React UI on `5173`
- `api`: FastAPI on `8000`
- `worker`: Celery background jobs
- `mongo`: MongoDB
- `redis`: Redis
- `minio`: S3-compatible object storage

## Trust Guarantees
- Immutable append-only audit trail with SHA-256 hash chaining
- Ed25519 signatures for each audit entry
- File SHA-256 persisted at ingestion
- Duplicate SHA-256 detection within case and globally
- Case-level Merkle root snapshots

## Demo Credentials
Seed users can be created by hitting the admin register endpoint or by direct DB insert.

## Notes
This scaffold is production-oriented but simplified for demo speed.
