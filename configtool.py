import ConfigParser
from common import FTP_SECT_PREF, FTP_HOST, FTP_USER, FTP_PASS, CONF_FILE_PATH, SYNC_FILE_PATH
from common import DIR_SECT_PREF, DIR_MASK, DIR_PATH, DIR_PERIOD_DAYS, DIR_FTP_LIFETIME, DIR_FTP_PATH, DIR_ONLY_CHANGED
import random

config = ConfigParser.RawConfigParser()
if False:
    for i in range(1, 5):
        section = "{} {}".format(FTP_SECT_PREF, i)
        config.add_section(section)
        config.set(section, FTP_HOST, "localhost")
        config.set(section, FTP_USER, "root")
        config.set(section, FTP_PASS, "passwd")


        #for i in range(1, 4):
    section = "{} #{}".format(DIR_SECT_PREF, i)
    config.add_section(section)
    config.set(section, DIR_PATH, "/home/nikitayakuntsev")
    config.set(section, DIR_MASK, "*.*")
    config.set(section, DIR_PERIOD_DAYS, random.randint(1, 14))
    config.set(section, DIR_FTP_LIFETIME, 7)
    config.set(section, DIR_ONLY_CHANGED, False)
    config.set(section, DIR_FTP_PATH, "160314_Test")

with open(CONF_FILE_PATH, 'wb') as conffile:
    config.write(conffile)

with open(SYNC_FILE_PATH, 'wb') as fl:
    fl.write("0")
