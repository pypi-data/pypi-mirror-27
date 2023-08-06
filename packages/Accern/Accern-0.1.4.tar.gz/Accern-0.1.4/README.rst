Accern for Python
=================

.. image:: https://raw.githubusercontent.com/Accern/accern-python/yz-docs/docs/_static/accern.png
  :target: _static/accern.png

|pypi| |circleci| |sphinx|

.. snig

A python library to consume Accern Realtime Streaming API, REST API and get
historical data.

Overview
--------

Accern is a fast-growing NYC startup that is disrupting the way quantitative
hedge funds can gain a competitive advantage using news and social media data.
It currently has the world’s largest financial news coverage, covering over
1 billion public news websites, blogs, financial documents, and social media
websites. Furthermore, Accern derives proprietary analytics from each news
stories to help quantitative hedge funds make accurate trading decisions.

Accern consolidates multiple news data feeds into one to help both small and
large funds reduce costs drastically. With Accern proprietary data filters, it
is able to deliver relevant articles to clients with a 99 percent accuracy rate.
Accern’s delivery mechanism is a RESTful API where it delivers derived analytics
from news articles, including the original article URLs so quantitative hedge
funds can derive their own analytics in-house from the relevant articles.

Accern library for Python helps user to get fast, flexible data structures from
Accern's Streaming, REST APIs and batch historical data.


Install
------------

.. code-block:: console

    pip install accern

Quick Start
---------------

1. Contact `support@accern.com`. and inquire an Accern API token.

2. To quickly start using Accern ``Stream API``, simply create ``Stream`` and  ``StreamListener`` clients:

.. code-block:: python

    from accern import Stream, StreamListener
    token = 'YOUR TOKEN'
    myStreamListener = StreamListener()
    stream = Stream(myStreamListener, token)

3. Accern ``Historical API`` will be available in the future releases.

.. snap

For more information see the `full documentation
<https://accern-python.readthedocs.io>`_ on Read The Docs.


.. |circleci| image:: https://circleci.com/gh/Accern/accern-python.svg?style=shield&circle-token=4a51eaa89bd79c92bb9df0e48642146ad7091afc
   :target: https://circleci.com/gh/Accern/accern-python

.. |sphinx| image:: https://readthedocs.org/projects/accern-python/badge/?version=latest
   :target: http://accern-python.readthedocs.io/en/latest/?badge=latest

.. |pypi| image:: https://badge.fury.io/py/Accern.svg
   :target: https://badge.fury.io/py/Accern
