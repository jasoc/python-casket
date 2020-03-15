"""
crypto_utils.py

Class for encrypting, decrypting and hashing strings.
"""

__authors__ = "Jasoc"
__version__ = "0.1.beta1"
__license__ = "GNU General Public License v3.0"


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

    algorithms = {
        "sha256" : hashes.SHA256()
    }

    @staticmethod
    def hash(password):
        return crypto_utils.pwd_context.hash(password)

    @staticmethod
    def check_hash(password, hashed):
        return crypto_utils.pwd_context.verify(password, hashed)

    @staticmethod
    def make_key(password, algorithm, salt):
        kdf = PBKDF2HMAC(
            algorithm=crypto_utils.algorithms[algorithm],
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        return base64.urlsafe_b64encode(kdf.derive(password))

    @staticmethod
    def encrypt_password(master_pswd, plain_pswd, salt = os.urandom(16), algorithm = "sha256"):
        key = crypto_utils.make_key(master_pswd.encode("utf-8"), algorithm, salt)
        cipher_suite = Fernet(key)
        cipher_text = cipher_suite.encrypt(plain_pswd.encode("utf-8"))
        enc_pswd = base64.b64encode(salt).decode(
            'utf-8') + cipher_text.decode('utf-8')
        return enc_pswd

    @staticmethod
    def decrypt_password(master_pswd, enc_pswd, algorithm = "sha256"):
        salt = base64.b64decode(enc_pswd[:24].encode("utf-8"))
        key = crypto_utils.make_key(master_pswd.encode("utf-8"), algorithm, salt)
        cipher_suite = Fernet(key)
        plain_text = cipher_suite.decrypt(enc_pswd[24:].encode("utf-8"))
        plain_text_utf8 = plain_text.decode("utf-8")
        return plain_text_utf8
