
.. raw:: mediawiki

   {{for revison 1.02}}

Notes
^^^^^

This provides the code for the transaction type. There are seven of
these: C - Commitment, D - Disbursement, E - Expenditure, IF - Incoming
funds, IR - Interest Repayment, LR - Loan Repayment, and R -
Reimbursement.

Example Usage
^^^^^^^^^^^^^

The code should be declared in any usage of this element:

``
    <transaction-type code="C"/>
``

Additionally, a text description of the code can be provided:

``
    <transaction-type code="C">Commitment</transaction-type>
``

Where this text description is in a language that differs from the
default, then this should be declared accordingly:

``
    <transaction-type code="C" xml:lang="en">Commitment</transaction-type>
``
