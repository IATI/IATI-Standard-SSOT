from lxml import etree as ET
import os, json, csv, shutil, re
import textwrap
import jinja2

languages = ['en','fr']

# Namespaces necessary for opening schema files
namespaces = {
    'xsd': 'http://www.w3.org/2001/XMLSchema'
}
# Attributes that have documentation that differs to that in the schema
custom_attributes = {
    'xml:lang': 'ISO 2 letter code specifying the language of text in this element.'
}

def get_github_url(repo, path=''):
    github_branches = {
        'IATI-Schemas': 'version-1.04',
        'IATI-Codelists': 'version-1.04',
        'IATI-Rulesets': 'version-1.04',
        'IATI-Extra-Documentation': 'version-1.04',
        'IATI-Codelists-NonEmbedded': 'master',
    }
    return 'https://github.com/IATI/{0}/blob/{1}/{2}'.format(repo, github_branches[repo], path)

def human_list(l):
    """
    Returns a human friendly version of a list. Currently seperates list items
    with comas, but could be extended to insert 'and'/'or' correctly.

    """
    return ', '.join(l)

# TODO - This function should be moved into the IATI-Rulesets submodule
rulesets = json.load(open('./IATI-Rulesets/rulesets/standard.json'))
def ruleset_text(path):
    """ Return a list of text describing the rulesets for a given path (xpath) """
    out = []
    for xpath, rules in rulesets.items():
        if xpath.startswith('//'):
            try:
                reduced_path = path.split(xpath[2:]+'/')[1]
                for rule in rules:
                    cases = rules[rule]['cases']
                    for case in cases:
                        simplify_xpath = lambda x: re.sub('\[[^\]]*\]', '', x)
                        if 'paths' in case:
                            for case_path in case['paths']:
                                # Don't forget [@ ]
                                if simplify_xpath(case_path) == reduced_path:
                                    other_paths = case['paths']
                                    other_paths.remove(case_path)
                                    if rule == 'only_one':
                                        out.append('``{0}`` must be present only once.'.format(case_path))
                                        if other_paths:
                                            out.append('``{0}`` must not be present if ``{1}`` are present.'.format(case_path, human_list(other_paths)))
                                    elif rule == 'atleast_one':
                                        if other_paths:
                                            out.append('Either ``{0}`` or ``{1}`` must be present.'.format(case_path, human_list(other_paths)))
                                        else:
                                            out.append('``{0}`` must be present.\n\n'.format(case_path))
                                    elif rule == 'startswith':
                                        out.append('``{0}`` should start with the value in ``{1}``'.format(case_path, case['start']))
                                    else: print case_path, rule, case['paths'] 
                        elif rule == 'date_order':
                            if simplify_xpath(case['less']) == reduced_path or simplify_xpath(case['more']) == reduced_path:
                                if case['less'] == 'NOW':
                                    out.append('``{0}`` must be in the future.\n\n'.format(case['more']))
                                elif case['more'] == 'NOW':
                                    out.append('``{0}`` must be today, or in the past.\n\n'.format(case['less']))
                                else:
                                    out.append('``{0}`` must be before ``{1}``\n\n'.format(case['less'], case['more']))
                        else: print case_path, rule, case['paths'] 
            except IndexError:
                pass
    return out


from collections import defaultdict
codelists_paths = defaultdict(list)
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
                codelist = mapping.find('codelist').attrib['ref']
                if not path in codelists_paths[codelist]:
                    codelists_paths[codelist].append(path)
                return codelist
            else:
                pass # FIXME
    return

def path_to_ref(path):
    return path.replace('//','_').replace('@','.')


def get_extra_docs(rst_filename):
    extra_docs_file = os.path.join('IATI-Extra-Documentation', rst_filename)
    if os.path.isfile(extra_docs_file):
        with open(extra_docs_file) as fp:
            return fp.read().decode('utf8')
    else:
        return ''
            


