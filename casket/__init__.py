from logzero import logger

from .crypto_utils import crypto_utils as crypto
from .home_folder import home_folder as home
from .session import session as sess

def log(arg):
    logger.info(str(arg))

def new_user():
    pass
