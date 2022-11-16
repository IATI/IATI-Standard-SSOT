import re
import textwrap
import json
import sys
from gen import Schema2Doc, codelist_mappings, codelists_paths


# Define the namespaces necessary for opening schema files
namespaces = {
    'xsd': 'http://www.w3.org/2001/XMLSchema'
}


def match_codelists(path):
    """
    Looks up the codelist that the given path (xpath) should be on.
    Returns a tuple of the codelist name, and a boolean as describing whether any conditions apply.
    If there is no codelist for the given path, the first part of the tuple is None.

    """
    codelist_tuples = []
    for mapping in codelist_mappings:
        if mapping.find('path').text.startswith('//'):
            if path.endswith(mapping.find('path').text.strip('/')):
                codelist = mapping.find('codelist').attrib['ref']
                if path not in codelists_paths[codelist]:
                    codelists_paths[codelist].append(path)
                condition = mapping.find('condition')
                tup = (codelist, '' if condition is None else condition.text)
                codelist_tuples.append(tup)
            else:
                pass
    return codelist_tuples


def field_to_label(field):
    up_str = ''
    for word in field.split('_'):
        if up_str == '':
            up_str = word.capitalize()
        else:
            up_str += " " + word.capitalize()
    return up_str


def get_codelist_json(name):
    return json.load(open('IATI-Codelists/out/clv3/json/en/' + name + '.json'))


def path_to_solr(path):
    final = path
    if 'iati-activities/iati-activity/@' in path:
        final = path.replace('iati-activities/iati-activity/@', '')
    elif 'iati-activities/iati-activity/' in path:
        final = path.replace('iati-activities/iati-activity/', '')
    elif 'iati-activities' in path:
        final = path.replace('iati-activities', 'dataset')
    return final.replace('/@', '_').replace('/', '_').replace('-', '_').replace(':', '_')


def xsd_type_to_search(element_name=None, xsd_type=None):
    if (element_name is not None and re.search('_narrative$', element_name) is not None):
        return "text"

    if (element_name == 'location_administrative_level'):
        return "text"

    switch = {
        'xsd:string': 'text',
        'xsd:NMTOKEN': 'text',
        'xsd:anyURI': 'text',
        'xsd:decimal': 'number',
        'xsd:dateTime': 'date',
        'xsd:date': 'date',
        'xsd:boolean': 'boolean',
        'xsd:nonNegativeInteger': 'integer',
        'xsd:positiveInteger': 'integer',
        'xsd:int': 'integer'
    }
    return switch.get(xsd_type, "text")


def filter_columns(row):
    if row['field'] in ['dataset', 'dataset_iati_activity']:
        return False
    return True


class Schema2Solr(Schema2Doc):

    def output_solr(self, element_name, path, element=None, output=False, template_path='', filename='', codelist_dest='', collection='', out_type='order', minOccurs='', maxOccurs='', ref_element=None, type_element=None, parent_req=True, parent_multi=False):
        if element is None:
            element = self.get_schema_element('element', element_name)
            if element is None:
                return

        full_path = '/'.join(path.split('/')[1:]) + element_name
        solr_name = path_to_solr(full_path)
        xsd_type = element.get('type') if element.get('type') and element.get('type').startswith('xsd:') else ''
        if type_element is not None:
            complex_base_types = [x for x in type_element.xpath('xsd:simpleContent/xsd:extension/@base', namespaces=namespaces) if x.startswith('xsd:')]
            if len(complex_base_types) and xsd_type == '':
                xsd_type = complex_base_types[0]
        required = (minOccurs == '1') and parent_req
        if element_name == 'iati-activity':
            maxOccurs = '1'
        multivalued = (maxOccurs == 'unbounded') or parent_multi

        rows = []
        # elements should only be in solr if they contain something with a type, otherwise they wouldn't have a flattened value
        if element.xpath('xsd:complexType[@mixed="true"] or xsd:complexType/xsd:simpleContent', namespaces=namespaces) or xsd_type != '':
            rows = [{
                "field": solr_name,
                "label": field_to_label(solr_name),
                'type': xsd_type_to_search(solr_name, xsd_type),
                "description": textwrap.dedent(self.schema_documentation(element, ref_element, type_element)),
                "name": element_name,
                'path': full_path,
                'xsd_type': xsd_type,
                'solr_required': 'true' if required else 'false',
                'solr_multivalued': 'true' if multivalued else 'false'
            }]

        for a_name, a_type, a_description, a_required in self.attribute_loop(element):
            full_path = '/'.join(path.split('/')[1:]) + element_name + '/@' + a_name
            solr_name = path_to_solr(full_path)
            codelist_name_tup = match_codelists(full_path)
            codelist_names = [tup[0] for tup in codelist_name_tup]
            codelist_conditions = [tup[1] for tup in codelist_name_tup]

            # use parent description if attribute description is blank (mainly for @iso-date)
            description = ''
            if a_description == '':
                description = self.schema_documentation(element, ref_element, type_element)
            else:
                description = a_description
            rows.append({
                'field': solr_name,
                "label": field_to_label(solr_name),
                'type': 'combo' if len(codelist_conditions) > 0 else 'select' if len(codelist_names) > 0 else xsd_type_to_search(solr_name, xsd_type=a_type),
                'description': textwrap.dedent(description),
                'codelist_names': codelist_names,
                'codelist_conditions': codelist_conditions,
                'attribute_name': a_name,
                'path': full_path,
                'xsd_type': a_type,
                'solr_required': 'true' if required and a_required else 'false',
                'solr_multivalued': 'true' if multivalued else 'false'
            })

        for child_name, child_element, child_ref_element, child_type_element, minOccurs, maxOccurs in self.element_loop(element, path):
            rows += self.output_solr(child_name, path + element.attrib['name'] + '/', child_element, minOccurs=minOccurs, maxOccurs=maxOccurs, ref_element=child_ref_element, type_element=child_type_element, parent_req=required, parent_multi=multivalued)

        if output:
            out = ''
            if out_type == 'filter':
                out = list(filter(filter_columns, rows))
                with open(filename, 'w') as fp:
                    json.dump(out, fp, indent=2)
                codelists = {}
                for row in out:
                    if 'codelist_name' in row and row['codelist_name'] != '':
                        name = row['codelist_name']
                        codelists[name] = (get_codelist_json(name))
                with open(codelist_dest, 'w') as fp:
                    json.dump(codelists, fp, indent=2)
        return rows


if __name__ == '__main__':
    filter_dest = sys.argv[1]
    codelist_dest = sys.argv[2]

    activities = Schema2Solr('iati-activities-schema.xsd', lang='en')
    activities.output_solr(
        'iati-activities', 'activity-standard/', minOccurs='1', maxOccurs='1', output=True,
        filename=filter_dest, codelist_dest=codelist_dest, out_type='filter'
    )