class Schema2Doc(object):
    """
    Class for converting an IATI XML schema to documentation in the
    reStructuredText format.

    """
    def __init__(self, schema, lang):
        """
        schema -- the filename of the schema to use, e.g.
                  'iati-activities-schema.xsd'

        """
        self.tree = ET.parse("./IATI-Schemas/"+schema)
        self.tree2 = ET.parse("./IATI-Schemas/iati-common.xsd")
        self.jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
        self.lang = lang

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

        github_urls = {
            'schema': element.base.replace('./IATI-Schemas/', get_github_url('IATI-Schemas')) + '#L' + str(element.sourceline),
            'extra_documentation': get_github_url('IATI-Extra-Documentation', self.lang+'/'+path[:-1]+'.rst')
        }
        try:
            os.makedirs(os.path.join('docs', self.lang, path))
        except OSError: pass

        rst_filename = os.path.join(self.lang, path, element_name+'.rst')

        children = self.element_loop(element, path)
        for child_name, child_element in children:
            self.output_docs(child_name, path+element.attrib['name']+'/', child_element)
                
        with open('docs/'+rst_filename, 'w') as fp:
            t = self.jinja_env.get_template(self.lang+'/schema_element.rst')
            fp.write(t.render(
                element_name=element_name,
                element_name_underline='='*len(element_name),
                element=element,
                path='/'.join(path.split('/')[1:]),
                github_urls=github_urls,
                schema_documentation=textwrap.dedent(element.find(".//xsd:documentation", namespaces=namespaces).text),
                extended_types=element.xpath('xsd:complexType/xsd:simpleContent/xsd:extension/@base', namespaces=namespaces),
                attributes=self.attribute_loop(element),
                textwrap=textwrap,
                match_codelist=match_codelist,
                path_to_ref=path_to_ref,
                ruleset_text=ruleset_text,
                childnames = [x[0] for x in children],
                extra_docs=get_extra_docs(rst_filename)
            ).encode('utf8'))


    def output_schema_table(self, element_name, path, element=None, output=False, filename='', title=''):
        if element is None:
            element = self.get_schema_element('element', element_name)
            if element is None:
                return

        extended_types = element.xpath('xsd:complexType/xsd:simpleContent/xsd:extension/@base', namespaces=namespaces)
        rows = [{
            'name': element_name,
            'path': '/'.join(path.split('/')[1:])+element_name,
            'doc': path+element_name,
            'description': textwrap.dedent(element.find(".//xsd:documentation", namespaces=namespaces).text),
            'type': element.get('type') if element.get('type') and element.get('type').startswith('xsd:') else '',
            'section': len(path.split('/')) < 5
        }]

        if element.xpath('xsd:complexType[@mixed="true"] or xsd:complexType/xsd:simpleContent', namespaces=namespaces):
            rows.append({
                'path': '/'.join(path.split('/')[1:])+element_name+'/text()',
                'description': '',
                'type': 'mixed' if element.xpath('xsd:complexType[@mixed="true"]', namespaces=namespaces) else  ','.join([x for x in extended_types if x.startswith('xsd:')]),
            })

        for a_name, a_type, a_description, a_required in self.attribute_loop(element):
            rows.append({
                'attribute_name': a_name,
                'path': '/'.join(path.split('/')[1:])+element_name+'/@'+a_name,
                'description': textwrap.dedent(a_description),
                'type': a_type,
                'occur': '1..1' if a_required else '0..1'
            })

        for child_name, child_element in self.element_loop(element, path):
            rows += self.output_schema_table(child_name, path+element.attrib['name']+'/', child_element)

        if output:
            with open(os.path.join('docs', self.lang, filename), 'w') as fp:
                t = self.jinja_env.get_template(self.lang+'/schema_table.rst')
                fp.write(t.render(
                    rows=rows,
                    title=title,
                    root_path=path,
                    match_codelist=match_codelist,
                    description=self.tree.xpath('xsd:annotation/xsd:documentation[@xml:lang="en"]', namespaces=namespaces)[0].text
                ).encode('utf8'))
        else:
            return rows
            
        


    def element_loop(self, element, path):
        """
        Loop over the children of a given element, and run output_docs on each.

        Returns the names of the child elements.

        """
        children = ( element.findall('xsd:complexType/xsd:choice/xsd:element', namespaces=namespaces)
            + element.findall("xsd:complexType/xsd:all/xsd:element", namespaces=namespaces) )
        child_tuples = []
        for child in children:
            a = child.attrib
            if 'name' in a:
                child_tuples.append((a['name'], child))
            else:
                child_tuples.append((a['ref'], None))
        return child_tuples

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
            doc = attribute.find(".//xsd:documentation", namespaces=namespaces)
            if 'ref' in attribute.attrib:
                if attribute.get('ref') in custom_attributes:
                    out.append((attribute.get('ref'), '', custom_attributes[attribute.get('ref')], attribute.get('use')=='required'))
                    continue
                attribute = self.get_schema_element('attribute', attribute.get('ref'))
                if doc is None:
                    # Only fetch the documentation of the referenced definition
                    # if we don't already have documentation.
                    doc = attribute.find(".//xsd:documentation", namespaces=namespaces)
            if doc is not None:
                out.append((attribute.get('name'), attribute.get('type'), doc.text, attribute.get('use')=='required'))
            else:
                print 'Ack', ET.tostring(attribute)
        return out


