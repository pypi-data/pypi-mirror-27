ethermine-monitor
=================

.. image:: https://badge.fury.io/py/ethermine-monitor.png
    :target: https://badge.fury.io/py/ethermine-monitor

.. image:: https://travis-ci.org/narfman0/ethermine-monitor.png?branch=master
    :target: https://travis-ci.org/narfman0/ethermine-monitor

Monitor workers on ethermine, send email and other signals if there is an issue

Usage
-----

Intended to be used with zappa. Take a look at zappa_settings.json, and populate:

`WORKER_ID` - the wallet id where your ethereum should be stashed

`SENDER` - Email sender address, verified by amazon SES

`RECIPIENT` - Email recipient address

License
-------

Copyright (c) 2017 Jon Robison

See included LICENSE for licensing information
