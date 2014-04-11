Ruleset
=======

{% for xpath, rule_texts in ruleset.items() %}

{{xpath}}
{{'='*(xpath|count)}}

{% for rule_text in rule_texts %}
{{rule_text}}

{% endfor %}

{% endfor %}
