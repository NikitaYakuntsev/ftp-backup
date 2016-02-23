import ConfigParser
from common import FTP_SECT, HOST, USER, PASS, CONF_FILE_PATH

config = ConfigParser.RawConfigParser()

config.add_section(FTP_SECT)
config.set(FTP_SECT, HOST, "localhost")
config.set(FTP_SECT, USER, "root")
config.set(FTP_SECT, PASS, "passwd")

with open(CONF_FILE_PATH, 'wb') as conffile:
    config.write(conffile)
