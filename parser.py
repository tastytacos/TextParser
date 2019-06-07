import xml.etree.ElementTree as xml
from datetime import datetime
from measurements_handler import handle_measure_date, handle_measure_value


def handle_lines(lines):
    '''
    Grab the lines which match to requirement pattern from the set of given lines
    :param lines: given lines
    :return: the lines which have three elements divided by space
    '''
    cleared_lines = []
    for line in lines:
        if len(line.split(" ")) == 3:
            cleared_lines.append(line)
    return cleared_lines


def to_xml(handled_lines, locations_data):
    root = xml.Element("Measurements", ValidAt=str(datetime.now()))
    for line in handled_lines:
        a = line.split(" ")[2][0]
        # the next checks are a requirement of specification
        if len(line.split(" ")) != 3:
            print("The size of the \"{}\" must be equal 3".format(line))
            continue
        if line.split(" ")[2][0] != '8':
            print(str(line.split(" ")[2]) + " must start with 8")
            continue
        station_index = line.split(" ")[0]
        measure_date = handle_measure_date(line.split(" ")[1])
        measure_value = handle_measure_value(line.split(" ")[2])

        measurement_results = xml.SubElement(root, "MeasurementResult")
        dose_rate = xml.SubElement(measurement_results, "DoseRateType").text = "Gamma"
        measurement_period = xml.SubElement(measurement_results, "MeasuringTime")
        start_m_time = xml.SubElement(measurement_period, "StartTime").text = measure_date
        measurements = xml.SubElement(measurement_results, "Measurements")
        measurement = xml.SubElement(measurements, "Measurement")
        location = xml.SubElement(measurement, "Location", station_index=station_index)
        value_units = xml.SubElement(measurement, "Value", Unit="Sv/s").text = measure_value
        validated = xml.SubElement(measurement, "Validated").text = "NotValidated"
    tree = xml.ElementTree(root)
    return tree


def create_xml_doc(id_tree, measures_tree):
    pass


def create_id_xml():
    pass


def get_location_data():
    pass


def parse(filename):
    id_xml_tree = create_id_xml()
    file = open(filename, "r")
    lines = file.read().splitlines()
    handled_lines = handle_lines(lines)
    locations_data = get_location_data()
    measures_location_xml_tree = to_xml(handled_lines, locations_data)
    xml_document = create_xml_doc(id_xml_tree, measures_location_xml_tree)
    return xml_document
