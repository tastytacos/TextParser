import xml.etree.ElementTree as xml
from datetime import datetime

from credentials import log_directory, excel_file_location, id_xml_file_location
from tools import get_excel_information
import pandas as pd
import logging

from trees_constructors import create_id_xml, default_fill_id_xml, to_xml, get_time_value

xmlms = {'base': "http://www.iaea.org/2012/IRIX/Format/Base",
         'html': "http://www.w3.org/1999/xhtml",
         'id': "http://www.iaea.org/2012/IRIX/Format/Identification",
         'irix': "http://www.iaea.org/2012/IRIX/Format",
         'irmis': "http://iec.iaea.org/irmis/2014/irix/format/extensions",
         'loc': "http://www.iaea.org/2012/IRIX/Format/Locations",
         'mon': "http://www.iaea.org/2012/IRIX/Format/Measurements"}


def has_five_digits(line):
    '''
    Checks whether the third element of line has 5 numbers or not
    :return: True if line meets the requirement
    '''
    third_line = line.split()[2]
    digits_number = 0
    for symbol in third_line:
        if symbol.isdigit():
            digits_number += 1
    return digits_number == 5


def handle_lines(lines):
    '''
    Grab the lines which match to requirement pattern from the set of given lines
    :param lines: given lines
    :return: the lines which match to a special pattern
    '''
    cleared_lines = []
    for line in lines:
        if len(line.split()) == 3 and has_five_digits(line):
            cleared_lines.append(line)
        elif len(line.split()) >= 4 and has_five_digits(line):
            line1 = line.split()[0] + " "
            line2 = line.split()[1] + " "
            line3 = line.split()[2]
            if "=" not in line3:
                # this condition is very important, because of the fools who like writing two lines without separation.
                # after splitting it causes the line with 2 '=' signs in a row. This completely spoil the calculation.
                # this checking is here to avoid doubling the equality sign.
                line3 += "="
            new_line = line1 + line2 + line3
            cleared_lines.append(new_line)
            logging.warning("The line - {} were thrown out but {} was handled".format(line, new_line))

        else:
            logging.warning("The line - {} were thrown out because of wrong format".format(line))
    return list(set(cleared_lines))


def get_report_root():
    root = xml.Element("irix:Report")
    root.attrib["version"] = "1.0"
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
    try:
        id_xml_tree = create_id_xml(id_xml_file_location)
        logging.info(
            "Successfully created id:Identification xml tree according to the out from {}".format(id_xml_file_location))
    except Exception:
        logging.error("Error while creating id:Identification xml tree")
        id_xml_tree = default_fill_id_xml()
        logging.info("Created default id:Identification xml tree")
    file = open(filename, "r")
    lines = file.read().splitlines()
    handled_lines = handle_lines(lines)
    try:
        locations_data = get_location_data(excel_file_location)
    except OSError:
        logging.critical(
            "File {} is not found. Impossible to get out of stations locations".format(excel_file_location))
    measures_xml_tree, location_xml_tree = to_xml(handled_lines, locations_data)
    logging.info("Successfully created the mon:Measurements and loc:Location xml trees")
    xml_document = create_xml_doc(id_xml_tree, measures_xml_tree, location_xml_tree)
    logging.info("Successfully created the irix:Report xml tree")
    return xml_document
