from parser import parse

input_file_location = "res/Radiation.txt"
output_file_location = "res/output.xml"


xml_doc = parse(input_file_location)
xml_doc.write(output_file_location)

