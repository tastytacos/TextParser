import xml.etree.ElementTree as xml


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


def handle_measure_value(value):
    return value


def handle_measure_date(date):
    return date


def to_xml(handled_lines):
    root = xml.Element("Measurements")
    for line in handled_lines:
        if len(line.split(" ")) != 3:
            print("The size of the \"{}\" must be equal 3".format(line))
            continue
        station_index = line.split(" ")[0]
        measure_date = handle_measure_date(line.split(" ")[1])
        measure_value = handle_measure_value(line.split(" ")[2])

        measurement_results = xml.SubElement(root, "MeasurementResult")
        dose_rate = xml.SubElement(measurement_results, "DoseRateType")
        dose_rate.text = "Gamma"
        measurement_period = xml.SubElement(measurement_results, "MeasuringTime")
        start_m_time = xml.SubElement(measurement_period, "StartTime")
        start_m_time.text = measure_date
        measurements = xml.SubElement(measurement_results, "Measurements")
        measurement = xml.SubElement(measurements, "Measurement")
        location = xml.SubElement(measurement, "Location", station_index=station_index)
        value_units = xml.SubElement(measurement, "Value", Unit="Sv/s")
        value_units.text = measure_value
        validated = xml.SubElement(measurement, "Validated")
        validated.text = "NotValidated"
    tree = xml.ElementTree(root)
    return tree


def create_xml_doc(xml_tree):
    xml_tree.write("res/output.xml")


def parse(filename):
    file = open(filename, "r")
    lines = file.read().splitlines()
    handled_lines = handle_lines(lines)
    lines_xml_tree = to_xml(handled_lines)
    xml_document = create_xml_doc(lines_xml_tree)


parse("res/Radiation.txt")
