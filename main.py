from datetime import datetime

import pysftp

from credentials import input_file_location, output_file_location, log_directory, sftp_host, sftp_username, \
    sftp_password, remote_folder, output_file_backup_directory
from parser import parse
import logging
import traceback

from tools import generate_filename_by_datetime, transform_month


def send_to_sftp(filename):
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    with pysftp.Connection(host=sftp_host, username=sftp_username, password=sftp_password) as sftp:
        with sftp.cd(remote_folder):  # temporarily chdir to public
            sftp.put(filename)  # upload file to public/ on remote


def check_calendar_data(calendar_data):
    if len(calendar_data) != 2:  # 2 because you need day and month in this dict
        return False
    for key, value in calendar_data.items():
        if not str(calendar_data[key]).isdigit():
            return False
    return True


def start(par_input_file_location, par_output_file_location, write_to_server=True, **calendar_data):
    '''
    :param par_input_file_location:
    :param par_output_file_location:
    :param write_to_server:
    :param calendar_data: contains day and mont for program to start. You need it if you gonna to parse the file with
            data for other day (not current day and month)
    :return:
    '''
    logfile_name = generate_filename_by_datetime(log_directory, 'log')
    logging.basicConfig(format='%(levelname)-8s [%(asctime)s] %(message)s', level=logging.DEBUG, filename=logfile_name)
    res = check_calendar_data(calendar_data)
    if not res:
        calendar_data['day'] = datetime.now().strftime("%d")
        calendar_data['month'] = str(transform_month(datetime.now().month))
    xml_doc = parse(par_input_file_location, calendar_data)
    if xml_doc is None:
        logging.critical("xml_doc object is None. Something went wrong here")
    logging.info("Successfully parsed the xml information from - {} file".format(par_input_file_location))
    try:
        xml_doc.write(par_output_file_location, encoding="utf-8", xml_declaration=True, method="xml")
        logging.info("Successfully created the - {} xml file".format(par_output_file_location))
    except Exception:
        logging.error(traceback.format_exc())
        traceback.print_exc()
    try:
        xml_doc.write(generate_filename_by_datetime(output_file_backup_directory, 'xml'))
        logging.info("Successfully created the - {} xml file".format(output_file_backup_directory))
    except Exception:
        logging.error(traceback.format_exc())
        traceback.print_exc()
    if write_to_server:
        try:
            send_to_sftp(par_output_file_location)
            logging.info("Successfully send the file to sftp server")
        except Exception:
            logging.error(traceback.format_exc())
            logging.error("Error happened while writing file to sftp")
            traceback.print_exc()


if __name__ == '__main__':
    # if you need a test mode provide the call of the function like in the next line
    start("rubbish/Radiation0119.txt", output_file_location, write_to_server=False, day='15', month='1')
    #start(input_file_location, output_file_location, write_to_server=False)
