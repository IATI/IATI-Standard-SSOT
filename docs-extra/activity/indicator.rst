
Page for revison 1.02. See this page for: `revison
1.02 </standard/documentation/1.02/indicator>`__, `revison
1.01 </standard/documentation/1.0/indicator>`__

Example Usage
~~~~~~~~~~~~~

The Indicator element is contained within a result set, and also
contains other elements.

The type of measurement for the indicator value e.g. unit, percentage,
NDP can be described:

.. code-block:: xml

    <result>
    ....
        <indicator measure="NDP">
        ....
        </indicator>
    .....
    </result>    

Additionally, a flag to indicate whether the data in this indicator
improves from small to large (ascending = “true”), or whether it is
reversed and improves from large to small (ascending=“false”). Boolean.
If omitted 'true' is assumed.

.. code-block:: xml

    <result>
    ....
        <indicator measure="NDP" ascending="true">
        ....
        </indicator>
    .....
    </result>    

