TrailScraper
============

|PyPi Release| |Build Status|

A command-line tool to get valuable information out of AWS CloudTrail

Installation
------------

.. code:: bash

    # install custom dependeny since PR cloudtools/awacs#87 isn't merged yet
    $ pip install 'http://github.com/flosell/awacs/tarball/add_equality_and_hashes#egg=awacs-0.7.2'
    # install trailscraper
    $ pip install trailscraper

Usage
-----

.. code:: bash

    # Download some logs
    $ trailscraper download --bucket <some-bucket> \
                            --account-id <some account id> \
                            --region <some region to look at> \ 
                            --past-days <number of past days to look at> \
    # Generate an IAM Policy  
    $ trailscraper generate
    {
        "Statement": [
            {
                "Action": [
                    "ec2:DescribeInstances",
                    "ec2:DescribeSecurityGroups",
                    "ec2:DescribeSubnets",
                    "ec2:DescribeVolumes",
                    "ec2:DescribeVpcs",
                ],
                "Effect": "Allow",
                "Resource": [
                    "*"
                ]
            },
            {
                "Action": [
                    "sts:AssumeRole"
                ],
                "Effect": "Allow",
                "Resource": [
                    "arn:aws:iam::1111111111:role/someRole"
                ]
            }
        ],
        "Version": "2012-10-17"
    } 

Development
-----------

.. code:: bash

    $ ./go setup   # set up venv, dependencies and tools
    $ ./go test    # run some tests
    $ ./go check   # run some style checks
    $ ./go         # let's see what we can do here

Troubleshooting
~~~~~~~~~~~~~~~

Click thinks you are in an ASCII environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``Click will abort further execution because Python 3 was configured to use ASCII as encoding for the environment.``

Set these environment variables:

::

    LC_ALL=C.UTF-8
    LANG=C.UTF-8

.. |PyPi Release| image:: https://img.shields.io/pypi/v/trailscraper.svg
   :target: https://pypi.python.org/pypi/trailscraper
.. |Build Status| image:: https://travis-ci.org/flosell/trailscraper.svg?branch=master
   :target: https://travis-ci.org/flosell/trailscraper


Changelog
=========

This changelog contains a loose collection of changes in every release
including breaking changes to the API.

The format is based on `Keep a Changelog <http://keepachangelog.com/>`__

0.2.0
-----

Added
~~~~~

-  Basic filtering for role-arns when generating policy (#3)

.. section-1:

0.1.0
-----

*Initial Release*

.. added-1:

Added
~~~~~

-  Basic feature to download CloudTrail Logs from S3 for certain
   accounts and timeframe
-  Basic feature to generate IAM Policies from a set of downloaded
   CloudTrail logs


