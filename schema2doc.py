from __future__ import print_function
import os
import json
import shutil
import textwrap
import jinja2
from lxml import etree as ET
from collections import defaultdict
from iatirulesets.text import rules_text
import re
from utils import get_github_url
from utils import see_also
from utils import standard_ruleset
from utils import codelist_mappings
from utils import codelists_paths
from utils import get_extra_docs
from utils import path_to_ref

# Define the namespaces necessary for opening schema files
namespaces = {
    'xsd': 'http://www.w3.org/2001/XMLSchema'
}

# Define attributes that have documentation that differs to that in the schema
custom_attributes = {
}


def ruleset_text(path):
    """Return a list of text describing the rulesets for a given path (xpath)"""
    out = []
    for xpath, rules in standard_ruleset().items():
        if xpath.startswith('//'):
            try:
                # Use slice 1: to ensure we match /budget/ but not /total-budget/
                reduced_path = path.split(xpath[1:] + '/')[1]
            except IndexError:
                continue
            out += rules_text(rules, reduced_path)
    return out

codelists_paths = codelists_paths()

def match_codelists(path):
    """
    Looks up the codelist that the given path (xpath) should be on.
    Returns a tuble of the codelist name, and a boolean as describing whether any conditions apply.
    If there is no codelist for the given path, the first part of the tuple is None.

    """
    codelist_tuples = []
    for mapping in codelist_mappings():
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
            self.jinja_env (jinja2.environment.Environment): The templates contained within the 'templates' folder.
            self.lang (str): The input language.
        """
        self.tree = ET.parse("./IATI-Schemas/" + schema)
        self.tree2 = ET.parse("./IATI-Schemas/iati-common.xsd")
        self.jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
        self.lang = lang

        self.jinja_env.filters['is_complete_codelist'] = is_complete_codelist

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
            os.makedirs(os.path.join('docs', self.lang, path))
        except OSError:
            pass

        rst_filename = os.path.join(self.lang, path, element_name + '.rst')

        children = self.element_loop(element, path)
        for child_name, child_element, child_ref_element, child_type_element, child_minOccurs, child_maxOccurs in children:
            self.output_docs(child_name, path + element.attrib['name'] + '/', child_element, child_minOccurs, child_maxOccurs, child_ref_element, child_type_element)

        min_occurss = element.xpath('xsd:complexType/xsd:choice/@minOccur', namespaces=namespaces)
        # Note that this min_occurs is different to the python variables
        # minOccurs and maxOccurs, because this is read from a choice element,
        # whereas those are read from the individual element definitions (only
        # possible within a sequence element)
        if min_occurss:
            min_occurs = int(min_occurss[0])
        else:
            min_occurs = 0

        with open('docs/' + rst_filename, 'w') as fp:
            t = self.jinja_env.get_template(self.lang + '/schema_element.rst')
            fp.write(t.render(
                element_name=element_name,
                element_name_underline='=' * len(element_name),
                element=element,
                path='/'.join(path.split('/')[1:]),  # Strip e.g. activity-standard/ from the path
                github_urls=github_urls,
                schema_documentation=textwrap.dedent(self.schema_documentation(element, ref_element, type_element)),
                extended_types=element.xpath('xsd:complexType/xsd:simpleContent/xsd:extension/@base', namespaces=namespaces),
                attributes=self.attribute_loop(element),
                textwrap=textwrap,
                match_codelists=match_codelists,
                path_to_ref=path_to_ref,
                ruleset_text=ruleset_text,
                childnames=[x[0] for x in children],
                extra_docs=get_extra_docs(rst_filename),
                min_occurs=min_occurs,
                minOccurs=minOccurs,
                maxOccurs=maxOccurs,
                see_also=see_also(path + element_name, self.lang)
            ))

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
            with open(os.path.join('docs', self.lang, filename), 'w') as fp:
                t = self.jinja_env.get_template(self.lang + '/schema_table.rst')
                fp.write(t.render(
                    rows=rows,
                    title=title,
                    root_path='/'.join(path.split('/')[1:]),  # Strip e.g. activity-standard/ from the path
                    match_codelists=match_codelists,
                    ruleset_text=ruleset_text,
                    description=self.tree.xpath('xsd:annotation/xsd:documentation[@xml:lang="en"]', namespaces=namespaces)[0].text,
                    extra_docs=get_extra_docs(os.path.join(self.lang, filename))
                ))
        else:
            return rows

    def output_overview_pages(self, standard):
        if self.lang == 'en':  # FIXME
            try:
                os.mkdir(os.path.join('docs', self.lang, standard, 'overview'))
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
        with open(os.path.join('docs', self.lang, standard, 'overview', page + '.rst'), 'w') as fp:
            t = self.jinja_env.get_template(self.lang + '/overview.rst')
            fp.write(t.render(
                extra_docs=get_extra_docs(os.path.join(self.lang, standard, 'overview', page + '.rst')),
                reference_pages=reference_pages
            ))

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
    