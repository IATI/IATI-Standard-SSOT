

Example Usage
~~~~~~~~~~~~~

This example from Cafod declares two participating organisations in the
activity. Caford as the Funding organisation, with a reference to the
Charity Commission. The Implementing organisation is not referenced:

.. code-block:: xml

    <participating-org role="Funding" ref="GB-CHC-285776">CAFOD</participating-org>
    <participating-org role="Implementing">Caritas Africa</participating-org>

This example from DfID declares three participating organisations, all
with a different role. The type of organisation (10 = Government) is
also declared for two.

.. code-block:: xml

    <participating-org ref="GB" type="10" role="Funding">UNITED KINGDOM</participating-org>
    <participating-org ref="GB-1" type="10" role="Extending">Department for International Development</participating-org>
    <participating-org ref="22000" role="Implementing">Donor country-based NGO</participating-org>