def codelists_to_docs(lang):
    dirname = 'IATI-Codelists/out/json/'+lang
    try:
        os.mkdir('docs/'+lang+'/codelists/')
    except OSError: pass

    for fname in os.listdir(dirname):
        json_file = os.path.join(dirname, fname)
        if not fname.endswith('.json'): continue
        with open(json_file) as fp: 
            codelist_json = json.load(fp)
        
        fname = fname[:-5]
        if os.path.exists(os.path.join('IATI-Codelists','xml',fname+'.xml')):
            github_url = get_github_url('IATI-Codelists', 'xml/{0}.xml'.format(fname))
        else:
            github_url = get_github_url('IATI-Codelists-NonEmbedded', 'xml/{0}.xml'.format(fname))

        rst_filename = os.path.join(lang, 'codelists', fname+'.rst')
        with open(os.path.join('docs', rst_filename), 'w') as fp:
            jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
            t = jinja_env.get_template(lang+'/codelist.rst')
            fp.write(t.render(
                codelist_json=codelist_json,
                fname=fname,
                len=len,
                github_url=github_url,
                codelist_paths=codelists_paths.get(fname),
                path_to_ref=path_to_ref,
                extra_docs=get_extra_docs(rst_filename),
                lang=lang).encode('utf-8'))

def extra_extra_docs():
    """
    Copy over files from IATI-Extra-Documentation that haven't been created in
    the docs folder by another function.

    """
    for dirname, dirs, files in os.walk('IATI-Extra-Documentation', followlinks=True):
        for fname in files:
            if len(dirname.split(os.path.sep)) == 1:
                rst_dirname = ''
            else:
                rst_dirname = os.path.join(*dirname.split(os.path.sep)[1:])
            rst_filename = os.path.join(rst_dirname, fname)
            if not os.path.exists(os.path.join('docs', rst_filename)):
                try:
                    os.makedirs(os.path.join('docs', rst_dirname))
                except OSError:
                    pass
                if fname.endswith('.rst'):
                    with open(os.path.join('docs', rst_filename), 'w') as fp:
                        fp.write(get_extra_docs(rst_filename).encode('utf-8'))
                else:
                    shutil.copy(os.path.join(dirname,fname), os.path.join('docs', rst_filename))

if __name__ == '__main__':
    for language in languages:
        activities = Schema2Doc('iati-activities-schema.xsd', lang=language)
        activities.output_docs('iati-activities', 'activities-standard/')
        activities.output_schema_table('iati-activities', 'activities-standard/', output=True,
            filename='activities-standard/overview-table.rst',
            title='Activity Standard Overview Table')

        orgs = Schema2Doc('iati-organisations-schema.xsd', lang=language)
        orgs.output_docs('iati-organisations', 'organisation-standard/')
        orgs.output_schema_table('iati-organisations', 'organisation-standard/', output=True,
            filename='organisation-standard/overview-table.rst',
            title='Organisation Standard Overview Table')
        
        codelists_to_docs(lang=language)
    extra_extra_docs()

