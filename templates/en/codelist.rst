{{codelist_json.metadata.name}}
{{'='*len(codelist_json.metadata.name)}}

{% if codelist_json.metadata.description %}
{{dedent(codelist_json.metadata.description)}}
{% endif %}

{% if codelist_json.metadata.url %}
External URL: {{codelist_json.metadata.url}}
{% endif %}

{% if codelist_paths %}
Use this codelist for
---------------------
{% for path in codelist_paths %}
* :ref:`{{path}} <{{path_to_ref(path)}}>`
{% endfor %}
{% endif %}

Download this codelist
----------------------

| CLv1 (Current): `XML <../../_static/codelists/clv1/codelist/{{fname}}.xml>`__ `CSV <../../_static/codelists/clv1/codelist/{{fname}}.csv>`__ `JSON <../../_static/codelists/clv1/codelist/{{fname}}.json>`__
| CLv2 (New): `XML <../../_static/codelists/clv2/xml/{{fname}}.xml>`__ `CSV <../../_static/codelists/clv2/csv/{{lang}}/{{fname}}.csv>`__ `JSON <../../_static/codelists/clv2/json/{{lang}}/{{fname}}.json>`__

`GitHub Source (New XML) <{{github_url}}>`__

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
