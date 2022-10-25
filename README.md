
## libs/argparser.py
1. --src-path 压缩文件的输入路径
2. --dest-path 压缩文件的输出路径  


## 对应不同压缩类型的解压脚本，统一在目录allz/unarchive
脚本命名：以压缩类型为前缀，统一以 _process.py结尾

## libs 工具脚本和抽象方法

## defs.py 配置文件
1. UNARCHIVE_TYPE_COMMAND 普通解压文件对应的模块和class名称配置
process_module 模块名称，即allz/unarchive目录下，对应解压类型的脚本名称
process_class 类名称，即allz/unarchive目录下脚本对应的class名称
