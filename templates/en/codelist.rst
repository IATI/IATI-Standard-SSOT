{{codelist_json.metadata.name}}
{{'='*len(codelist_json.metadata.name)}}

{% if codelist_json.metadata.description %}
{{dedent(codelist_json.metadata.description)}}
{% endif %}

{% if codelist_json.metadata.url %}
External URL: {{codelist_json.metadata.url}}
{% endif %}

{% if codelist_json.metadata.category=="Core" %}
This is a :ref:`Core codelist <core_codelist>`.
{% else %}
This is a :ref:`{{codelist_json.metadata.category}} codelist <non_core_codelist>`.
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

.. list-table::
   :header-rows: 1

   * - :ref:`CLv1 <codelist_api_1.04>`:
     - :ref:`CLv2 <codelist_api_1.04>`:
     - :ref:`CLv3 <codelist_api_1.04>`:
     - :ref:`CLv3 (french) <codelist_api_1.04>`:

   * - `CSV <../downloads/clv1/codelist/{{fname}}.csv>`__
     - `CSV <../downloads/clv2/csv/{{lang}}/{{fname}}.csv>`__
     - `CSV <../downloads/clv3/csv/{{lang}}/{{fname}}.csv>`__
     - `CSV <../downloads/clv3/csv/fr/{{fname}}.csv>`__

   * - `JSON <../downloads/clv1/codelist/{{fname}}.json>`__
     - `JSON <../downloads/clv2/json/{{lang}}/{{fname}}.json>`__
     - `JSON <../downloads/clv3/json/{{lang}}/{{fname}}.json>`__
     - `JSON <../downloads/clv3/json/fr/{{fname}}.json>`__

   * - `XML <../downloads/clv1/codelist/{{fname}}.xml>`__
     - `XML <../downloads/clv2/xml/{{fname}}.xml>`__
     - `XML <../downloads/clv3/xml/{{fname}}.xml>`__
     - `XML <../downloads/clv3/xml/{{fname}}.xml>`__

`GitHub Source <{{github_url}}>`__

{% if show_withdrawn and embedded==False %}

This codelist has some withdrawn elements, for details on these check the `Non-Core Codelist changelog record <http://iatistandard.org/upgrades/noncore-codelist-changelog>`__
{% endif %}

The codelists were translated in French in April 2018 with the support of the Government of Canada. Please note that if any codelists have been added since then, they will not be currently available in French.

Codes
-----

.. _{{fname}}:
.. list-table::
   :header-rows: 1


   * - Code
     - Name
     - Description{% if show_category_column %}
     - Category{% endif %}{% if show_url_column %}
     - URL{% endif %}{% if fname == 'OrganisationRegistrationAgency' %}
     - Public Database?{% endif %}

   {% for codelist_item in codelist_json.data %}
       {% if codelist_item.status == 'withdrawn' %} 
       .. rst-class:: withdrawn
   * - {{codelist_item.code + " (withdrawn)"}}
       {% else %}
   * - {{codelist_item.code}}   
       {% endif %}
     - {{codelist_item.name}}
     - {% if codelist_item.description %}{{codelist_item.description}}{% endif %}{% if show_category_column %}
     - {% if codelist_item.category %}{% if codelist_json.attributes['category-codelist'] %}:ref:`{{codelist_item.category}} <{{codelist_json.attributes['category-codelist']}}>`{%else%}{{codelist_item.category}}{%endif%}{% endif %}{% endif %}{% if show_url_column %}
     - {% if codelist_item.url %}{{codelist_item.url}}{% endif %}{% if fname == 'OrganisationRegistrationAgency' %}
     - {{codelist_item['public-database']}}{% endif %}{% endif %}
   {% endfor %}

{{extra_docs}}
