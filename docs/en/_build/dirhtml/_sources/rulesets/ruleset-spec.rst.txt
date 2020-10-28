
IATI Ruleset Spec
=================

An IATI Ruleset is a JSON document. The structure is described below.

A `JSON schema <https://github.com/IATI/IATI-Rulesets/blob/version-2.01/schema.json>`_ is availible to test that the structure of a Ruleset is correct.

Each JSON document has the form.::

    {
        "CONTEXT": {
            "RULE_NAME": {
                "cases": CASE_DICT_ARRAY
            }
        }

    }

Where ``CONTEXT`` is an xpath expression. This will be used to select the XML elements that the contained rules will be tested against.
``RULE_NAME`` is one of rule names listed below
``CASE_DICT`` is a dictionary where the contents depend on ``RULE_NAME``
``CASE_DICT_ARRAY`` is an array of case dictionaries. The contents of each dictionary depend on the ``RULE_NAME``

The possible keys in a case dictionary are:

``condition``
    An xpath string. If this evaluates to True, the rule will be ignored.
``eval``
    An xpath string. Can evaluate to True or False.
``paths``
    An array of xpath strings. These are evaluated to give a list of elements that the named rule then operates upon.
``less``
    A string containing the xpath of the smaller value (or older value when working with dates).
``more``
    A string containing the xpath of the larger value (or more recent value when working with dates).
``regex``
    A string containing a perl style regular expression.
``sum``
    A number.
``excluded``
    An array of xpath strings. Evaluate which elements should not coexist with other elements.
``date``
    A string containing the xpath to a date.
``start``
    A string containing the xpath to a start date.
``end``
    A string containing the xpath to an end date.
``one``
    A string containing the xpath of something that must exist or ``all`` must be followed.
``all``
    A string containing the condition that must be met for all elements if ``one`` is not met.
``foreach``
    An array of xpath strings. Containing a set of xpaths to be evaluated under a different rule.
``do``
    An array of rules. To evaluate with ``foreach``.
``subs``
    An array of xpath strings. These are to be evaluated with the rules in ``do``.

Rule Names
----------


**Rule names are listed in bold**
    Keys: The keys for each rule are then listed.

    Followed by a brief description of the rule's function.


**no_more_than_one**
    Keys: ``condition``, ``paths``

    There must be no more than one element described by the given paths.

**atleast_one**
    Keys: ``condition``, ``paths``

    There must be at least one element described by the given paths.

**only_one_of**
    Keys: ``excluded``, ``paths``

    If there's a match of the elements in ``excluded``, there must not be any matches in ``paths``, if there are no matches in ``excluded``, there must be exactly one element from ``paths``.

**one_or_all**
    Keys: ``one``, ``all``

    ``one`` must exist otherwise ``all`` other attributes or elements must exist.

**dependent**
    Keys: ``condition``, ``paths``

    If one of the provided paths exists, they must all exist.

**sum**
    Keys: ``condition``, ``paths``, ``sum``

    The numerical sum of the values of elements matched by ``paths`` must match the value for the ``sum`` key

**date_order**
    Keys: ``condition``, ``less``, ``more``

    The date matched by ``less`` must not be after the date matched by ``more``. If either of these dates is not found, the rule is ignored.

**date_now**
    Keys: ``date``

    The ``date`` must not be after the current date.

**time_limit**
    Keys: ``start``, ``end``

    The difference between the ``start`` date and the ``end`` date must not be greater than a year.

**between_dates**
    Keys: ``date``, ``start``, ``end``

    The ``date`` must be between the ``start`` and ``end`` dates.

**regex_matches**
    Keys: ``condition``, ``paths``, ``regex``

    The provided ``regex`` must match the text of all elements matched by ``paths``

**regex_no_matches**
    Keys: ``condition``, ``paths``, ``regex``

    The provided ``regex`` must match the text of none of the elements matched by ``paths``

**startswith**
    Keys: ``condition``, ``paths``, ``start``

    The text of each element matched by ``paths`` must start with the text of the element matched by ``start``

**unique**
    Keys: ``condition``, ``paths``

    The text of each of the elements described by ``paths`` must be unique

**evaluates_to_true**
    Keys: ``cases``, ``eval``

    Each expression defined in ``eval`` must resolve to true

**if_then**
    Keys: ``condition``, ``cases``, ``if``, ``then``

    If the condition evaluated in ``if`` is true, then ``then`` must resolve to true as well

**loop**
    Keys: ``foreach``, ``do``, ``cases``, ``subs``

    All elements in ``foreach`` are evaluated under the rules inside ``do``

**strict_sum**
    Keys: ``paths``, ``sum``

    The decimal sum of the values of elements matched by ``paths`` must match the value for the ``sum`` key
