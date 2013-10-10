
.. raw:: mediawiki

   {{for revison 1.02}}

Example Usage
^^^^^^^^^^^^^

The code should be declared in any usage of this element:

``
    <disbursement-channel code="1"/>
``

Additionally, a text description of the code can be provided:

``
    <disbursement-channel code="1">Cash to treasury</disbursement-channel-code>
``

Where this text description is in a language that differs from the
default, then this should be declared accordingly:

``
<disbursement-channel code="1" xml:lang="en">Cash to treasury</disbursement-channel-code>
 ``
