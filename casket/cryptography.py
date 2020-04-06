# -*- coding: utf-8 -*-
# Casket python module
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, see <http://www.gnu.org/licenses/>.

"""
cryptography.py

Class for encrypting, decrypting and hashing strings.
"""

import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from passlib.context import CryptContext

import casket


class cryptoutils:

    pwd_context = CryptContext(
        schemes=["pbkdf2_sha256"],
        default="pbkdf2_sha256",
        pbkdf2_sha256__default_rounds=30000
    )

    algorithms = {
        "sha256": hashes.SHA256(),
        "sha224": hashes.SHA224(),
        "sha384": hashes.SHA256(),
        "sha512": hashes.SHA256(),
        "blake2b": hashes.BLAKE2b(64),
        "blake2s": hashes.BLAKE2s(32),
        "sha3_256": hashes.SHA3_256(),
        "sha3_224": hashes.SHA3_224(),
        "sha3_384": hashes.SHA3_384(),
        "sha3_512": hashes.SHA3_512()
    }

    @staticmethod
    def list_algorithms():
        return [_ for _ in cryptoutils.algorithms]

    @staticmethod
    def hash(password):
        return cryptoutils.pwd_context.hash(password)

    @staticmethod
    def check_hash(password, hashed):
        return cryptoutils.pwd_context.verify(password, hashed)

    @staticmethod
    def make_key(password, algorithm, salt):
        if not algorithm in cryptoutils.algorithms:
            raise casket.invalid_algorithm("Algorithm %s is not supported." % (
                algorithm))
        else:
            algorithm = cryptoutils.algorithms[algorithm]

        kdf = PBKDF2HMAC(
            algorithm=algorithm,
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        return base64.urlsafe_b64encode(kdf.derive(password))

    @staticmethod
    def encrypt_password(master_pswd, plain_pswd, salt=os.urandom(16), algorithm="sha256"):
        key = cryptoutils.make_key(
            master_pswd.encode("utf-8"), algorithm, salt)
        cipher_suite = Fernet(key)
        cipher_text = cipher_suite.encrypt(plain_pswd.encode("utf-8"))
        enc_pswd = base64.b64encode(salt).decode(
            'utf-8') + cipher_text.decode('utf-8')
        return enc_pswd

    @staticmethod
    def decrypt_password(master_pswd, enc_pswd, algorithm="sha256"):
        salt = base64.b64decode(enc_pswd[:24].encode("utf-8"))
        key = cryptoutils.make_key(
            master_pswd.encode("utf-8"), algorithm, salt)
        cipher_suite = Fernet(key)
        plain_text = cipher_suite.decrypt(enc_pswd[24:].encode("utf-8"))
        plain_text_utf8 = plain_text.decode("utf-8")
        return plain_text_utf8
