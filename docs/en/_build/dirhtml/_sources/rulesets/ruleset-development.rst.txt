Ruleset development
===================

IATI rules and rulesets can be developed and deployed in a number of possible ways.

Different types of rules
------------------------

So far, the Standard Ruleset deploys two types of rules:

* ``Starts with`` - conditions around the formation of the ``iati-identifier``
* ``Date order`` - logics around the ordering of various date elements.

Other rules are also possible /  feasible.

Making new rulesets
-------------------

Individual rules can be used and re-used in various collections of Rulesets. 

The Standard Ruleset could be extended by adding rules particular to a single publisher, to allow them, and others, to check the data they are producing matches a certain criteria.


Limitations of rulesets
-----------------------
Via the IATI Validator, Rulesets do not currently apply to an entire dataset, consisting of several files.  Hence, a ruleset cannot test if an activity identifier has been used once, and only once, by a publisher across their entire dataset.

Rulesets do not allow for checks such as whether or not supplied text contains meaningful information. 

Rulesets do not check codes against codelists.

