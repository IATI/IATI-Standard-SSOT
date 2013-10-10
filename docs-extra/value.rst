
.. raw:: mediawiki

   {{for revison 1.02}}

Notes
^^^^^

The monetary value of the transaction in the specified currency –
negative for repayments or reduced/cancelled commitments.

Example Usage
^^^^^^^^^^^^^

The total value for the specified period should be declared as a
positive integer:

``
<value value-date="2010-10-01">700000</value>
``

A date of value for currency conversions should also be provided as
yyyy-mm-dd:

``
<value value-date="2010-10-01">700000</value>
``

The ISO 4217 code for the currency in which the project is denominated
should be declared, only if different to default currency

``
<value currency="GBP" value-date="2010-10-01">700000</value>
``

Changelog
^^^^^^^^^

1.03
~~~~

Currency values are now allowed to be declared as decimals instead of
integers.
