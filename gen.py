from lxml import etree as ET
import string

tree = ET.parse("./iati-schemas/iati-activities-schema.xsd")
tree2 = ET.parse("./iati-schemas/iati-common.xsd")

namespaces = {
    'xsd': 'http://www.w3.org/2001/XMLSchema'
}

import re

index = open('docs/activity/index.rst', 'w')
index.write('IATI Activities Standard\n====\n\n')
index.write('.. toctree::\n   :maxdepth: 1\n\n')

def get_element(element_name, indent=''):
    element = tree.find("//xsd:element[@name='{0}']".format(element_name), namespaces=namespaces)
    if element is None:
        element = tree2.find("//xsd:element[@name='{0}']".format(element_name), namespaces=namespaces)
    if element is None: return

    index.write('   '+element_name+'\n')
    with open('docs/activity/'+element_name+'.rst', 'w') as fp:
        fp.write(element_name+'\n'+('='*len(element_name))+'\n\n')
        fp.write('From the schema\n^^^^^^^^^^^^^^^\n\n')
        fp.write(element.find(".//xsd:documentation", namespaces=namespaces).text)
        fp.write('\n\n')

    element_loop(element, indent)


def print_column_info(name, indent='', required=False):
    print indent+"'{0}':".format(name)
    print indent+"  datatype: 'column'"
    if required: print indent+"  required: true"
    else: print indent+"  required: false"

def element_loop(element, indent=''):
    children = ( element.findall('xsd:complexType/xsd:choice/xsd:element', namespaces=namespaces)
        + element.findall("xsd:complexType/xsd:all/xsd:element", namespaces=namespaces) )
    for child in children:
        a = child.attrib
        if 'name' in a:
            element_loop(child, indent+'    ')
        else:
            get_element(a['ref'], indent+'    ')

def attribute_loop(element, indent=''):
    if element.find("xsd:complexType[@mixed='true']", namespaces=namespaces) is not None:
        print_column_info('text', indent)
        
    a = element.attrib
    if 'type' in a:
        if a['type'] in ['plainType','textType','codeType','codeReqType','currencyType','dateType','xsd:anyURI','xsd:decimal']:
            print_column_info('text', indent+'  ')
            if a['type'] == 'codeReqType':
                print_column_info('code', indent+'  ', True)
            if a['type'] == 'codeType':
                print_column_info('code', indent+'  ', False)
            if a['type'] == 'currencyType':
                print_column_info('currency', indent+'  ', False)
                print_column_info('value-date', indent+'  ', False)
            if a['type'] == 'dateType':
                print_column_info('iso-date', indent+'  ', False)
        else: raise Exception, a['type']

    for attribute in (
        element.findall('xsd:complexType/xsd:attribute', namespaces=namespaces) +
        element.findall('xsd:complexType/xsd:simpleContent/xsd:extension/xsd:attribute', namespaces=namespaces)
        ):
        print_column_info( attribute.get('ref') or attribute.get('name'), indent, attribute.get('use') == 'required' )

get_element('iati-activities', '  ')

