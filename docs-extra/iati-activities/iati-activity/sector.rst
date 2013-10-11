

Example Usage
~~~~~~~~~~~~~

A code for the sector can be declared:

.. code-block:: xml

    <sector code="13040"/>

Additionally, a text description for the code can be provided:

.. code-block:: xml

    <sector code="13040">STD control including HIV/AIDS</sector>

The vocabulary attribute can be used to declare which code reference
list is in use. If this is omitted, then IATI assumes the DAC
vocabulary.

.. code-block:: xml

    <sector vocabulary="WB" code="BC">Central government administration</sector>

If the specific vocabulary in use is not on the vocabulary codelist,
then the value of RO (Reporting Organisation) can be used:

.. code-block:: xml

    <sector vocabulary="RO">Education</sector>

When multiple sectors are in use in the same activity, then the
percentage attribute should be used - the total of all percentages
within the same activity should total 100.

.. code-block:: xml

    <sector code="13040" percentage="60">STD control including HIV/AIDS</sector>
    <sector code="12220" percentage="40">Basic health care</sector>

Should a description be used that is different to the default language
set for the activity, then this should be declared as follows:

.. code-block:: xml

    <sector code="13040" xml:lang="en">STD control including HIV/AIDS</sector>

Changelog
~~~~~~~~~

1.03
^^^^

Where used, the @percentage attribute is now designated as a decimal
value and no longer as a positive Integer
