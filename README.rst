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

    ./gen.sh

The built documentation is now in ``docs/<language>/_build/dirhtml``


Editing the documentation
=========================

Make any changes in ``IATI-Extra-Documentation``, as the ``docs`` directory is generated from
this and other sources each time ``./gen.sh`` is run.


Building a website that also includes additonal guidance
========================================================

There is additonal guidance in the following git repositories:

* https://github.com/IATI/IATI-Guidance
* https://github.com/IATI/IATI-Developer-Documentation/

These are not versioned with the standard, so are not included in this repository (`IATI-Standard-SSOT <https://github.com/IATI/IATI-Standard-SSOT>`__) or its submodules.

To generate a copy of the website with these extra repositories included, run:

.. code-block:: bash

   # If you have not done already create the docs directory as a git repository
   # (more info below)
   mkdir docs
   cd docs
   git init
   cd ..
   # Actually run the generate script
   ./combined_gen.sh

This generates the website in the ``docs`` directory, but then copies it to ``docs-copy`` at the end, so that a webserver can be pointed to ``docs-copy/en/_build/dirhtml`` and not be interrupted when the site is being rebuilt.

The ``docs`` directory should be a git repository in order to support adding the "Last updated" line to the bottom of the page. We build the live and dev websites in different directories so that the last updated date corresponds to when the site was actually changed, not when the relevant commit was added to the source git respository.


Generating a local version with the IATI theme
==============================================

A local version of the website (with the full IATI theme) can be generated after cloning the theme files and setting up the required symlinks for Sphinx to follow when generating the HTML files.

.. code-block:: bash

   # Clone the repository containing the IATI theme at the same level where you cloned IATI-Standard-SSOT
   git clone https://github.com/IATI/IATI-Websites.git IATI-Websites

   # Set-up symlinks to the template file/folders
   # for the symlinks to work, you'll have to be inside the IATI-Extra-Documentation folder cloned inside IATI-Standard-SSOT
   cd IATI-Extra-Documentation/en
   ln -s ../../../IATI-Websites/iatistandard/_templates/ ./
   ln -s ../../../IATI-Websites/iatistandard/_static/ ./
   ln -s ../../../IATI-Websites/iatistandard/_templates/layout_dev.html ./_templates/layout.html

   # Generate a version of the documentation
   cd ../../
   ./combined_gen.sh

   # The documentation HTML files are stored in the `docs-copy/en/_build/dirhtml` folder
   # You can navigate around your generated version of the site using a Python HTTP webserver
   cd docs-copy/en/_build/dirhtml
   python3 -m http.server
   # View the site in a browser at http://0.0.0.0:8000/
