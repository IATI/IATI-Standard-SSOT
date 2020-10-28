Related Activity Type
=====================






This is a :ref:`Core codelist <core_codelist>`.



Use this codelist for
---------------------

* :ref:`iati-activities/iati-activity/related-activity/@type <iati-activities/iati-activity/related-activity/.type>`



Download this codelist
----------------------

.. list-table::
   :header-rows: 1

   * - :ref:`CLv1 <codelist_api_1.04>`:
     - :ref:`CLv2 <codelist_api_1.04>`:
     - :ref:`CLv3 <codelist_api_1.04>`:
     - :ref:`CLv3 (french) <codelist_api_1.04>`:

   * - `CSV <../downloads/clv1/codelist/RelatedActivityType.csv>`__
     - `CSV <../downloads/clv2/csv/en/RelatedActivityType.csv>`__
     - `CSV <../downloads/clv3/csv/en/RelatedActivityType.csv>`__
     - `CSV <../downloads/clv3/csv/fr/RelatedActivityType.csv>`__

   * - `JSON <../downloads/clv1/codelist/RelatedActivityType.json>`__
     - `JSON <../downloads/clv2/json/en/RelatedActivityType.json>`__
     - `JSON <../downloads/clv3/json/en/RelatedActivityType.json>`__
     - `JSON <../downloads/clv3/json/fr/RelatedActivityType.json>`__

   * - `XML <../downloads/clv1/codelist/RelatedActivityType.xml>`__
     - `XML <../downloads/clv2/xml/RelatedActivityType.xml>`__
     - `XML <../downloads/clv3/xml/RelatedActivityType.xml>`__
     - `XML <../downloads/clv3/xml/RelatedActivityType.xml>`__

`GitHub Source <https://github.com/IATI/IATI-Codelists/blob/version-2.03/xml/RelatedActivityType.xml>`__



The codelists were translated in French in April 2018 with the support of the Government of Canada. Please note that if any codelists have been added since then, they may not be available in French.

Codes
-----

.. _RelatedActivityType:
.. list-table::
   :header-rows: 1


   * - Code
     - Name
     - Description

   
       
   * - 1   
       
     - Parent
     - An activity that contains sub-activities (sub-components) which are reported separately to IATI
   
       
   * - 2   
       
     - Child
     - A sub-activity (or sub-component) that sits within a larger activity (parent) which is also reported to IATI
   
       
   * - 3   
       
     - Sibling
     - A sub-activity (or sub-component) that is related to another sub-activity with the same parent
   
       
   * - 4   
       
     - Co-funded
     - An activity that receives funding from more than one organisation
   
       
   * - 5   
       
     - Third Party
     - A report by another organisation on the same activity you are reporting (excluding activities reported as part of a financial transaction - e.g. provider-activity-id or a co-funded activity, using code 4)
   

Changelog
~~~~~~~~~

2.01
^^^^
| The following new code was added to *RelatedActivityType*: `5 (Third Party)  <http://iatistandard.org/upgrades/integer-upgrade-to-2-01/2-01-changes/#related-activity-type-new-code>`__
