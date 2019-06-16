from parser import parse
import logging

input_file_location = "res/Radiation1.txt"
output_file_location = "res/output.xml"


def start():
    xml_doc = parse(input_file_location)
    logging.info("Successfully parsed the xml information from - {} file".format(input_file_location))
    xml_doc.write(output_file_location)
    logging.info("Successfully created the - {} xml file".format(output_file_location))


if __name__ == '__main__':
    start()
