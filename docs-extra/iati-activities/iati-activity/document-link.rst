

Example Usage
~~~~~~~~~~~~~

A web address where the document can be downloaded can be declared
through the url attribute:

.. code-block:: xml

        <document-link url="http://www.aidtransparency.net/wp-content/uploads/2009/06/Summary-IATI-Standard-Version-1-Final.doc">

Additionally, the Internet Media Type (“MIME type”) of the document
linked to, as defined and maintained by the Internet Assigned Numbers
Authority can be declared via the format attribute:

.. code-block:: xml

        <document-link format="application/msword" url="http://www.aidtransparency.net/wp-content/uploads/2009/06/Summary-IATI-Standard-Version-1-Final.doc">

Changelog
~~~~~~~~~

1.02
^^^^

Removed language attribute from, and introduced an new language child
element to, the document-link element.

1.01
^^^^

See previous version on the IATI Standard
`wiki <http://wiki.iatistandard.org/standard/documentation/1.0/document-link>`__
and
`website <http://iatistandard.org/101/activities-standard/related-documents/activity-documents/>`__
