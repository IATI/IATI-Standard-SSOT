from __future__ import print_function
import os
import json
import textwrap
from lxml import etree as ET
from collections import defaultdict
from iatirulesets.text import rules_text


OUTPUT_DIRECTORY = 'outputs/version-2.03'
EXTRA_DOC_PAGES = ['schema.rst', 'activity-standard.rst', 'codelists.rst', 'organisation-standard.rst', 'rulesets.rst', 'standard_ruleset.rst', 'ruleset-development.rst']
languages = ['en', 'fr']

# Define the namespaces necessary for opening schema files
namespaces = {
    'xsd': 'http://www.w3.org/2001/XMLSchema'
}
# Define attributes that have documentation that differs to that in the schema
custom_attributes = {
}


def get_github_url(repo, path=''):
    """Return a link to the Github UI for a given repository and filepath.

    Args:
        repo (str): The repository that contains the file at the input path.
        path (str): The path (within the repository) to the file. There should be no preceeding slash ('/').

    Returns:
        str: Link to the Github UI page.
    """
    github_branches = {
        'IATI-Schemas': 'version-2.03',
        'IATI-Codelists': 'version-2.03',
        'IATI-Rulesets': 'version-2.03',
        'IATI-Extra-Documentation': 'version-2.03',
        'IATI-Codelists-NonEmbedded': 'master',
    }
    return 'https://github.com/IATI/{0}/blob/{1}/{2}'.format(repo, github_branches[repo], path)


def human_list(l):
    """Return a human-friendly version of a list.

    Currently seperates list items with commas, but could be extended to insert 'and'/'or' correctly.

    Args:
        l (list): The list to be made human-friendly.

    Returns:
        str: The human-friendly represention of the list.
    """
    return ', '.join(l)


def lookup_see_also(standard, mapping, path):
    """Return a generator object containing paths relating to the current element as defined by overview-mapping.json.

    Args:
        standard (str): Can be either organisation-standard or activity-standard)
        mapping (list): List for all templates elements within [standard]/overview-mapping.json
        path (str): Last sections of the path passed to see_also, if shorter than 3 sections it will just be the entire path

    Returns:
        generator or str: Yields paths of elements related to the current element
    """
    if path == '':
        return
    for overview, elements in mapping.items():
        if path in elements:
            yield '/' + standard + '/overview/' + overview
    for x in lookup_see_also(standard, mapping, '/'.join(path.split('/')[:-1])):
        yield x


def see_also(path, lang):
    standard = path.split('/')[0]
    if lang == 'en':  # FIXME
        mapping = json.load(open(os.path.join('IATI-Extra-Documentation', lang, standard, 'overview-mapping.json')))  # Loading this file is incredibly inefficient
        # Common 'simple' path e.g. iati-activities or budget/period-start
        # Using this prevents subpages of iati-activity using the activity file overview
        simpler = len(path.split('/')) > 3
        simple_path = '/'.join(path.split('/')[3:]) if simpler else path
        return list(lookup_see_also(standard, mapping, simple_path))


standard_ruleset = json.load(open('./IATI-Rulesets/rulesets/standard.json'))


def ruleset_page(lang):
    ruleset = {xpath: rules_text(rules, '', True) for xpath, rules in standard_ruleset.items()}
    rst_filename = os.path.join(lang, 'rulesets', 'standard-ruleset')

    try:
        os.mkdir(os.path.join(OUTPUT_DIRECTORY, lang, 'rulesets'))
    except OSError:
        pass

    with open(os.path.join(OUTPUT_DIRECTORY, rst_filename + '.json'), 'w') as fp:
        outputdict = {
            'ruleset': ruleset,
            'extra_docs': get_extra_docs(rst_filename + '.rst')
        }
        json.dump(outputdict, fp, indent=2)


