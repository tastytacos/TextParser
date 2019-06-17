import xml.etree.ElementTree as xml
from datetime import datetime

from credentials import log_directory, excel_file_location
from tools import handle_measure_date, handle_measure_value, format_time
import pandas as pd
import logging

from trees_constructors import create_id_xml, default_fill_id_xml, to_xml


def generate_logfile_name():
    return log_directory + "/{}.log".format(datetime.now().strftime("%Y-%m-%d %X"))


logfile_name = generate_logfile_name()

logging.basicConfig(format='%(levelname)-8s [%(asctime)s] %(message)s', level=logging.DEBUG, filename=logfile_name)

xmlms = {'base': "http://www.iaea.org/2012/IRIX/Format/Base",
         'html': "http://www.w3.org/1999/xhtml",
         'id': "http://www.iaea.org/2012/IRIX/Format/Identification",
         'irix': "http://www.iaea.org/2012/IRIX/Format",
         'irmis': "http://iec.iaea.org/irmis/2014/irix/format/extensions",
         'loc': "http://www.iaea.org/2012/IRIX/Format/Locations",
         'mon': "http://www.iaea.org/2012/IRIX/Format/Measurements"}


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
        row = file.iloc[i]
        key = str(row[1])
        name = row[2]
        latitude = row[3]
        longitude = row[4]
        height = str(row[5])
        if key.isdigit():
            data[key] = {'name': name, 'latitude': latitude, 'longitude': longitude, 'height': height}
    return data


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
        else:
            logging.warning("The line - {} were thrown out because of wrong format".format(line))
    return cleared_lines


def get_report_root():
    root = xml.Element("irix:Report")
    for key, value in xmlms.items():
        root.attrib['xmlns:' + key] = value
    return root


def create_xml_doc(id_tree, measures_tree, locations_xml_tree):
    report_root = get_report_root()
    result_tree = combine_xml(report_root, [id_tree, measures_tree, locations_xml_tree])
    report_root_tree = xml.ElementTree(result_tree)
    return report_root_tree


def combine_xml(root, trees):
    first = root
    for tree in trees:
        data = tree.getroot()
        first.append(data)
    return first


def get_location_data(file):
    data = get_excel_information(file)
    return data


def parse(filename):
    logging.info("Creating file {}".format(filename))
    file = "sometestfile.txt"
    try:
        id_xml_tree = create_id_xml(file)
        logging.info("Successfully created id:Identification xml tree according to the out from {}".format(file))
    except Exception:
        logging.error("Error while creating id:Identification xml tree")
        id_xml_tree = default_fill_id_xml()
        logging.info("Created default id:Identification xml tree")
    file = open(filename, "r")
    lines = file.read().splitlines()
    handled_lines = handle_lines(lines)
    try:
        locations_data = get_location_data(excel_file_location)
    except FileNotFoundError:
        logging.critical(
            "File {} is not found. Impossible to get out of stations locations".format(excel_file_location))
    measures_xml_tree, location_xml_tree = to_xml(handled_lines, locations_data)
    logging.info("Successfully created the mon:Measurements and loc:Location xml trees")
    xml_document = create_xml_doc(id_xml_tree, measures_xml_tree, location_xml_tree)
    logging.info("Successfully created the irix:Report xml tree")
    return xml_document
