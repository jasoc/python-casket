from passlib.context import CryptContext

class CryptoUtils:

    pwd_context = CryptContext(
            schemes=["pbkdf2_sha256"],
            default="pbkdf2_sha256",
            pbkdf2_sha256__default_rounds=30000
    )

    @staticmethod
    def encryptPassword(password):
        return CryptoUtils.pwd_context.hash(password)

    @staticmethod
    def decryptPassword(hashed):
        return CryptoUtils.pwd_context.decrypt(hashed)

    @staticmethod
    def checkPassword(password, hashed):
        return CryptoUtils.pwd_context.verify(password, hashed)
