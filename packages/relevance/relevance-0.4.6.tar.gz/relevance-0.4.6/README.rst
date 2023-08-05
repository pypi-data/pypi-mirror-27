Relevance: Full-stack search engine
###################################

Relevance is a software suite that aims to address the common and recurring problem
of ingesting content, delivering it, searching it with relevant results, analyzing
its usage by the end-users, acting on the analytic data to provide the best results
possible.

Its primary goals are rapid deployment, extensibility and ease of use.

This software is still under heavy development, and is available for preview.
Contributions are welcome.

.. contents::

.. section-numbering::

Features
========

Current features
----------------

- Federated search across ElasticSearch indices
- Simple configuration
- Simple query language
- Simple query API
- Command line tools
- Mapping API

Upcoming features
-----------------

- Ingestion API
- Crawler integration
- NLP integration

Planned features
----------------

- Security layer
- Configuration API
- Query extensions
- MySQL support
- Postgres support
- Query learning
- Analytics
- SQLite support

Installation
============

The fastest way to install is to retrieve the release tarball using ``git``, and
install using ``pip``:

.. code-block:: bash

    # Make sure we have an up-to-date version of pip and setuptools:
    $ pip install --upgrade pip setuptools
    $ pip install relevance

Requirements
------------

Currently, a running instance of ElasticSearch 2.x is required.

Python version
--------------

Although Python 3+ should work, all development is done on Python 3.6.2.
As such, only 3.6 and newer is currently officially supported.

Usage
=====

First, create a your configuration files:

.. code-block:: bash

    $ cp /etc/search.yml-example /etc/search.yml

Then start the server:

.. code-block:: bash

    $ python -m relevance.search.service

Then query away:

.. code-block:: bash

    $ curl -XGET 'http://localhost:55345/myEngine?q="toast"'

The query language is simple and reminiscent of Python expressions:

.. code-block::

    ("term1" or "term2") and str_facet=="value" and interval_facet>10 and other==None

The simple query language support additional options:

.. code-block::

    "search expr" with slice(10, 10) with sort(date, desc) with facet(popularity, author)

You can also limit search to specific document types:

.. code-block::

    "search" or "term" with type(tweet, article)

The options, query terms and facets can be mixed and matched.

You can fetch the document types for a specific instance:

.. code-block:: bash

    $ curl -XGET 'http://localhost:55345/myEngine/mapping'

...and you can describe the mapping for that document type:

.. code-block:: bash

    $ curl -XGET 'http://localhost:55345/myEngine/mapping/tweet'

Documentation
=============

To build the documentation, from the source repository, run:

.. code-block:: bash

    $ ./setup.py build_apidoc
    $ ./setup.py build_sphinx

The documentation will be generated in the `build/docs/` directory.

Contributing
============

Contributions are always welcome. If you want to contribute:

- Fork the project
- Test your code (see below)
- Push your code
- Submit a pull request

Testing
-------

Contributions must pass both the tests and styling guidelines. Before submitting a patch,
make sure you run:

.. code-block:: bash

    $ ./setup.py test validate

About the project
=================

Change log
----------

See `CHANGELOG <https://bitbucket.org/overridelogic/relevance-ce/raw/master/CHANGELOG.rst>`_.


Licence
-------

MIT License: see `LICENSE <https://bitbucket.org/overridelogic/relevance-ce/raw/master/LICENSE>`_.


Authors
-------

**Francis Lacroix** `@netcoder1` created Relevance while at **OverrideLogic**.
