IATI Standard SSOT
==================

.. image:: https://travis-ci.org/IATI/IATI-Standard-SSOT.svg?branch=version-2.03
    :target: https://travis-ci.org/IATI/IATI-Standard-SSOT
.. image:: https://requires.io/github/IATI/IATI-Standard-SSOT/requirements.svg?branch=version-2.03
    :target: https://requires.io/github/IATI/IATI-Standard-SSOT/requirements/?branch=version-2.03
    :alt: Requirements Status
.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://github.com/IATI/IATI-Standard-SSOT/blob/version-2.03/LICENSE

Introduction
------------

This is the main github repository for the IATI Standard Single Source of Truth (SSOT). For more detailed information about the SSOT, please see http://iatistandard.org/developer/ssot/


Building the documentation
==========================

Requirements:

* Git
* Unix based setup (e.g. Linux, Mac OS X) with bash etc.
* Python 2.7
* `python-virtualenv <http://www.virtualenv.org/en/latest/>`_ (recommended)
* gcc
* Development files for libxml and libxslt e.g. libxml2-dev, libxslt-dev


Fetch the source code:

    git clone https://github.com/IATI/IATI-Standard-SSOT.git

Running the initial setup:

    make dev_install

or run each step separately:

    make clean

    make setup
    
    make clone_components
    

Building the documentation
    
    make build_docs

The built documentation is now in ``docs/<language>/_build/dirhtml``


Building the entire site (with full content)

    make build_dev


Running the server

    make run


Editing the documentation
=========================

Make any changes in ``IATI-Extra-Documentation``, as the ``docs`` directory is generated from
this and other sources each time ``make build_docs`` is run.
