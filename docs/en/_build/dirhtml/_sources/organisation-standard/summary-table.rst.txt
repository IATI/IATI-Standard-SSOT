Organisation Standard Summary Table
===================================

.. list-table::
    :header-rows: 1

    * - Section
      - Item
      - Description
      - Type
      - Codelist
      - XML
      - Occur
      - Rules


    * - :doc:`iati-organisations </organisation-standard/iati-organisations>`
      - 
      - Top-level list of one or more IATI organisation records.
      - 
      - 
      - iati-organisations
      - ..
      - 

    * - 
      - version
      - A number indicating the IATI specification version in use.
        This is mandatory and must be a valid version.
      - xsd:string
      - :doc:`/codelists/Version`
      - iati-organisations/\@version
      - 1..1
      - 

    * - 
      - generated-datetime
      - A date/time stamp for when this file was generated. This
        is not necessarily the last-updated date for the
        individual activity records in it. Use of this attribute
        is highly recommended, to allow recipients to know when a
        file has been updated.
      - xsd:dateTime
      - 
      - iati-organisations/\@generated-datetime
      - 0..1
      - 

    * - :doc:`iati-organisation </organisation-standard/iati-organisations/iati-organisation>`
      - 
      - Top-level element for a single IATI organisation report.
      - 
      - 
      - iati-organisations/iati-organisation
      - 1..*
      - 

    * - 
      - last-updated-datetime
      - The last date/time that the data for this specific
        organisation was updated.  This date must change whenever
        the value of any field changes.
      - xsd:dateTime
      - 
      - iati-organisations/iati-organisation/\@last-updated-datetime
      - 0..1
      - ``@last-updated-datetime`` must not be more recent than the current date

    * - 
      - xml:lang
      - A code specifying the default language of text in this organisation. It is recommended that wherever possible only codes from ISO 639-1 are used. If this is not declared then the xml:lang attribute MUST be specified for each narrative element.
      - 
      - :doc:`/codelists/Language`
      - iati-organisations/iati-organisation/\@xml:lang
      - 0..1
      - ``@xml:lang`` must exist, otherwise all ``lang`` must exist.

    * - 
      - default-currency
      - Default ISO 4217 currency code for all financial values in
        this activity report. If this is not declared then the
        currency attribute MUST be specified for all monetary
        values.
      - xsd:string
      - :doc:`/codelists/Currency`
      - iati-organisations/iati-organisation/\@default-currency
      - 0..1
      - ``@default-currency`` must exist, otherwise all ``currency`` must exist.

    * - :doc:`organisation-identifier </organisation-standard/iati-organisations/iati-organisation/organisation-identifier>`
      - 
      - Machine-readable identification string for the organisation issuing the report. Must be in the format {RegistrationAgency}-{RegistrationNumber} where {RegistrationAgency} is a valid code in the Organisation Registration Agency code list and {RegistrationNumber} is a valid identifier issued by the {RegistrationAgency}.
      - 
      - 
      - iati-organisations/iati-organisation/organisation-identifier
      - 1..1
      - ``organisation-identifier`` should match the regex ``[^\/\&\|\?]+``

    * - :doc:`name </organisation-standard/iati-organisations/iati-organisation/name>`
      - 
      - The human-readable name of the organisation.
      - 
      - 
      - iati-organisations/iati-organisation/name
      - 1..1
      - 

    * - 
      - :doc:`narrative </organisation-standard/iati-organisations/iati-organisation/name/narrative>`
      - The free text name or description of the item being described. This can
        be repeated in multiple languages.
      - 
      - 
      - iati-organisations/iati-organisation/name/narrative
      - 1..*
      - 

    * - 
      - 
      - 
      - xsd:string
      - 
      - iati-organisations/iati-organisation/name/narrative/text()
      - 
      - 

    * - 
      - xml:lang
      - A code specifying the language of text in this element. It is recommended that wherever possible only codes from ISO 639-1 are used. If not present, the default language is assumed.
      - 
      - :doc:`/codelists/Language`
      - iati-organisations/iati-organisation/name/narrative/\@xml:lang
      - 0..1
      - 

    * - :doc:`reporting-org </organisation-standard/iati-organisations/iati-organisation/reporting-org>`
      - 
      - The organisation issuing the report.
        May be a primary source (reporting on its own activity as
        donor, implementing agency, etc) or a secondary source
        (reporting on the activities of another organisation).
        
        Specifying the @ref attribute is mandatory.
        May contain the organisation name as content.
        
        All activities in an activity xml file must contain the same
        @ref AND this @ref must be the same as the iati-identifier
        recorded in the registry publisher record of the account under
        which this file is published.
      - 
      - 
      - iati-organisations/iati-organisation/reporting-org
      - 1..1
      - 

    * - 
      - ref
      - Machine-readable identification string for the organisation issuing the report. Must be in the format {RegistrationAgency}-{RegistrationNumber} where {RegistrationAgency} is a valid code in the Organisation Registration Agency code list and {RegistrationNumber} is a valid identifier issued by the {RegistrationAgency}.
      - xsd:string
      - 
      - iati-organisations/iati-organisation/reporting-org/\@ref
      - 1..1
      - ``reporting-org/@ref`` should match the regex ``[^\/\&\|\?]+``

    * - 
      - type
      - The type of organisation issuing the report. See IATI codelist for values.
      - xsd:string
      - :doc:`/codelists/OrganisationType`
      - iati-organisations/iati-organisation/reporting-org/\@type
      - 1..1
      - 

    * - 
      - secondary-reporter
      - A flag indicating that the reporting organisation of this activity is acting as a secondary reporter. A secondary reporter is one that reproduces data on the activities of an organisation for which it is not directly responsible. This does not include a publisher officially assigned as a proxy to report on behalf of another.
      - xsd:boolean
      - 
      - iati-organisations/iati-organisation/reporting-org/\@secondary-reporter
      - 0..1
      - 

    * - 
      - :doc:`narrative </organisation-standard/iati-organisations/iati-organisation/reporting-org/narrative>`
      - The name of the organisation. May be repeated for
        different languages.
      - 
      - 
      - iati-organisations/iati-organisation/reporting-org/narrative
      - 1..*
      - 

    * - 
      - 
      - 
      - xsd:string
      - 
      - iati-organisations/iati-organisation/reporting-org/narrative/text()
      - 
      - 

    * - 
      - xml:lang
      - A code specifying the language of text in this element. It is recommended that wherever possible only codes from ISO 639-1 are used. If not present, the default language is assumed.
      - 
      - :doc:`/codelists/Language`
      - iati-organisations/iati-organisation/reporting-org/narrative/\@xml:lang
      - 0..1
      - 

    * - :doc:`total-budget </organisation-standard/iati-organisations/iati-organisation/total-budget>`
      - 
      - The total-budget element allows for the reporting of the organisation's
        own budget. The recommendation is that, where and when possible, the
        organisation's total annual planned budget for each of the next three
        years is reported. The status explains whether the budget being reported
        is indicative or has been formally committed. The value should appear
        within the BudgetStatus codelist. If the @status attribute is not present,
        the budget is assumed to be indicative.
      - 
      - 
      - iati-organisations/iati-organisation/total-budget
      - 0..*
      - 

    * - 
      - status
      - The status explains whether the budget being reported is indicative or has
        been formally committed. The value should appear within the BudgetStatus
        codelist. If the @status attribute is not present, the budget is assumed
        to be indicative.
      - xsd:string
      - :doc:`/codelists/BudgetStatus`
      - iati-organisations/iati-organisation/total-budget/\@status
      - 0..1
      - 

    * - 
      - :doc:`period-start </organisation-standard/iati-organisations/iati-organisation/total-budget/period-start>`
      - The start of the budget period.
      - 
      - 
      - iati-organisations/iati-organisation/total-budget/period-start
      - 1..1
      - 

    * - 
      - iso-date
      - 
      - xsd:date
      - 
      - iati-organisations/iati-organisation/total-budget/period-start/\@iso-date
      - 1..1
      - ``period-start/@iso-date`` must be before or the same as ``period-end/@iso-date``
        The time between ``period-start/@iso-date`` and ``period-end/@iso-date`` must not be over a year

    * - 
      - :doc:`period-end </organisation-standard/iati-organisations/iati-organisation/total-budget/period-end>`
      - The end of the period (which must not be greater than one year)
      - 
      - 
      - iati-organisations/iati-organisation/total-budget/period-end
      - 1..1
      - 

    * - 
      - iso-date
      - 
      - xsd:date
      - 
      - iati-organisations/iati-organisation/total-budget/period-end/\@iso-date
      - 1..1
      - ``period-start/@iso-date`` must be before or the same as ``period-end/@iso-date``
        The time between ``period-start/@iso-date`` and ``period-end/@iso-date`` must not be over a year

    * - 
      - :doc:`value </organisation-standard/iati-organisations/iati-organisation/total-budget/value>`
      - The total value of the organisation's aid budget for
        this period.
      - 
      - 
      - iati-organisations/iati-organisation/total-budget/value
      - 1..1
      - 

    * - 
      - currency
      - A three letter ISO 4217 code for the original currency of the
        amount. This is required for all currency amounts unless
        the iati-organisation/\@default-currency attribute is
        specified.
      - xsd:string
      - :doc:`/codelists/Currency`
      - iati-organisations/iati-organisation/total-budget/value/\@currency
      - 0..1
      - 

    * - 
      - value-date
      - The date to be used for determining the exchange rate for
        currency conversions.
      - xsd:date
      - 
      - iati-organisations/iati-organisation/total-budget/value/\@value-date
      - 1..1
      - 

    * - 
      - :doc:`budget-line </organisation-standard/iati-organisations/iati-organisation/total-budget/budget-line>`
      - A breakdown of the total budget into sub-totals. The
        breakdown is determined by the reporting organisation
        and described in the narrative. The period covered is
        the same as that covered by the parent total-budget
        element. The sum of budget-line values does not have to
        equal the value given in the parent element.
      - 
      - 
      - iati-organisations/iati-organisation/total-budget/budget-line
      - 0..*
      - 

    * - 
      - ref
      - An internal reference for this budget line taken
        from the reporting organisation's own system.
        Optional.
      - xsd:string
      - 
      - iati-organisations/iati-organisation/total-budget/budget-line/\@ref
      - 0..1
      - 

    * - 
      - :doc:`value </organisation-standard/iati-organisations/iati-organisation/total-budget/budget-line/value>`
      - The budget sub-total. The definition of the
        sub-division is determined by
        iati-organisation/total-budget/budget-line/narrative
      - 
      - 
      - iati-organisations/iati-organisation/total-budget/budget-line/value
      - 1..1
      - 

    * - 
      - currency
      - A three letter ISO 4217 code for the original currency of the
        amount. This is required for all currency amounts unless
        the iati-organisation/\@default-currency attribute is
        specified.
      - xsd:string
      - 
      - iati-organisations/iati-organisation/total-budget/budget-line/value/\@currency
      - 0..1
      - 

    * - 
      - value-date
      - The date to be used for determining the exchange rate for
        currency conversions.
      - xsd:date
      - 
      - iati-organisations/iati-organisation/total-budget/budget-line/value/\@value-date
      - 1..1
      - 

    * - 
      - :doc:`narrative </organisation-standard/iati-organisations/iati-organisation/total-budget/budget-line/narrative>`
      - The free text name or description of the item being described. This can
        be repeated in multiple languages.
      - 
      - 
      - iati-organisations/iati-organisation/total-budget/budget-line/narrative
      - 1..*
      - 

    * - 
      - 
      - 
      - xsd:string
      - 
      - iati-organisations/iati-organisation/total-budget/budget-line/narrative/text()
      - 
      - 

    * - 
      - xml:lang
      - A code specifying the language of text in this element. It is recommended that wherever possible only codes from ISO 639-1 are used. If not present, the default language is assumed.
      - 
      - :doc:`/codelists/Language`
      - iati-organisations/iati-organisation/total-budget/budget-line/narrative/\@xml:lang
      - 0..1
      - 

    * - :doc:`recipient-org-budget </organisation-standard/iati-organisations/iati-organisation/recipient-org-budget>`
      - 
      - The recipient-org-budget element allows for the reporting of
        forward looking budgets for each institution which receives
        core funding from the reporting organisation. The
        recommendation is that, where and when possible, annual
        planned budgets for each recipient institution for each of the
        next three financial years are reported. This is primarily
        applicable to donors but any provider of core funding is
        expected to use it. Earmarked budgets should be reported at
        activity-level through the Activity Standard. The status
        explains whether the budget being reported is indicative or
        has been formally committed. The value should appear within
        the BudgetStatus codelist. If the @status attribute is not
        present, the budget is assumed to be indicative.
      - 
      - 
      - iati-organisations/iati-organisation/recipient-org-budget
      - 0..*
      - 

    * - 
      - status
      - The status explains whether the budget being reported is indicative or has
        been formally committed. The value should appear within the BudgetStatus
        codelist. If the @status attribute is not present, the budget is assumed
        to be indicative.
      - xsd:string
      - :doc:`/codelists/BudgetStatus`
      - iati-organisations/iati-organisation/recipient-org-budget/\@status
      - 0..1
      - 

    * - 
      - :doc:`recipient-org </organisation-standard/iati-organisations/iati-organisation/recipient-org-budget/recipient-org>`
      - The organisation that will receive the funds.
      - 
      - 
      - iati-organisations/iati-organisation/recipient-org-budget/recipient-org
      - 1..1
      - 

    * - 
      - ref
      - Machine-readable identification string for the organisation issuing the report. Must be in the format {RegistrationAgency}-{RegistrationNumber} where {RegistrationAgency} is a valid code in the Organisation Registration Agency code list and {RegistrationNumber} is a valid identifier issued by the {RegistrationAgency}. If this is not present then the narrative MUST contain the name of the organisation.
      - xsd:string
      - 
      - iati-organisations/iati-organisation/recipient-org-budget/recipient-org/\@ref
      - 0..1
      - 

    * - 
      - :doc:`narrative </organisation-standard/iati-organisations/iati-organisation/recipient-org-budget/recipient-org/narrative>`
      - The name of the organisation. This can be repeated in multiple languages.
      - 
      - 
      - iati-organisations/iati-organisation/recipient-org-budget/recipient-org/narrative
      - 1..*
      - 

    * - 
      - 
      - 
      - xsd:string
      - 
      - iati-organisations/iati-organisation/recipient-org-budget/recipient-org/narrative/text()
      - 
      - 

    * - 
      - xml:lang
      - A code specifying the language of text in this element. It is recommended that wherever possible only codes from ISO 639-1 are used. If not present, the default language is assumed.
      - 
      - :doc:`/codelists/Language`
      - iati-organisations/iati-organisation/recipient-org-budget/recipient-org/narrative/\@xml:lang
      - 0..1
      - 

    * - 
      - :doc:`period-start </organisation-standard/iati-organisations/iati-organisation/recipient-org-budget/period-start>`
      - The start of the budget period.
      - 
      - 
      - iati-organisations/iati-organisation/recipient-org-budget/period-start
      - 1..1
      - 

    * - 
      - iso-date
      - 
      - xsd:date
      - 
      - iati-organisations/iati-organisation/recipient-org-budget/period-start/\@iso-date
      - 1..1
      - ``period-start/@iso-date`` must be before or the same as ``period-end/@iso-date``
        The time between ``period-start/@iso-date`` and ``period-end/@iso-date`` must not be over a year

    * - 
      - :doc:`period-end </organisation-standard/iati-organisations/iati-organisation/recipient-org-budget/period-end>`
      - The end of the period (which must not be greater than one year)
      - 
      - 
      - iati-organisations/iati-organisation/recipient-org-budget/period-end
      - 1..1
      - 

    * - 
      - iso-date
      - 
      - xsd:date
      - 
      - iati-organisations/iati-organisation/recipient-org-budget/period-end/\@iso-date
      - 1..1
      - ``period-start/@iso-date`` must be before or the same as ``period-end/@iso-date``
        The time between ``period-start/@iso-date`` and ``period-end/@iso-date`` must not be over a year

    * - 
      - :doc:`value </organisation-standard/iati-organisations/iati-organisation/recipient-org-budget/value>`
      - The total value of the money budgeted to be disbursed to
        the specified recipient organisation during this time
        period.
      - 
      - 
      - iati-organisations/iati-organisation/recipient-org-budget/value
      - 1..1
      - 

    * - 
      - currency
      - A three letter ISO 4217 code for the original currency of the
        amount. This is required for all currency amounts unless
        the iati-organisation/\@default-currency attribute is
        specified.
      - xsd:string
      - :doc:`/codelists/Currency`
      - iati-organisations/iati-organisation/recipient-org-budget/value/\@currency
      - 0..1
      - 

    * - 
      - value-date
      - The date to be used for determining the exchange rate for
        currency conversions.
      - xsd:date
      - 
      - iati-organisations/iati-organisation/recipient-org-budget/value/\@value-date
      - 1..1
      - 

    * - 
      - :doc:`budget-line </organisation-standard/iati-organisations/iati-organisation/recipient-org-budget/budget-line>`
      - A breakdown of the recipient organisation's budget into
        sub-totals. The breakdown is determined by the
        reporting organisation and described in the narrative.
        The period covered is the same as that covered by the
        parent recipient-org-budget element. The sum of
        budget-line values does not have to equal the value
        given in the parent element.
      - 
      - 
      - iati-organisations/iati-organisation/recipient-org-budget/budget-line
      - 0..*
      - 

    * - 
      - ref
      - An internal reference for this budget line taken
        from the reporting organisation's own system.
        Optional.
      - xsd:string
      - 
      - iati-organisations/iati-organisation/recipient-org-budget/budget-line/\@ref
      - 0..1
      - 

    * - 
      - :doc:`value </organisation-standard/iati-organisations/iati-organisation/recipient-org-budget/budget-line/value>`
      - The budget sub-total. The definition of the
        sub-division is determined by
        iati-organisation/recipient-org-budget/budget-line/narrative
      - 
      - 
      - iati-organisations/iati-organisation/recipient-org-budget/budget-line/value
      - 1..1
      - 

    * - 
      - currency
      - A three letter ISO 4217 code for the original currency of the
        amount. This is required for all currency amounts unless
        the iati-organisation/\@default-currency attribute is
        specified.
      - xsd:string
      - :doc:`/codelists/Currency`
      - iati-organisations/iati-organisation/recipient-org-budget/budget-line/value/\@currency
      - 0..1
      - 

    * - 
      - value-date
      - The date to be used for determining the exchange rate for
        currency conversions.
      - xsd:date
      - 
      - iati-organisations/iati-organisation/recipient-org-budget/budget-line/value/\@value-date
      - 1..1
      - 

    * - 
      - :doc:`narrative </organisation-standard/iati-organisations/iati-organisation/recipient-org-budget/budget-line/narrative>`
      - The free text name or description of the item being described. This can
        be repeated in multiple languages.
      - 
      - 
      - iati-organisations/iati-organisation/recipient-org-budget/budget-line/narrative
      - 1..*
      - 

    * - 
      - 
      - 
      - xsd:string
      - 
      - iati-organisations/iati-organisation/recipient-org-budget/budget-line/narrative/text()
      - 
      - 

    * - 
      - xml:lang
      - A code specifying the language of text in this element. It is recommended that wherever possible only codes from ISO 639-1 are used. If not present, the default language is assumed.
      - 
      - :doc:`/codelists/Language`
      - iati-organisations/iati-organisation/recipient-org-budget/budget-line/narrative/\@xml:lang
      - 0..1
      - 

    * - :doc:`recipient-region-budget </organisation-standard/iati-organisations/iati-organisation/recipient-region-budget>`
      - 
      - The recipient-region-budget element allows for the reporting of forward
        looking budgets where the organisation maintains region-wide, rather than
        or in addition to country-specific budgets. The recommendation is that,
        where and when possible, the organisation’s total annual planned budget
        for each of the next three financial years is reported for each recipient
        region. This must NOT include an aggregation of budgets reported in the
        recipient-country-budget element. It is strongly recommended that
        publishers report to existing defined regions wherever possible. The
        status explains whether the budget being reported is indicative or has
        been formally committed. The value should appear within the BudgetStatus
        codelist. If the @status attribute is not present, the budget is assumed
        to be indicative.
      - 
      - 
      - iati-organisations/iati-organisation/recipient-region-budget
      - 0..*
      - 

    * - 
      - status
      - The status explains whether the budget being reported is indicative or has
        been formally committed. The value should appear within the BudgetStatus
        codelist. If the @status attribute is not present, the budget is assumed
        to be indicative.
      - xsd:string
      - :doc:`/codelists/BudgetStatus`
      - iati-organisations/iati-organisation/recipient-region-budget/\@status
      - 0..1
      - 

    * - 
      - :doc:`recipient-region </organisation-standard/iati-organisations/iati-organisation/recipient-region-budget/recipient-region>`
      - The supranational geographic region where funds have been allocated.
      - 
      - 
      - iati-organisations/iati-organisation/recipient-region-budget/recipient-region
      - 1..1
      - 

    * - 
      - vocabulary
      - An IATI code for the vocabulary from which the region code is
        drawn. If it is not present, code 1 ('OECD DAC') is assumed.
      - xsd:string
      - :doc:`/codelists/RegionVocabulary`
      - iati-organisations/iati-organisation/recipient-region-budget/recipient-region/\@vocabulary
      - 0..1
      - 

    * - 
      - vocabulary-uri
      - The URI where this vocabulary is defined. If the vocabulary is 99 (reporting organisation), the URI where this internal vocabulary is defined. While this is an optional field it is STRONGLY RECOMMENDED that all publishers use it to ensure that the meaning of their codes are fully understood by data users.
      - xsd:anyURI
      - 
      - iati-organisations/iati-organisation/recipient-region-budget/recipient-region/\@vocabulary-uri
      - 0..1
      - 

    * - 
      - code
      - Either an OECD DAC, UN region code or (if code ‘99’ Reporting
        organisation is selected for recipient-region/\@vocabulary) a
        code from your internal vocabulary. The codelist is determined
        by vocabulary attribute. The value in recipient-region/\@code
        should appear within the Region codelist, if the vocabulary
        code 1 ('OECD DAC') is used.
      - xsd:string
      - (:doc:`/codelists/Region`)
      - iati-organisations/iati-organisation/recipient-region-budget/recipient-region/\@code
      - 0..1
      - 

    * - 
      - :doc:`narrative </organisation-standard/iati-organisations/iati-organisation/recipient-region-budget/recipient-region/narrative>`
      - The free text name or description of the item being described. This can
        be repeated in multiple languages.
      - 
      - 
      - iati-organisations/iati-organisation/recipient-region-budget/recipient-region/narrative
      - 0..*
      - 

    * - 
      - 
      - 
      - xsd:string
      - 
      - iati-organisations/iati-organisation/recipient-region-budget/recipient-region/narrative/text()
      - 
      - 

    * - 
      - xml:lang
      - A code specifying the language of text in this element. It is recommended that wherever possible only codes from ISO 639-1 are used. If not present, the default language is assumed.
      - 
      - :doc:`/codelists/Language`
      - iati-organisations/iati-organisation/recipient-region-budget/recipient-region/narrative/\@xml:lang
      - 0..1
      - 

    * - 
      - :doc:`period-start </organisation-standard/iati-organisations/iati-organisation/recipient-region-budget/period-start>`
      - The start of the budget period.
      - 
      - 
      - iati-organisations/iati-organisation/recipient-region-budget/period-start
      - 1..1
      - 

    * - 
      - iso-date
      - 
      - xsd:date
      - 
      - iati-organisations/iati-organisation/recipient-region-budget/period-start/\@iso-date
      - 1..1
      - ``period-start/@iso-date`` must be before or the same as ``period-end/@iso-date``
        The time between ``period-start/@iso-date`` and ``period-end/@iso-date`` must not be over a year

    * - 
      - :doc:`period-end </organisation-standard/iati-organisations/iati-organisation/recipient-region-budget/period-end>`
      - The end of the period (which must not be greater than one year)
      - 
      - 
      - iati-organisations/iati-organisation/recipient-region-budget/period-end
      - 1..1
      - 

    * - 
      - iso-date
      - 
      - xsd:date
      - 
      - iati-organisations/iati-organisation/recipient-region-budget/period-end/\@iso-date
      - 1..1
      - ``period-start/@iso-date`` must be before or the same as ``period-end/@iso-date``
        The time between ``period-start/@iso-date`` and ``period-end/@iso-date`` must not be over a year

    * - 
      - :doc:`value </organisation-standard/iati-organisations/iati-organisation/recipient-region-budget/value>`
      - The total value of the money budgeted to be disbursed to
        the specified region during this time period.  This
        element is required.
      - 
      - 
      - iati-organisations/iati-organisation/recipient-region-budget/value
      - 1..1
      - 

    * - 
      - currency
      - A three letter ISO 4217 code for the original currency of the
        amount. This is required for all currency amounts unless
        the iati-organisation/\@default-currency attribute is
        specified.
      - xsd:string
      - :doc:`/codelists/Currency`
      - iati-organisations/iati-organisation/recipient-region-budget/value/\@currency
      - 0..1
      - 

    * - 
      - value-date
      - The date to be used for determining the exchange rate for
        currency conversions.
      - xsd:date
      - 
      - iati-organisations/iati-organisation/recipient-region-budget/value/\@value-date
      - 1..1
      - 

    * - 
      - :doc:`budget-line </organisation-standard/iati-organisations/iati-organisation/recipient-region-budget/budget-line>`
      - A breakdown of the recipient region’s budget into sub-totals. The
        breakdown is determined by the reporting organisation and described
        in the narrative. The period covered is the same as that covered by
        the parent recipient-region-budget element. The sum of budget-line
        values does not have to equal the value given in the parent element.
      - 
      - 
      - iati-organisations/iati-organisation/recipient-region-budget/budget-line
      - 0..*
      - 

    * - 
      - ref
      - An internal reference for this budget line taken
        from the reporting organisation's own system.
        Optional.
      - xsd:string
      - 
      - iati-organisations/iati-organisation/recipient-region-budget/budget-line/\@ref
      - 0..1
      - 

    * - 
      - :doc:`value </organisation-standard/iati-organisations/iati-organisation/recipient-region-budget/budget-line/value>`
      - The budget sub-total. The definition of the
        sub-division is determined by
        iati-organisation/recipient-region-budget/budget-line/narrative
      - 
      - 
      - iati-organisations/iati-organisation/recipient-region-budget/budget-line/value
      - 1..1
      - 

    * - 
      - currency
      - A three letter ISO 4217 code for the original currency of the
        amount. This is required for all currency amounts unless
        the iati-organisation/\@default-currency attribute is
        specified.
      - xsd:string
      - :doc:`/codelists/Currency`
      - iati-organisations/iati-organisation/recipient-region-budget/budget-line/value/\@currency
      - 0..1
      - 

    * - 
      - value-date
      - The date to be used for determining the exchange rate for
        currency conversions.
      - xsd:date
      - 
      - iati-organisations/iati-organisation/recipient-region-budget/budget-line/value/\@value-date
      - 1..1
      - 

    * - 
      - :doc:`narrative </organisation-standard/iati-organisations/iati-organisation/recipient-region-budget/budget-line/narrative>`
      - The free text name or description of the item being described. This can
        be repeated in multiple languages.
      - 
      - 
      - iati-organisations/iati-organisation/recipient-region-budget/budget-line/narrative
      - 1..*
      - 

    * - 
      - 
      - 
      - xsd:string
      - 
      - iati-organisations/iati-organisation/recipient-region-budget/budget-line/narrative/text()
      - 
      - 

    * - 
      - xml:lang
      - A code specifying the language of text in this element. It is recommended that wherever possible only codes from ISO 639-1 are used. If not present, the default language is assumed.
      - 
      - :doc:`/codelists/Language`
      - iati-organisations/iati-organisation/recipient-region-budget/budget-line/narrative/\@xml:lang
      - 0..1
      - 

    * - :doc:`recipient-country-budget </organisation-standard/iati-organisations/iati-organisation/recipient-country-budget>`
      - 
      - The recipient-country-budget element allows for the reporting of
        forward looking budgets for each country in which the organisation
        operates. The recommendation is that, where and when possible, the
        organisation's total annual planned budget for each of the next
        three financial years is reported for each recipient country.
        It is strongly recommended that the start and end of the reported
        financial years match those of the recipient country's
        budgetary/planning cycle. The status explains whether the budget
        being reported is indicative or has been formally committed. The
        value should appear within the BudgetStatus codelist. If the
        @status attribute is not present, the budget is assumed to be
        indicative.
      - 
      - 
      - iati-organisations/iati-organisation/recipient-country-budget
      - 0..*
      - 

    * - 
      - status
      - The status explains whether the budget being reported is indicative or has
        been formally committed. The value should appear within the BudgetStatus
        codelist. If the @status attribute is not present, the budget is assumed
        to be indicative.
      - xsd:string
      - :doc:`/codelists/BudgetStatus`
      - iati-organisations/iati-organisation/recipient-country-budget/\@status
      - 0..1
      - 

    * - 
      - :doc:`recipient-country </organisation-standard/iati-organisations/iati-organisation/recipient-country-budget/recipient-country>`
      - The recipient country.
      - 
      - 
      - iati-organisations/iati-organisation/recipient-country-budget/recipient-country
      - 1..1
      - 

    * - 
      - code
      - ISO 3166-1 alpha-2 code for the country.
      - xsd:string
      - :doc:`/codelists/Country`
      - iati-organisations/iati-organisation/recipient-country-budget/recipient-country/\@code
      - 1..1
      - 

    * - 
      - :doc:`narrative </organisation-standard/iati-organisations/iati-organisation/recipient-country-budget/recipient-country/narrative>`
      - The free text name or description of the item being described. This can
        be repeated in multiple languages.
      - 
      - 
      - iati-organisations/iati-organisation/recipient-country-budget/recipient-country/narrative
      - 0..*
      - 

    * - 
      - 
      - 
      - xsd:string
      - 
      - iati-organisations/iati-organisation/recipient-country-budget/recipient-country/narrative/text()
      - 
      - 

    * - 
      - xml:lang
      - A code specifying the language of text in this element. It is recommended that wherever possible only codes from ISO 639-1 are used. If not present, the default language is assumed.
      - 
      - :doc:`/codelists/Language`
      - iati-organisations/iati-organisation/recipient-country-budget/recipient-country/narrative/\@xml:lang
      - 0..1
      - 

    * - 
      - :doc:`period-start </organisation-standard/iati-organisations/iati-organisation/recipient-country-budget/period-start>`
      - The start of the budget period.
      - 
      - 
      - iati-organisations/iati-organisation/recipient-country-budget/period-start
      - 1..1
      - 

    * - 
      - iso-date
      - 
      - xsd:date
      - 
      - iati-organisations/iati-organisation/recipient-country-budget/period-start/\@iso-date
      - 1..1
      - ``period-start/@iso-date`` must be before or the same as ``period-end/@iso-date``
        The time between ``period-start/@iso-date`` and ``period-end/@iso-date`` must not be over a year

    * - 
      - :doc:`period-end </organisation-standard/iati-organisations/iati-organisation/recipient-country-budget/period-end>`
      - The end of the period (which must not be greater than one year)
      - 
      - 
      - iati-organisations/iati-organisation/recipient-country-budget/period-end
      - 1..1
      - 

    * - 
      - iso-date
      - 
      - xsd:date
      - 
      - iati-organisations/iati-organisation/recipient-country-budget/period-end/\@iso-date
      - 1..1
      - ``period-start/@iso-date`` must be before or the same as ``period-end/@iso-date``
        The time between ``period-start/@iso-date`` and ``period-end/@iso-date`` must not be over a year

    * - 
      - :doc:`value </organisation-standard/iati-organisations/iati-organisation/recipient-country-budget/value>`
      - The total value of the money budgeted to be disbursed to
        the specified country during this time period.  This
        element is required.
      - 
      - 
      - iati-organisations/iati-organisation/recipient-country-budget/value
      - 1..1
      - 

    * - 
      - currency
      - A three letter ISO 4217 code for the original currency of the
        amount. This is required for all currency amounts unless
        the iati-organisation/\@default-currency attribute is
        specified.
      - xsd:string
      - :doc:`/codelists/Currency`
      - iati-organisations/iati-organisation/recipient-country-budget/value/\@currency
      - 0..1
      - 

    * - 
      - value-date
      - The date to be used for determining the exchange rate for
        currency conversions.
      - xsd:date
      - 
      - iati-organisations/iati-organisation/recipient-country-budget/value/\@value-date
      - 1..1
      - 

    * - 
      - :doc:`budget-line </organisation-standard/iati-organisations/iati-organisation/recipient-country-budget/budget-line>`
      - A breakdown of the recipient country's budget into
        sub-totals.  The breakdown is determined by the
        reporting organisation and described in the narrative.
        The period covered is the same as that covered by the
        parent recipient-country-budget element. The sum of
        budget-line values does not have to equal the value
        given in the parent element.
      - 
      - 
      - iati-organisations/iati-organisation/recipient-country-budget/budget-line
      - 0..*
      - 

    * - 
      - ref
      - An internal reference for this budget line taken
        from the reporting organisation's own system.
        Optional.
      - xsd:string
      - 
      - iati-organisations/iati-organisation/recipient-country-budget/budget-line/\@ref
      - 0..1
      - 

    * - 
      - :doc:`value </organisation-standard/iati-organisations/iati-organisation/recipient-country-budget/budget-line/value>`
      - The budget sub-total. The definition of the
        sub-division is determined by
        iati-organisation/recipient-country-budget/budget-line/narrative
      - 
      - 
      - iati-organisations/iati-organisation/recipient-country-budget/budget-line/value
      - 1..1
      - 

    * - 
      - currency
      - A three letter ISO 4217 code for the original currency of the
        amount. This is required for all currency amounts unless
        the iati-organisation/\@default-currency attribute is
        specified.
      - xsd:string
      - :doc:`/codelists/Currency`
      - iati-organisations/iati-organisation/recipient-country-budget/budget-line/value/\@currency
      - 0..1
      - 

    * - 
      - value-date
      - The date to be used for determining the exchange rate for
        currency conversions.
      - xsd:date
      - 
      - iati-organisations/iati-organisation/recipient-country-budget/budget-line/value/\@value-date
      - 1..1
      - The ``budget-line/value/@value-date`` must be between the ``period-start/@iso-date`` and ``period-end/@iso-date`` dates.

    * - 
      - :doc:`narrative </organisation-standard/iati-organisations/iati-organisation/recipient-country-budget/budget-line/narrative>`
      - The free text name or description of the item being described. This can
        be repeated in multiple languages.
      - 
      - 
      - iati-organisations/iati-organisation/recipient-country-budget/budget-line/narrative
      - 1..*
      - 

    * - 
      - 
      - 
      - xsd:string
      - 
      - iati-organisations/iati-organisation/recipient-country-budget/budget-line/narrative/text()
      - 
      - 

    * - 
      - xml:lang
      - A code specifying the language of text in this element. It is recommended that wherever possible only codes from ISO 639-1 are used. If not present, the default language is assumed.
      - 
      - :doc:`/codelists/Language`
      - iati-organisations/iati-organisation/recipient-country-budget/budget-line/narrative/\@xml:lang
      - 0..1
      - 

    * - :doc:`total-expenditure </organisation-standard/iati-organisations/iati-organisation/total-expenditure>`
      - 
      - The total-expenditure element allows for the reporting of the
        organisation’s international development expenditure. The
        recommendation is that, where and when possible, the organisation’s
        total expenditure for each of the past three years is reported.
        The expense line allows publishers to record further breakdown.
      - 
      - 
      - iati-organisations/iati-organisation/total-expenditure
      - 0..*
      - 

    * - 
      - :doc:`period-start </organisation-standard/iati-organisations/iati-organisation/total-expenditure/period-start>`
      - The start of the budget period.
      - 
      - 
      - iati-organisations/iati-organisation/total-expenditure/period-start
      - 1..1
      - 

    * - 
      - iso-date
      - 
      - xsd:date
      - 
      - iati-organisations/iati-organisation/total-expenditure/period-start/\@iso-date
      - 1..1
      - The time between ``period-start/@iso-date`` and ``period-end/@iso-date`` must not be over a year
        ``period-start/@iso-date`` must be before or the same as ``period-end/@iso-date``

    * - 
      - :doc:`period-end </organisation-standard/iati-organisations/iati-organisation/total-expenditure/period-end>`
      - The end of the period (which must not be greater than one year)
      - 
      - 
      - iati-organisations/iati-organisation/total-expenditure/period-end
      - 1..1
      - 

    * - 
      - iso-date
      - 
      - xsd:date
      - 
      - iati-organisations/iati-organisation/total-expenditure/period-end/\@iso-date
      - 1..1
      - The time between ``period-start/@iso-date`` and ``period-end/@iso-date`` must not be over a year
        ``period-start/@iso-date`` must be before or the same as ``period-end/@iso-date``

    * - 
      - :doc:`value </organisation-standard/iati-organisations/iati-organisation/total-expenditure/value>`
      - The total value of the organisation's aid expenditure for
        this period.
      - 
      - 
      - iati-organisations/iati-organisation/total-expenditure/value
      - 1..1
      - 

    * - 
      - currency
      - A three letter ISO 4217 code for the original currency of the
        amount. This is required for all currency amounts unless
        the iati-organisation/\@default-currency attribute is
        specified.
      - xsd:string
      - 
      - iati-organisations/iati-organisation/total-expenditure/value/\@currency
      - 0..1
      - 

    * - 
      - value-date
      - The date to be used for determining the exchange rate for
        currency conversions.
      - xsd:date
      - 
      - iati-organisations/iati-organisation/total-expenditure/value/\@value-date
      - 1..1
      - 

    * - 
      - :doc:`expense-line </organisation-standard/iati-organisations/iati-organisation/total-expenditure/expense-line>`
      - A breakdown of the total expenditure into sub-totals.
        The breakdown is determined by the reporting
        organisation and described in the narrative. The period
        covered is the same as that covered by the parent
        total-expenditure element. The sum of expenditure-line
        values does not have to equal the value given in the
        parent element.
      - 
      - 
      - iati-organisations/iati-organisation/total-expenditure/expense-line
      - 0..*
      - 

    * - 
      - ref
      - An internal reference for this expenditure line taken
        from the reporting organisation’s own system. Optional.
      - xsd:string
      - 
      - iati-organisations/iati-organisation/total-expenditure/expense-line/\@ref
      - 0..1
      - 

    * - 
      - :doc:`value </organisation-standard/iati-organisations/iati-organisation/total-expenditure/expense-line/value>`
      - The expenditure sub-total. The definition of the
        sub-division is determined by
        iati-organisation/total-expenditure/expenditure-line/narrative
      - 
      - 
      - iati-organisations/iati-organisation/total-expenditure/expense-line/value
      - 1..1
      - 

    * - 
      - currency
      - A three letter ISO 4217 code for the original currency of the
        amount. This is required for all currency amounts unless
        the iati-organisation/\@default-currency attribute is
        specified.
      - xsd:string
      - 
      - iati-organisations/iati-organisation/total-expenditure/expense-line/value/\@currency
      - 0..1
      - 

    * - 
      - value-date
      - The date to be used for determining the exchange rate for
        currency conversions.
      - xsd:date
      - 
      - iati-organisations/iati-organisation/total-expenditure/expense-line/value/\@value-date
      - 1..1
      - 

    * - 
      - :doc:`narrative </organisation-standard/iati-organisations/iati-organisation/total-expenditure/expense-line/narrative>`
      - The free text name or description of the item being described. This can
        be repeated in multiple languages.
      - 
      - 
      - iati-organisations/iati-organisation/total-expenditure/expense-line/narrative
      - 1..*
      - 

    * - 
      - 
      - 
      - xsd:string
      - 
      - iati-organisations/iati-organisation/total-expenditure/expense-line/narrative/text()
      - 
      - 

    * - 
      - xml:lang
      - A code specifying the language of text in this element. It is recommended that wherever possible only codes from ISO 639-1 are used. If not present, the default language is assumed.
      - 
      - :doc:`/codelists/Language`
      - iati-organisations/iati-organisation/total-expenditure/expense-line/narrative/\@xml:lang
      - 0..1
      - 

    * - :doc:`document-link </organisation-standard/iati-organisations/iati-organisation/document-link>`
      - 
      - A link to an online, publicly accessible web page or document.
      - 
      - 
      - iati-organisations/iati-organisation/document-link
      - 0..*
      - 

    * - 
      - url
      - The target URL of the external document, e.g. "http://www.example.org/doc.odt".
      - xsd:anyURI
      - 
      - iati-organisations/iati-organisation/document-link/\@url
      - 1..1
      - 

    * - 
      - format
      - An IANA code for the MIME type of the document being referenced, e.g. "application/pdf".
      - xsd:string
      - :doc:`/codelists/FileFormat`
      - iati-organisations/iati-organisation/document-link/\@format
      - 1..1
      - 

    * - 
      - :doc:`recipient-country </organisation-standard/iati-organisations/iati-organisation/document-link/recipient-country>`
      - The recipient country that is the focus of the document.
        May be repeated for multiple countries.
      - 
      - 
      - iati-organisations/iati-organisation/document-link/recipient-country
      - 0..*
      - 

    * - 
      - code
      - ISO 3166-1 alpha-2 code for the country.
      - xsd:string
      - :doc:`/codelists/Country`
      - iati-organisations/iati-organisation/document-link/recipient-country/\@code
      - 1..1
      - 

    * - 
      - :doc:`narrative </organisation-standard/iati-organisations/iati-organisation/document-link/recipient-country/narrative>`
      - The free text name or description of the item being described. This can
        be repeated in multiple languages.
      - 
      - 
      - iati-organisations/iati-organisation/document-link/recipient-country/narrative
      - 0..*
      - 

    * - 
      - 
      - 
      - xsd:string
      - 
      - iati-organisations/iati-organisation/document-link/recipient-country/narrative/text()
      - 
      - 

    * - 
      - xml:lang
      - A code specifying the language of text in this element. It is recommended that wherever possible only codes from ISO 639-1 are used. If not present, the default language is assumed.
      - 
      - :doc:`/codelists/Language`
      - iati-organisations/iati-organisation/document-link/recipient-country/narrative/\@xml:lang
      - 0..1
      - 

    * - 
      - :doc:`title </organisation-standard/iati-organisations/iati-organisation/document-link/title>`
      - A short, human-readable title.
      - 
      - 
      - iati-organisations/iati-organisation/document-link/title
      - 1..1
      - 

    * - 
      - :doc:`narrative </organisation-standard/iati-organisations/iati-organisation/document-link/title/narrative>`
      - The free text name or description of the item being described. This can
        be repeated in multiple languages.
      - 
      - 
      - iati-organisations/iati-organisation/document-link/title/narrative
      - 1..*
      - 

    * - 
      - 
      - 
      - xsd:string
      - 
      - iati-organisations/iati-organisation/document-link/title/narrative/text()
      - 
      - 

    * - 
      - xml:lang
      - A code specifying the language of text in this element. It is recommended that wherever possible only codes from ISO 639-1 are used. If not present, the default language is assumed.
      - 
      - :doc:`/codelists/Language`
      - iati-organisations/iati-organisation/document-link/title/narrative/\@xml:lang
      - 0..1
      - 

    * - 
      - :doc:`description </organisation-standard/iati-organisations/iati-organisation/document-link/description>`
      - A description of the document contents, or guidance on where to access the relevant information in the document.
      - 
      - 
      - iati-organisations/iati-organisation/document-link/description
      - 0..1
      - 

    * - 
      - :doc:`narrative </organisation-standard/iati-organisations/iati-organisation/document-link/description/narrative>`
      - The free text name or description of the item being described. This can
        be repeated in multiple languages.
      - 
      - 
      - iati-organisations/iati-organisation/document-link/description/narrative
      - 1..*
      - 

    * - 
      - 
      - 
      - xsd:string
      - 
      - iati-organisations/iati-organisation/document-link/description/narrative/text()
      - 
      - 

    * - 
      - xml:lang
      - A code specifying the language of text in this element. It is recommended that wherever possible only codes from ISO 639-1 are used. If not present, the default language is assumed.
      - 
      - :doc:`/codelists/Language`
      - iati-organisations/iati-organisation/document-link/description/narrative/\@xml:lang
      - 0..1
      - 

    * - 
      - :doc:`category </organisation-standard/iati-organisations/iati-organisation/document-link/category>`
      - IATI Document Category Code
      - 
      - 
      - iati-organisations/iati-organisation/document-link/category
      - 1..*
      - 

    * - 
      - code
      - An IATI code defining the category of the document.
      - xsd:string
      - :doc:`/codelists/DocumentCategory`
      - iati-organisations/iati-organisation/document-link/category/\@code
      - 1..1
      - 

    * - 
      - :doc:`language </organisation-standard/iati-organisations/iati-organisation/document-link/language>`
      - The ISO 639-1 language code in which target document is written, e.g. "en". Can be repeated to describe multi-lingual documents.
      - 
      - 
      - iati-organisations/iati-organisation/document-link/language
      - 0..*
      - 

    * - 
      - code
      - ISO 639-1 language code
      - xsd:string
      - :doc:`/codelists/Language`
      - iati-organisations/iati-organisation/document-link/language/\@code
      - 1..1
      - 

    * - 
      - :doc:`document-date </organisation-standard/iati-organisations/iati-organisation/document-link/document-date>`
      - The date of publication of the document that is being linked to.
      - 
      - 
      - iati-organisations/iati-organisation/document-link/document-date
      - 0..1
      - 

    * - 
      - iso-date
      - 
      - xsd:date
      - 
      - iati-organisations/iati-organisation/document-link/document-date/\@iso-date
      - 1..1
      - 


::

  
        International Aid Transparency Initiative: Organisation-Information Schema
  
        Release 2.03, 2018-02-19
  
        NOTE: the xml.xsd and iati-common.xsd schemas must be in the
        same directory as this one.
  
        This W3C XML Schema defines an XML document type for information
        about an aid organisation, following the standard published at
        http://iatistandard.org
  
        This document type may be extended with additional elements and
        attributes, but they must belong to an explicit XML namespace.
      

.. meta::
  :order: 1
