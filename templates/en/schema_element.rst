{{element_name}}
{{element_name_underline}}

``{{path}}{{element_name}}``

.. index::
  single: {{element_name}}

DRAFT
-----

From the schema
~~~~~~~~~~~~~~~

{{schema_documentation}}

{{ruleset_text}}

{% for extended_type in extended_types %}{% if extended_type.startswith('xsd:') %}The text in this element should be of type {{extended_type}}.


{% endif %}{% endfor %}{% if element.get('type') and element.get('type').startswith('xsd:') %}The text in this element should be of type {{element.get('type')}}.


{% endif %}{% if attributes %}Attributes
~~~~~~~~~~

{% for attribute, attribute_type, text, required in attributes %}
.. _{{path_to_ref(path+element_name+'/@'+attribute)}}:

@{{attribute}}
  {{ textwrap.dedent(text).strip().replace('\n','\n  ') }}
{% set codelist = match_codelist(path+element_name+'/@'+attribute) %}{% if attribute_type %}  
  This value should be of type {{attribute_type}}.

{% endif %}{% if codelist %}  
  This value should be on the :doc:`{{codelist}} codelist </codelists/{{codelist}}>`.

{% endif %}  
  
{{ ruleset_text_(path+element_name+'/@'+attribute) }}{% endfor %}

{% endif %}{% if childnames %}
Subelements
~~~~~~~~~~~

.. toctree::
   :titlesonly:
   :maxdepth: 1

{% for childname in childnames %}   {{element_name}}/{{childname}}
{%endfor%}
{% endif %}

{{extra_docs}}

Developer tools
~~~~~~~~~~~~~~~

`View this element in the schema source <{{github_url}}>`_
