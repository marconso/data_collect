def total_files_dbc(ftp, directory):
    ftp.cwd(directory)
    total_files = 0
    for file_dbc in ftp.nlst():
        if file_dbc.endswith('.dbc'):
            total_files += 1
    return total_files
