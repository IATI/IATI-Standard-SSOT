from __future__ import print_function
from lxml import etree as ET
import os, json, csv, shutil, re
import textwrap
import jinja2
from iatirulesets.text import rules_text

languages = ['en']

# Namespaces necessary for opening schema files
namespaces = {
    'xsd': 'http://www.w3.org/2001/XMLSchema'
}
# Attributes that have documentation that differs to that in the schema
custom_attributes = {
}

def get_github_url(repo, path=''):
    github_branches = {
        'IATI-Schemas': 'version-2.02',
        'IATI-Codelists': 'version-2.02',
        'IATI-Rulesets': 'version-2.02',
        'IATI-Extra-Documentation': 'version-2.02',
        'IATI-Codelists-NonEmbedded': 'master',
    }
    return 'https://github.com/IATI/{0}/blob/{1}/{2}'.format(repo, github_branches[repo], path)

def human_list(l):
    """
    Returns a human friendly version of a list. Currently seperates list items
    with comas, but could be extended to insert 'and'/'or' correctly.

    """
    return ', '.join(l)


def lookup_see_also(standard, mapping, path):
    if path == '': return
    for overview, elements in mapping.items():
        if path in elements:
            yield '/'+standard+'/overview/'+overview
    for x in lookup_see_also(standard, mapping, '/'.join(path.split('/')[:-1])):
        yield x

def see_also(path, lang):
    standard = path.split('/')[0]
    if lang == 'en': # FIXME
        mapping = json.load(open(os.path.join('IATI-Extra-Documentation', lang, standard, 'overview-mapping.json'))) # Loading this file is incredibly inefficient
        # Common 'simple' path e.g. iati-activities or budget/period-start
        # Using this prevents subpages of iati-activity using the activity file overview
        simpler = len(path.split('/')) > 3
        simple_path = '/'.join(path.split('/')[3:]) if simpler else path
        return list(lookup_see_also(standard, mapping, simple_path))

standard_ruleset = json.load(open('./IATI-Rulesets/rulesets/standard.json'))

def ruleset_page(lang):
    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
    ruleset = { xpath:rules_text(rules, '', True) for xpath, rules in standard_ruleset.items() }
    rst_filename = os.path.join(lang, 'rulesets', 'standard-ruleset.rst')

    try:
        os.mkdir(os.path.join('docs', lang, 'rulesets'))
    except OSError: pass

    with open(os.path.join('docs', rst_filename), 'w') as fp:
        t = jinja_env.get_template(lang+'/ruleset.rst')
        fp.write(t.render(
            ruleset = ruleset,
            extra_docs=get_extra_docs(rst_filename)
        ).encode('utf8'))

def ruleset_text(path):
    """ Return a list of text describing the rulesets for a given path (xpath) """
    out = []
    for xpath, rules in standard_ruleset.items():
        if xpath.startswith('//'):
            try:
                # Use slice 1: to ensure we match /budget/ but not /total-budget/
                reduced_path = path.split(xpath[1:]+'/')[1]
            except IndexError:
                continue
            out += rules_text(rules, reduced_path)
    return out


from collections import defaultdict
codelists_paths = defaultdict(list)
# TODO - This function should be moved into the IATI-Codelists submodule
codelist_mappings = ET.parse('./IATI-Codelists/mapping.xml').getroot().findall('mapping')
def match_codelist(path):
    """
    Looks up the codelist that the given path (xpath) should be on.
    Returns a tuble of the codelist name, and a boolean as describing whether any conditions apply.
    If there is no codelist for the given path, the first part of the tuple is None.

    """
    for mapping in codelist_mappings:
        if mapping.find('path').text.startswith('//'):
            if path.endswith(mapping.find('path').text.strip('/')):
                codelist = mapping.find('codelist').attrib['ref']
                if not path in codelists_paths[codelist]:
                    codelists_paths[codelist].append(path)
                return (codelist, mapping.find('condition') is not None)
            else:
                pass # FIXME
    return

