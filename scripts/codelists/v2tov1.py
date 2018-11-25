from __future__ import print_function
from lxml import etree as ET
from lxml.builder import E
from gen import languages
from collections import OrderedDict
import os
import datetime, pytz
import json, csv

language = 'en'

OUTPUTDIR = os.path.join('out','clv1')

try:
    os.makedirs(os.path.join(OUTPUTDIR,'codelist'))
except OSError: pass

def utf8_encode_dict(d):
    def enc(a):
        if a is None: return None
        else: return a.encode('utf8')
    return dict( (enc(k), enc(v)) for k, v in d.items() )

old_codelist_index = E.codelists()
old_codelist_index_json_list = []

for fname in os.listdir(os.path.join('out','clv2','xml')):
    codelist = ET.parse(os.path.join('out','clv2','xml',fname))
    attrib = codelist.getroot().attrib


    count = len(codelist.getroot().find('codelist-items').findall('codelist-item'))
    description = codelist.find('metadata').find('description').text if codelist.find('metadata').find('description') is not None else ''
    if description is None: description = ''
    old_codelist_index.append(
        E.codelist(E.name(attrib['name']),
        E.description(description),
        E.count(unicode(count)))
    )
    old_codelist_index_json_list.append({
        'name': attrib['name'],
        'description': description,
        'count': count
    })


    old_codelist_json = OrderedDict({
            'name':attrib['name'],
            'date-last-modified': datetime.datetime.now(pytz.utc).isoformat(),
            'version':'',
            '{http://www.w3.org/XML/1998/namespace}lang':language,
        })
    old_codelist = E.codelist(**old_codelist_json)
    del(old_codelist_json['{http://www.w3.org/XML/1998/namespace}lang'])
    old_codelist_json['xml:lang'] = language

    old_codelist_json_list = []
    for codelist_item in codelist.getroot().find('codelist-items').findall('codelist-item'):
        code = codelist_item.xpath('code[not(xml:lang) or xml:lang="en"]')[0].text
        try:
            name = codelist_item.xpath('name[not(xml:lang) or xml:lang="en"]')[0].text
        except IndexError:
            name = ''
        old_codelist_item = E(attrib['name'],
            E.code(code),
            E.name(name),
            E.language(language)
            )
        old_codelist_json_item = {
            'code':code,
            'name':name,
            'language':language
        }

        if codelist_item.xpath('description[not(xml:lang) or xml:lang="en"]'):
            description = codelist_item.xpath('description[not(xml:lang) or xml:lang="en"]')[0].text
            if description:
                old_codelist_item.append(E.description(description))
                old_codelist_json_item['description'] = description

        category = codelist_item.find('category')
        if category is not None:
            old_codelist_item.append(E('category', category.text))
            old_codelist_json_item['category'] = category.text

            try:
                category_item = ET.parse(os.path.join('out','clv2','xml',attrib['category-codelist']+'.xml')).xpath('//codelist-item[code="{0}"]'.format(category.text))[0]
                category_name = category_item.xpath('name[not(xml:lang) or xml:lang="en"]')[0].text
            except (IndexError, KeyError):
                category_item = None
                category_name = ''

            old_codelist_item.append(E('category-name', category_name))
            old_codelist_json_item['category-name'] = category_name

            if category_item is not None and category_item.xpath('description[not(xml:lang) or xml:lang="en"]'):
                category_description = category_item.xpath('description[not(xml:lang) or xml:lang="en"]')[0].text
                if category_description:
                    old_codelist_item.append(E('category-description', category_description))
                    old_codelist_json_item['category-description'] = category_description

        old_codelist.append(old_codelist_item)
        old_codelist_json_list.append(old_codelist_json_item)


    with open(os.path.join(OUTPUTDIR,'codelist',attrib['name']+'.csv'), 'w') as fp:
        dictwriter = csv.DictWriter(fp, ['code','name','description','language','category','category-name','category-description'])
        dictwriter.writeheader()
        for line in old_codelist_json_list:
            dictwriter.writerow(utf8_encode_dict(line))

    ET.ElementTree(old_codelist).write(os.path.join(OUTPUTDIR,'codelist',fname), pretty_print=True)
    with open(os.path.join(OUTPUTDIR,'codelist',attrib['name']+'.json'), 'w') as fp:
        old_codelist_json[attrib['name']] = old_codelist_json_list
        json.dump(old_codelist_json, fp)

ET.ElementTree(old_codelist_index).write(os.path.join(OUTPUTDIR, 'codelist.xml'), pretty_print=True)
with open(os.path.join(OUTPUTDIR,'codelist.json'), 'w') as fp:
    json.dump({'codelist':old_codelist_index_json_list}, fp)

