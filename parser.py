import xml.etree.ElementTree as xml
from datetime import datetime
import uuid

from measurements_handler import handle_measure_date, handle_measure_value
import pandas as pd

creation_time = datetime.now()


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
    return cleared_lines


# Measurements and Locations block
def to_xml(handled_lines, locations_data):
    measurement_root = xml.Element("Measurements", ValidAt=str(creation_time))
    locations_root = xml.Element("Locations")
    for line in handled_lines:
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

        measurement_results = xml.SubElement(measurement_root, "MeasurementResult")
        dose_rate = xml.SubElement(measurement_results, "DoseRateType").text = "Gamma"
        measurement_period = xml.SubElement(measurement_results, "MeasuringTime")
        start_m_time = xml.SubElement(measurement_period, "StartTime").text = measure_date
        measurements = xml.SubElement(measurement_results, "Measurements")
        measurement = xml.SubElement(measurements, "Measurement")
        measurement_location = xml.SubElement(measurement, "Location", station_index=station_index)
        value_units = xml.SubElement(measurement, "Value", Unit="Sv/s").text = measure_value
        validated = xml.SubElement(measurement, "Validated").text = "NotValidated"

        location = xml.SubElement(locations_root, "Location", id=station_index)
        name = locations_data.get(station_index).get("name")
        stantion_name = xml.SubElement(location, "Name").text = name
        geo_coord = xml.SubElement(location, "GeographicCoordinates")
        latitude = xml.SubElement(geo_coord, "Latitude").text = locations_data.get(station_index).get("latitude")
        longitude = xml.SubElement(geo_coord, "Longitude").text = locations_data.get(station_index).get("longitude")
        height = xml.SubElement(geo_coord, "Height", Above="Sea", Unit="m").text = locations_data.get(
            station_index).get("height")

    measurements_tree = xml.ElementTree(measurement_root)
    locations_tree = xml.ElementTree(locations_root)
    return measurements_tree, locations_tree


def create_xml_doc(id_tree, measures_tree, locations_xml_tree):
    report_root = xml.Element("Report")
    result_tree = combine_xml(report_root, [id_tree, measures_tree, locations_xml_tree])
    report_root_tree = xml.ElementTree(result_tree)
    return report_root_tree


def combine_xml(root, trees):
    first = root
    for tree in trees:
        data = tree.getroot()
        first.append(data)
    return first


def format_time(given_time):
    pass


# Identification block
def create_id_xml():
    id_root = xml.Element("Identification")
    org_reporting = xml.SubElement(id_root, "OrganisationsReporting").text = "meteo.gov.ua"
    time = format_time(creation_time)
    report_datetime = xml.SubElement(id_root, "DateAndTimeOfCreation").text = str(time)
    report_context = xml.SubElement(id_root, "ReportContext").text = "Routine"
    report_uuid = xml.SubElement(id_root, "ReportUUID").text = str(uuid.uuid4())
    confidentiality = xml.SubElement(id_root, "Confidentiality").text = "For Authority Use Only"
    identifications_fields = xml.SubElement(id_root, "Identifications")

    person_info = xml.SubElement(identifications_fields, "PersonContactInfo")
    name = xml.SubElement(person_info, "Name").text = "Leonid Tabachnyi"
    org_person_id = xml.SubElement(person_info, "OrganisationID").text = "tabachnyi@meteo.gov.ua"
    email = xml.SubElement(person_info, "EmailAdress").text = "380442399353"

    org_contacts_info = xml.SubElement(identifications_fields, "OrganisationContactInfo")
    org_name = xml.SubElement(org_contacts_info, "Name").text = "Radiation Accidents Consequences Prediction Center"
    org_id = xml.SubElement(org_contacts_info, "OrganisationInfo").text = "meteo.gov.ua"
    org_country = xml.SubElement(org_contacts_info, "Country").text = "UA"
    org_phone_number = xml.SubElement(org_contacts_info, "PhoneNumber").text = "380442399353"
    org_fax_number = xml.SubElement(org_contacts_info, "FaxNumber").text = "380442796680"
    org_email = xml.SubElement(org_contacts_info, "EmailAddress").text = "ceprac@meteo.gov.ua"
    org_description = xml.SubElement(org_contacts_info, "Descrition").text = "Data originator for this report"

    org1_contacts_info = xml.SubElement(identifications_fields, "OrganisationContactInfo")
    org1_name = xml.SubElement(org1_contacts_info, "Name").text = "Ukrainian Hydrometeorological Center"
    org1_id = xml.SubElement(org1_contacts_info, "OrganisationID").text = "meteo.gov.ua"
    org1_country = xml.SubElement(org1_contacts_info, "Country").text = "UA"
    org1_phone_number = xml.SubElement(org1_contacts_info, "PhoneNumber").text = "380442399387"
    org1_fax_number = xml.SubElement(org1_contacts_info, "FaxNUmber").text = "380442791080"
    org1_email = xml.SubElement(org1_contacts_info, "EmailAddress").text = "office@meteo.gov.ua"
    org1_description = xml.SubElement(org1_contacts_info, "Description").text = "Data originator for this report"
    id_tree = xml.ElementTree(id_root)
    return id_tree


def get_location_data():
    file_location = "res/MeteoSt-RAD.xls"
    data = get_excel_information(file_location)
    return data


def parse(filename):
    id_xml_tree = create_id_xml()
    file = open(filename, "r")
    lines = file.read().splitlines()
    handled_lines = handle_lines(lines)
    locations_data = get_location_data()
    measures_xml_tree, location_xml_tree = to_xml(handled_lines, locations_data)
    xml_document = create_xml_doc(id_xml_tree, measures_xml_tree, location_xml_tree)
    return xml_document