def is_complete_codelist(codelist_name):
    """Determine whether the specified Codelist is complete.

    Args:
        codelist_name (str): The name of the Codelist. This is case-sensitive and must match the mapping file.

    Returns:
        bool: Whether the Codelist is complete.

    Note:
        Need to manually specify which Codelists are incomplete - it is not auto-detected. This is due to the surrounding architecture making it a challenge to auto-detect this information.

    """
    # use a list of incomplete Codelists since it is shorter
    incomplete_codelists = [
        'Country',
        'HumanitarianScopeType',
        'HumanitarianScopeVocabulary',
        'IndicatorVocabulary',
        'OrganisationIdentifier',
        'OrganisationRegistrationAgency'
    ]
    return codelist_name not in incomplete_codelists

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
        lang -- the language code to build the documentation for (e.g. 'en')

        """
        self.tree = ET.parse("./IATI-Schemas/"+schema)
        self.tree2 = ET.parse("./IATI-Schemas/iati-common.xsd")
        self.jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
        self.lang = lang
        
        self.jinja_env.filters['is_complete_codelist'] = is_complete_codelist

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

    def schema_documentation(self, element, ref_element):
        if ref_element is not None:
            xsd_docuementation = ref_element.find(".//xsd:documentation", namespaces=namespaces)
            if xsd_docuementation is not None:
                return ref_element.find(".//xsd:documentation", namespaces=namespaces).text
        return element.find(".//xsd:documentation", namespaces=namespaces).text


    def output_docs(self, element_name, path, element=None, minOccurs='', maxOccurs='', ref_element=None):
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
            'extra_documentation': get_github_url('IATI-Extra-Documentation', self.lang+'/'+path+element_name+'.rst')
        }
        try:
            os.makedirs(os.path.join('docs', self.lang, path))
        except OSError: pass

        rst_filename = os.path.join(self.lang, path, element_name+'.rst')

        children = self.element_loop(element, path)
        for child_name, child_element, child_ref_element, child_minOccurs, child_maxOccurs in children:
            self.output_docs(child_name, path+element.attrib['name']+'/', child_element, child_minOccurs, child_maxOccurs, child_ref_element)

        min_occurss = element.xpath('xsd:complexType/xsd:choice/@minOccur', namespaces=namespaces)
        # Note that this min_occurs is different to the python variables
        # minOccurs and maxOccurs, because this is read from a choice element,
        # whereas those are read from the individual element definitions (only
        # possible within a sequence element)
        if min_occurss:
            min_occurs = int(min_occurss[0])
        else:
            min_occurs = 0

        with open('docs/'+rst_filename, 'w') as fp:
            t = self.jinja_env.get_template(self.lang+'/schema_element.rst')
            fp.write(t.render(
                element_name=element_name,
                element_name_underline='='*len(element_name),
                element=element,
                path='/'.join(path.split('/')[1:]), # Strip e.g. activity-standard/ from the path
                github_urls=github_urls,
                schema_documentation=textwrap.dedent(self.schema_documentation(element, ref_element)),
                extended_types=element.xpath('xsd:complexType/xsd:simpleContent/xsd:extension/@base', namespaces=namespaces),
                attributes=self.attribute_loop(element),
                textwrap=textwrap,
                match_codelist=match_codelist,
                path_to_ref=path_to_ref,
                ruleset_text=ruleset_text,
                childnames = [x[0] for x in children],
                extra_docs=get_extra_docs(rst_filename),
                min_occurs=min_occurs,
                minOccurs=minOccurs,
                maxOccurs=maxOccurs,
                see_also=see_also(path+element_name, self.lang)
            ).encode('utf8'))


    def output_schema_table(self, element_name, path, element=None, output=False, filename='', title='', minOccurs='', maxOccurs='', ref_element=None):
        if element is None:
            element = self.get_schema_element('element', element_name)
            if element is None:
                return


        extended_types = element.xpath('xsd:complexType/xsd:simpleContent/xsd:extension/@base', namespaces=namespaces)
        rows = [{
            'name': element_name,
            'path': '/'.join(path.split('/')[1:])+element_name,
            'doc': '/'+path+element_name,
            'description': textwrap.dedent(self.schema_documentation(element, ref_element)),
            'type': element.get('type') if element.get('type') and element.get('type').startswith('xsd:') else '',
            'occur': (minOccurs or '') + '..' + ('*' if maxOccurs=='unbounded' else maxOccurs or ''),
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

        for child_name, child_element, child_ref_element, minOccurs, maxOccurs in self.element_loop(element, path):
            rows += self.output_schema_table(child_name, path+element.attrib['name']+'/', child_element, minOccurs=minOccurs, maxOccurs=maxOccurs, ref_element=child_ref_element)

        if output:
            with open(os.path.join('docs', self.lang, filename), 'w') as fp:
                t = self.jinja_env.get_template(self.lang+'/schema_table.rst')
                fp.write(t.render(
                    rows=rows,
                    title=title,
                    root_path='/'.join(path.split('/')[1:]), # Strip e.g. activity-standard/ from the path
                    match_codelist=match_codelist,
                    ruleset_text=ruleset_text,
                    description=self.tree.xpath('xsd:annotation/xsd:documentation[@xml:lang="en"]', namespaces=namespaces)[0].text
                ).encode('utf8'))
        else:
            return rows

    def output_overview_pages(self, standard):
        if self.lang == 'en': # FIXME
            try:
                os.mkdir(os.path.join('docs', self.lang, standard, 'overview'))
            except OSError: pass

            mapping = json.load(open(os.path.join('IATI-Extra-Documentation', self.lang, standard, 'overview-mapping.json')))
            for page, reference_pages in mapping.items():
                self.output_overview_page(standard, page, reference_pages)

    def output_overview_page(self, standard, page, reference_pages):
        if standard == 'activity-standard':
            f = lambda x: x if x.startswith('iati-activities') else 'iati-activities/iati-activity/'+x
        else:
            f = lambda x: x if x.startswith('iati-organisations') else 'iati-organisations/iati-organisation/'+x
        reference_pages = [ (x, '/'+standard+'/'+f(x)) for x in reference_pages ]
        with open(os.path.join('docs', self.lang, standard, 'overview', page+'.rst'), 'w') as fp:
            t = self.jinja_env.get_template(self.lang+'/overview.rst')
            fp.write(t.render(
                extra_docs=get_extra_docs(os.path.join(self.lang, standard, 'overview', page+'.rst')),
                reference_pages=reference_pages
            ).encode('utf8'))



    def element_loop(self, element, path):
        """
        Loop over the children of a given element, and run output_docs on each.

        Returns the names of the child elements.

        """

        a = element.attrib
        type_elements = []
        if 'type' in a:
            complexType = self.get_schema_element('complexType', a['type'])
            if complexType is not None:
                type_elements = ( complexType.findall('xsd:choice/xsd:element', namespaces=namespaces) +
                    complexType.findall('xsd:sequence/xsd:element', namespaces=namespaces) )

        children = ( element.findall('xsd:complexType/xsd:choice/xsd:element', namespaces=namespaces)
            + element.findall('xsd:complexType/xsd:sequence/xsd:element', namespaces=namespaces)
            + element.findall("xsd:complexType/xsd:all/xsd:element", namespaces=namespaces)
            + type_elements)
        child_tuples = []
        for child in children:
            a = child.attrib
            if 'name' in a:
                child_tuples.append((a['name'], child, None, a.get('minOccurs'), a.get('maxOccurs')))
            else:
                child_tuples.append((a['ref'], None, child, a.get('minOccurs'), a.get('maxOccurs')))
        return child_tuples

    def attribute_loop(self, element):
        """
        Returns a list containing a tuple for each attribute the given element
        can have.

        The format of the tuple is (name, type, documentation, is_required)

        """
        #if element.find("xsd:complexType[@mixed='true']", namespaces=namespaces) is not None:
        #    print_column_info('text', indent)

        a = element.attrib
        type_attributes = []
        type_attributeGroups = []
        if 'type' in a:
            complexType = self.get_schema_element('complexType', a['type'])
            if complexType is None:
                print('Notice: No attributes for', a['type'])
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
                referenced_attribute = self.get_schema_element('attribute', attribute.get('ref'))
                if referenced_attribute is not None:
                    attribute = referenced_attribute
                if doc is None:
                    # Only fetch the documentation of the referenced definition
                    # if we don't already have documentation.
                    doc = attribute.find(".//xsd:documentation", namespaces=namespaces)
            out.append((attribute.get('name') or attribute.get('ref'), attribute.get('type'), doc.text if doc is not None else '', attribute.get('use')=='required'))
        return out


def codelists_to_docs(lang):
    dirname = 'IATI-Codelists/out/clv2/json/'+lang
    try:
        os.mkdir('docs/'+lang+'/codelists/')
    except OSError: pass

    for fname in os.listdir(dirname):
        json_file = os.path.join(dirname, fname)
        if not fname.endswith('.json'): continue
        with open(json_file) as fp:
            codelist_json = json.load(fp)

        fname = fname[:-5]
        embedded = os.path.exists(os.path.join('IATI-Codelists','xml',fname+'.xml'))
        if embedded:
            github_url = get_github_url('IATI-Codelists', 'xml/{0}.xml'.format(fname))
        else:
            github_url = get_github_url('IATI-Codelists-NonEmbedded', 'xml/{0}.xml'.format(fname))

        rst_filename = os.path.join(lang, 'codelists', fname+'.rst')
        with open(os.path.join('docs', rst_filename), 'w') as fp:
            jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
            t = jinja_env.get_template(lang+'/codelist.rst')
            fp.write(t.render(
                codelist_json=codelist_json,
                show_category_column=not all(not 'category' in x for x in codelist_json['data']),
                show_url_column=not all(not 'url' in x for x in codelist_json['data']),
                fname=fname,
                len=len,
                github_url=github_url,
                codelist_paths=codelists_paths.get(fname),
                path_to_ref=path_to_ref,
                extra_docs=get_extra_docs(rst_filename),
                dedent=textwrap.dedent,
                embedded=embedded,
                lang=lang).encode('utf-8'))

def extra_extra_docs():
    """
    Copy over files from IATI-Extra-Documentation that haven't been created in
    the docs folder by another function.

    """
    for dirname, dirs, files in os.walk('IATI-Extra-Documentation', followlinks=True):
        if dirname.startswith('.'): continue
        for fname in files:
            if fname.startswith('.'): continue
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
        activities.output_docs('iati-activities', 'activity-standard/')
        activities.output_schema_table('iati-activities', 'activity-standard/', output=True,
            filename='activity-standard/summary-table.rst',
            title='Activity Standard Summary Table')
        activities.output_overview_pages('activity-standard')

        orgs = Schema2Doc('iati-organisations-schema.xsd', lang=language)
        orgs.output_docs('iati-organisations', 'organisation-standard/')
        orgs.output_schema_table('iati-organisations', 'organisation-standard/', output=True,
            filename='organisation-standard/summary-table.rst',
            title='Organisation Standard Summary Table')
        orgs.output_overview_pages('organisation-standard')

        ruleset_page(lang=language)
        codelists_to_docs(lang=language)
    extra_extra_docs()

