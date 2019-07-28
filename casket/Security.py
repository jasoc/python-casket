from passlib.context import CryptContext

class Security:

    pwd_context = CryptContext(
            schemes=["pbkdf2_sha256"],
            default="pbkdf2_sha256",
            pbkdf2_sha256__default_rounds=30000
    )

    @staticmethod
    def encryptPassword(password):
        return Security.pwd_context.hash(password)

    @staticmethod
    def checkPassword(password, hashed):
        return Security.pwd_context.verify(password, hashed)
