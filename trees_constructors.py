import logging
import xml.etree.ElementTree as xml
from datetime import datetime
import uuid

import pytz

from tools import format_time, handle_measure_date, handle_measure_value

creation_time = datetime.now()


# Identification block
def create_id_xml(file):
    file_data = xml.parse(file)

    id_root = xml.Element("id:Identification")
    org_reporting = xml.SubElement(id_root, "id:OrganisationsReporting").text = file_data.find(
        "OrganisationReporting").text
    time = format_time(creation_time)
    report_datetime = xml.SubElement(id_root, "id:DateAndTimeOfCreation").text = str(time)
    report_context = xml.SubElement(id_root, "id:ReportContext").text = file_data.find("ReportContext").text
    report_sequence_number = xml.SubElement(id_root, "id:SequenceNumber").text = file_data.find(
        ".//SequenceNumber").text
    # todo provide parameter for uuid
    report_uuid = xml.SubElement(id_root, "id:ReportUUID").text = str(uuid.uuid4())
    confidentiality = xml.SubElement(id_root, "id:Confidentiality").text = file_data.find("Confidentiality").text
    addresses = xml.SubElement(id_root, "id:Addressees")
    addressee = xml.SubElement(addresses, "id:Addressee").text = file_data.find(".//Addressee").text

    reporting_bases = xml.SubElement(id_root, "id:ReportingBases")
    reporting_basis = xml.SubElement(reporting_bases, "id:ReportingBasis").text = file_data.find(
        ".//ReportingBasis").text
    contact_person = xml.SubElement(id_root, "id:ContactPerson").text = file_data.find(".//ContactPerson").text

    identifications_fields = xml.SubElement(id_root, "id:Identifications")

    person_info = xml.SubElement(identifications_fields, "base:PersonContactInfo")
    name = xml.SubElement(person_info, "base:Name").text = file_data.findall(".//Name")[0].text
    userID = xml.SubElement(person_info, "base:UserID").text = file_data.find(".//UserID").text
    position = xml.SubElement(person_info, "base:Position").text = file_data.find(".//Position").text
    organisation_id = xml.SubElement(person_info, "base:OrganisationID").text = file_data.findall(
        ".//OrganisationID")[0].text

    org_contacts_info = xml.SubElement(identifications_fields, "base:OrganisationContactInfo")
    org_name = xml.SubElement(org_contacts_info,
                              "base:Name").text = file_data.findall(".//Name")[1].text
    org_id = xml.SubElement(org_contacts_info, "base:OrganisationID").text = file_data.findall(
        ".//OrganisationID")[1].text
    org_country = xml.SubElement(org_contacts_info, "base:Country").text = file_data.find(".//Country").text
    org_phone_number = xml.SubElement(org_contacts_info, "base:PhoneNumber").text = file_data.find(
        ".//PhoneNumber").text
    org_fax_number = xml.SubElement(org_contacts_info, "base:FaxNumber").text = file_data.find(".//FaxNumber").text

    id_tree = xml.ElementTree(id_root)
    return id_tree


def default_fill_id_xml():
    '''
    The create_id_xml creates the Identification xml tree according to the out from outer file. If the file is
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


def get_time_value(handled_lines):
    new_dict = dict()
    arr = []
    times = [t.split(" ")[1] for t in handled_lines]
    unique_times = set(times)
    for element in unique_times:
        for line in handled_lines:
            if line.split(" ")[1] == element:
                arr.append(line)
        new_dict[element] = arr
        arr = []
    return new_dict


def validate(time_value, times):
    return_time = []
    for time in times:
        a = time_value.get(time)
        try:
            start_time, end_time = handle_measure_date(a[0].split(" ")[1], creation_time)
            return_time.append(time)
        except ValueError:
            logging.error(
                "Value error in - {} with line - {}".format(a[0].split(" ")[1], a))
            continue
    return return_time


def to_xml(handled_lines, locations_data):
    time_value = get_time_value(handled_lines)
    times = sorted(list(time_value.keys()))
    validated_times = validate(time_value, times)
    latest_time = max(validated_times)
    start_latest_time, end_latest_time = handle_measure_date(latest_time, creation_time)
    measurement_root = xml.Element("mon:Measurements", ValidAt=format_time(end_latest_time))
    locations_root = xml.Element("loc:Locations")

    for time in validated_times:
        a = time_value.get(time)
        try:
            start_time, end_time = handle_measure_date(a[0].split(" ")[1], creation_time)
        except ValueError:
            logging.error(
                "Value error in - {} with line - {}".format(a[0].split(" ")[1], a))
            continue
        measurement_results = xml.SubElement(measurement_root, "mon:DoseRate")
        dose_rate = xml.SubElement(measurement_results, "mon:DoseRateType").text = "Gamma"
        measurement_period = xml.SubElement(measurement_results, "mon:MeasuringPeriod")
        start_m_time = xml.SubElement(measurement_period, "mon:StartTime").text = format_time(start_time)
        end_m_time = xml.SubElement(measurement_period, "mon:EndTime").text = format_time(end_time)

        for line in time_value.get(time):
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
                logging.error(
                    "Error while trying to get the station with index - {}. Probably there is no such a station".format(
                        station_index))
                continue
            measure_value = handle_measure_value(line.split(" ")[2])
            measurements = xml.SubElement(measurement_results, "mon:Measurements")
            measurement = xml.SubElement(measurements, "mon:Measurement")
            measurement_location = xml.SubElement(measurement, "loc:Location", ref=station_index)
            value_units = xml.SubElement(measurement, "mon:Value", Unit="Sv/s").text = format(measure_value, '.3g')

            location = xml.SubElement(locations_root, "loc:Location", id=station_index)
            stantion_name = xml.SubElement(location, "loc:Name").text = name
            geo_coord = xml.SubElement(location, "loc:GeographicCoordinates")
            latitude = xml.SubElement(geo_coord, "loc:Latitude").text = locations_data.get(station_index).get(
                "latitude")
            longitude = xml.SubElement(geo_coord, "loc:Longitude").text = locations_data.get(station_index).get(
                "longitude")
            height = xml.SubElement(geo_coord, "loc:Height", Above="Sea", Unit="m").text = locations_data.get(
                station_index).get("height")

    measurements_tree = xml.ElementTree(measurement_root)
    locations_tree = xml.ElementTree(locations_root)
    return measurements_tree, locations_tree
