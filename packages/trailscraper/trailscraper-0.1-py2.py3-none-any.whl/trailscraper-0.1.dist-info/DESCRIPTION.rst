TrailScraper
============

A command-line tool to get valuable information out of AWS CloudTrail

Usage
-----

none yet…

Development
-----------

.. code:: bash

    $ ./go setup   # set up venv and dependencies
    $ source ./go enable  # enable venv
    $ ./go         # let's see what we can do here

Troubleshooting
~~~~~~~~~~~~~~~

``Click will abort further execution because Python 3 was configured to use ASCII as encoding for the environment.``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Set these environment variables:

::

    LC_ALL=C.UTF-8
    LANG=C.UTF-8


Changelog
=========

This changelog contains a loose collection of changes in every release
including breaking changes to the API.

The format is based on `Keep a Changelog <http://keepachangelog.com/>`__

0.1.0
-----

*Initial Release*

Added
~~~~~

-  Basic feature to download CloudTrail Logs from S3 for certain
   accounts and timeframe
-  Basic feature to generate IAM Policies from a set of downloaded
   CloudTrail logs