def ruleset_text(path):
    """Return a list of text describing the rulesets for a given path (xpath)"""
    out = []
    for xpath, rules in standard_ruleset.items():
        if xpath.startswith('//'):
            try:
                # Use slice 1: to ensure we match /budget/ but not /total-budget/
                reduced_path = path.split(xpath[1:] + '/')[1]
            except IndexError:
                continue
            out += rules_text(rules, reduced_path)
    return out


codelists_paths = defaultdict(list)
# TODO - This function should be moved into the IATI-Codelists submodule
codelist_mappings = ET.parse('./IATI-Codelists/mapping.xml').getroot().findall('mapping')


def match_codelists(path):
    """
    Looks up the codelist that the given path (xpath) should be on.
    Returns a tuble of the codelist name, and a boolean as describing whether any conditions apply.
    If there is no codelist for the given path, the first part of the tuple is None.

    """
    codelist_tuples = []
    for mapping in codelist_mappings:
        if mapping.find('path').text.startswith('//'):
            if path.endswith(mapping.find('path').text.strip('/')):
                codelist = mapping.find('codelist').attrib['ref']
                if path not in codelists_paths[codelist]:
                    codelists_paths[codelist].append(path)
                tup = (codelist, mapping.find('condition') is not None)
                codelist_tuples.append(tup)
            else:
                pass  # FIXME
    return codelist_tuples


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
        'Language',
        'OrganisationIdentifier',
        'OrganisationRegistrationAgency'
    ]
    return codelist_name not in incomplete_codelists


def path_to_ref(path):
    return path.replace('//', '_').replace('@', '.')


def get_extra_docs(rst_filename, source_repository='IATI-Extra-Documentation'):
    rst_root = os.path.splitext(rst_filename)[0]
    extra_docs_file = os.path.join(source_repository, rst_root + '.json')
    if os.path.isfile(extra_docs_file):
        with open(extra_docs_file, "r") as extra_docs_f:
            extra_docs_json = json.loads(extra_docs_f.read())
            return extra_docs_json
    else:
        return list()


