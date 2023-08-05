Accern for Python
=================
.. image:: https://circleci.com/gh/Accern/accern-python.svg?style=shield&circle-token=4a51eaa89bd79c92bb9df0e48642146ad7091afc
   :target: https://circleci.com/gh/Accern/accern-python


.. snip

A python library to consume Accern Realtime Streaming API, REST API and get
historical data.

Accern primarily serves institutional investors. The majority of our current
clients are quantitative hedge funds. Many small firms are coming to us
because of our flexible and affordable pricing options. Large firms are coming
to us due to our dedicated support, news source customization, and much more.
Aside from hedge funds, our existing clients include pension and endowment
funds, banks, brokerage firms, and more.

Accern library for Python helps user to get fast, flexible data structures from
Accern's Streaming, REST APIs and batch historical data.


Installation
------------

.. code-block:: console

    pip install accern

Getting started
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
