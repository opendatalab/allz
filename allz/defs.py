
# 自定义的解压类型与key的mapping映射, key为unarchive目录下的脚本名称,key与下面UNARCHIVE_TYPE_COMMAND中的key保持一致
COMPRESS_TYPE_KEY_MAPPING = {
    "zip_process": [".zip"],
    "tar_bz_process": [".tar.bz", ".tar.bz2"],
    "unar_process": [".7z", ".tar", ".tar.bz2", ".tar.gz", ".tar.lzma", ".tar.xz", ".tgz", ".bz2", ".gz", ".lzma", ".xz", ".zip", "gzip"],
    "rar_process": [".rar"]
}

# 解压类型与解压命令、python处理脚本的module/class字典配置
COMPRESS_TYPE_COMMAND = {
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

SPLIT_COMPRESS_FILE_TYPES = [".tar.bz2", ".tar.bz", ".tar.gz", ".tgz", ".tar.7z", ".tar", ".7z", ".zip"]

# 分片解压类型与key定义
SPLIT_COMPRESS_TYPE_KEY_MAPPING = {
    "bz2_split_process": [".tar.bz2", ".tar.bz"],
    "gz_split_process": [".tar.gz", ".tgz"],
    "tar_7z_split_process": [".tar.7z"],
    "tar_split_process": [".tar"],
    "z7_split_process": [".7z", ".zip"],
    "rar_split_process": [".rar"]
}

SPLIT_COMPRESS_TYPE_COMMAND = {
    "bz2_split_process": {
        "process_module": "bz2_split_process",
        "process_class": "Bz2SplitProcess"
    },

    "gz_split_process": {
        "process_module": "gz_split_process",
        "process_class": "GzSplitProcess"
    },

    "tar_7z_split_process": {
        "process_module": "tar_7z_split_process",
        "process_class": "Tar7zSplitProcess"
    },

    "tar_split_process": {
        "process_module": "tar_split_process",
        "process_class": "TarSplitProcess"
    },

    "z7_split_process": {
        "process_module": "z7_split_process",
        "process_class": "Z7SplitProcess"
    },

    "rar_split_process": {
        "process_module": "rar_split_process",
        "process_class": "RarSplitProcess"
    },

}

COMPRESS_FILE_TYPES = [".7z", ".tar", ".tar.bz2", ".tar.bz", ".tar.gz", ".tar.lzma", ".tar.xz", ".rar", ".tgz", ".bz2", ".gz", ".lzma", ".xz", ".zip", ".tar.7z", "gzip"]

# 日志打印出来的格式
LOG_LEVEL = 'INFO'
LOG_MODE_NORMAL = 'normal'
LOG_MODE_QUIET = 'quiet'
LOG_FORMAT = "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level}    | {file}:{function}:{line} - {message}"
LOG_STDOUT_FORMAT = "<green>{time:YYYYMMDD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{module}</cyan>.<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
