# coding=utf-8
import ConfigParser
import common
import os
from os import path
from fnmatch import fnmatch
import time
from ftplib import FTP
import tarfile
import logging

from ftputils import chdir, go_up

logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s',
                    level=logging.DEBUG, #logging.INFO
                    filename=u'log.log')


def load_configuration(filepath):
    config = ConfigParser.RawConfigParser()
    config.read(filepath)
    logging.debug(u'Config loaded from {}'.format(filepath))
    return config


def save_sync_time():
    with open(common.SYNC_FILE_PATH, 'wb') as fl:
        fl.write(str(common.now()))


def get_last_sync_time():
    with open(common.SYNC_FILE_PATH, 'r') as fl:
        result = int(fl.read())
    return result


def parse_config(config):
    """
    Parses configuration with sections [FTP NAME].
    :param config: ConfigParser's object.
    :return: Tuple of:
     - Array of dir's dicts {sect_name, path, mask, period, ftp_path, archive_only_changed, ftp_lifetime}.
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
                  common.DIR_PERIOD_DAYS: config.getint(sect, common.DIR_PERIOD_DAYS),
                  common.DIR_FTP_PATH: config.get(sect, common.DIR_FTP_PATH),
                  common.DIR_ONLY_CHANGED: config.getboolean(sect, common.DIR_ONLY_CHANGED),
                  common.DIR_FTP_LIFETIME: config.getint(sect, common.DIR_FTP_LIFETIME)}
            dirs.append(dr)
    logging.debug(u'Parsed directories: {0}'.format(dirs))
    logging.debug(u'Parsed ftp servers: {0}'.format(servers))
    return dirs, servers


def prepare_file_list(filepath, mask, period):
    """
    Creates list of files from filepath that were modified since last sync but not later than "period" days before today
    and have name with "mask" pattern.
    :param filepath: root folder.
    :param mask: pattern for file name.
    :param period: number of days file shouldn't be older than
    """
    result = []

    norm_path = path.normpath(filepath)
    if not path.exists(norm_path):
        logging.error(u'Bad path: {}'.format(norm_path))
        raise Exception("Bad path.")
    else:
        rem_dir = path.normpath(os.path.basename(norm_path))
        #        print rem_dir

        for root, dirs, files in os.walk(norm_path):
            for name in files:
                local_file = path.join(root, name)
                file_path = path.join(root[len(norm_path):], name)

                if path.exists(local_file):
                    mod_time = path.getmtime(local_file)
                    if (mod_time >= LAST_SYNC_TIME) and (common.now() - mod_time <= period * common.DAY) \
                            and (fnmatch(local_file, mask)):
                        # TODO optimization: if you have to backup all directory than skip previous check
                        fl = {"local_file_path": local_file,
                              "remote_dir_path": rem_dir,
                              "file_path": file_path}
                        result.append(fl)

    return result


def get_file_list(directories):
    """
    Prepares the list of archive files from directories that should be send to FTP servers.
    :param directories: map of directories from config.
    """
    result = []
    for dr in directories:
        preres = prepare_file_list(dr[common.DIR_PATH], dr[common.DIR_MASK], dr[common.DIR_PERIOD_DAYS])
        name = {"name": "",
                "remote_dir": dr[common.DIR_FTP_PATH]}
        if preres is not None and len(preres) > 0:
            if dr[common.DIR_ONLY_CHANGED]:
                name["name"] = create_archive(preres)
            else:
                name["name"] = create_archive(dr[common.DIR_PATH])
            result.append(name)
    logging.debug(u'Prepared archives to be loaded: {}'.format(result))
    return result


def create_archive(object):
    """
    Recieves list of files or path to create archive from.
    :return: name of archive
    """
    name = str("{0}.tar.gz".format(common.now()))
    tar = tarfile.open(name, "w:gz")
    if isinstance(object, list):
        for fl in object:
            tar.add(fl["local_file_path"])
    else:
        tar.add(object)

    tar.close()
    return name


def load_files_to_server(file_list, host, user, passw):
    logging.debug(u'Loading files to ftp {}@{}'.format(user, host))
    ftp = FTP(host=host, user=user, passwd=passw)
    for fl in file_list:
        local_file = fl["name"]
        if path.exists(local_file):
            f = open(local_file, 'rb')
            remote = "{}{}{}".format(fl["remote_dir"], os.path.sep, local_file)
            chdir(remote, ftp)
            #            print "remote = {}".format(remote)
            ftp.storbinary("STOR {}".format(local_file), f)
            f.close()
            go_up(1, ftp)


    ftp.close()
    logging.debug(u'Ftp session {}@{} closed.'.format(user, host))

def load_files_to_servers(file_list, server_list):
    if len(file_list) > 0:
        for srv in server_list:
            host = srv[common.FTP_HOST]
            usr = srv[common.FTP_USER]
            passwd = srv[common.FTP_PASS]
            load_files_to_server(file_list, host, usr, passwd)


def clean_up(file_list):
    for fl in file_list:
        os.remove(fl["name"])


LAST_SYNC_TIME = get_last_sync_time()
logging.info(u'\n\n\n')
logging.info(u'Initialization...')
conf = load_configuration(common.CONF_FILE_PATH)
logging.info(u'Config loaded...')
parse_result = parse_config(conf)
dirs_dict = parse_result[0]
servers_dict = parse_result[1]
logging.info(u'Config parsed.')

# print servers_dict
# print dirs_dict

logging.info(u'Starting performing files validation...')
before = time.time()
files = get_file_list(dirs_dict)
logging.info(u'Spent: {} seconds for preparing list of files'.format(time.time() - before))
# print files
logging.info(u'Starting loading archives {} to {} servers...'.format(files, len(servers_dict)))
load_files_to_servers(files, servers_dict)
logging.info(u'All files successfully loaded.')

clean_up(files)


save_sync_time()
