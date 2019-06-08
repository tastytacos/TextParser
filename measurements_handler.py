from datetime import datetime


def handle_measure_value(value):
    return value


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
    return str(start_time), str(end_time)


def format_time(given_time):
    date = str(given_time.date())
    time = str(given_time.strftime("%X"))
    return date + "T" + time + "Z"
