A universal command line tool for compression and decompression

# Command Using
allz -d -q -f src_path -o dest_path

-d      Decompress normal or split compressed files.
-q      Run in quiet mode.
-f      Always overwrite files when a file to be unpacked already exists on disk. By default, the program will skips the file.
  
Available options:  
--output-directory (-o) <string>    The directory to write the contents of the archive to. Defaults to the current directory.
