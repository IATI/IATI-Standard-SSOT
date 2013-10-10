
Page for revison 1.02. See this page for: `revison
1.01 </standard/documentation/1.0/transaction-type>`__, `revison
1.02 </standard/documentation/1.02/transaction-type>`__

Notes
~~~~~

This provides the code for the transaction type. There are seven of
these: C - Commitment, D - Disbursement, E - Expenditure, IF - Incoming
funds, IR - Interest Repayment, LR - Loan Repayment, and R -
Reimbursement.

Example Usage
~~~~~~~~~~~~~

The code should be declared in any usage of this element:

.. code-block:: xml

        <transaction-type code="C"/>

Additionally, a text description of the code can be provided:

.. code-block:: xml

        <transaction-type code="C">Commitment</transaction-type>

Where this text description is in a language that differs from the
default, then this should be declared accordingly:

.. code-block:: xml

        <transaction-type code="C" xml:lang="en">Commitment</transaction-type>

