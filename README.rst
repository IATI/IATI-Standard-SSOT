IATI Standard SSOT
==================

.. image:: https://github.com/IATI/IATI-Standard-SSOT/workflows/CI/badge.svg
    :target: https://github.com/IATI/IATI-Standard-SSOT/actions

.. image:: https://requires.io/github/IATI/IATI-Standard-SSOT/requirements.svg?branch=version-2.03
    :target: https://requires.io/github/IATI/IATI-Standard-SSOT/requirements/?branch=version-2.03
    :alt: Requirements Status
.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://github.com/IATI/IATI-Standard-SSOT/blob/version-2.03/LICENSE

Introduction
------------

This is the IATI Standard Single Source of Truth (SSOT). It brings together 5 repos that contain parts of the IATI Standard and related information.

IATI-Schemas, IATI-Rulesets, IATI-Codelists and IATI-Extra-Documentation are included as submodules. 

IATI-Codelists-NonEmbedded is included at build time by gen.sh 

An additional 3 repos, IATI-Developer-Documentation, IATI-Guidance and IATI-Websites are included via combined_gen.sh, however this is no longer in use for the production IATI website. 

Updating the SSOT
-----------------

Once the PR(s) have been merged into the relevant repos:

Check out the repo:::

    git clone https://github.com/IATI/IATI-Standard-SSOT.git

Create a new branch:::

    git checkout -b branch-name

Pull in the git submodules:::

    git submodule init
    git submodule update

Commit & push the updated submodule versions:::

    git commit -a -m "commit message" && git push


Deploying an Updated SSOT to the IATI Website
---------------------------------------------

Go to https://github.com/IATI/IATI-Reference-Generator/ and follow the instructions there
