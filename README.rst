IATI Standard SSOT
==================

This is the main github repository for the IATI Standard Single Source of Truth (SSOT). For more detailed information about the SSOT, please see https://github.com/IATI/IATI-Standard-SSOT/blob/master/meta-docs/index.rst 

This repository is currently under development, and does not necessarily represent any current or future version of the IATI standard.


Building the documentation
==========================

Requirements:

* Git
* Unix based setup (e.g. Linux, Mac OS X) with bash etc.
* Python 2.7
* `python-virtualenv<http://www.virtualenv.org/en/latest/>`_ (recommended)
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
    virtualenv pyenv

    # Activate the virtual environment if you created one
    # This must repeated each time you open a new shell
    source pyenv/bin/activate

    # Install python requirements
    pip install -r requirements.txt
    
Build the documentation:::

    ./gen.sh

The built documentation is now in ``docs/_build/html`` 


Editing the documentation
=========================

Make any changes in ``IATI-Extra-Documentation``, as the ``docs`` directory is generated from
this and other sources each time ``./gen.sh`` is run. 
