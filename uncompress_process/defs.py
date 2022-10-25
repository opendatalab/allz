
# 自定义的解压类型与key的mapping映射, key为unarchive目录下的脚本名称,key与下面UNARCHIVE_TYPE_COMMAND中的key保持一致
UNARCHIVE_TYPE_KEY_MAPPING = {
    "zip_process": [".zip"],
    "tar_bz_process": [".tar.bz", ".tar.bz2"]
}


# 解压类型与解压命令、python处理脚本的module/class字典配置
UNARCHIVE_TYPE_COMMAND = {
    "zip_process": {
        "comm_unar_prefix_cmd": "7z x",
        "comm_unar_middle_cmd": "",
        "comm_unar_suffix_cmd": "-o",
        "process_module": "zip_process",
        "process_class": "ZipProcess"
    },

    "tar_bz_process": {
        "comm_unar_prefix_cmd": "tar xjf",
        "comm_unar_middle_cmd": "",
        "comm_unar_suffix_cmd": "-C",
        "process_module": "tar_bz_process",
        "process_class": "TarBzProcess"
    },

    "unar_process": {
        "comm_unar_prefix_cmd": "unar -q -D -o",
        "comm_unar_middle_cmd": "",
        "comm_unar_suffix_cmd": "",
        "process_module": "unar_process",
        "process_class": "UnarProcess"
    }
}

UNARCHIVE_FILE_TYPES = ".tar .gz .tar.bz2 .tar.bz .zip .7z .tar.lz .tar.lzma .tar.lzo .tar.z .xz"

# 日志打印出来的格式
LOG_LEVEL = 'INFO'
LOG_FORMAT = "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level}    | {file}:{function}:{line} - {message}"
LOG_STDOUT_FORMAT = "<green>{time:YYYYMMDD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{module}</cyan>.<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
