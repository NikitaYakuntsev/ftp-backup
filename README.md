#Ftp backup tool.


This tool allows you to backup specified directories (that are not subfolders of each other)
to multiple FTP servers as archives in 2 ways:

- archive all folder where changes were made
- archive only changed files

Usage: <b>python backuper.py</b>


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
delay_period = 2
ftp_lifetime = 7
archive_only_changed = True
ftp_path = 160314_Test
```

Here <b>path</b> is absolute location of directory,
<b>mask</b> specifies what files should be saved,
<b>period</b> is a number of days before current date when changes of file should be tracked,
<b>delay_period</b> is a number of minutes. If the period between file modifications less that this parameter, that means the file is still in work (e.g. log file is writing) and that file wouldn't be added to backup archive.
<b>ftp_lifetime</b> is a number of days shows how long should file be stored on ftp. not in use now,
<b>archive_only_changed</b> flag if true than only changed files will be archived, all specified folder otherwise, <b>ftp_path</b> is a name of remote folder on ftp server.
