.. list-table::
{% for row in rows %}
    * - :doc:`{{row.name}} <{{row.doc}}>`
      - {{row.description.replace('\n', '\n        ').strip(' \n')}}
      - {{row.type}}
      - {{row.path}}
{% endfor %}
