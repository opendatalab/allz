
# 自定义的解压类型与key的mapping映射, key为unarchive目录下的脚本名称,key与下面UNARCHIVE_TYPE_COMMAND中的key保持一致
UNARCHIVE_TYPE_KEY_MAPPING = {
    "zip_process": [".zip"],
    "tar_bz_process": [".tar.bz", ".tar.bz2"],
    "unar_process": [".tar", ".tar.bz", ".tar.bz2"],
    "rar_process": [".rar"]
}


# 解压类型与解压命令、python处理脚本的module/class字典配置
UNARCHIVE_TYPE_COMMAND = {
    "zip_process": {
        "process_module": "zip_process",
        "process_class": "ZipProcess"
    },

    "tar_bz_process": {
        "process_module": "tar_bz_process",
        "process_class": "TarBzProcess"
    },

    "unar_process": {
        "process_module": "unar_process",
        "process_class": "UnarProcess"
    },

    "rar_process": {
        "process_module": "rar_process",
        "process_class": "RarProcess"
    }
}

UNARCHIVE_FILE_TYPES = [".7z", ".tar", ".tar.bz2", ".tar.gz", ".tar.lzma", ".tar.xz", ".rar", ".tgz", ".bz2", ".gz", ".lzma", ".xz", ".zip"]

# 日志打印出来的格式
LOG_LEVEL = 'INFO'
LOG_MODE = 'normal'
LOG_FORMAT = "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level}    | {file}:{function}:{line} - {message}"
LOG_STDOUT_FORMAT = "<green>{time:YYYYMMDD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{module}</cyan>.<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"

__version__ = "0.0.1"
