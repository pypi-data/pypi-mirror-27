CheckSpot
=========

A simple CLI tool to check the spot prices of AWS instances. Available
for Python3 only

Installation
------------

To install, use pip such that

.. code:: bash

    pip3 install --user checkspot

Setup
-----

Since ``checkspot`` uses boto3, you’ll have to setup the same way. You
can view the `docs
here <http://boto3.readthedocs.io/en/latest/guide/quickstart.html>`__

Usage
-----

To use, run

.. code:: bash

    checkspot

and a series of questions will be prompted.

Repeatable Usage
~~~~~~~~~~~~~~~~

If you don’t want to enter the CLI every time, you can run the CLI with
the options

::

    checkspot --InstanceType=t2.micro --ProductDescription=Linux/UNIX --StartTime=$(date -d "3 days ago" +"%Y-%m-%d") --EndTime=$(date +"%Y-%m-%d")

Version
-------

-  **1.0.0**

   -  First publish
