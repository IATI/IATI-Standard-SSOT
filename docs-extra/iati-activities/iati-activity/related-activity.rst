

Example Usage
~~~~~~~~~~~~~

The reference and type of relation can be cited in this element:

.. code-block:: xml

       <related-activity type="1" ref="GB-1-105838"/>

Additionally, a text title of the specific related activity can be
provided:

.. code-block:: xml

        <related-activity type="1" ref="GB-1-105838">Trade Sector Programme</related-activity>

Where this text is in a language that differs from the default set in
<iati-activity>, then this should be declared accordingly:

.. code-block:: xml

        <related-activity type="1" ref="GB-1-105838" xml:lang="fr">Programme du secteur commercial</related-activity>
