# A universal command line tool for compression and decompression


- Supports more normal compressed file formats than I can remember, like Zip, Tar, Gzip, Bzip2, 7-Zip, Rar, Rar.bz2, Tar.gz and so on.
- Supports split volumn compressed file for certain formats, like Tar.bz2, Tar.bz, Tar.gz, Tgz, Tar.7z, Tar, 7z, Zip, Rar.
- Supports decompress normal and split volumn compressed file in the same command. In split volumn mode, any part of the input split file can be decompress correctly.
- Support for automatic creation of target folders. If you have a path with spaces in it, it will handle that too.
- The decompress engine itself and command-line tool has only been tested in Linux environment so far.


## Install Cli
```bash
pip install allz
```

## Command Description
```bash
allz -d -q -f src_path -o dest_path
```
- src_path  &emsp;&emsp;&nbsp;&nbsp; The input source path.  
- dest_path &emsp;&emsp; The output destination path.

- -d &emsp;&emsp;&emsp;&emsp;&emsp;&nbsp; Decompress normal or split compressed files.  
- -q &emsp;&emsp;&emsp;&emsp;&emsp;&nbsp; Run in quiet mode.  
- -f &emsp;&emsp;&emsp;&emsp;&emsp;&ensp; Always overwrite files when a file to be unpacked already exists on disk. By default, the program will skips the file.
- -p &emsp;&emsp;&emsp;&emsp;&emsp;&nbsp; Output regular expressions for both regular compressed files and slice compressed files successively: the first line is for the normal compressed file, the second line is for the split volumn compressed file.
  - -p --only-normal &emsp;&emsp; Output regular matching expressions for normal compressed files only.
  - -p --only-split  &emsp;&emsp;&emsp;&nbsp; Output regular expressions for split volumn compressed files only.

### Available options:  
- --output-directory (-o) <string>  &emsp;&emsp;&ensp; The directory to write the contents of the archive to. Defaults to the current directory.

## Examples
####  Suppose we now have a normal compressed file MNIST.7z and two split volumn compressed files MNIST.tar.7z.001, MNIST.tar.7z.002.

#### 1. View the version  
```bash
allz --version
```

#### 2. View the help
```bash
allz -h
```
or 
```bash
allz --help
```

#### 3. Check which types are supported for decompression in your local environment
```bash
allz check
```

#### 4. Decompress the normal file MNIST.7z to current directory
```bash
allz -d MNIST.7z
```

In default, if the compressed file have already decompress before, it will skip the same file. You can use option -f to overwrite the files.
```bash
allz -d -f MNIST.7z
```

You can also mask screen log output by use option -q.
```bash
allz -d -q MNIST.7z
```

#### 5. Decompress the normal file MNIST.7z to the specified directory by use option -o
```bash
allz -d MNIST.7z -o /tmp
```

You can also use the relative destination path.
```bash
allz -d MNIST.7z -o ..
```

#### 6. Decompress the split volumn file MNIST.tar.7z.001
```bash
allz -d MNIST.tar.7z.001 
```

Decompress the split volumn file to specified directory by use option -o.
```bash
allz -d MNIST.tar.7z.001 -o /tmp
```

#### 7.Handle the path with space in it
Methods of using escapes
```bash
allz -d 20220101\ todo/MNIST.7z -o /tmp/20220101\ done/MNIST.7z
```
Methods of using quotation marks
```bash
allz -d "20220101 todo/MNIST.7z" -o "/tmp/20220101 done/MNIST.7z"
```

#### 8. Decompress the file into a recurvise destination directory
It will automatically create folders that do not exist.
```bash
allz -d MNIST.7z -o /tmp/today/fruit/apple/
```
  
  
## SDK
###  1. Function get_compressed_files_classify_lst
- Source code: allz/libs/file_type_tester  
- FileTypeTester.get_compressed_files_classify_lst(file_lst)
  - Return a nested list which will sort the input file list into multiple common or split volumn compressed file lists. The input parameter file_lst is a list of files in the same hierarchical directory. The list can be a file name, a full path or a relative path name. Function only processes compressed files, including normal compressed files and split volumn compressed files, ignoring the processing of normal files.

- A short usage example:
  ```python
    from allz.libs.file_type_tester import FileTypeTester

    file_lst = ["MNIST.tar.0000", "MNIST.tar.0001", "MNIST.tar.0002", "MNIST.tar.0003", "MNIST.tar.0004", "MNIST.tar.7z.001", "MNIST.tar.7z.002", "MNIST.part1.rar", "MNIST.part2.rar", "MNIST.part3.rar", "MNIST.part4.rar", "MNIST.7z.001", "MNIST.7z.002", "123.rar", "abc.zip", "abc", "000", "0000.tar", "02287.txt"]

    tester = FileTypeTester() 
    res_lst = tester.get_compressed_files_classify_lst(file_lst)
    print(res_lst)

  ```

  Output:  
  [['/home/work/srccode/github/allz/allz/libs/MNIST.tar.0000', '/home/work/srccode/github/allz/allz/libs/MNIST.tar.0002', '/home/work/srccode/github/allz/allz/libs/MNIST.tar.0004', '/home/work/srccode/github/allz/allz/libs/MNIST.tar.0003', '/home/work/srccode/github/allz/allz/libs/MNIST.tar.0001'], ['/home/work/srccode/github/allz/allz/libs/MNIST.tar.7z.002', '/home/work/srccode/github/allz/allz/libs/MNIST.tar.7z.001'], ['/home/work/srccode/github/allz/allz/libs/MNIST.part4.rar', '/home/work/srccode/github/allz/allz/libs/MNIST.part1.rar', '/home/work/srccode/github/allz/allz/libs/MNIST.part2.rar', '/home/work/srccode/github/allz/allz/libs/MNIST.part3.rar'], ['/home/work/srccode/github/allz/allz/libs/MNIST.7z.001', '/home/work/srccode/github/allz/allz/libs/MNIST.7z.002'], ['/home/work/srccode/github/allz/allz/libs/123.rar'], ['/home/work/srccode/github/allz/allz/libs/000.tar']]