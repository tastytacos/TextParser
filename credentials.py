from datetime import datetime

from tools import generate_filename_by_datetime


def generate_input_file_location():
    directory = "/home/rodosuser/Desktop/Meteodat/"
    year = str(datetime.now().year)
    month = datetime.now().strftime("%m")
    day = datetime.now().strftime("%d")
    filename = directory + year + "_" + month + "/" + day + "_" + month + "/Radiation.txt"
    return "res/Radiation2207.txt"


def generate_output_file_location(directory):
    return generate_filename_by_datetime(directory, 'xml')


sftp_host = 'host'
sftp_username = 'user'
sftp_password = 'pass'
remove_folder = "HGMSU"

input_file_location = generate_input_file_location()
local_file_directory = "out/"
output_file_location = generate_output_file_location(local_file_directory)
id_xml_file_location = "res/id.xml"
log_directory = "logs"
excel_file_location = "res/MeteoSt-RAD.xls"
# output_file_backup_directory = "/home/rodosuser/Documents/HGMSU/"