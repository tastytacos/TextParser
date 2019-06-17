import xml.etree.ElementTree as xml

tree = xml.parse("res/id.xml")
root = tree.getroot()
org = tree.findall(".//OrganisationID")[1].text

print(org)
