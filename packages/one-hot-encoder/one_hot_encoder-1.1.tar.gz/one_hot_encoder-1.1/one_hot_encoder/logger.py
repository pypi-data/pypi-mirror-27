import logging
import sys


def getLogger():
    """
    :return: The root logger configured with the stream handler
    """

    logger = logging.getLogger('one_hot_encoder')
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
