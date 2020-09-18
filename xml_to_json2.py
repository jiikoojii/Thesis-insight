#!/usr/bin/env python3

import xml.etree.ElementTree as ET
import xmltodict
import json
import sys

xml_file = sys.argv[1] #Requires user input when running the script. Give the filename you want to convert.
#user_named = sys.argv[2]
tree = ET.parse(xml_file)
xml_data = tree.getroot()

xmlstr = ET.tostring(xml_data, encoding='utf-8', method='xml')

data_dict = dict(xmltodict.parse(xmlstr))

json_file = xml_file + ".json"
with open(json_file, 'w+') as json_file:
    json.dump(data_dict, json_file, indent=4, sort_keys=True)
