from dotenv import dotenv_values
import logging
import os

ENV = dotenv_values(".env")
LOG_PATH = ENV["LOG_PATH"]


class Filter(object):
    def __init__(self, level):
        self.__level = level

    def filter(self, logRecord):
        return logRecord.levelno <= self.__level


if not os.path.exists(LOG_PATH):
    os.makedirs(LOG_PATH)

logger = logging.getLogger('logger')

FORMAT = "%(asctime)s|%(filename)s:%(lineno)s|%(funcName)s|%(message)s"

logging.basicConfig(
    format=FORMAT,
    level=logging.INFO,
    filename=LOG_PATH + "log.log",
    encoding="ISO-8859-1",
)
