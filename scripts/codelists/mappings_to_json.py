from lxml import etree as ET
import os, json

def mapping_to_json(mappings):
    for mapping in mappings.getroot().xpath('//mapping'):
        out = {
            'path': mapping.find('path').text,
            'codelist': mapping.find('codelist').attrib['ref']
        }
        if mapping.find('condition') is not None:
            out['condition'] = mapping.find('condition').text
        yield out

mappings = ET.parse('mapping.xml')
with open('mapping.json', 'w') as fp:
    json.dump(list(mapping_to_json(mappings)), fp)

