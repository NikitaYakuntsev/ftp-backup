# coding=utf-8
import ConfigParser
import common
import os
from os import path
from fnmatch import fnmatch
import time
from ftplib import FTP

from ftputils import chdir, go_up


def load_configuration(filepath):
    config = ConfigParser.RawConfigParser()
    config.read(filepath)
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
                  common.DIR_PERIOD_DAYS: config.get(sect, common.DIR_PERIOD_DAYS),
                  common.DIR_FTP_PATH: config.get(sect, common.DIR_FTP_PATH),
                  common.DIR_ONLY_CHANGED: config.get(sect, common.DIR_ONLY_CHANGED),
                  common.DIR_FTP_LIFETIME: config.get(sect, common.DIR_FTP_LIFETIME)}
            dirs.append(dr)
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
        raise Exception("Bad path.")
    else:
        rem_dir = path.normpath(os.path.basename(norm_path))
        print rem_dir

        for root, dirs, files in os.walk(norm_path):
            for name in files:

                local_file = path.join(root, name)
                file_path = path.join(root[len(norm_path):], name)
                #rem_file = "{}{}".format(rem_dir, file_path)
                #print "local = {} \nrem_dir = {}\nfile = {}\nrem_file = {}\n\n".format(local_file, rem_dir, file_path,
                #                                                                      rem_file)

                if path.exists(local_file):
                    mod_time = path.getmtime(local_file)
                    if (mod_time >= LAST_SYNC_TIME) and (common.now() - mod_time <= period * common.DAY) \
                            and (fnmatch(local_file, mask)):
                        # rem_file = rem_dir + file_path
                        fl = {"local_file_path": local_file,
                              "remote_dir_path": rem_dir,
                              "file_path": file_path}
                        result.append(fl)


    return result


def get_file_list(directories):
    """
    Prepares the list of files from directories that should be send to FTP servers.
    :param directories: map of directories from config.
    """
    result = []
    for dr in directories:
        preres = prepare_file_list(dr[common.DIR_PATH], dr[common.DIR_MASK], dr[common.DIR_PERIOD_DAYS])
        name = ""
        if preres is not None and len(preres) > 0:
            if dr[common.DIR_ONLY_CHANGED] == True:
                name = create_archive(preres)
            else:
                name = create_archive(dr[common.DIR_PATH])
            result.append(name)

    return result


def create_archive(object):
    name = ""
    if isinstance(object, list):
        name = "list"
    else:
        name = "path" #add to archive this path
    return name

def load_files_to_server(file_list, host, user, passw):
    ftp = FTP(host=host, user=user, passwd=passw)
    for fl in file_list:

        local_file = fl["local_file_path"]
        if path.exists(local_file):
            f = open(local_file, 'rb')
            remote = "{}{}".format(fl["remote_dir_path"], fl["file_path"])
            chdir(remote, ftp)
            print "remote = {}".format(remote)
            ftp.storbinary("STOR {}".format(remote.split(path.sep)[-1]), f)
            f.close()
            go_up(local_file.count(path.sep), ftp)

    ftp.close()

def load_files_to_servers(file_list, server_list):
    if len(file_list) > 0:
        for srv in server_list:
            host = srv[common.FTP_HOST]
            usr = srv[common.FTP_USER]
            passwd = srv[common.FTP_PASS]
            load_files_to_server(file_list, host, usr, passwd)


LAST_SYNC_TIME = get_last_sync_time()

conf = load_configuration(common.CONF_FILE_PATH)
parse_result = parse_config(conf)
dirs_dict = parse_result[0]
servers_dict = parse_result[1]

print servers_dict
print dirs_dict


before = time.time()
files = get_file_list(dirs_dict)
print "Spent: {} seconds".format(time.time() - before)
print files

#load_files_to_servers(files, servers_dict)

save_sync_time()
