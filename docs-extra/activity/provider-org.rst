

Notes
~~~~~

The unique organisation identifier for the provider organisation. Some
large organisations already have existing codes assigned through the
OECD. For those organisations where no code exists, the organisation can
generate their own code for IATI use in the format of
[country-registration] - [company-registration number]. (e.g. the
organisation identifier for DIPR is: GB-COH-06368740.)

Additional notes
^^^^^^^^^^^^^^^^

Organisation IDs: It is now recommended that organisation ids are built
to a convention, so the schema declaration that @ref must be on a
codelist is out of date. A change to the schema must occur through our
change control process. As such this is flagged for change.

Example Usage
~~~~~~~~~~~~~

The full name of the organisation making the financial transaction
(receiving in the case of loan and interest repayments).:

.. code-block:: xml

        <provider-org>DFID</provider-org>

The unique Organisation Identifier for the provider.:

.. code-block:: xml

        <provider-org ref="GB-1">DFID</provider-org>

If the funds are being provided from another reported activity, this
must record the unique activity identifier for that activity:

.. code-block:: xml

        <provider-org provider-activity-id="GB-1-10538"/>
