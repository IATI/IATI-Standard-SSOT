from lxml import etree as ET
import string
import os
import textwrap


namespaces = {
    'xsd': 'http://www.w3.org/2001/XMLSchema'
}
custom_attributes = {
    'xml:lang': 'ISO 2 letter code specifying the language of text in this element.'
}

import re

class Schema2Doc(object):
    def __init__(self, schema):
        self.tree = ET.parse("./iati-schemas/"+schema)
        self.tree2 = ET.parse("./iati-schemas/iati-common.xsd")

    def get_complexType(self, complexType_name):
        complexType = self.tree.find("//xsd:complexType[@name='{0}']".format(complexType_name), namespaces=namespaces)
        if complexType is None:
            complexType = self.tree2.find("//xsd:complexType[@name='{0}']".format(complexType_name), namespaces=namespaces)
        return complexType

    def get_attribute(self, attribute_name):
        attribute = self.tree.find("//xsd:attribute[@name='{0}']".format(attribute_name), namespaces=namespaces)
        if attribute is None:
            attribute = self.tree2.find("//xsd:attribute[@name='{0}']".format(attribute_name), namespaces=namespaces)
        return attribute

    def get_element(self, element_name, path):
        element = self.tree.find("//xsd:element[@name='{0}']".format(element_name), namespaces=namespaces)
        if element is None:
            element = self.tree2.find("//xsd:element[@name='{0}']".format(element_name), namespaces=namespaces)
        if element is None: return

        self.output_docs(element_name, element, path)


    def output_docs(self, element_name, element, path):
        #print element_name
        try:
            os.makedirs('docs/'+path)
        except OSError: pass
        with open('docs/'+path+element_name+'.rst', 'w') as fp:
            fp.write(element_name+'\n'+('='*len(element_name))+'\n\n')
            
            fp.write('\nFrom the schema\n~~~~~~~~~~~~~~~\n\n')
            fp.write(element.find(".//xsd:documentation", namespaces=namespaces).text)
            fp.write('\n\n')

            #FIXME (element_loop does not belong here)
            attributes = self.attribute_loop(element)
            fp.write('Attributes\n~~~~~~~~~~\n\n')
            fp.write('\n'.join([ a[0]+'\n  '+textwrap.dedent(a[1]).strip().replace('\n','\n  ') for a in attributes ]))

            #FIXME (element_loop does not belong here)
            childnames = self.element_loop(element, path)
            if childnames:
                fp.write('\nSubelements\n~~~~~~~~~~~\n\n')
                fp.write('.. toctree::\n   :titlesonly:\n\n')
                fp.write('\n'.join([ '   '+element_name+'/'+c for c in childnames]))
                fp.write('\n\n')
            


    def element_loop(self, element, path):
        children = ( element.findall('xsd:complexType/xsd:choice/xsd:element', namespaces=namespaces)
            + element.findall("xsd:complexType/xsd:all/xsd:element", namespaces=namespaces) )
        childnames = []
        for child in children:
            a = child.attrib
            if 'name' in a:
                self.output_docs(a['name'], child, path+element.attrib['name']+'/')
                childnames.append(a['name'])
            else:
                self.get_element(a['ref'], path+element.attrib['name']+'/')
                childnames.append(a['ref'])
        return childnames

    def attribute_loop(self, element):
        #if element.find("xsd:complexType[@mixed='true']", namespaces=namespaces) is not None:
        #    print_column_info('text', indent)
            
        a = element.attrib
        type_attributes = []
        if 'type' in a:
            complexType = self.get_complexType(a['type'])
            if complexType is None:
                print 'Notice: No attributes for', a['type']
            else:
                type_attributes = complexType.findall('xsd:attribute', namespaces=namespaces)
            #print_column_info('text', indent+'  ')
            """"
            if a['type'] == 'codeReqType':
                print_column_info('code', indent+'  ', True)
            if a['type'] == 'codeType':
                print_column_info('code', indent+'  ', False)
            if a['type'] == 'currencyType':
                print_column_info('currency', indent+'  ', False)
                print_column_info('value-date', indent+'  ', False)
            if a['type'] == 'dateType':
                print_column_info('iso-date', indent+'  ', False)
            """

        out = []
        for attribute in (
            element.findall('xsd:complexType/xsd:attribute', namespaces=namespaces) +
            element.findall('xsd:complexType/xsd:simpleContent/xsd:extension/xsd:attribute', namespaces=namespaces) +
            type_attributes
            ):
            if 'ref' in attribute.attrib:
                if attribute.get('ref') in custom_attributes:
                    out.append((attribute.get('ref'), custom_attributes[attribute.get('ref')]))
                    continue
                attribute = self.get_attribute(attribute.get('ref'))
            doc = attribute.find(".//xsd:documentation", namespaces=namespaces)
            if doc is not None:
                out.append((attribute.get('name'), doc.text))
            else:   
                print 'Ack', ET.tostring(attribute)
        return out

activities = Schema2Doc('iati-activities-schema.xsd')
activities.get_element('iati-activities', '')

orgs = Schema2Doc('iati-organisations-schema.xsd')
orgs.get_element('iati-organisations', '')


