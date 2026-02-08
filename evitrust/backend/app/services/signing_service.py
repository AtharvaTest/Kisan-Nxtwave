import base64
from nacl.signing import SigningKey
from app.config import settings

class SigningService:
    def __init__(self):
        if settings.ed25519_private_key_b64:
            seed = base64.b64decode(settings.ed25519_private_key_b64)
            self.sk = SigningKey(seed)
        else:
            self.sk = SigningKey.generate()

    def sign_hex_hash(self, hex_hash: str) -> str:
        signed = self.sk.sign(bytes.fromhex(hex_hash))
        return base64.b64encode(signed.signature).decode()

signing_service = SigningService()
