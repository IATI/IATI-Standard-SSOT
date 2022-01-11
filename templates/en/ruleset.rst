{{extra_docs}}

{% for xpath, rule_texts in ruleset.items() %}

{{xpath}}
{{'-'*(xpath|count)}}

{% for rule_text in rule_texts %}
* `{{ rule_text[0] }} <{{ rule_text[2] }}>`_: {{ rule_text[1] }}
{% endfor %}

{% endfor %}
