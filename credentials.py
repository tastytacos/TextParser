from datetime import datetime

from tools import generate_filename_by_datetime


def generate_input_file_location():
    directory = "/home/rodosuser/Desktop/Meteodat/"
    year = str(datetime.now().year)
    month = datetime.now().month
    if month < 10:
        month = '0' + str(month)
    else:
        month = str(month)
    day = datetime.now().day
    if day < 10:
        day = '0' + str(day)
    else:
        day = str(day)
    filename = directory + year + "_" + month + "/" + day + "_" + month + "/Radiation.txt"
    return "res/Radiation10.txt"


def generate_output_file_location():
    directory = "out/"
    return generate_filename_by_datetime(directory, 'xml')


sftp_host = 'host'
sftp_username = 'user'
sftp_password = 'pass'

input_file_location = generate_input_file_location()
output_file_location = generate_output_file_location()
id_xml_file_location = "res/id.xml"
log_directory = "logs"
excel_file_location = "res/MeteoSt-RAD.xls"
