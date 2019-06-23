from datetime import datetime

from tools import generate_filename_by_datetime


def generate_input_file_location():
    return "res/Radiation1.txt"


def generate_output_file_location():
    directory = "out/"
    return generate_filename_by_datetime(directory, 'xml')


sftp_host = 'hm.meteo.gov.ua'
sftp_username = 'hm-operator'
sftp_password = 'PsDHJjng'

input_file_location = generate_input_file_location()
output_file_location = generate_output_file_location()
id_xml_file_location = "res/id.xml"
log_directory = "logs"
excel_file_location = "res/MeteoSt-RAD.xls"