class Schema2Doc(object):
    """Class for converting an IATI XML schema to documentation in the reStructuredText format."""
    def __init__(self, schema, lang):
        """
        Args:
            schema (str): The filename of the schema to use, e.g. 'iati-activities-schema.xsd'
            lang (str): A two-letter (ISO 639-1) language code to build the documentation for (e.g. 'en')

        Sets:
            self.tree (lxml.etree._ElementTree): Representing the input schema.
            self.tree2 (lxml.etree._ElementTree): Representing the iati-common.xsd schema.
            self.lang (str): The input language.
        """
        self.tree = ET.parse("./IATI-Schemas/" + schema)
        self.tree2 = ET.parse("./IATI-Schemas/iati-common.xsd")
        self.lang = lang

    def get_schema_element(self, tag_name, name_attribute):
        """Returns the xsd definition for a given element from schemas defined in `self.tree` (or `self.tree2` if nothing found).

        Args:
            tag_name (str): The name of the tag in the schema - will typically be 'element'.
            name_attribute (str): The value of the 'name' attribute in the schema - i.e. the name of the element/type etc. being described, e.g. 'iati-activities'.

        Returns:
            None / lxml.etree._Element: The element tree representng the xsd definition for the given inputs. None if no match found.
        """
        schema_element = self.tree.find("xsd:{0}[@name='{1}']".format(tag_name, name_attribute), namespaces=namespaces)
        if schema_element is None:
            schema_element = self.tree2.find("xsd:{0}[@name='{1}']".format(tag_name, name_attribute), namespaces=namespaces)
        return schema_element

    def schema_documentation(self, element, ref_element, type_element=None):
        """Return a documention string for either a given ref_element (if not None) or an element.

        If the element is a document-link, it will obtain the documentation string from its extension root instead of the extension itself.

        Args:
            element (lxml.etree._Element): An xsd element definition.
            ref_element (lxml.etree._Element): An element that the `element` inherits properties definitions from (using the xsd `ref` inheritance).  If set to None, the documention string for the element is returned.
            type_element (lxml.etree._Element): An element that the `element` inherits properties definitions from (using the xsd `type` inheritance). Defaults to None, implying element properties/definitions are defined within `element` or `ref_element`.

        Returns:
            str: The documentation string, extracted from the input ref_element or element.
        """
        if ref_element is not None:
            xsd_docuementation = ref_element.find(".//xsd:documentation", namespaces=namespaces)
            if xsd_docuementation is not None:
                return xsd_docuementation.text

        xsd_documentation = element.find(".//xsd:documentation", namespaces=namespaces)
        if xsd_documentation is not None:
            return xsd_documentation.text

        if type_element is not None:
            xsd_documentation = type_element.find(".//xsd:documentation", namespaces=namespaces)
            if xsd_documentation is not None:
                return xsd_documentation.text

            extension = type_element.find(".//xsd:extension", namespaces=namespaces)
            if extension is not None:
                base_name = type_element.find(".//xsd:extension", namespaces=namespaces).get("base")
                base_element = self.get_schema_element('complexType', base_name)
                if base_element is not None:
                    return base_element.find(".//xsd:documentation", namespaces=namespaces).text

    def output_docs(self, element_name, path, element=None, minOccurs='', maxOccurs='', ref_element=None, type_element=None):
        """Output documentation for the given element, and it's children.

        If element is not given, we try to find it in the schema using it's
        element_name.

        Args:
            element_name (str):
            path (str): The xpath of the context where this element was found. For the root context (i.e. iati-activities), this is an empty string.
            element (lxml.etree._Element): If element is not given, we try to find it in the schema using it's element_name.
            minOccurs (str): The number of minimum occurances for the given element_name / element.
            maxOccurs (str): The number of minimum occurances for the given element_name / element.
            ref_element (lxml.etree._Element): An element that the `element` inherits properties definitions from (using the xsd `ref` inheritance). Defaults to None, implying element properties are defined within `element` or `type_element`.
            type_element (lxml.etree._Element): An element that the `element` inherits properties definitions from (using the xsd `type` inheritance). Defaults to None, implying element properties are defined within `element` or `ref_element`.
        """
        if element is None:
            element = self.get_schema_element('element', element_name)
            if element is None:
                return

        github_urls = {
            'schema': element.base.replace('./IATI-Schemas/', get_github_url('IATI-Schemas')) + '#L' + str(element.sourceline),
            'extra_documentation': get_github_url('IATI-Extra-Documentation', self.lang + '/' + path + element_name + '.rst')
        }
        try:
            os.makedirs(os.path.join(OUTPUT_DIRECTORY, self.lang, path))
        except OSError:
            pass

        rst_filename = os.path.join(self.lang, path, element_name + '.json')

        children = self.element_loop(element, path)
        for child_name, child_element, child_ref_element, child_type_element, child_minOccurs, child_maxOccurs in children:
            self.output_docs(child_name, path + element.attrib['name'] + '/', child_element, child_minOccurs, child_maxOccurs, child_ref_element, child_type_element)

        attributes = []
        for attribute, attribute_type, text, required in self.attribute_loop(element):
            attrib_path = '/'.join(path.split('/')[1:]) + element_name + '/@' + attribute
            attributes.append({
                'attribute': attribute,
                'attribute_type': attribute_type,
                'text': textwrap.dedent(text).strip().replace('\n', '\n  '),
                'required': required,
                'match_codelists': match_codelists(attrib_path),
                'path': attrib_path,
                'ruleset_text': ruleset_text(attrib_path)
            })

        with open(OUTPUT_DIRECTORY + '/' + rst_filename, 'w') as fp:
            outputdict = {
                'element_name': element_name,
                'element_type': element.get('type'),
                'path': '/'.join(path.split('/')[1:]),  # Strip e.g. activity-standard/ from the path
                'github_urls': github_urls,
                'schema_documentation': self.schema_documentation(element, ref_element, type_element),
                'extended_types': element.xpath('xsd:complexType/xsd:simpleContent/xsd:extension/@base', namespaces=namespaces),
                'ruleset': ruleset_text('/'.join(path.split('/')[1:]) + element_name),
                'attributes': attributes,
                'childnames': [x[0] for x in children],
                'extra_docs': get_extra_docs(rst_filename),
                'minOccurs': minOccurs,
                'maxOccurs': maxOccurs,
            }
            json.dump(outputdict, fp, indent=2)

    def output_schema_table(self, element_name, path, element=None, output=False, filename='', title='', minOccurs='', maxOccurs='', ref_element=None, type_element=None):
        if element is None:
            element = self.get_schema_element('element', element_name)
            if element is None:
                return

        extended_types = element.xpath('xsd:complexType/xsd:simpleContent/xsd:extension/@base', namespaces=namespaces)
        rows = [{
            'name': element_name,
            'path': '/'.join(path.split('/')[1:]) + element_name,
            'doc': '/' + path + element_name,
            'description': textwrap.dedent(self.schema_documentation(element, ref_element, type_element)),
            'type': element.get('type') if element.get('type') and element.get('type').startswith('xsd:') else '',
            'occur': (minOccurs or '') + '..' + ('*' if maxOccurs == 'unbounded' else maxOccurs or ''),
            'section': len(path.split('/')) < 5
        }]

        if element.xpath('xsd:complexType[@mixed="true"] or xsd:complexType/xsd:simpleContent', namespaces=namespaces):
            rows.append({
                'path': '/'.join(path.split('/')[1:]) + element_name + '/text()',
                'description': '',
                'type': 'mixed' if element.xpath('xsd:complexType[@mixed="true"]', namespaces=namespaces) else ','.join([x for x in extended_types if x.startswith('xsd:')]),
            })

        for a_name, a_type, a_description, a_required in self.attribute_loop(element):
            rows.append({
                'attribute_name': a_name,
                'path': '/'.join(path.split('/')[1:]) + element_name + '/@' + a_name,
                'description': textwrap.dedent(a_description),
                'type': a_type,
                'occur': '1..1' if a_required else '0..1'
            })

        for child_name, child_element, child_ref_element, child_type_element, minOccurs, maxOccurs in self.element_loop(element, path):
            rows += self.output_schema_table(child_name, path + element.attrib['name'] + '/', child_element, minOccurs=minOccurs, maxOccurs=maxOccurs, ref_element=child_ref_element, type_element=child_type_element)

        if output:
            for row in rows:
                row['match_codelists'] = match_codelists('/'.join(path.split('/')[1:]) + row['path'])
                row['ruleset_text'] = ruleset_text(row['path'])

            with open(os.path.join(OUTPUT_DIRECTORY, self.lang, filename), 'w') as fp:
                outputdict = {
                    'rows': rows,
                    'title': title,
                    'root_path': '/'.join(path.split('/')[1:]),  # Strip e.g. activity-standard/ from the path
                    'description': self.tree.xpath('xsd:annotation/xsd:documentation[@xml:lang="en"]', namespaces=namespaces)[0].text
                }
                json.dump(outputdict, fp, indent=2)
        else:
            return rows

    def output_overview_pages(self, standard):
        if self.lang == 'en':  # FIXME
            try:
                os.mkdir(os.path.join(OUTPUT_DIRECTORY, self.lang, standard, 'overview'))
            except OSError:
                pass

            mapping = json.load(open(os.path.join('IATI-Extra-Documentation', self.lang, standard, 'overview-mapping.json')))
            for page, reference_pages in mapping.items():
                self.output_overview_page(standard, page, reference_pages)

    def output_overview_page(self, standard, page, reference_pages):
        if standard == 'activity-standard':
            f = lambda x: x if x.startswith('iati-activities') else 'iati-activities/iati-activity/' + x
        else:
            f = lambda x: x if x.startswith('iati-organisations') else 'iati-organisations/iati-organisation/' + x
        reference_pages = [(x, '/' + standard + '/' + f(x)) for x in reference_pages]
        with open(os.path.join(OUTPUT_DIRECTORY, self.lang, standard, 'overview', page + '.json'), 'w') as fp:
            outputdict = {
                'extra_docs': get_extra_docs(os.path.join(self.lang, standard, 'overview', page + '.rst')),
                'reference_pages': reference_pages
            }
            json.dump(outputdict, fp, indent=2)

    def element_loop(self, element, path):
        """Find child elements for a given input element.

        Args:
            element (lxml.etree._Element): The base element to find child elements for.
            path (str): Unused.

        Returns:
            list: A list containing tuples for each child element found. Each tuple takes the form of:
                str: Element name,
                lxml.etree._Element: Represention of the element,
                Unknown: ref element,
                lxml.etree._Element or None: type_element,
                str: minimum number of occurances,
                str: maximum number of occurances (could be a number or 'unbounded')
        """
        a = element.attrib
        type_elements = []
        if 'type' in a:
            complexType = self.get_schema_element('complexType', a['type'])
            if complexType is not None:
                type_elements = (
                    complexType.findall('xsd:choice/xsd:element', namespaces=namespaces) +
                    complexType.findall('xsd:sequence/xsd:element', namespaces=namespaces) +
                    complexType.findall('xsd:complexContent/xsd:extension/xsd:sequence/xsd:element', namespaces=namespaces))

                # If this complexType is an extension of another complexType, find the base element and include any child elements
                try:
                    base_name = complexType.find('xsd:complexContent/xsd:extension', namespaces=namespaces).attrib.get('base')
                    base_type_element = self.get_schema_element('complexType', base_name)
                    type_elements += (
                        base_type_element.findall('xsd:choice/xsd:element', namespaces=namespaces) +
                        base_type_element.findall('xsd:sequence/xsd:element', namespaces=namespaces))
                except AttributeError:
                    pass
                    # This complexType is not extended from a complexType base

        children = (
            element.findall('xsd:complexType/xsd:choice/xsd:element', namespaces=namespaces)
            + element.findall('xsd:complexType/xsd:sequence/xsd:element', namespaces=namespaces)
            + element.findall("xsd:complexType/xsd:all/xsd:element", namespaces=namespaces)
            + type_elements
        )
        child_tuples = []
        for child in children:
            a = child.attrib
            if 'type' in a:
                type_element = self.get_schema_element('complexType', a['type'])
            else:
                type_element = None

            if 'name' in a:
                child_tuples.append((a['name'], child, None, type_element, a.get('minOccurs'), a.get('maxOccurs')))
            else:
                child_tuples.append((a['ref'], None, child, type_element, a.get('minOccurs'), a.get('maxOccurs')))

        return child_tuples

    def attribute_loop(self, element):
        """Returns a list containing a tuple for each attribute that the input element can have.

        Args:
            element (lxml.etree._Element): The base element to find attributes for.

        Returns:
            list: A list containing tuples for each attribute found. Each tuple takes the form of:
                str: The name of the attribute.
                str: The xsd type of the attribute.
                str: The documentation string for the given attribute.
                bool: A boolean value representing if the attribute is required.
        """
        # if element.find("xsd:complexType[@mixed='true']", namespaces=namespaces) is not None:
        # print_column_info('text', indent)

        a = element.attrib
        type_attributes = []
        type_attributeGroups = []
        if 'type' in a:
            complexType = self.get_schema_element('complexType', a['type'])

            # If this complexType is an extension of another complexType, find the base element and use this to find any attributes
            try:
                base_name = complexType.find('.//xsd:complexContent/xsd:extension', namespaces=namespaces).attrib.get('base')
                complexType = self.get_schema_element('complexType', base_name)
            except AttributeError:
                pass
                # This complexType is not extended from a complexType base

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
            occurs = attribute.get('use')
            if 'ref' in attribute.attrib:
                if attribute.get('ref') in custom_attributes:
                    out.append((attribute.get('ref'), '', custom_attributes[attribute.get('ref')], attribute.get('use') == 'required'))
                    continue
                referenced_attribute = self.get_schema_element('attribute', attribute.get('ref'))
                if referenced_attribute is not None:
                    attribute = referenced_attribute
                if doc is None:
                    # Only fetch the documentation of the referenced definition
                    # if we don't already have documentation.
                    doc = attribute.find(".//xsd:documentation", namespaces=namespaces)
                if occurs is None:
                    occurs = attribute.get('use')
            out.append((attribute.get('name') or attribute.get('ref'), attribute.get('type'), doc.text if doc is not None else '', occurs == 'required'))
        return out


