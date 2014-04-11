{{codelist_json.metadata.name}}
{{'='*len(codelist_json.metadata.name)}}

{% if codelist_json.metadata.description %}
{{dedent(codelist_json.metadata.description)}}
{% endif %}

{% if codelist_json.metadata.url %}
External URL: {{codelist_json.metadata.url}}
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

.. _{{fname}}:
.. list-table::
   :header-rows: 1


   * - Code
     - Name
     - Description
     - Category
     - URL
{% if fname == 'OrganisationRegistrationAgency' %}     - Public Database?{% endif %}

   {% for codelist_item in codelist_json.data %}

   * - {{codelist_item.code}}
     - {{codelist_item.name}}
     - {% if codelist_item.description %}{{codelist_item.description}}{% endif %}
     - {% if codelist_item.category %}:ref:`{{codelist_item.category}} <{{codelist_json.attributes['category-codelist']}}>`{% endif %}
     - {% if codelist_item.url %}{{codelist_item.url}}{% endif %}
{% if fname == 'OrganisationRegistrationAgency' %}     - {{codelist_item['public-database']}}{% endif %}

   {% endfor %}

{{extra_docs}}
