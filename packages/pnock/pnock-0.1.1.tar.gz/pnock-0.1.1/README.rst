=====================================
Pnock - knocking ports in pure python
=====================================

.. image:: https://img.shields.io/pypi/v/pnock.svg
   :target: https://pypi.python.org/pypi/pnock
   :alt: PyPI Version

.. image:: https://img.shields.io/pypi/pyversions/pnock.svg
   :target: https://pypi.python.org/pypi/pnock
   :alt: Supported Python Versions

.. image:: https://img.shields.io/badge/wheel-yes-brightgreen.svg
   :target: https://pypi.python.org/pypi/pnock
   :alt: Wheel Status

Finds which hosts are running a server on a given port on your local network, in just a second.

This package can be used as a library, or as a CLI tool

Requirements
============

* Python 2.7 or Python 3.4+

Install
=======

    pip install pnock

CLI Usage
=========
    usage: pnock [-h] [-i IFACE_IP] [-t TIMEOUT] port

    LAN Port knocker

    positional arguments:
      port                  The port to knock on

    optional arguments:
      -h, --help            show this help message and exit
      -i IFACE_IP, --interface IFACE_IP
                            The interface to scan the LAN of
      -t TIMEOUT, --timeout TIMEOUT
                            The timeout to wait for replies on the knocks
