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
* Python 3.x
* gcc
* Development files for libxml and libxslt e.g. libxml2-dev, libxslt-dev

Fetch the source code:::

    git clone https://github.com/IATI/IATI-Standard-SSOT.git

Pull in the git submodules:::

    git submodule init
    git submodule update

Set up a virtual environment:

.. code-block:: bash

    # Create a virtual environment (recommended)
    python3 -m venv pyenv

    # Activate the virtual environment if you created one
    # This must repeated each time you open a new shell
    source pyenv/bin/activate

    # Install python requirements
    pip install -r requirements.txt

Build the documentation:::

    ./gen_rst.sh

The built documentation is now in ``outputs/<language>/_build/dirhtml`` as json files
