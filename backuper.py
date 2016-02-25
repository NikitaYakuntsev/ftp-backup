import ConfigParser
import common
import os
from ftplib import FTP


def load_configuration():
    config = ConfigParser.RawConfigParser()
    config.read(common.CONF_FILE_PATH)
    return config


def parse_config(config):
    """
    Parses configuration with sections [FTP NAME].
    :param config: ConfigParser's object.
    :return: Array of servers' dicts {sect_name, hostname, username, password}.
    """
    servers = []
    dirs = []
    for sect in config.sections():
        if str(sect).startswith(common.FTP_SECT_PREF):
            srv = {"name": sect,
                   common.FTP_HOST: config.get(sect, common.FTP_HOST),
                   common.FTP_USER: config.get(sect, common.FTP_USER),
                   common.FTP_PASS: config.get(sect, common.FTP_PASS)}
            servers.append(srv)
        elif str(sect).startswith(common.DIR_SECT_PREF):
            dr = {"name": sect,
                  common.DIR_PATH: config.get(sect, common.DIR_PATH),
                  common.DIR_MASK: config.get(sect, common.DIR_MASK),
                  common.DIR_PERIOD_DAYS: config.get(sect, common.DIR_PERIOD_DAYS)}
            dirs.append(dr)
    return dirs, servers


conf = load_configuration()
parse_result = parse_config(conf)
dirs_dict = parse_result[0]
servers_dict = parse_result[1]

print servers_dict
print dirs_dict
# TODO go through list of files or through list of servers, create connection, send data, continue...
# ftp = FTP(host=hostname, user=username, passwd=password)
