from __future__ import print_function
import os
import json
import shutil
import textwrap
from collections import defaultdict
import jinja2
from lxml import etree as ET
from iatirulesets.text import rules_text
import re
from utils import get_github_url
from utils import see_also
from utils import standard_ruleset
from utils import codelists_paths
from utils import get_extra_docs
from utils import path_to_ref
from schema2doc import Schema2Doc

languages = ['en']

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

def ruleset_page(lang):
    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
    ruleset = {xpath: rules_text(rules, '', True) for xpath, rules in standard_ruleset().items()}
    rst_filename = os.path.join(lang, 'rulesets', 'standard-ruleset.rst')

    try:
        os.mkdir(os.path.join('docs', lang, 'rulesets'))
    except OSError:
        pass

    with open(os.path.join('docs', rst_filename), 'w') as fp:
        t = jinja_env.get_template(lang + '/ruleset.rst')
        fp.write(t.render(
            ruleset=ruleset,
            extra_docs=get_extra_docs(rst_filename)
        ))

codelists_paths = codelists_paths()

def codelists_to_docs(lang):
    dirname = 'IATI-Codelists/out/clv2/json/' + lang
    try:
        os.mkdir('docs/' + lang + '/codelists/')
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

        rst_filename = os.path.join(lang, 'codelists', fname + '.rst')
        with open(os.path.join('docs', rst_filename), 'w') as fp:
            jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
            t = jinja_env.get_template(lang + '/codelist.rst')
            fp.write(t.render(
                codelist_json=codelist_json,
                show_category_column=not all('category' not in x for x in codelist_json['data']),
                show_url_column=not all('url' not in x for x in codelist_json['data']),
                show_withdrawn=any('status' in x and x['status'] != 'active' for x in codelist_json['data']),
                fname=fname,
                len=len,
                github_url=github_url,
                codelist_paths=codelists_paths.get(fname),
                path_to_ref=path_to_ref,
                extra_docs=get_extra_docs(rst_filename),
                dedent=textwrap.dedent,
                lang=lang))


def extra_extra_docs():
    """
    Copy over files from IATI-Extra-Documentation that haven't been created in
    the docs folder by another function.

    """
    for dirname, dirs, files in os.walk('IATI-Extra-Documentation', followlinks=True):
        if dirname.startswith('.'):
            continue
        for fname in files:
            if fname.startswith('.'):
                continue
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
                        fp.write(get_extra_docs(rst_filename))
                else:
                    shutil.copy(os.path.join(dirname, fname), os.path.join('docs', rst_filename))


if __name__ == '__main__':
    for language in languages:
        activities = Schema2Doc('iati-activities-schema.xsd', lang=language)
        activities.output_docs('iati-activities', 'activity-standard/')
        activities.output_schema_table(
            'iati-activities', 'activity-standard/', output=True,
            filename='activity-standard/summary-table.rst',
            title='Activity Standard Summary Table'
        )
        # activities.output_overview_pages('activity-standard')

        orgs = Schema2Doc('iati-organisations-schema.xsd', lang=language)
        orgs.output_docs('iati-organisations', 'organisation-standard/')
        orgs.output_schema_table(
            'iati-organisations', 'organisation-standard/', output=True,
            filename='organisation-standard/summary-table.rst',
            title='Organisation Standard Summary Table'
        )
        # orgs.output_overview_pages('organisation-standard')

        ruleset_page(lang=language)
        codelists_to_docs(lang=language)
    extra_extra_docs()
