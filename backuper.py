import ConfigParser
import common
from ftplib import FTP


def load_configuration():
    config = ConfigParser.RawConfigParser()
    config.read(common.CONF_FILE_PATH)
    return config


def parse_ftps(config):
    """
    Parses configuration.
    :param config: ConfigParser's object.
    :return: Array of servers' dicts {sect_name, hostname, username, password}.
    """
    result = []
    for sect in config.sections():
        if str(sect).startswith(common.FTP_SECT):
            srv = {"name": sect,
                   "hostname": config.get(sect, common.HOST),
                   "username": config.get(sect, common.USER),
                   "password": config.get(sect, common.PASS)}
            result.append(srv)
    return result


conf = load_configuration()
servers = parse_ftps(conf)

print servers

# ftp = FTP(host=hostname, user=username, passwd=password)
