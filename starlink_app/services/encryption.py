from __future__ import annotations

from cryptography.fernet import Fernet


class EncryptionService:
    def __init__(self, key: bytes | None = None) -> None:
        self._key = key or Fernet.generate_key()
        self._fernet = Fernet(self._key)

    @property
    def key(self) -> bytes:
        return self._key

    def encrypt_json_bytes(self, payload: bytes) -> bytes:
        return self._fernet.encrypt(payload)

    def decrypt_json_bytes(self, token: bytes) -> bytes:
        return self._fernet.decrypt(token)