def codelists_to_docs(lang):
    dirname = 'IATI-Codelists/out/clv2/json/' + lang
    try:
        os.mkdir(OUTPUT_DIRECTORY + '/' + lang + '/codelists/')
    except OSError:
        pass

    for fname in os.listdir(dirname):
        json_file = os.path.join(dirname, fname)
        if not fname.endswith('.json'):
            continue
        with open(json_file, 'r+') as fp:
            codelist_json = json.load(fp)

        fname = fname[:-5]
        embedded = os.path.exists(os.path.join('IATI-Codelists', 'xml', fname + '.xml'))
        if embedded:
            github_url = get_github_url('IATI-Codelists', 'xml/{0}.xml'.format(fname))
        else:
            github_url = get_github_url('IATI-Codelists-NonEmbedded', 'xml/{0}.xml'.format(fname))

        rst_filename = os.path.join(lang, 'codelists', fname + '.json')

        with open(os.path.join(OUTPUT_DIRECTORY, rst_filename), 'w') as fp:
            outputdict = {
                'codelist_json': codelist_json,
                'show_category_column': not all('category' not in x for x in codelist_json['data']),
                'show_url_column': not all('url' not in x for x in codelist_json['data']),
                'show_withdrawn': any('status' in x and x['status'] != 'active' for x in codelist_json['data']),
                'github_url': github_url,
                'codelist_paths': codelists_paths.get(fname),
                'extra_docs': get_extra_docs(rst_filename),
                'lang': lang
            }
            json.dump(outputdict, fp, indent=2)


