

Example Usage
~~~~~~~~~~~~~

This element is a container for other sub elements:

.. code-block:: xml

        <contact-info type="1">
           ....
        </contact-info>

This example from DfID, contains the Organisation, telephone, email and
mailing address for the activity.

.. code-block:: xml

    <contact-info type="1">
    <person-name>A Smith</person-name>
    <organisation>Department for International Development</organisation>
    <telephone>+44 (0) 1355 84 3132</telephone>
    <email>enquiry@dfid.gov.uk</email>
    <mailing-address>
    Public Enquiry Point, Abercrombie House, Eaglesham Road, East Kilbride, Glasgow G75 8EA
    </mailing-address>
    <website>https://www.gov.uk/government/organisations/department-for-international-development</website>
    </contact-info>

Changelog
~~~~~~~~~

1.03
^^^^

Added the optional contact-info/website element

Added the optional contact-info/@type attribute

Changed the following subelements of contact-info to allow
multiple-language versions explicitly (no change to parsing; purely
semantic):

-  organisation
-  person-name
-  job-title
-  mailing-address
