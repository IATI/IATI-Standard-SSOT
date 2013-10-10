

Example Usage
~~~~~~~~~~~~~

Example from DfID of an activity with one each of the four activity date
types

.. code-block:: xml

    <activity-date type="start-planned">2006-04-01</activity-date>
    <activity-date type="start-actual">2007-01-01</activity-date>
    <activity-date type="end-planned">2009-12-31</activity-date>
    <activity-date type="end-actual">2009-12-31</activity-date>

In some cases, not all dates are known, depending on the status of the
activity:

.. code-block:: xml

        <activity-date type="start-actual" iso-date="2010-03-01"/>
        <activity-date type="end-planned" iso-date="2013-03-30"/>
