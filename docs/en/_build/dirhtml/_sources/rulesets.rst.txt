Rulesets
========
The **IATI rulesets** provide additional instructions for IATI publishers.

Data published to meet the IATI Standard is created as XML. IATI maintain a number of :doc:`XML schema </schema>` that describe the structure of an IATI XML document.  However, the design of IATI means that these XML schema cannot enforce all of the rules inherent in the IATI Standard on their own.

For example, the schema, as it stands, cannot check to see if an activity has a start date that occurs before its end date.

The IATI Standard has many rules such as the above, that machines are able to test for, given the correct instructions.

IATI has created 'Rulesets' as a way of agreeing what those instructions should be, and grouping them into meaningful collections.

Rulesets are constructed as follows:

* Individual *rules* detail any constraint or condition.
* Collectively, these rules then make up a *ruleset*.

This section details the current Standard Ruleset, and provides information around how to utilise and develop rules.

More info
---------

.. toctree::
   :glob:
   :titlesonly:

   rulesets/standard-ruleset
   rulesets/ruleset-spec
   rulesets/ruleset-development

.. meta::
  :order: 3
