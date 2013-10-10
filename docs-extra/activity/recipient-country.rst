
Page for revison 1.02. See this page for: `revison
1.02 </standard/documentation/1.02/recipient-country>`__, `revison
1.01 </standard/documentation/1.0/recipient-country>`__

Example Usage
~~~~~~~~~~~~~

Recipient country can be declared just through the relevant code:

.. code-block:: xml

    <recipient-country code="CG"/>

Additionally, the name of the country can also be declared.

.. code-block:: xml

    <recipient-country code="CG">Democratic Republic of Congo</recipient-country>

Where the name of the country is declared in a language other than the
default, it is good practice to cite this:

.. code-block:: xml

     <recipient-country code="CG" xml:lang="fr">Republique Democratique du Congo</recipient-country>

When multiple countries are declared, then the percentages should equal
100% for that activity

.. code-block:: xml

    <recipient-country code="CG" percentage="60"/>
    <recipient-country code="AO" percentage="40"/>

Changelog
~~~~~~~~~

1.03
^^^^

Where used, the @percentage attribute is now designated as a decimal
value and no longer as a positive Integer
