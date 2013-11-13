IATI Standard SSOT
==================

This repository is currently under development, and does not necessarily represent any current or future version of the IATI standard.


Building the documentation
==========================

Requirements:

* Git
* Unix based setup (e.g. Linux, Mac OS X) with bash etc.
* Python 2.7
* python-virtualenv
* gcc
* Development files for libxml and libxslt e.g. libxml2-dev, libxslt-dev

Fetch the source code:::

    git clone git@github.com:Bjwebb/IATI-Documentation.git

Pull in the git submodules:::
    
    git submodule init
    git submodule update

Set up a virtual environment:

.. code-block:: bash

    # Create a virtual environment
    virtualenv pyenv

    # Activate the virtual environment
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
