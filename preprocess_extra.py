import os
import json
import re
import pdb
from docutils import nodes
from docutils.parsers.rst import Parser
from docutils.frontend import OptionParser
from docutils.utils import new_document


def doc_to_ref(var):
    doc_full_string = var.group(2)
    try:
        doc_text = re.findall(r"^(.*)(?=<)", doc_full_string)[0].strip()
        hyperlink_href = "/iati-standard/" + re.findall(r"(?<=<)(.*)(?=>)", doc_full_string)[0]
    except IndexError:
        doc_text = doc_full_string
        hyperlink_href = doc_full_string
    return "`{} <{}>`_".format(doc_text, hyperlink_href)


def sphinx_to_docutils(full_text):
    full_text = full_text.replace("`__", "`_")
    full_text = full_text.replace("literalinclude", "include")
    full_text = full_text.replace("toctree", "contents")
    full_text = full_text.replace(":language: xml\n\t", "")
    full_text = full_text.replace(":language: xml\n", "\n")  # needed for organisation-standard/iati-organisations/iati-organisation/document-link/description/narrative
    full_text = re.sub(r"(:doc:`)(.*?)(`)", doc_to_ref, full_text)
    return full_text


def recursive_tree_traversal(node):
    if node.tagname == "reference":
        try:
            return {"name": node.attributes['name'], "href": node.attributes['refuri']}
        except KeyError:
            child_name = str(node.children[0])
            return {"name": child_name, "href": node.attributes['refuri']}
    if node.tagname == "target":
        return {"id": node.attributes['ids'][0], "href": node.attributes['refuri']}
    if node.tagname == "#text":
        return str(node)
    children = node.children
    if len(children) == 1 and children[0].tagname == "#text":
        return str(children[0])
    child_list = list()
    for child in children:
        child_dictionary = dict()
        child_dictionary[child.tagname] = recursive_tree_traversal(child)
        child_list.append(child_dictionary)
    return child_list


languages = ['en', 'fr']
parser = Parser()
settings = OptionParser().get_default_values()
settings.tab_width = 8
settings.pep_references = False
settings.rfc_references = False
settings.file_insertion_enabled = True
settings.syntax_highlight = False
settings.raw_enabled = True
settings.halt_level = 5
settings.report_level = 5
settings.character_level_inline_markup = False


for language in languages:
    for dirname, dirs, files in os.walk('IATI-Extra-Documentation/{}'.format(language), followlinks=True):
        dir_split = dirname.split(os.path.sep)
        rst_files = [file for file in files if os.path.splitext(file)[1] == ".rst"]
        for rst_file in rst_files:
            input_path = os.path.sep.join([dirname, rst_file])
            document = new_document(input_path, settings)
            with open(input_path, 'r') as extra_docs_f:
                extra_docs_text = sphinx_to_docutils(extra_docs_f.read())
                parser.parse(extra_docs_text, document)
                # Remove system messages
                for node in document.traverse(nodes.system_message):
                    node.parent.remove(node)
                json_text = json.dumps(recursive_tree_traversal(document), indent=4)
                output_path = os.path.sep.join([dirname, os.path.splitext(rst_file)[0] + ".json"])
                if "problematic" in json_text:
                    pdb.set_trace()
                with open(output_path, 'w') as output_json:
                    output_json.write(json_text)