def extra_documentation_pages():
    """
    Copy Extra-Documentation and Guidance pages that are used in the Reference section of iatistandard.org.
    """
    for dirname, dirs, files in os.walk('IATI-Extra-Documentation', followlinks=True):
        for fname in files:
            if fname in EXTRA_DOC_PAGES:
                create_documentation_json(dirname, fname, 'IATI-Extra-Documentation', OUTPUT_DIRECTORY)
            elif fname == 'codelist-management.rst':
                create_documentation_json(dirname, fname, 'IATI-Extra-Documentation')
    create_documentation_json('IATI-Guidance/en', 'upgrades.rst')
    for dirname, dirs, files in os.walk('IATI-Guidance/en/upgrades', followlinks=True):
        for fname in files:
            create_documentation_json(dirname, fname)


def create_documentation_json(dirname, fname, flag='IATI-Guidance', out='outputs/'):
    if len(dirname.split(os.path.sep)) == 1:
        directory_name = ''
    else:
        directory_name = os.path.join(*dirname.split(os.path.sep)[1:])
    rst_filename = os.path.join(directory_name, fname)
    json_filename = os.path.join(directory_name, fname[:-3] + 'json')
    if not os.path.exists(os.path.join(OUTPUT_DIRECTORY, json_filename)):
        try:
            os.makedirs(os.path.join(out, directory_name))
        except OSError:
            pass
        if fname.endswith('.rst'):
            with open(os.path.join(out, json_filename), 'w') as fp:
                json.dump({'extra_docs': get_extra_docs(rst_filename, flag)}, fp, indent=2)


