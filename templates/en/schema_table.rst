{{title}}
{{'='*(title|count)}}

.. list-table::

    * - Section
      - Item
      - Description
      - Type
      - XML
      - Occur

{% for row in rows %}
    * - {%if row.section%}:doc:`{{row.name}} <{{row.doc}}>`{%endif%}
      - {%if not row.section%}{%if row.name%}:doc:`{{row.name}} <{{row.doc}}>`{%else%}{{row.attribute_name}}{%endif%}{%endif%}
      - {{row.description.replace('\n', '\n        ').strip(' \n')}}
      - {{row.type}}
      - ``{{row.path}}``
      - {{row.occur}}
{% endfor %}
