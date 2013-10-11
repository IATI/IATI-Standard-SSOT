

Example Usage
~~~~~~~~~~~~~

Recipient region can be declared just through the relevant code:

.. code-block:: xml

    <recipient-region code="289"/>

Additionally, the name of the region can also be declared.

.. code-block:: xml

    <recipient-region code="289">South of Sahara, regional<recipient-region>

Where the name of the region is declared in a language other than the
default, it is good practice to cite this:

.. code-block:: xml

    <recipient-region code="289" xml:lang="es">Africa subsahariana</recipient-region>

When multiple regions are declared, then the percentages should equal
100% for that activity

.. code-block:: xml

    <recipient-region percentage="60" code="289">South of Sahara, regional</recipient-region>
    <recipient-region percentage="40" code="189">North of Sahara, regional</recipient-region>

Changelog
~~~~~~~~~

1.03
^^^^

Where used, the @percentage attribute is now designated as a decimal
value and no longer as a positive Integer
