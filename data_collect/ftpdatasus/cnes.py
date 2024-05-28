from ftplib import FTP
from pathlib import Path
import re
from tqdm import tqdm

from utils import total_files_dbc


def connect_ftp_datasus():
    ftp = FTP('ftp.datasus.gov.br')
    ftp.login()
    return ftp


def list_cnes():
    ftp = connect_ftp_datasus()
    ftp.cwd('/dissemin/publicos/cnes/200508_/dados')
    cneses = ftp.nlst()
    ftp.close()
    return cneses


def download_cnes(cnes, save_folder):
    def write_file(ftp, file_dbc, save_folder):
        with open(download_file, 'wb') as fwb:
            ftp.retrbinary(f'RETR {directory}/{file_dbc}', fwb.write)

    ftp = connect_ftp_datasus()
    directory = f'/dissemin/publicos/cnes/200508_/dados/{cnes}' 
    ftp.cwd(directory)

    downloaded, total_files = 0, total_files_dbc(ftp, directory)
    pbar = tqdm(total=total_files)

    for file_dbc in filter(lambda x: x.endswith('.dbc'), ftp.nlst()):
        local_file = Path(save_folder)
        local_file.mkdir(parents=True, exist_ok=True)

        download_file = local_file / file_dbc 
        pbar.set_description(desc=f'{directory}/{file_dbc} -> {download_file}')
        write_file(ftp, file_dbc, download_file)
        downloaded += 1
        pbar.update(downloaded)

    ftp.close()
