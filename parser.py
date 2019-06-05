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
    pass


def handle_measure_date(date):
    pass


def to_xml(handled_lines):
    for line in handled_lines:
        if len(line) != 3:
            raise ValueError("The size of the \"{}\" must be equal 3".format(line))
        station_index = line[0]
        measure_date = handle_measure_date(line[1])
        measure_value = handle_measure_value(line[2])

    pass


def create_xml_doc(xml_lines):
    pass


def parse(filename):
    file = open(filename, "r")
    lines = file.read().splitlines()
    handled_lines = handle_lines(lines)
    xml_lines = to_xml(handled_lines)
    xml_document = create_xml_doc(xml_lines)

# parse("res/Radiation.txt")
