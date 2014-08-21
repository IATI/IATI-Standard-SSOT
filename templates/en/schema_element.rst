{{element_name}}
{{element_name_underline}}

``{{path}}{{element_name}}``

``{{dashboard_url}}``

This is the reference page for the XML element ``{{element_name}}``. {% if see_also %}See also the relevant overview page{% if see_also|count > 1%}s{%endif%}: {% for page in see_also %}:doc:`{{page}}`{% if not loop.last %}, {% endif %} {% endfor %}{% endif %}

.. index::
  single: {{element_name}}

Definition
~~~~~~~~~~

{{schema_documentation}}

{% for extended_type in extended_types %}
{% if extended_type.startswith('xsd:') %}The text in this element should be of type {{extended_type}}.{% endif %}
{% endfor %}

{% if element.get('type') and element.get('type').startswith('xsd:') %}The text in this element should be of type {{element.get('type')}}.
{% endif %}

{% set rtext = ruleset_text(path+element_name) %}
{% if rtext %}
Rules
~~~~~

{{'\n\n'.join(rtext)}}

{%endif%}

{% if attributes %}
Attributes
~~~~~~~~~~

{% for attribute, attribute_type, text, required in attributes %}
.. _{{path_to_ref(path+element_name+'/@'+attribute)}}:

@{{attribute}}
  {{ textwrap.dedent(text).strip().replace('\n','\n  ') }}
{% set codelist_tuple = match_codelist(path+element_name+'/@'+attribute) %}{% if attribute_type %}  
  This value should be of type {{attribute_type}}.

{% endif %}{% if codelist_tuple[0] %}  
  This value should be on the :doc:`{{codelist_tuple[0]}} codelist </codelists/{{codelist_tuple[0]}}>`{% if codelist_tuple[1] %}, if the relevant vocabulary is used{% endif %}.

{% endif %}  
  
  {{ '\n\n  '.join(ruleset_text(path+element_name+'/@'+attribute)) }}{% endfor %}

{% endif %}

Example Usage
~~~~~~~~~~~~~

Example usage and changelog are hidden becuase they have not yet been updated for 2.01.

Developer tools
~~~~~~~~~~~~~~~

Find the source of this documentation on github:

* `Schema <{{github_urls.schema}}>`_
* `Extra Documentation <{{github_urls.extra_documentation}}>`_

{% if childnames %}
Subelements
~~~~~~~~~~~

.. toctree::
   :titlesonly:
   :maxdepth: 1

{% for childname in childnames %}   {{element_name}}/{{childname}}
{%endfor%}
{% endif %}
