from lxml import etree as ET
import sys

def update_from_narrative(parent, element_name):
    element = parent.find(element_name)
    if element is not None and element.findall('narrative'):
        for narrative in element.findall('narrative'):
            narrative.tag = element_name
            parent.append(narrative)
        parent.remove(element)

parser = ET.XMLParser(remove_blank_text=True)
tree = ET.parse(sys.argv[1], parser)

metadata = tree.find('metadata')
update_from_narrative(metadata, 'name')
update_from_narrative(metadata, 'description')

for codelist_item in tree.find('codelist-items').findall('codelist-item'):
    update_from_narrative(codelist_item, 'name')
    update_from_narrative(codelist_item, 'description')

# Adapted from code at http://effbot.org/zone/element-lib.htm
def indent(elem, level=0, shift=2):
    i = "\n" + level*" "*shift
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + " "*shift
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1, shift)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

indent(tree.getroot(), 0, 4)

tree.write(sys.stdout, encoding='utf-8')