# def extra_extra_docs():
#     """
#     Copy over files from IATI-Extra-Documentation that haven't been created in
#     the docs folder by another function.
#
#     """
#     for dirname, dirs, files in os.walk('IATI-Extra-Documentation', followlinks=True):
#         if dirname.startswith('.') or 'overview' in dirname:
#             continue
#         for fname in files:
#             if fname.startswith('.'):
#                 continue
#             if len(dirname.split(os.path.sep)) == 1:
#                 rst_dirname = ''
#             else:
#                 rst_dirname = os.path.join(*dirname.split(os.path.sep)[1:])
#             rst_filename = os.path.join(rst_dirname, fname)
#             if fname.endswith('.rst'):
#                 json_filename = os.path.join(rst_dirname, fname[:-3]+'json')
#             else:
#                 json_filename = os.path.join(rst_dirname, fname)
#             if not os.path.exists(os.path.join(OUTPUT_DIRECTORY, json_filename)):
#                 try:
#                     os.makedirs(os.path.join(OUTPUT_DIRECTORY, rst_dirname))
#                 except OSError:
#                     pass
#                 if fname.endswith('.rst'):
#                     with open(os.path.join(OUTPUT_DIRECTORY, json_filename), 'w') as fp:
#                         json.dump({'extra_docs':get_extra_docs(rst_filename)}, fp, indent=2)
#                 else:
#                     shutil.copy(os.path.join(dirname, fname), os.path.join(OUTPUT_DIRECTORY, json_filename))
#     for dirname, dirs, files in os.walk('IATI-Guidance', followlinks=True):
#         if dirname.startswith('.'):
#             continue
#         for fname in files:
#             if fname.startswith('.'):
#                 continue
#             if len(dirname.split(os.path.sep)) == 1:
#                 rst_dirname = ''
#             else:
#                 rst_dirname = os.path.join(*dirname.split(os.path.sep)[1:])
#             rst_filename = os.path.join(rst_dirname, fname)
#             if fname.endswith('.rst'):
#                 json_filename = os.path.join(rst_dirname, fname[:-3]+'json')
#             else:
#                 json_filename = os.path.join(rst_dirname, fname)
#             if not os.path.exists(os.path.join(OUTPUT_DIRECTORY, json_filename)):
#                 try:
#                     os.makedirs(os.path.join(OUTPUT_DIRECTORY, rst_dirname))
#                 except OSError:
#                     pass
#                 if fname.endswith('.rst'):
#                     with open(os.path.join(OUTPUT_DIRECTORY, json_filename), 'w') as fp:
#                         json.dump({'guidance_page':get_extra_docs(rst_filename, 'IATI-Guidance')}, fp, indent=2)
#                 else:
#                     shutil.copy(os.path.join(dirname, fname), os.path.join(OUTPUT_DIRECTORY, json_filename))


if __name__ == '__main__':
    for language in languages:
        activities = Schema2Doc('iati-activities-schema.xsd', lang=language)
        activities.output_docs('iati-activities', 'activity-standard/')
        activities.output_schema_table(
            'iati-activities', 'activity-standard/', output=True,
            filename='activity-standard/summary-table.json',
            title='Activity Standard Summary Table'
        )
        # activities.output_overview_pages('activity-standard')

        orgs = Schema2Doc('iati-organisations-schema.xsd', lang=language)
        orgs.output_docs('iati-organisations', 'organisation-standard/')
        orgs.output_schema_table(
            'iati-organisations', 'organisation-standard/', output=True,
            filename='organisation-standard/summary-table.json',
            title='Organisation Standard Summary Table'
        )
        # orgs.output_overview_pages('organisation-standard')

        ruleset_page(lang=language)
        codelists_to_docs(lang=language)
    extra_documentation_pages()
