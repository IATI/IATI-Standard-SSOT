

Example Usage
~~~~~~~~~~~~~

This example declares that the activity has a default language of
English (en) and a default currency of US dollars. It was last updated
on the 31st March 2012, and has a hierarchy value of 1.

.. code-block:: xml

     <iati-activity xml:lang="en" default-currency="USD" last-updated-datetime="2012-03-31T01:01:01" hierarchy="1">
           ....
     </iati-activity>

Additionally, a IATI version number can be declared. NB: This would
already be within the <iati-activities> element, but could differ.

.. code-block:: xml

     <iati-activity xml:lang="en" default-currency="USD" last-updated-datetime="2012-03-31T01:01:01" hierarchy="1" version="1.01">
           ....
     </iati-activity>

Finally, this example, includes the linked-data-uri attribute,
introduced in the decimal upgrade 1.02

.. code-block:: xml

     <iati-activity xml:lang="en" default-currency="USD" last-updated-datetime="2012-03-31T01:01:01" hierarchy="1" version="1.01" linked-data-uri="">
           ....
     </iati-activity>

Changelog
~~~~~~~~~

1.02
^^^^

Introduced the @linked-data-uri attribute on iati-activity element

1.01
^^^^

See previous version on the IATI Standard
`wiki <http://wiki.iatistandard.org/standard/documentation/1.0/iati-activity>`__
and
`website <http://iatistandard.org/101/activities-standard/container-elements/record-header/>`__
