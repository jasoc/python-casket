import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from passlib.context import CryptContext

class crypto_utils:

    pwd_context = CryptContext(
        schemes=["pbkdf2_sha256"],
        default="pbkdf2_sha256",
        pbkdf2_sha256__default_rounds=30000
        )


    @staticmethod
    def get_key_from_user_password(password, salt = "diocan"):
        password = password.encode()
        salt = salt.encode()
        kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
        )
        return base64.urlsafe_b64encode(kdf.derive(password))

    @staticmethod
    def hash(password):
        return crypto_utils.pwd_context.hash(password)

    @staticmethod
    def checkHash(password, hashed):
        return crypto_utils.pwd_context.verify(password, hashed)
