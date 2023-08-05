|Show Logo|

=================
ProsperDatareader
=================

.. inclusion-marker-do-not-remove

|Build Status| |Coverage Status| |PyPI Badge| |Docs|

Helper libraries for reading/parsing common data used in Prosper tools

===============
Getting Started
===============

	``pip install prosperdatareader``

Testing
-------

	``python setup.py test``

Notes
-----

- Only supporting >=3.5 Python

===============
Supported Feeds
===============

**Utils**: General utilities for additional insights 

- `vader_sentiment`_: grade text blobs with NLTK

**Stocks**: meant as companion APIs to `pandas-datareader`_

- Company News Feeds: Google, Robinhood
- Market News Feed: Google
- Price Quote: Robinhood

**Coins**: helper libraries for fetching info on crypto currencies (via `hitBTC`_)

- Ticker Info: get info about coin<->currency conversion metadata
- Price Quote: get latest OHLC data for given coin 
- Order Book: view current orders

.. _pandas-datareader: https://pandas-datareader.readthedocs.io/en/latest/index.html
.. _vader_sentiment: http://www.nltk.org/api/nltk.sentiment.html#module-nltk.sentiment.vader
.. _hitBTC: https://hitbtc.com

.. |Show Logo| image:: http://dl.eveprosper.com/podcast/logo-colour-17_sm2.png
   :target: http://eveprosper.com
.. |Build Status| image:: https://travis-ci.org/EVEprosper/ProsperDatareader.svg?branch=master
   :target: https://travis-ci.org/EVEprosper/ProsperDatareader
.. |Coverage Status| image:: https://coveralls.io/repos/github/EVEprosper/ProsperDatareader/badge.svg?branch=master
   :target: https://coveralls.io/github/EVEprosper/ProsperDatareader?branch=master
.. |PyPI Badge| image:: https://badge.fury.io/py/ProsperDatareader.svg
   :target: https://badge.fury.io/py/ProsperDatareader
.. |Docs| image:: https://readthedocs.org/projects/prosperdatareader/badge/?version=latest
   :target: http://prosperdatareader.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status
