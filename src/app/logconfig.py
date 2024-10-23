import logging

CUSTOM_LEVEL = 25
logging.addLevelName(CUSTOM_LEVEL, "CUSTOM")

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s:\t%(message)s")
logger = logging.getLogger(__name__)


def custom_log(message):
    logger.log(CUSTOM_LEVEL, message)
