"""
The MIT License (MIT)

Copyright (c) 2016 Nikita Yakuntsev

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from time import time

CONF_FILE_PATH = "conf/settings.ini"
SYNC_FILE_PATH = "conf/.time"

FTP_SECT_PREF = "FTP"
FTP_HOST = "host"
FTP_USER = "username"
FTP_PASS = "password"

DIR_SECT_PREF = "DIR"
DIR_PATH = "local_path"
DIR_MASK = "mask"
DIR_PERIOD_DAYS = "period"
DIR_DELAY_PERIOD_MINS = "delay_period"
DIR_ONLY_CHANGED = "archive_only_changed"
DIR_FTP_PATH = "ftp_path"
DIR_FTP_LIFETIME = "ftp_lifetime"


MIN = 60
HOUR = 60 * MIN
DAY = 24 * HOUR

def now():
    return int(time())