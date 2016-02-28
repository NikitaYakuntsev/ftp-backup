import ConfigParser
import common
import os
from ftplib import FTP


def load_configuration(filepath):
    config = ConfigParser.RawConfigParser()
    config.read(filepath)
    return config


def parse_config(config):
    """
    Parses configuration with sections [FTP NAME].
    :param config: ConfigParser's object.
    :return: Tuple of:
     - Array of dir's dicts {sect_name, path, mask, period}.
     - Array of servers' dicts {sect_name, hostname, username, password}.
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


def get_file_list(directories):
    for dr in directories:
        prepare_file_list(dr[common.DIR_PATH], dr[common.DIR_MASK], dr[common.DIR_PERIOD_DAYS])


def prepare_file_list(path, mask, period):
    norm = os.path.normpath(path)
    rem_dir = os.path.normpath(os.path.basename(norm))
    print rem_dir

    for root, dirs, files in os.walk(norm):
        for name in files:
            local_file = os.path.join(root, name)
            file_path = os.path.join(root[len(norm):], name)
            rem_file = "{}{}".format(rem_dir, file_path)
            print "local = {} \nrem_dir = {}\nfile = {}\nrem_file = {}\n\n".format(local_file, rem_dir, file_path, rem_file)


conf = load_configuration(common.CONF_FILE_PATH)
parse_result = parse_config(conf)
dirs_dict = parse_result[0]
servers_dict = parse_result[1]

print servers_dict
print dirs_dict

"""
 TODO go through list of files or through list of servers, create connection,
 send data (check mask and period), continue...
"""
# ftp = FTP(host=hostname, user=username, passwd=password)
get_file_list(dirs_dict)