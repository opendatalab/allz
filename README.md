# 重要方法

## libs/argparser.py
1. --archive-file-type 支持的压缩文件格式，每种格式以 .点开头，以空格分隔
2. --archive-type 压缩文件的类型，如果不指定，则通过解析压缩文件后缀获取压缩类型
3. --unar-cmd 解压命令，如果不指定则通过压缩文件后缀，判定解压命令
4. --src-path 压缩文件的输入路径
5. --dest-path 压缩文件的输出路径  


## 对应不同压缩类型的解压脚本，统一在目录uncompress_process/unarchive
脚本命名：以压缩类型为前缀，统一以 _process.py结尾

## libs 工具脚本和抽象方法

## defs.py 配置文件
1. UNARCHIVE_TYPE_COMMAND 普通解压文件类型、命令、模块的配置
2. 以zip压缩文件为例， 字典的key是压缩格式，以 . 点号开头，如果支持多个，则以空格分隔
comm_unar_prefix_cmd 解压命令的前缀
comm_unar_prefix_cmd 解压命令的中缀
comm_unar_suffix_cmd 解压命令的后缀

process_module 模块名称，即uncompress_process/unarchive目录下，对应解压类型的脚本名称
process_class 类名称，即uncompress_process/unarchive目录下脚本对应的class名称
