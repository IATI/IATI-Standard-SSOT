

Example Usage
~~~~~~~~~~~~~

.. code-block:: xml

    <crs-add>
      <aidtype-flag code="XX" significance="true">XXX</aidtype-flag>
      <loan-terms rate-1="4" rate-2="3">
          <repayment-type code="1">Equal Principal Payments (EPP)</repayment-type>
          <repayment-plan code="4">Quarterly</repayment-plan>
          <commitment-date iso-date="2013-09-01"/>
          <repayment-first-date iso-date="2014-01-01"/>
          <repayment-final-date iso-date="2020-12-31"/>
      </loan-terms>
      <loan-status year="2014" currency="GBP" value-date="2013-05-24">
          <interest-received>200000</interest-received>
          <principal-outstanding>1500000</principal-outstanding>
          <principal-arrears>0</principal-arrears>
          <interest-arrears>0</interest-arrears>
      </loan-status>
    </crs-add>

Changelog
~~~~~~~~~

1.03
^^^^

| New in 1.03
|  Added the optional crs-add element and its child elements
