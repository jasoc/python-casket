from logzero import logger

from .crypto_utils import crypto_utils as crypto
from .user_data import user_data as home

def log(arg):
    logger.info(str(arg))
