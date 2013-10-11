

Example Usage
~~~~~~~~~~~~~

The location element is used a contain various other elements

.. code-block:: xml

        <location>
           ....
        </location>

If more than one location is reported, percentage of activity commitment
allocated to this location (if available).

.. code-block:: xml

        <location percentage="85>
           ....
        </location>
        <location percentage="15>
           ....
        </location>

Example from UNOPS:

.. code-block:: xml

    <location>
          <name>Herat</name>
          <coordinates latitude="34.341944400000003000" longitude="62.203055599999971000" precision="2" />
          <location-type code="PPL" />
          <administrative country="AF">Afghanistan, Herat, Injil</administrative>
        </location>

Changelog
~~~~~~~~~

1.03
^^^^

Where used, the @percentage attribute is now designated as a decimal
value and no longer as a positive Integer
