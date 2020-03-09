import os
import json
import re
import pdb
from docutils import nodes
from docutils.parsers.rst import Parser
from docutils.frontend import OptionParser
from docutils.utils import new_document

languages = ['en', 'fr']
top_levels = ["IATI-Extra-Documentation", "IATI-Guidance"]

ref_dict = dict()
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


def doc_to_ref_mapping(var):
    doc_full_string = var.group(2)
    try:
        doc_text = re.findall(r"^(.*)(?=<)", doc_full_string)[0].strip()
        hyperlink_href = re.findall(r"(?<=<)(.*)(?=>)", doc_full_string)[0]
    except IndexError:
        doc_text = doc_full_string
        hyperlink_href = doc_full_string
    return "`{} <{}>`_".format(doc_text, hyperlink_href)


def doc_to_ref(var):
    doc_full_string = var.group(2)
    link_type = var.group(1)
    try:
        doc_text = re.findall(r"^(.*)(?=<)", doc_full_string)[0].strip()
        hyperlink_href = re.findall(r"(?<=<)(.*)(?=>)", doc_full_string)[0]
        if link_type == ':doc:`':
            hyperlink_href = os.path.join("/iati-standard", hyperlink_href)
        else:
            hyperlink_href = ref_dict[hyperlink_href]
    except IndexError:
        doc_text = doc_full_string
        hyperlink_href = doc_full_string
    return "`{} <{}>`_".format(doc_text, hyperlink_href)


def sphinx_to_docutils(full_text, mapping=False):
    full_text = full_text.replace("`__", "`_")
    full_text = full_text.replace("literalinclude", "include")
    full_text = full_text.replace("toctree", "contents")
    full_text = full_text.replace(":language: xml\n\t", "")
    full_text = full_text.replace(":language: xml\n", "\n")  # needed for organisation-standard/iati-organisations/iati-organisation/document-link/description/narrative
    if not mapping:
        full_text = re.sub(r"(:doc:`)(.*?)(`)", doc_to_ref, full_text)
        full_text = re.sub(r"(:ref:`)(.*?)(`)", doc_to_ref, full_text)
    else:
        full_text = re.sub(r"(:doc:`)(.*?)(`)", doc_to_ref_mapping, full_text)
        full_text = re.sub(r"(:ref:`)(.*?)(`)", doc_to_ref_mapping, full_text)
    return full_text


def recursive_ref_build(node, file_path):
    if node.tagname == "target":
        node_target = node.attributes['ids'][0]
        if 'refuri' in node.attributes.keys():
            node_href = node.attributes['refuri']
        else:
            node_href = node.attributes['names'][0]
        if node_href[0] == "#":
            node_path = file_path + node_target
            ref_dict[node_href[1:]] = node_path
        else:
            node_path = file_path + "#" + node_target
        ref_dict[node_href] = node_path
    for child_node in node.children:
        recursive_ref_build(child_node, file_path)


def recursive_tree_traversal(node):
    if node.tagname == "system_message":
        return None
    if node.tagname == "reference":
        if 'name' in node.attributes.keys():
            node_name = node.attributes['name']
        else:
            node_name = str(node.children[0])
        if 'refuri' in node.attributes.keys():
            node_href = node.attributes['refuri']
        else:
            node_href = node.attributes['refname']
        return {"name": node_name, "href": node_href}
    if node.tagname == "target":
        if 'refuri' in node.attributes.keys():
            node_href = node.attributes['refuri']
        else:
            node_href = ref_dict[node.attributes['names'][0]]
        return {"id": node.attributes['ids'][0], "href": node_href}
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


# Once to map ref_dict
# NOTE: When parsing this, `title` elements will need to create their own invisible targets
for top_level in top_levels:
    for language in languages:
        for dirname, dirs, files in os.walk('{}/{}'.format(top_level, language), followlinks=True):
            dir_split = dirname.split(os.path.sep)
            rst_files = [file for file in files if os.path.splitext(file)[1] == ".rst"]
            for rst_file in rst_files:
                input_path = os.path.sep.join([dirname, rst_file])
                input_base = os.path.sep.join([dirname, os.path.splitext(rst_file)[0]])
                document = new_document(input_path, settings)
                with open(input_path, 'r') as extra_docs_f:
                    extra_docs_text = sphinx_to_docutils(extra_docs_f.read(), mapping=True)
                    parser.parse(extra_docs_text, document)
                    # Remove system messages
                    for node in document.traverse(nodes.system_message):
                        node.parent.remove(node)
                    recursive_ref_build(document, input_base)

# And then again to build json
for top_level in top_levels:
    for language in languages:
        for dirname, dirs, files in os.walk('{}/{}'.format(top_level, language), followlinks=True):
            dir_split = dirname.split(os.path.sep)
            rst_files = [file for file in files if os.path.splitext(file)[1] == ".rst"]
            for rst_file in rst_files:
                input_path = os.path.sep.join([dirname, rst_file])
                input_base = os.path.sep.join([dirname, os.path.splitext(rst_file)[0]])
                document = new_document(input_path, settings)
                with open(input_path, 'r') as extra_docs_f:
                    extra_docs_text = sphinx_to_docutils(extra_docs_f.read())
                    parser.parse(extra_docs_text, document)
                    # Remove system messages
                    for node in document.traverse(nodes.system_message):
                        node.parent.remove(node)
                    json_text = json.dumps(recursive_tree_traversal(document), indent=4)
                    output_path = input_base + ".json"
                    if "problematic" in json_text:
                        pdb.set_trace()
                    with open(output_path, 'w') as output_json:
                        output_json.write(json_text)
