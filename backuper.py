import ConfigParser
import common
from ftplib import FTP


def load_configuration():
    config = ConfigParser.RawConfigParser()
    config.read(common.CONF_FILE_PATH)
    return config


conf = load_configuration()
hostname = conf.get(common.FTP_SECT, common.HOST)
username = conf.get(common.FTP_SECT, common.USER)
password = conf.get(common.FTP_SECT, common.PASS)

ftp = FTP(host=hostname, user=username, passwd=password)

