import sys
import logging

formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
# file_handler = logging.FileHandler(filename = 'log.txt', mode = 'a', encoding = 'utf-8')
# file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)


def get_logger(name=None):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
#     logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger

default_logger = get_logger()  # default logger
