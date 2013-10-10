

Example Usage
~~~~~~~~~~~~~

When default language has been declared in the <iati-activity> element
then this will suffice:

.. code-block:: xml

        <title>Grant Performance Report</title>

If a default langage has NOT been declared in the <iati-activity>
element, then a language must be specified

.. code-block:: xml

        <title xml:lang="en">Grant Performance Report</title>

A title may be repeated in many languages. This example assumes a
default language of English has previously been declared:

.. code-block:: xml

        <title>Grant Performance Report</title>
        <title xml:lang="es">Grant Informe sobre los resultados</title>
        <title xml:lang="fr">Rapport sur le rendement de subvention</title>

It is good practice to provide activity titles in the language(s) spoken
in the country(ies) where the activity take place, or is aimed at.
