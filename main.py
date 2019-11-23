import pysftp

from credentials import input_file_location, output_file_location, log_directory, sftp_host, sftp_username, \
    sftp_password, remote_folder, output_file_backup_directory
from parser import parse
import logging
import traceback

from tools import generate_filename_by_datetime



def send_to_sftp(filename):
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    with pysftp.Connection(host=sftp_host, username=sftp_username, password=sftp_password) as sftp:
        with sftp.cd(remote_folder):  # temporarily chdir to public
            sftp.put(filename)  # upload file to public/ on remote


def start(write_to_server=True):
    logfile_name = generate_filename_by_datetime(log_directory, 'log')
    logging.basicConfig(format='%(levelname)-8s [%(asctime)s] %(message)s', level=logging.DEBUG, filename=logfile_name)

    xml_doc = parse(input_file_location)
    logging.info("Successfully parsed the xml information from - {} file".format(input_file_location))
    try:
        xml_doc.write(output_file_location, encoding="utf-8", xml_declaration=True, method="xml")
    except Exception:
        logging.error(traceback.format_exc())
        traceback.print_exc()
    logging.info("Successfully created the - {} xml file".format(output_file_location))
    try:
        xml_doc.write(generate_filename_by_datetime(output_file_backup_directory, 'xml'))
    except Exception:
        logging.error(traceback.format_exc())
        traceback.print_exc()
    logging.info("Successfully created the - {} xml file".format(output_file_backup_directory))
    if write_to_server:
        try:
            send_to_sftp(output_file_location)
            logging.info("Successfully send the file to sftp server")
        except Exception:
            logging.error("Error happened while writing file to sftp")
            traceback.print_exc()


if __name__ == '__main__':
    start(True)
