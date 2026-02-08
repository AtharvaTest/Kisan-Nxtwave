from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from app.services.storage_service import storage_service

class ReportService:
    def build_pdf(self, evidence: dict, analysis: dict, latest_audit_hash: str, verification_code: str, merkle_root: str):
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        y = 800
        for line in [
            "EviTrust Evidence Report",
            f"Evidence ID: {evidence['_id']}",
            f"Verification Code: {verification_code}",
            f"SHA-256: {evidence['sha256']}",
            f"Latest Audit Hash: {latest_audit_hash}",
            f"Case Merkle Root: {merkle_root}",
            f"Risk Score: {analysis['risk_score']} ({analysis['risk_level']})",
            f"Confidence: {analysis['confidence']}  Uncertainty: {analysis['uncertainty']}",
            f"Summary: {analysis['explanations']['summary']}",
        ]:
            c.drawString(40, y, line)
            y -= 20
        c.save()
        return buffer.getvalue()

    def store_pdf(self, key: str, pdf_bytes: bytes):
        storage_service.upload_bytes(key, pdf_bytes, "application/pdf")

report_service = ReportService()
