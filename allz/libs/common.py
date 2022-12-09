# -*- coding:utf-8 -*-
import sys

from allz.defs import LOG_LEVEL, LOG_STDOUT_FORMAT, LOG_MODE_NORMAL
from loguru import logger
from allz.libs.file_type_tester import FileTypeTester


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


def set_log_mode(class_name, log_mode=LOG_MODE_NORMAL):
    return get_logger(class_name, log_mode)


def get_split_volumn_suffix(src_path):
    fileTester = FileTypeTester()
    is_split, suffix_str = fileTester.is_split_volume_compressed_file(src_path)
    if is_split and suffix_str:
        prefix_path = src_path.replace(suffix_str, "")
        
        return True, prefix_path
    else:
        return False, ""
