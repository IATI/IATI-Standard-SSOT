import json
import os
from collections import defaultdict
from lxml import etree as ET

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

def see_also(path, lang):
    return list()

def standard_ruleset():
    return json.load(open('./IATI-Rulesets/rulesets/standard.json'))

def codelists_paths():
    return defaultdict(list)

# TODO - This function should be moved into the IATI-Codelists submodule

def codelist_mappings():
    return ET.parse('./IATI-Codelists/mapping.xml').getroot().findall('mapping')

def get_extra_docs(rst_filename):
    extra_docs_file = os.path.join('IATI-Extra-Documentation', rst_filename)
    if os.path.isfile(extra_docs_file):
        with open(extra_docs_file) as fp:
            return fp.read()
    else:
        return ''

def path_to_ref(path):
    return path.replace('//', '_').replace('@', '.')
