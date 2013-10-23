from lxml import etree as ET
import string
import os
import textwrap
import json

namespaces = {
    'xsd': 'http://www.w3.org/2001/XMLSchema'
}
custom_attributes = {
    'xml:lang': 'ISO 2 letter code specifying the language of text in this element.'
}

import re

def human_list(l):
    return ', '.join(l)

rulesets = json.load(open('./IATI-Rulesets/rulesets.json'))
def ruleset_text(path):
    out = ''
    for xpath, rules in rulesets.items():
        if xpath.startswith('//'):
            try:
                reduced_path = path.split(xpath[2:]+'/')[1]
                for rule in rules:
                    cases = rules[rule]['cases']
                    for case in cases:
                        if 'paths' in case:
                            for case_path in case['paths']:
                                # Don't forget [@ ]
                                if case_path == reduced_path:
                                    other_paths = case['paths']
                                    other_paths.remove(case_path)
                                    if rule == 'only_one':
                                        out += 'This element must be present only once. '
                                        if other_paths:
                                            out += 'This element must not be present if {0} are present. '.format(human_list(other_paths))
                                    elif rule == 'atleast_one':
                                        if other_paths:
                                            out += 'Either this element or {0} must be present. '.format(human_list)
                                        else:
                                            out += 'This element must be present. ' 
                                    else: print case_path, rule, case['paths'] 
                                    break
            except IndexError:
                pass
    if out != '':
        out += '(`see rulesets.json <https://github.com/Bjwebb/IATI-Rulesets/blob/master/rulesets.json>`_)'
    return out


codelist_mappings = ET.parse('./IATI-Codelists/mapping.xml').getroot().findall('mapping')
def match_codelist(path):
    for mapping in codelist_mappings:
        if mapping.find('path').text.startswith('//'):
            #print mapping.find('path').text.strip('/'), path
            if mapping.find('path').text.strip('/') in path:
                return mapping.find('codelist').attrib['ref']
            else:
                pass # FIXME
    return



class Schema2Doc(object):
    def __init__(self, schema):
        self.tree = ET.parse("./IATI-Schemas/"+schema)
        self.tree2 = ET.parse("./IATI-Schemas/iati-common.xsd")

    def get_complexType(self, complexType_name):
        complexType = self.tree.find("//xsd:complexType[@name='{0}']".format(complexType_name), namespaces=namespaces)
        if complexType is None:
            complexType = self.tree2.find("//xsd:complexType[@name='{0}']".format(complexType_name), namespaces=namespaces)
        return complexType

    def get_attributeGroup(self, attributeGroup_name):
        attributeGroup = self.tree.find("//xsd:attributeGroup[@name='{0}']".format(attributeGroup_name), namespaces=namespaces)
        if attributeGroup is None:
            attributeGroup = self.tree2.find("//xsd:attributeGroup[@name='{0}']".format(attributeGroup_name), namespaces=namespaces)
        return attributeGroup

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
        url = element.base.replace('./IATI-Schemas/', 'https://github.com/Bjwebb/IATI-Schemas/blob/master/') + '#L' + str(element.sourceline)
        try:
            os.makedirs('docs/'+path)
        except OSError: pass
        with open('docs/'+path+element_name+'.rst', 'w') as fp:
            fp.write(element_name+'\n'+('='*len(element_name))+'\n\n')
            fp.write('DRAFT\n-----\n\n')
            
            fp.write('\nFrom the schema\n~~~~~~~~~~~~~~~\n\n')
            fp.write('`View this element in the schema source <'+url+'>`_\n')
            fp.write(textwrap.dedent(element.find(".//xsd:documentation", namespaces=namespaces).text))
            fp.write('\n\n')
            fp.write(ruleset_text(path+element_name))
            fp.write('\n\n')
            for extended_type in element.xpath('xsd:complexType/xsd:simpleContent/xsd:extension/@base', namespaces=namespaces):
                if extended_type.startswith('xsd:'):
                    fp.write('The text in this element should be of type {0}.\n'.format(extended_type))
                    fp.write('\n\n')
            if element.get('type') and element.get('type').startswith('xsd:'):
                fp.write('The text in this element should be of type {0}.\n'.format(element.get('type')))
                fp.write('\n\n')

            #FIXME (element_loop does not belong here)
            attributes = self.attribute_loop(element)
            if attributes:
                fp.write('Attributes\n~~~~~~~~~~\n\n')
                for attribute, attribute_type, text in attributes:
                    fp.write( '@'+attribute+'\n  '+textwrap.dedent(text).strip().replace('\n','\n  ') )
                    codelist = match_codelist(path+element_name+'/@'+attribute)
                    if attribute_type:
                        fp.write('\n  \n  This value should be of type {0}.\n'.format(attribute_type)) 
                    if codelist is not None:
                        fp.write('\n  \n  This value should be on the :doc:`{0} codelist </codelists/{0}>`.\n'.format(codelist)) 
                    fp.write('\n  \n  '+ruleset_text(path+element_name+'/@'+attribute))
                    fp.write('\n')
                fp.write('\n\n')

            #FIXME (element_loop does not belong here)
            childnames = self.element_loop(element, path)
            if childnames:
                fp.write('\nSubelements\n~~~~~~~~~~~\n\n')
                fp.write('.. toctree::\n   :titlesonly:\n   :maxdepth: 1\n\n')
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
        type_attributeGroups = []
        if 'type' in a:
            complexType = self.get_complexType(a['type'])
            if complexType is None:
                print 'Notice: No attributes for', a['type']
            else:
                type_attributes = complexType.findall('xsd:attribute', namespaces=namespaces)
                type_attributeGroups = complexType.findall('xsd:attributeGroup', namespaces=namespaces)
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

        group_attributes = []
        for attributeGroup in ( 
            element.findall('xsd:complexType/xsd:attributeGroup', namespaces=namespaces) +
            element.findall('xsd:complexType/xsd:simpleContent/xsd:extension/xsd:attributeGroup', namespaces=namespaces) +
            type_attributeGroups
            ):
            group_attributes += self.get_attributeGroup(attributeGroup.attrib['ref']).findall('xsd:attribute', namespaces=namespaces)

        out = []
        for attribute in (
            element.findall('xsd:complexType/xsd:attribute', namespaces=namespaces) +
            element.findall('xsd:complexType/xsd:simpleContent/xsd:extension/xsd:attribute', namespaces=namespaces) +
            type_attributes + group_attributes
            ):
            if 'ref' in attribute.attrib:
                if attribute.get('ref') in custom_attributes:
                    out.append((attribute.get('ref'), '', custom_attributes[attribute.get('ref')]))
                    continue
                attribute = self.get_attribute(attribute.get('ref'))
            doc = attribute.find(".//xsd:documentation", namespaces=namespaces)
            if doc is not None:
                out.append((attribute.get('name'), attribute.get('type'), doc.text))
            else:   
                print 'Ack', ET.tostring(attribute)
        return out

activities = Schema2Doc('iati-activities-schema.xsd')
activities.get_element('iati-activities', '')

orgs = Schema2Doc('iati-organisations-schema.xsd')
orgs.get_element('iati-organisations', '')


