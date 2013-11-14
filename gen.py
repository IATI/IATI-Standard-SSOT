from lxml import etree as ET
import os
import textwrap
import json
import jinja2

# Namespaces necessary for opening schema files
namespaces = {
    'xsd': 'http://www.w3.org/2001/XMLSchema'
}
# Attrbitues that have documentation that differs to that in the schema
custom_attributes = {
    'xml:lang': 'ISO 2 letter code specifying the language of text in this element.'
}

def human_list(l):
    """
    Returns a human friendly version of a list. Currently seperates list items
    with comas, but could be extended to insert 'and'/'or' correctly.

    """
    return ', '.join(l)

# TODO - This function should be moved into the IATI-Rulesets submodule
rulesets = json.load(open('./IATI-Rulesets/rulesets.json'))
def ruleset_text(path):
    """ Return text describing the rulesets for a given path (xpath) """
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
                                            out += 'Either this element or {0} must be present. '.format(human_list(other_paths))
                                        else:
                                            out += 'This element must be present. ' 
                                    else: print case_path, rule, case['paths'] 
                                    break
            except IndexError:
                pass
    if out != '':
        out += '(`see rulesets.json <https://github.com/IATI/IATI-Rulesets/blob/master/rulesets.json>`_)'
    return out


# TODO - This function should be moved into the IATI-Codelists submodule
codelist_mappings = ET.parse('./IATI-Codelists/mapping.xml').getroot().findall('mapping')
def match_codelist(path):
    """
    Returns the name of the codelist that the given path (xpath) should be on.
    If there is no codelist for the given path, None is returned.

    """
    for mapping in codelist_mappings:
        if mapping.find('path').text.startswith('//'):
            #print mapping.find('path').text.strip('/'), path
            if mapping.find('path').text.strip('/') in path:
                return mapping.find('codelist').attrib['ref']
            else:
                pass # FIXME
    return



class Schema2Doc(object):
    """
    Class for converting an IATI XML schema to documentation in the
    reStructuredText format.

    """
    def __init__(self, schema):
        """
        schema -- the filename of the schema to use, e.g.
                  'iati-activities-schema.xsd'

        """
        self.tree = ET.parse("./IATI-Schemas/"+schema)
        self.tree2 = ET.parse("./IATI-Schemas/iati-common.xsd")
        self.jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))

    def get_schema_element(self, tag_name, name_attribute):
        """
        Returns the specified element from the schema.

        tag_name -- the name of the tag in the schema, e.g. 'complexType'
        name_attribute -- the value of the 'name' attribute in the schema, ie.
                          the name of the element/type etc. being described,
                          e.g. iati-activities

        """
        schema_element = self.tree.find("xsd:{0}[@name='{1}']".format(tag_name, name_attribute), namespaces=namespaces)
        if schema_element is None:
            schema_element = self.tree2.find("xsd:{0}[@name='{1}']".format(tag_name, name_attribute), namespaces=namespaces)
        return schema_element

    def output_docs(self, element_name, path, element=None):
        """
        Output documentation for the given element, and it's children.

        If element is not given, we try to find it in the schema using it's
        element_name.

        path is the xpath of the context where this element was found, for the
        root context, this is the empty string 

        """
        if element is None:
            element = self.get_schema_element('element', element_name)
            if element is None:
                return

        url = element.base.replace('./IATI-Schemas/', 'https://github.com/IATI/IATI-Schemas/blob/master/') + '#L' + str(element.sourceline)
        try:
            os.makedirs('docs/'+path)
        except OSError:
            pass
        with open('docs/'+path+element_name+'.rst', 'w') as fp:
            t = self.jinja_env.get_template('schema_element.rst')
            fp.write(t.render(
                element_name=element_name,
                element_name_underline='='*len(element_name),
                element=element,
                path=path,
                url=url,
                schema_documentation=textwrap.dedent(element.find(".//xsd:documentation", namespaces=namespaces).text),
                ruleset_text=ruleset_text(path+element_name),
                extended_types=element.xpath('xsd:complexType/xsd:simpleContent/xsd:extension/@base', namespaces=namespaces),
                attributes=self.attribute_loop(element),
                textwrap=textwrap, match_codelist=match_codelist, ruleset_text_=ruleset_text, #FIXME
                childnames = self.element_loop(element, path)
            ))

    def element_loop(self, element, path):
        """
        Loop over the children of a given element, and run output_docs on each.

        Returns the names of the child elements.

        """
        children = ( element.findall('xsd:complexType/xsd:choice/xsd:element', namespaces=namespaces)
            + element.findall("xsd:complexType/xsd:all/xsd:element", namespaces=namespaces) )
        childnames = []
        for child in children:
            a = child.attrib
            if 'name' in a:
                self.output_docs(a['name'], path+element.attrib['name']+'/', child)
                childnames.append(a['name'])
            else:
                self.output_docs(a['ref'], path+element.attrib['name']+'/')
                childnames.append(a['ref'])
        return childnames

    def attribute_loop(self, element):
        """
        Returns a list containing a tuple for each attribute the given element
        can have.

        The format of the tuple is (name, type, documentation)

        """
        #if element.find("xsd:complexType[@mixed='true']", namespaces=namespaces) is not None:
        #    print_column_info('text', indent)
            
        a = element.attrib
        type_attributes = []
        type_attributeGroups = []
        if 'type' in a:
            complexType = self.get_schema_element('complexType', a['type'])
            if complexType is None:
                print 'Notice: No attributes for', a['type']
            else:
                type_attributes = (
                    complexType.findall('xsd:attribute', namespaces=namespaces) +
                    complexType.findall('xsd:simpleContent/xsd:extension/xsd:attribute', namespaces=namespaces)
                    )
                type_attributeGroups = (
                    complexType.findall('xsd:attributeGroup', namespaces=namespaces) +
                    complexType.findall('xsd:simpleContent/xsd:extension/xsd:attributeGroup', namespaces=namespaces)
                    )

        group_attributes = []
        for attributeGroup in ( 
            element.findall('xsd:complexType/xsd:attributeGroup', namespaces=namespaces) +
            element.findall('xsd:complexType/xsd:simpleContent/xsd:extension/xsd:attributeGroup', namespaces=namespaces) +
            type_attributeGroups
            ):
            group_attributes += self.get_schema_element('attributeGroup', attributeGroup.attrib['ref']).findall('xsd:attribute', namespaces=namespaces)

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
                attribute = self.get_schema_element('attribute', attribute.get('ref'))
            doc = attribute.find(".//xsd:documentation", namespaces=namespaces)
            if doc is not None:
                out.append((attribute.get('name'), attribute.get('type'), doc.text))
            else:
                print 'Ack', ET.tostring(attribute)
        return out

if __name__ == '__main__':
    activities = Schema2Doc('iati-activities-schema.xsd')
    activities.output_docs('iati-activities', '')

    orgs = Schema2Doc('iati-organisations-schema.xsd')
    orgs.output_docs('iati-organisations', '')

