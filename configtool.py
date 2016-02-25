import ConfigParser
from common import FTP_SECT, HOST, USER, PASS, CONF_FILE_PATH

config = ConfigParser.RawConfigParser()

for i in range(1, 5):
    section = "{} {}".format(FTP_SECT, i)
    config.add_section(section)
    config.set(section, HOST, "localhost")
    config.set(section, USER, "root")
    config.set(section, PASS, "passwd")

with open(CONF_FILE_PATH, 'wb') as conffile:
    config.write(conffile)
