import xml.etree.ElementTree as xml
from datetime import datetime
import uuid

from measurements_handler import handle_measure_date, handle_measure_value, format_time
import pandas as pd
import logging


def generate_logfile_name():
    directory = "logs"
    return directory + "/{}.log".format(datetime.now().strftime("%Y-%m-%d %X"))


logfile_name = generate_logfile_name()

logging.basicConfig(format='%(levelname)-8s [%(asctime)s] %(message)s', level=logging.DEBUG, filename=logfile_name)

excel_file_location = "res/MeteoSt-RAD.xls"

creation_time = datetime.now()
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


# Measurements and Locations block
def to_xml(handled_lines, locations_data):
    measurement_root = xml.Element("mon:Measurements", ValidAt=format_time(creation_time))
    locations_root = xml.Element("loc:Locations")
    for line in handled_lines:
        # the next checks are a requirement of specification
        if len(line.split(" ")) != 3:
            print("The size of the \"{}\" must be equal 3".format(line))
            continue
        if line.split(" ")[2][0] != '8':
            print(str(line.split(" ")[2]) + " must start with 8")
            continue
        station_index = line.split(" ")[0]
        try:
            name = locations_data.get(station_index).get("name")
        except AttributeError:
            logging.error("Error while trying to get the station - {}, with index - {}".format(name, station_index))
            continue
        try:
            start_time, end_time = handle_measure_date(line.split(" ")[1], creation_time)
        except ValueError:
            logging.error("Value error in - {} with line - {}".format(line.split(" ")[1], line))
            continue
        measure_value = handle_measure_value(line.split(" ")[2])

        measurement_results = xml.SubElement(measurement_root, "mon:DoseRate")
        dose_rate = xml.SubElement(measurement_results, "mon:DoseRateType").text = "Gamma"
        measurement_period = xml.SubElement(measurement_results, "mon:MeasuringPeriod")
        start_m_time = xml.SubElement(measurement_period, "mon:StartTime").text = start_time
        end_m_time = xml.SubElement(measurement_period, "mon:EndTime").text = end_time
        measurements = xml.SubElement(measurement_results, "mon:Measurements")
        measurement = xml.SubElement(measurements, "mon:Measurement")
        measurement_location = xml.SubElement(measurement, "mon:Location", station_index=station_index)
        value_units = xml.SubElement(measurement, "mon:Value", Unit="Sv/s").text = measure_value
        validated = xml.SubElement(measurement, "mon:Validated").text = "NotValidated"

        location = xml.SubElement(locations_root, "loc:Location", id=station_index)
        stantion_name = xml.SubElement(location, "loc:Name").text = name
        geo_coord = xml.SubElement(location, "loc:GeographicCoordinates")
        latitude = xml.SubElement(geo_coord, "loc:Latitude").text = locations_data.get(station_index).get("latitude")
        longitude = xml.SubElement(geo_coord, "loc:Longitude").text = locations_data.get(station_index).get("longitude")
        height = xml.SubElement(geo_coord, "loc:Height", Above="Sea", Unit="m").text = locations_data.get(
            station_index).get("height")

    measurements_tree = xml.ElementTree(measurement_root)
    locations_tree = xml.ElementTree(locations_root)
    return measurements_tree, locations_tree


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


# Identification block
def create_id_xml(file):
    id_root = xml.Element("id:Identification")
    org_reporting = xml.SubElement(id_root, "id:OrganisationsReporting").text = "meteo.gov.ua"
    time = format_time(creation_time)
    report_datetime = xml.SubElement(id_root, "id:DateAndTimeOfCreation").text = str(time)
    report_context = xml.SubElement(id_root, "id:ReportContext").text = "Routine"
    report_uuid = xml.SubElement(id_root, "id:ReportUUID").text = str(uuid.uuid4())
    confidentiality = xml.SubElement(id_root, "id:Confidentiality").text = "For Authority Use Only"
    identifications_fields = xml.SubElement(id_root, "id:Identifications")

    person_info = xml.SubElement(identifications_fields, "base:PersonContactInfo")
    name = xml.SubElement(person_info, "base:Name").text = "Leonid Tabachnyi"
    org_person_id = xml.SubElement(person_info, "base:OrganisationID").text = "tabachnyi@meteo.gov.ua"
    email = xml.SubElement(person_info, "base:EmailAdress").text = "380442399353"

    org_contacts_info = xml.SubElement(identifications_fields, "base:OrganisationContactInfo")
    org_name = xml.SubElement(org_contacts_info,
                              "base:Name").text = "Radiation Accidents Consequences Prediction Center"
    org_id = xml.SubElement(org_contacts_info, "base:OrganisationInfo").text = "meteo.gov.ua"
    org_country = xml.SubElement(org_contacts_info, "base:Country").text = "UA"
    org_phone_number = xml.SubElement(org_contacts_info, "base:PhoneNumber").text = "380442399353"
    org_fax_number = xml.SubElement(org_contacts_info, "base:FaxNumber").text = "380442796680"
    org_email = xml.SubElement(org_contacts_info, "base:EmailAddress").text = "ceprac@meteo.gov.ua"
    org_description = xml.SubElement(org_contacts_info, "base:Descrition").text = "Data originator for this report"

    org1_contacts_info = xml.SubElement(identifications_fields, "base:OrganisationContactInfo")
    org1_name = xml.SubElement(org1_contacts_info, "base:Name").text = "Ukrainian Hydrometeorological Center"
    org1_id = xml.SubElement(org1_contacts_info, "base:OrganisationID").text = "meteo.gov.ua"
    org1_country = xml.SubElement(org1_contacts_info, "base:Country").text = "UA"
    org1_phone_number = xml.SubElement(org1_contacts_info, "base:PhoneNumber").text = "380442399387"
    org1_fax_number = xml.SubElement(org1_contacts_info, "base:FaxNUmber").text = "380442791080"
    org1_email = xml.SubElement(org1_contacts_info, "base:EmailAddress").text = "office@meteo.gov.ua"
    org1_description = xml.SubElement(org1_contacts_info, "base:Description").text = "Data originator for this report"
    id_tree = xml.ElementTree(id_root)
    return id_tree


