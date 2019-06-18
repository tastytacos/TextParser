from datetime import datetime


def formula(valueRoentgen, multiplier):
    valueSievert = multiplier * 2.45e-12 *valueRoentgen
    return valueSievert


def get_multiplier(param):
    if param == 0:
        return 1
    if param == 1:
        return 10e3
    return 10e6


def handle_measure_value(given_data):
    new_data = given_data[1:-1]
    multiplier = get_multiplier(int(new_data[0]))
    # per hour
    valueRoentgen = int(new_data[-3] + new_data[-2] + new_data[-1])
    #per second
    valueSievert = formula(valueRoentgen, multiplier)
    return str(valueSievert)


months = {
    0: "10",
    1: "01",
    2: "02",
    3: "03",
    4: "04",
    5: "05",
}


def handle_month(unhandled_month, creation_time):
    m = months.get(int(unhandled_month))
    if unhandled_month == 6 or unhandled_month == 7:
        return creation_time.month
    return m


# todo test this function
def handle_measure_date(given_data, creation_time):
    year = creation_time.year
    day = int(given_data[0] + given_data[1])
    unhandled_month = given_data[2]
    month = int(handle_month(unhandled_month, creation_time))
    hour = int(given_data[-2] + given_data[-1])
    start_time = datetime(year, month, day, hour, 0, 0)
    end_time = datetime(year, month, day, hour + 1, 0, 0)
    return start_time, end_time


def format_time(given_time):
    date = str(given_time.date())
    time = str(given_time.strftime("%X"))
    return date + "T" + time + "Z"
