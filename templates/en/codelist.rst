{{fname}}
{{underline}}

{% if codelist_json.metadata.description %}
{{codelist_json.metadata.description}}
{% endif %}

{% if codelist_paths %}
Attributes
----------
{% for path in codelist_paths %}
* :ref:`{{path}} <{{path_to_ref(path)}}>`
{% endfor %}
{% endif %}

Download this codelist
----------------------

Old format:
`XML <../../_static/codelists/v1/codelist/{{fname}}.xml>`__
`CSV <../../_static/codelists/v1/codelist/{{fname}}.csv>`__
`JSON <../../_static/codelists/v1/codelist/{{fname}}.json>`__

New format: 
`XML <../../_static/codelists/xml/{{fname}}.xml>`__
`CSV <../../_static/codelists/csv/{{lang}}/{{fname}}.csv>`__
`JSON <../../_static/codelists/json/{{lang}}/{{fname}}.json>`__

`Github Source <{{github_url}}>`__

Codes
-----

.. _{{codelist_json.metadata.name}}:
.. list-table::


   * - Code
     - Name
     - Description
     - Category

   {% for codelist_item in codelist_json.data %}

   * - {{codelist_item.code}}
     - {{codelist_item.name}}
     - {{codelist_item.description}}
     - {% if codelist_item.category %}:ref:`{{codelist_item.category}} <{{codelist_json.metadata['category-codelist']}}>`{% endif %}

   {% endfor %}

{{extra_docs}}
