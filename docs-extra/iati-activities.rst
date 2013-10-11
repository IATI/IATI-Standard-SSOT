About the Activity Standard
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The activity standard is the most widely used part of IATI. A reporting organisation will typically produce one IATI activity file per country or geographical region.

The standard supports around forty different fields, referenced by standard code lists, and designed to capture information about many different kinds of aid activities.

Example Usage
~~~~~~~~~~~~~

Example that uses version 1.03, and was generated on 5th September 2013:

.. code-block:: xml

        <iati-activities version="1.03" generated-datetime="2013-09-05T00:00:00">
           ....
        </iati-activities>

With the optional linked-data-default attribute, introduced in decimal
upgrade 1.02

.. code-block:: xml

        <iati-activities version="1.02" generated-datetime="2013-09-05T00:00:00" linked-data-default="">
           ....
        </iati-activities>

Changelog
~~~~~~~~~

1.02
^^^^

Introduced the @linked-data-default attribute on iati-activities element

1.01
^^^^

See previous version on the IATI Standard
`wiki <http://wiki.iatistandard.org/standard/documentation/1.0/iati-activities>`__
and
`website <http://iatistandard.org/101/activities-standard/container-elements/file-header/>`__
