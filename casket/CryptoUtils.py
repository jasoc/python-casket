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
