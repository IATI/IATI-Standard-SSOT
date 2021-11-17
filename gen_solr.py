import re
from schema2doc import Schema2Doc

# Define the namespaces necessary for opening schema files
namespaces = {
    'xsd': 'http://www.w3.org/2001/XMLSchema'
}

def path_to_solr(path):
    final = path
    if 'iati-activities/iati-activity/@' in path:
        final = path.replace('iati-activities/iati-activity/@','')
    elif 'iati-activities/iati-activity/' in path:
        final = path.replace('iati-activities/iati-activity/','')
    elif 'iati-activities' in path:
        final = path.replace('iati-activities', 'dataset')
    return final.replace('/@','_').replace('/','_').replace('-', '_').replace(':','_')

def xsd_type_to_solr(element_name = None, xsd_type = None):
    if (element_name is not None and re.search('_narrative$', element_name) is not None):
        return "text_general"

    if (element_name == 'location_administrative_level'):
        return "text_gen_sort"
    
    switch={
    'xsd:string': 'text_gen_sort',
    'xsd:NMTOKEN': 'text_gen_sort',
    'xsd:anyURI': 'text_general',
    'xsd:decimal': 'pdoubles',
    'xsd:dateTime': 'pdate',
    'xsd:date': 'pdate',
    'xsd:boolean': 'boolean',
    'xsd:nonNegativeInteger': 'pint',
    'xsd:positiveInteger': 'pint',
    'xsd:int': 'pint',
    'currencyType': 'pdoubles'
    }
    return switch.get(xsd_type,"text_gen_sort")

class Schema2Solr(Schema2Doc):

    def output_solr(self, element_name, path, element=None, output=False, filename='', out_type='order', minOccurs='', maxOccurs='', ref_element=None, type_element=None, parent_req=True, parent_multi=False):
        if element is None:
            element = self.get_schema_element('element', element_name)
            if element is None:
                return

        extended_types = element.xpath('xsd:complexType/xsd:simpleContent/xsd:extension/@base', namespaces=namespaces)

        full_path = '/'.join(path.split('/')[1:]) + element_name
        solr_name = path_to_solr(full_path)       
        xsd_type = element.get('type') if element.get('type') and (element.get('type').startswith('xsd:') or element.get('type') == 'currencyType') else ''
        required = (minOccurs == '1') and parent_req
        if element_name == 'iati-activity':
            maxOccurs = '1'
        multivalued = (maxOccurs == 'unbounded') or parent_multi
        
        rows = []
        # elements should only be in solr if they contain something with a type, otherwise they wouldn't have a flattened value
        if element.xpath('xsd:complexType[@mixed="true"] or xsd:complexType/xsd:simpleContent', namespaces=namespaces) or xsd_type != '':
            rows = [{
                "name": element_name ,
                'path': full_path,
                "solr_field_name": solr_name ,
                'type': xsd_type,
                'solr_type': xsd_type_to_solr(solr_name, xsd_type),
                'required': required,
                'solr_required': 'true' if required else 'false',
                'solr_multivalued': 'true' if multivalued else 'false'
            }]

        for a_name, a_type, a_description, a_required in self.attribute_loop(element):
            full_path = '/'.join(path.split('/')[1:]) + element_name + '/@' + a_name
            solr_name = path_to_solr(full_path)      

            rows.append({
                'attribute_name': a_name,
                'path': full_path,
                'solr_field_name': solr_name,
                'type': a_type,
                'solr_type': xsd_type_to_solr(solr_name, xsd_type=a_type),
                'solr_required': 'true' if required and a_required else 'false',
                'solr_multivalued': 'true' if multivalued else 'false'
            })

        for child_name, child_element, child_ref_element, child_type_element, minOccurs, maxOccurs in self.element_loop(element, path):
            rows += self.output_solr(child_name, path + element.attrib['name'] + '/', child_element, minOccurs=minOccurs, maxOccurs=maxOccurs, ref_element=child_ref_element, type_element=child_type_element, parent_req=required, parent_multi=multivalued)

        if output:
            if out_type == 'order':
                with open(filename, 'w') as fp:
                    fp.write('<str name="fl">')
                    stop = len(rows)
                    for i, row in enumerate(rows):
                        if row['solr_field_name'] in ['dataset', 'dataset_iati_activity']:
                            continue
                        fp.write(row['solr_field_name'])
                        if i < stop - 1:
                            fp.write(',')
                    fp.write('</str>')
            if out_type == 'schema':
                with open(filename, 'w') as fp:
                    for row in rows:
                        if row['solr_field_name'] in ['dataset', 'dataset_iati_activity']:
                            continue
                        
                        line = '<field '
                        line += 'name="' + row['solr_field_name'] + '" '
                        line += 'type="' + row['solr_type'] + '" ' 
                        line += 'multiValued="' + row['solr_multivalued'] + '" '
                        line += 'indexed="true" '
                        line += 'required="false" '
                        line += 'stored="true" '
                        line += ' />\n'
                        fp.write(line)
        return rows



activities = Schema2Solr('iati-activities-schema.xsd', lang='en')
activities.output_solr(
    'iati-activities', 'activity-standard/', output=True,
    filename='solr_fl.xml', out_type='order'
)
activities.output_solr(
    'iati-activities', 'activity-standard/', minOccurs='1', maxOccurs='1', output=True,
    filename='solr_schema.xml', out_type='schema'
)
