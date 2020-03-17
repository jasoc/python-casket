from logzero import logger

from .cryptoutils import cryptoutils as crypto
from .homefolder import homefolder as home
from .dbutils import dbutils as database
from .sqlutils import sqlutils
from .session import session
from .exceptions import *
from .account import account

def log(arg):
    logger.info(str(arg))

def load_session(username, password):
    return session(method = "load", username = username, password_master = password)

def new_session(username, password, email, default_algorithm = "sha256"):
    return session(method = "new", username = username, password_master = password, email = email, algorithm = default_algorithm)

def sessions_list():
    res = database().select_sessions_name()
    return [ _[0] for _ in res ]
