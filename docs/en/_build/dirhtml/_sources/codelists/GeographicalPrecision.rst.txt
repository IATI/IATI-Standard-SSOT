Geographical Precision
======================


A system for clarifying the accuracy and usage of geographical coordinates 





This is a :ref:`Non-Core codelist <non_core_codelist>`.




Download this codelist
----------------------

.. list-table::
   :header-rows: 1

   * - :ref:`CLv1 <codelist_api_1.04>`:
     - :ref:`CLv2 <codelist_api_1.04>`:
     - :ref:`CLv3 <codelist_api_1.04>`:
     - :ref:`CLv3 (french) <codelist_api_1.04>`:

   * - `CSV <../downloads/clv1/codelist/GeographicalPrecision.csv>`__
     - `CSV <../downloads/clv2/csv/en/GeographicalPrecision.csv>`__
     - `CSV <../downloads/clv3/csv/en/GeographicalPrecision.csv>`__
     - `CSV <../downloads/clv3/csv/fr/GeographicalPrecision.csv>`__

   * - `JSON <../downloads/clv1/codelist/GeographicalPrecision.json>`__
     - `JSON <../downloads/clv2/json/en/GeographicalPrecision.json>`__
     - `JSON <../downloads/clv3/json/en/GeographicalPrecision.json>`__
     - `JSON <../downloads/clv3/json/fr/GeographicalPrecision.json>`__

   * - `XML <../downloads/clv1/codelist/GeographicalPrecision.xml>`__
     - `XML <../downloads/clv2/xml/GeographicalPrecision.xml>`__
     - `XML <../downloads/clv3/xml/GeographicalPrecision.xml>`__
     - `XML <../downloads/clv3/xml/GeographicalPrecision.xml>`__

`GitHub Source <https://github.com/IATI/IATI-Codelists-NonEmbedded/blob/master/xml/GeographicalPrecision.xml>`__



The codelists were translated in French in April 2018 with the support of the Government of Canada. Please note that if any codelists have been added since then, they may not be available in French.

Codes
-----

.. _GeographicalPrecision:
.. list-table::
   :header-rows: 1


   * - Code
     - Name
     - Description

   
       
   * - 1   
       
     - Exact location
     - The coordinates corresponds to an exact location, such as a populated place or a hill. The code is also used for locations that join a location which is a line (such as a road or railroad). Lines are not coded only the points that connect lines. All points that are mentioned in the source are coded.
   
       
   * - 2   
       
     - Near exact location
     - The location is mentioned in the source as being "near", in the "area" of, or up to 25 km away from an exact location. The coordinates refer to that adjacent, exact, location.
   
       
   * - 3   
       
     - Second order administrative division
     - The location is, or lies in, a second order administrative division (ADM2), such as a district, municipality or commune
   
       
   * - 4   
       
     - First order administrative division
     - The location is, or lies in, a first order administrative division (ADM1), such as a province, state or governorate.
   
       
   * - 5   
       
     - Estimated coordinates
     - The location can only be related to estimated coordinates, such as when a location lies between populated places; along rivers, roads and borders; more than 25 km away from a specific location; or when sources refer to parts of a country greater than ADM1 (e.g. "northern Uganda").
   
       
   * - 6   
       
     - Independent political entity
     - The location can only be related to an independent political entity, meaning the pair of coordinates that represent a country.
   
       
   * - 7   
       
     - Unclear - capital
     - Unclear. The capital is assumed to be one of two possible locations. (The other option is the country level, with precision 9.)
   
       
   * - 8   
       
     - Local or national capital
     - The location is estimated to be a seat of an administrative division (local capital) or the national capital. If aid goes to Luanda without further specification on the location, and there is an ADM1 and a capital called Luanda, then code the coordinates of the capital with precision 8. If it is not spelled out that aid goes to the capital; but if it is clear that it goes to a government ministry or to government financial institutions; and if those institutions are most likely located in the capital; then the coordinates of the capital are coded with precision 8. (However, if it can be verified that the recipient institution is located in the capital then precision 1 is used.)
   
       
   * - 9   
       
     - Unclear - country
     - Unclear. The locations is estimated to be the country level (often paired with the capital, with precision 7)
   

