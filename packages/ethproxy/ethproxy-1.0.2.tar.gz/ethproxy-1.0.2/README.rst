========
ethproxy
========

.. image:: https://img.shields.io/pypi/v/ethproxy.svg
        :target: https://pypi.python.org/pypi/ethproxy

.. image:: https://img.shields.io/travis/narfman0/ethproxy.svg
        :target: https://travis-ci.org/narfman0/ethproxy

Description
===========

This is Stratum Proxy for Ethereum based pools (RPCv2) using asynchronous networking written in Python Twisted.

*NOTE* This fork is still in development. Some features may be broken. Please report any broken features or issues.

Features
========

* Additional up to 20% increase of earning compared to standard pools
* ETH stratum proxy
* Automatically failover via proxy
* Only one connection to the pool
* Workers get new jobs immediately
* Submit of shares without network delay, it's like solo-mining but with benefits of professional pool
* Central Wallet configuration, miners doesn't need wallet as username
* Support monitoring via email
* Bypass worker_id for detailed statistic and per rig monitoring
* pass submitHashrate to pool
* Fast deployment through Docker

How it works
============

Example::

    rig1 ---- rig2 ---- rig3
                |
            stratum proxy (ethproxy)
            |          |
        Pool A      Pool B
       (Active)   (Failover)

Configuration
=============

* ethproxy/settings.py contains settings, all of which can be set via
  environment variables

Command line start
------------------

Recommended farm-recheck to use with stratum-proxy is 200::

    ./ethminer --farm-recheck 200 -G -F http://127.0.0.1:8080/rig1

Proxy working check
-------------------

* To check that proxy works open in browser http://127.0.0.1:8080/ (or your changed ip and port from config)
* If you see "Ethereum stratum proxy" and some infos about connections.
* If not then mostly case that you have application running on this port, at example Antivirus.

Requirements
============

eth-proxy is built in python. The requirements for running the software are below.

* Python 2.7+, 3.6+
* python-twisted

Installation
============

[Linux]
-------

With python (and pip) installed, use pip to install::

    pip install ethproxy

Start proxy with::

    ethproxy

[Windows]
---------

This are old directions, might be easier to pip install but twisted has native
dependencies so good luck with that :)

Download compiled version
https://github.com/Atrides/eth-proxy/releases

Or use python source code

1) Download Python Version 2.7.14 (or greater) for Windows
https://www.python.org/downloads/

2) Modify PATH variable (how-to http://www.java.com/en/download/help/path.xml) and add
   C:\Python27;C:\Python27\Scripts;

3) Install python setuptools
https://pypi.python.org/pypi/setuptools/#windows-7-or-graphical-install

4) Install Python-Twisted
https://pypi.python.org/pypi/Twisted/15.4.0
File Twisted-15.4.0.win32-py2.7.msi (32bit) or Twisted-15.4.0.win-amd64-py2.7.msi (64bit)

5) Install zope.interface, in console run::

    pip install -U zope.interface

6) Install PyWin32 v2.7
pywin32-219.win32-py2.7.exe or pywin32-219.win-amd64-py2.7.exe
http://sourceforge.net/projects/pywin32/files/pywin32/

7) Download eth-proxy. Extract eth-proxy.zip. Change settings and start with command::

    python xmr-proxy.py

[Docker]
--------

Use this generic command line (conf references likely need to be updated with package refactor)::

    docker run -d -v CONFIG:/app/eth-proxy.conf -p PORT:8080 --name eth-proxy fmauneko/eth-proxy

Exemple::

    docker run -d -v /srv/eth-proxy/eth-proxy.conf:/app/eth-proxy.conf -p 8080:8080 --name eth-proxy fmauneko/eth-proxy

TODO
====

* lint and make python more happy

Credits
=======

* Atrides work
* Original version by Slush0 (original stratum code)
* More Features added by GeneralFault, Wadee Womersley and Moopless

License
=======

Please see LICENSE for further info
