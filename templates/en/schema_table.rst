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
      - {% set codelist_tuples = match_codelists(root_path+row.path) %}{% for codelist_tuple in codelist_tuples %}{%if codelist_tuple[1]%}({%endif%}:doc:`/codelists/{{codelist_tuple[0]}}`{%if codelist_tuple[1]%}){%endif%}{% endfor %}
      - {{row.path.replace('@','\@')}}
      - {{row.occur}}
      - {% set rtexts = ruleset_text(row.path) %}{% for rtext in rtexts %}`{{ rtext[0] }} <{{ rtext[2] }}>`_: {{ rtext[1] }}{{ ' |br| \n        ' }}{% endfor %}
{% endfor %}

::

  {{description.replace('\n','\n  ')}}

{{extra_docs}}

.. |br| raw:: html

  <br/>