## 功能

- 压缩成单文件

- 压缩成分卷文件

- 解压单文件

- 解压分卷文件

- 测试压缩文件（含分卷）完整性

- 不解压情况下列出其中包含的文件



## 命令

```shell
allz  <command> [<switches>] <archive_name>  [<file_names>...]
```

**command**

1. `c`：压缩
2. `d`:解压缩
3. `e`:测试压缩文件完整性
4. `l`:不解压情况下罗列出来压缩包内的文件

**switches**

1. `w`:设置命令的工作目录。默认为命令执行所在目录，文件读取和生成都相对于这个目录，除非路径以根开始。
2. `f`: 压缩到文件/从文件解压
3. `t`: 设置文件的类型。压缩时如果没有设置则默认为`tar.gz`格式；解压时默认会按照文件后缀推断文件类型，采用对应的命令解压，如果规定了`t`参数，则严格按照规定的文件类型进行解压，不成功时返回错误代码
4. `v`: 如果设置则打印出所命令的原始输出。
5. `b` : 分卷的大小K,M,G。例如`-b 10M`则分卷大小为10MB每个。
6. `o`: 压缩输出到的目录，或者解压输出到的目录。



## 例子



```shell
#压缩为tar.gz格式文件
allz -cvf  test.tar.gz  dir1  dir2/ test.txt   /mnt/dir/a.log

# 压缩为tar.gz分卷文件,每个卷10MB
allz -cf -b 10M test.tar.gz   mybigdir/

# 查看某压缩文件内部的文件列表
allz -l  test.gz

# 测试某压缩文件完整性
allz -e  test.zip
allz -e test.zip.000 # 如果分卷，则输入任意一个卷即可

# 当前目录位于/home/donkey下,压缩/mnt/testdir下的a、b、c三个目录,最终生成/mnt/archive/test.tar.gz
allz -cvf -w /mnt/testdir test.tar.gz  -o /mnt/archive  a/ b/ c/ 





```



## 文件格式支持

