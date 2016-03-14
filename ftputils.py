def chdir(ftp_path, ftp_conn):
    dirs = [d for d in ftp_path.split('/') if d != '']
    dirs.pop()
    for p in dirs:
        check_dir(p, ftp_conn)


def check_dir(directory, ftp_conn):
    filelist = []
    ftp_conn.retrlines('LIST', filelist.append)
    found = False

    for f in filelist:
        if f.split()[-1] == directory and f.lower().startswith('d'):
            found = True

    if not found:
        ftp_conn.mkd(directory)
    ftp_conn.cwd(directory)


def go_up(depth, ftp_conn):
    while depth >= 0:
        ftp_conn.cwd("..")
        depth -= 1
