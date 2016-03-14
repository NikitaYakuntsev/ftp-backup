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
DIR_ONLY_CHANGED = "archive_only_changed"
DIR_FTP_PATH = "ftp_path"
DIR_FTP_LIFETIME = "ftp_lifetime"


MIN = 60
HOUR = 60 * MIN
DAY = 24 * HOUR

def now():
    return int(time())