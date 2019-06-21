from credentials import input_file_location, output_file_location
from parser import parse, generate_logfile_name
import logging
import traceback


def start():
    logfile_name = generate_logfile_name()
    logging.basicConfig(format='%(levelname)-8s [%(asctime)s] %(message)s', level=logging.DEBUG, filename=logfile_name)

    xml_doc = parse(input_file_location)
    logging.info("Successfully parsed the xml information from - {} file".format(input_file_location))
    try:
        xml_doc.write(output_file_location)
    except Exception:
        logging.error(traceback.format_exc())
        traceback.print_exc()
    logging.info("Successfully created the - {} xml file".format(output_file_location))


if __name__ == '__main__':
    start()
