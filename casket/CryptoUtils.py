import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from passlib.context import CryptContext


class CryptoUtils:

    pwd_context = CryptContext(
        schemes=["pbkdf2_sha256"],
        default="pbkdf2_sha256",
        pbkdf2_sha256__default_rounds=30000
    )

    @staticmethod
    def hash(password):
        return CryptoUtils.pwd_context.hash(password)

    @staticmethod
    def checkHash(password, hashed):
        return CryptoUtils.pwd_context.verify(password, hashed)

    @staticmethod
    def encrypt(pswd, key):
        return CryptoUtils.pwd_context.decrypt(hashed)

    @staticmethod
    def decrypt(pswd, key):
        return CryptoUtils.pwd_context.decrypt(hashed)

    @staticmethod
    def makeKey(password, salt):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        return base64.urlsafe_b64encode(kdf.derive(password))

    @staticmethod
    def encryptPassword(master_pswd, plain_pswd):
        salt = os.urandom(16)
        key = makeKey(master_pswd.encode("utf-8"), salt)
        cipher_suite = Fernet(key)
        cipher_text = cipher_suite.encrypt(plain_pswd.encode("utf-8"))
        enc_pswd = base64.b64encode(salt).decode(
            'utf-8') + cipher_text.decode('utf-8')
        return enc_pswd

    @staticmethod
    def decryptPassword(master_pswd, enc_pswd):
        salt = base64.b64decode(enc_pswd[:24].encode("utf-8"))
        key = makeKey(master_pswd.encode("utf-8"), salt)
        cipher_suite = Fernet(key)
        plain_text = cipher_suite.decrypt(enc_pswd[24:].encode("utf-8"))
        plain_text_utf8 = plain_text.decode("utf-8")
        return plain_text_utf8
