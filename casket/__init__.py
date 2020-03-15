from logzero import logger

from .crypto_utils import crypto_utils as crypto
from .home_folder import home_folder as home
from .db_utils import db_utils as database
from .sql_utils import sql_utils
from .session import session
from .exceptions import *
from .account import account

def log(arg):
    logger.info(str(arg))

def new_user():
    pass
