
Page for revison 1.02. See this page for: `revison
1.02 </standard/documentation/1.02/result>`__, `revison
1.01 </standard/documentation/1.0/result>`__

Example Usage
~~~~~~~~~~~~~

Container element for a result set. The type attribute can be used to
describe whether it is an output, outcome, or impact indicator:

.. code-block:: xml

        <result type="output">
        ....
        </result>

Additionally, a flag to indicate whether the data in this result set is
suitable for aggregation. Boolean. “True” means that the data can be
aggregated. If omitted 'true' is assumed.

.. code-block:: xml

        <result type="output" aggregation-status="false">
        ....
        </result>

