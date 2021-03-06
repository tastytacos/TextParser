import logging
import traceback
from datetime import datetime

import pandas as pd
import pytz


def generate_filename_by_datetime(directory, extension):
    ua_index = "UA"
    str = datetime.now().strftime("%Y-%m-%d %X")
    new_str = str.replace(' ', '_').replace(':', '_')
    return directory + "/" + ua_index + "{}.{}".format(new_str, extension)


def formula(valueRoentgen, multiplier):
    valueSievert = multiplier * 2.43e-12 * valueRoentgen
    return valueSievert


def get_multiplier(param):
    if param == 0:
        return 1
    if param == 1:
        return 1e3
    return 1e6


def transform_month(given_month_number):
    if given_month_number == 10:
        return 0
    elif given_month_number == 6 or given_month_number == 11:
        return 6
    elif given_month_number == 7 or given_month_number == 12:
        return 7
    return given_month_number


def handle_measure_value(given_data):
    new_data = given_data[1:-1]
    multiplier = get_multiplier(int(new_data[0]))
    # per hour
    valueRoentgen = int(new_data[-3] + new_data[-2] + new_data[-1])
    # per second
    valueSievert = formula(valueRoentgen, multiplier)
    return valueSievert

months = {
    0: "10",
    1: "01",
    2: "02",
    3: "03",
    4: "04",
    5: "05",
    8: "08",
    9: "09"
}

def handle_month(unhandled_month, creation_time):
    if unhandled_month == '6' or unhandled_month == '7':
        return creation_time.month
    return months.get(int(unhandled_month))


def handle_measure_date(given_data, creation_time):
    year = creation_time.year
    day = int(given_data[0] + given_data[1])
    unhandled_month = given_data[2]
    month = int(handle_month(unhandled_month, creation_time))
    hour = int(given_data[-2] + given_data[-1])
    try:
        start_time = datetime(year, month, day, hour, 0, 0)
        end_time = datetime(year, month, day, hour + 1, 0, 0)
    except Exception:
        logging.error(traceback.format_exc())
        return None
    return start_time, end_time


def format_time(given_time):
    utc_time = toUTC(given_time)
    date = str(utc_time.date())
    time = str(utc_time.strftime("%X"))
    return date + "T" + time + "Z"


def toUTC(current_local_time):
    current_local_time_timestamp = current_local_time.strftime("%s")
    return datetime.utcfromtimestamp(float(current_local_time_timestamp))


def get_excel_information(filename):
    '''
    Grab the information from given excel file and converts it to the dict
    :param filename: name of the file
    :return: dict: key = {name: ' ', latitude: ' ', longitude: ' '}
    '''
    file = pd.read_excel(filename)
    size = len(file)
    data = {}
    for i in range(size):
        row = file.get_values()[i]
        key = str(row[1])
        name = str(row[2])
        latitude = str(row[3])
        longitude = str(row[4])
        height = str(row[5])
        if key.isdigit():
            data[key] = {'name': name, 'latitude': latitude, 'longitude': longitude, 'height': height}
    return data
