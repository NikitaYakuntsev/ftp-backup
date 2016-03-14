#Ftp backup tool.


This tool allows you to backup specified directories (that are not subfolders of each other)
to multiple FTP servers as archives in 2 ways:
[x] archive all folder where changes were made
[x] archive only changed files


There could be multiple FTP sections in config file,
but names of sections should start from word "FTP" and should be unique.

Example:
```
[FTP name]
host = hostname
username = username
password = pass
```


There could be multiple directory sections in config file,
requirements are the same as for FTP section (should start from "DIR" and should be unique).

Example:
```
[DIR name]
path = /home/user/path/2
mask = *.*
period = 9
ftp_lifetime = 7
archive_only_changed = True
ftp_path = 160314_Test
```

Here path is absolute location of directory,
mask specifies what files should be saved,
period is a number of days before current date when changes of file should be tracked,
ftp_lifetime is a number of days shows how long should file be stored on ftp. not in use now
archive_only_changed flag if true than only changed files will be archived, all specified folder otherwise
ftp_path is a name of remote folder on ftp server.