def default_fill_id_xml():
    '''
    The create_id_xml creates the Identification xml tree according to the data from outer file. If the file is
    damaged or deleted the default filling of the tree goes here
    '''
    id_root = xml.Element("id:Identification")
    org_reporting = xml.SubElement(id_root, "id:OrganisationsReporting").text = "meteo.gov.ua"
    time = format_time(creation_time)
    report_datetime = xml.SubElement(id_root, "id:DateAndTimeOfCreation").text = str(time)
    report_context = xml.SubElement(id_root, "id:ReportContext").text = "Routine"
    report_uuid = xml.SubElement(id_root, "id:ReportUUID").text = str(uuid.uuid4())
    confidentiality = xml.SubElement(id_root, "id:Confidentiality").text = "For Authority Use Only"
    identifications_fields = xml.SubElement(id_root, "id:Identifications")

    person_info = xml.SubElement(identifications_fields, "base:PersonContactInfo")
    name = xml.SubElement(person_info, "base:Name").text = "Leonid Tabachnyi"
    org_person_id = xml.SubElement(person_info, "base:OrganisationID").text = "tabachnyi@meteo.gov.ua"
    email = xml.SubElement(person_info, "base:EmailAdress").text = "380442399353"

    org_contacts_info = xml.SubElement(identifications_fields, "base:OrganisationContactInfo")
    org_name = xml.SubElement(org_contacts_info,
                              "base:Name").text = "Radiation Accidents Consequences Prediction Center"
    org_id = xml.SubElement(org_contacts_info, "base:OrganisationInfo").text = "meteo.gov.ua"
    org_country = xml.SubElement(org_contacts_info, "base:Country").text = "UA"
    org_phone_number = xml.SubElement(org_contacts_info, "base:PhoneNumber").text = "380442399353"
    org_fax_number = xml.SubElement(org_contacts_info, "base:FaxNumber").text = "380442796680"
    org_email = xml.SubElement(org_contacts_info, "base:EmailAddress").text = "ceprac@meteo.gov.ua"
    org_description = xml.SubElement(org_contacts_info, "base:Descrition").text = "Data originator for this report"

    org1_contacts_info = xml.SubElement(identifications_fields, "base:OrganisationContactInfo")
    org1_name = xml.SubElement(org1_contacts_info, "base:Name").text = "Ukrainian Hydrometeorological Center"
    org1_id = xml.SubElement(org1_contacts_info, "base:OrganisationID").text = "meteo.gov.ua"
    org1_country = xml.SubElement(org1_contacts_info, "base:Country").text = "UA"
    org1_phone_number = xml.SubElement(org1_contacts_info, "base:PhoneNumber").text = "380442399387"
    org1_fax_number = xml.SubElement(org1_contacts_info, "base:FaxNUmber").text = "380442791080"
    org1_email = xml.SubElement(org1_contacts_info, "base:EmailAddress").text = "office@meteo.gov.ua"
    org1_description = xml.SubElement(org1_contacts_info, "base:Description").text = "Data originator for this report"
    id_tree = xml.ElementTree(id_root)
    return id_tree


def get_location_data(file):
    data = get_excel_information(file)
    return data


def parse(filename):
    logging.info("Creating file {}".format(filename))
    file = "sometestfile.txt"
    try:
        id_xml_tree = create_id_xml(file)
        logging.info("Successfully created id:Identification xml tree according to the data from {}".format(file))
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
            "File {} is not found. Impossible to get data of stations locations".format(excel_file_location))
    measures_xml_tree, location_xml_tree = to_xml(handled_lines, locations_data)
    logging.info("Successfully created the mon:Measurements and loc:Location xml trees")
    xml_document = create_xml_doc(id_xml_tree, measures_xml_tree, location_xml_tree)
    logging.info("Successfully created the irix:Report xml tree")
    return xml_document
