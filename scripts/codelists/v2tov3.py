from lxml import etree as ET
import sys

"""

Example usage:
    cp -r xml xml.old
    cd xml.old
    for f in *; do python ../v2tov3.py $f > ../xml/$f; done

"""

def update_to_narrative(parent, element_name):
    elements = parent.findall(element_name)
    if elements:
        new_element = ET.Element(element_name)
        parent.append(new_element)
        for element in elements:
            parent.remove(element)
            element.tag = 'narrative'
            new_element.append(element)

parser = ET.XMLParser(remove_blank_text=True)
tree = ET.parse(sys.argv[1], parser)

metadata = tree.find('metadata')
update_to_narrative(metadata, 'name')
update_to_narrative(metadata, 'description')
# Ensure that url is the last element
url = metadata.find('url')
if url is not None:
    metadata.remove(url)
    metadata.append(url)

for codelist_item in tree.find('codelist-items').findall('codelist-item'):
    update_to_narrative(codelist_item, 'name')
    update_to_narrative(codelist_item, 'description')

    codelist_item[:] = sum((codelist_item.findall(x) for x in ['code', 'name', 'description', 'category', 'url']), [])


            
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
