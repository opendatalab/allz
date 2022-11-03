# -*- coding:utf-8 -*-
import sys

from allz.defs import LOG_LEVEL, LOG_STDOUT_FORMAT, LOG_MODE_NORMAL
from loguru import logger


def get_logger(name: str, log_mode=LOG_MODE_NORMAL):
    logger.remove()

    mylogger = logger.bind(name=name)
    if log_mode != LOG_MODE_NORMAL:
        logger.disable(name)
    else:
        logger.add(sys.stdout, format=LOG_STDOUT_FORMAT, level=LOG_LEVEL, filter=lambda record: record["extra"].get('name') == name)
        logger.enable(name)

    return mylogger


def on_success(src_path: str, des_path: str, log_mode=LOG_MODE_NORMAL) -> None:
    mylogger = get_logger("common", log_mode)
    mylogger.info(f"The compressed file {src_path} was successfully extracted to {des_path}")


def on_failure(src_path: str, des_path: str, log_mode=LOG_MODE_NORMAL) -> None:
    mylogger = get_logger("common", log_mode)
    mylogger.info(f"The compressed file {src_path} failed to be extracted to {des_path}")
