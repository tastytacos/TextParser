def handle_lines(lines):
    pass


def to_xml(handled_lines):
    pass


def create_xml_doc(xml_lines):
    pass


def parse(filename):
    file = open(filename, "r")
    lines = file.read().splitlines()
    handled_lines = handle_lines(lines)
    xml_lines = to_xml(handled_lines)
    xml_document = create_xml_doc(xml_lines)

