from parser import parse
from datetime import datetime

input_file_location = "res/Radiation.txt"
output_file_location = "res/output.xml"


def start():
    xml_doc = parse(input_file_location)
    xml_doc.write(output_file_location)


if __name__ == '__main__':
    start()
