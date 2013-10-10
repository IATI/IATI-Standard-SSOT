

Notes
~~~~~

The unique organisation identifier for the receiver organisation. Some
large organisations already have existing codes assigned through the
OECD. For those organisations where no code exsits, the organisation can
generate their own code for IATI use in the format of
country-registration company-registration number. (e.g. the organisation
identifier for DIPR is: GB-COH-06368740.)

Additional notes
^^^^^^^^^^^^^^^^

Organisation IDs: It is now recommended that organisation ids are built
to a convention, so the schema declaration that @ref must be on a
codelist is out of date. A change to the schema must occur through our
change control process. As such this is flagged for change.

Example Usage
~~~~~~~~~~~~~

The full name of the organisation receiving the financial transaction
(receiving in the case of loan and interest repayments).:

.. code-block:: xml

    <transaction>
      ....
        <receiver-org>Ministere du Plan, RDC</receiver-org>
      ...
    </transaction>

The unique Organisation Identifier for the receiver.:

.. code-block:: xml

    <transaction>
      ....
        <receiver-org ref="GB-1">DFID</receiver-org>
      ...
    </transaction>

If the funds are being provided to another reported activity, this must
record the unique activity identifier for that activity:

.. code-block:: xml

    <transaction>
      ....
        <receiver-org receiver-activity-id="CG-3-1440"/>
      ...
    </transaction>
