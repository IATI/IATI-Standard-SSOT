{{title}}
{{'='*(title|count)}}

.. list-table::
    :header-rows: 1

    * - Section
      - Item
      - Description
      - Type
      - Codelist
      - XML
      - Occur
      - Rules

{% for row in rows %}
    * - {%if row.section%}:doc:`{{row.name}} <{{row.doc}}>`{%endif%}
      - {%if not row.section%}{%if row.name%}:doc:`{{row.name}} <{{row.doc}}>`{%else%}{{row.attribute_name}}{%endif%}{%endif%}
      - {{row.description.replace('\n', '\n        ').strip(' \n')}}
      - {% if row.type %}{{row.type}}{% endif %}
      - {% set codelist = match_codelist(root_path+row.path) %}{% if codelist %}:doc:`/codelists/{{codelist}}`{% endif %}
      - {{row.path.replace('@','\@')}}
      - {{row.occur}}
      - {{'\n        '.join(ruleset_text(row.path))}}
{% endfor %}

::

  {{description.replace('\n','\n  ')}}
