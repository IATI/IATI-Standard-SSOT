from __future__ import print_function
import sys
from lxml import etree as ET

if len(sys.argv) < 2:
    print('Usage python testcodelists.py file.xml [mapping.xml]')
    exit()

if len(sys.argv) > 2:
    mapping_file = sys.argv[2]
else:
    mapping_file = 'mapping.xml'

root = ET.parse(sys.argv[1]).getroot()

for mapping in ET.parse(mapping_file).getroot().findall('mapping'):
    codelist_name = mapping.find('codelist').attrib['ref']
    codelist = ET.parse('combined-xml/{0}.xml'.format(codelist_name))
    if codelist.getroot().attrib.get('complete') not in ['1', 'true']:
        continue
    codes = [ x.text for x in codelist.xpath('//code') ]
    for code in root.xpath(mapping.find('path').text):
        if mapping.find('condition') is not None:
            if not code.getparent().xpath(mapping.find('condition').text):
                continue
        if not code in codes:
            print('{0} not in {1}'.format(code, codelist_name))

