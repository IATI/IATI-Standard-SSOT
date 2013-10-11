

Example Usage
~~~~~~~~~~~~~

.. code-block:: xml

    <policy-marker vocabulary="DAC" code="04" significance="2"/>

A code for the policy marker can be declared:

.. code-block:: xml

    <policy-marker vocabulary="DAC" code="04"/>

Additionally, a text description for this code can be provided:

.. code-block:: xml

    <policy-marker vocabulary="DAC" code="04">Trade Development</policy-marker>

The significance can declare a score indicating if the activity
addresses the policy/theme as a principal or significant objective or
not at all.

.. code-block:: xml

    <policy-marker vocabulary="DAC" code="04" significance="2">Trade Development</policy-marker>

The vocabulary attribute can be used to declare which code reference
list is in use. If this is If omitted, then IATI assumes the DAC
vocabulary. If the specific vocabulary in use is not on the vocabulary
codelist, then the value of RO (Reporting Organisation) can be used.

.. code-block:: xml

    <policy-marker vocabulary="DAC" code="04">Trade Development</policy-marker>

Should a description be used that is different to the default language
set for the activity, then this should be declared as follows:

.. code-block:: xml

    <policy-marker vocabulary="DAC" code="04" xml:lang="fr">Developpement du commerce</policy-marker>
