# -*- coding:utf-8 -*-
import sys
from loguru import logger
from allz.defs import LOG_STDOUT_FORMAT, LOG_LEVEL, LOG_FORMAT


def get_logger(name: str):
    logger.remove()
    logger.add(sys.stdout, format=LOG_STDOUT_FORMAT, level=LOG_LEVEL, filter=lambda record: record["extra"].get('name') == name)
    logger.add(f"logs/{name}.log", format=LOG_FORMAT, rotation="1 day", filter=lambda record: record["extra"].get('name') == name)
    mylogger = logger.bind(name=name)
    return mylogger


def on_success(src_path: str, des_path: str) -> None:
    mylogger = get_logger("common")
    mylogger.info(f"压缩包{src_path} 解压到 {des_path} 处理成功")


def on_failure(src_path: str, des_path: str) -> None:
    mylogger = get_logger("common")
    mylogger.info(f"压缩包{src_path} 解压到 {des_path} 处理失败")
