

Example Usage
~~~~~~~~~~~~~

This is a new element for version 1.02. Previously, this was an
attribute.

The code should be declared in any usage of this element:

.. code-block:: xml

        <language code="en" />
        <language code="fr" />

Additionally, a text description of the code can be provided:

.. code-block:: xml

        <language code="fr" xml:lang="en">French</language>
        <language code="fr" xml:lang="fr">Francais</language>

Changelog
~~~~~~~~~

1.02
^^^^

Addition of a language element as a child of the document-link element:
document-link/language/text() (0..1) - The ISO 639 code for the language
of the document

1.01
^^^^

This element did not exist
