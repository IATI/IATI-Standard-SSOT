from lxml import etree as ET
import string
import os


namespaces = {
    'xsd': 'http://www.w3.org/2001/XMLSchema'
}

import re

class Schema2Doc(object):
    def __init__(self, schema):
        self.tree = ET.parse("./iati-schemas/"+schema)
        self.tree2 = ET.parse("./iati-schemas/iati-common.xsd")

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
            
            #FIXME (This does not belong here)
            childnames = self.element_loop(element, path)
            if childnames:
                fp.write('Subelements\n~~~~~~~~~~~\n\n')
                fp.write('.. toctree::\n   :titlesonly:\n\n')
                fp.write('\n'.join([ '   '+element_name+'/'+c for c in childnames]))
                fp.write('\n\n')

            fp.write('From the schema\n~~~~~~~~~~~~~~~\n\n')
            fp.write(element.find(".//xsd:documentation", namespaces=namespaces).text)
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

    def attribute_loop(self, element, indent=''):
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

activities = Schema2Doc('iati-activities-schema.xsd')
activities.get_element('iati-activities', '')

orgs = Schema2Doc('iati-organisations-schema.xsd')
orgs.get_element('iati-organisations', '')


