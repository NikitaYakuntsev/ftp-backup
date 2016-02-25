Ftp backup tool.


This tool allows you to backup specified directories (that are not subfolders of each other)
to multiple FTP servers.


There could be multiple FTP sections in config file,
but names of sections should start from word "FTP" and should be unique.

Example:

[FTP name]

host = hostname

username = username

password = pass



There could be multiple directory sections in config file,
requirements are the same as for FTP section (should start from "DIR" and should be unique).

Example:

[DIR name]

path = /home/user/path/2

mask = *.*

period = 14


Here path is absolute location of directory,
mask specifies what files should be saved
and period is a number of days before current date when changes of file should be tracked.

TODO Email configuration and logging.
