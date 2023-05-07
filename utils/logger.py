import logging

logger = logging.getLogger("tests")
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)
