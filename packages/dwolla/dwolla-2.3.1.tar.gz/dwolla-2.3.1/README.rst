About Dwolla
============

Dwolla is a software platform that makes it easy to move money between
banks. When using Dwolla APIs your software platform can move money
between any 2 bank accounts, or network members, with no per transaction
fees.

Our software platform is compatibale with all banks in the United
States. The developer documents are designed to support our development
partners who are building on top of Dwolla’s branded platform (v1) or
our white labeled infrastructure (v2).

The Dwolla API developer portal lives here:
https://developers.dwolla.com/

Our API portal is available on GitHub here:
https://github.com/Dwolla/developer-portal

Our v1 API documentation is available here: https://docs.dwolla.com/

Our v2 API documentation is available here: https://docsv2.dwolla.com/

dwolla-python
=============

`|Join the chat at https://gitter.im/Dwolla/dwolla-python| <https://gitter.im/Dwolla/dwolla-python?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge>`_

`|Build Status| <https://travis-ci.org/Dwolla/dwolla-python>`_

The new and improved Dwolla library based off of the Python ``requests`` client. ``dwolla-python`` includes support for all API endpoints, and is the new library officially supported by Dwolla.

Version
-------

2.3.1

Installation
------------

``dwolla-python`` is available on `PyPi <https://pypi.python.org/pypi/dwolla>`_, and therefore can be installed automagically via `pip <https://pip.pypa.io/en/latest/installing.html>`_.

**The Python ``requests`` library is required for ``dwolla-python`` to operate. It is included as a dependency on this package if your environment does not already have it.**

*To install via pip:*

::

    pip install dwolla

*To add to ``requirements.txt`` and make this a permanent dependency of your package:*

``requirements.txt YourApp SomeLibrary==1.2.3 dwolla>=2.0.0`` ``pip install -r requirements.txt``

*To install directly from source:* ``git clone https://github.com/Dwolla/dwolla-python && cd dwolla-python && python setup.py install``

Quickstart
----------

``dwolla-python`` makes it easy for developers to hit the ground running with our API. Before attempting the following, you should ideally create `an application key and secret <https://www.dwolla.com/applications>`_.

-  Change settings in ``constants.py`` on-the-fly by doing ``from dwolla import constants``, ``constants.some_setting = some_value``.
-  ``from dwolla import module`` where ``module`` is either ``accounts``, ``checkouts``, ``contacts``, ``fundingsources``, ``masspay``, ``oauth``, ``request``, or ``transactions``, or ``from dwolla import *`` to import all.

Sample Code
~~~~~~~~~~~

``dwolla-python`` allows you to import only the modules you need.

*For this example, we will get information about a Dwolla ID.*

::

    from dwolla import accounts

    print accounts.basic('812-121-7199')

or
^^

``dwolla-python`` also allows you to import the entire library to access everything at once.

*For this example, we will get information about a Dwolla ID, as well as request 5.00 from that same ID.*

::

    from dwolla import *

    # Get information about the ID

    print accounts.basic('812-121-7199')

    # Request $5.00 from that ID

    print request.create('812-121-7199', 5.00)

Configuration and Use
~~~~~~~~~~~~~~~~~~~~~

Whenever you change settings, they will only be partially applied. This means that settings in ``constants.py`` will remain until they are changed. You can do so on-the-fly or by editing the file.

Default Settings
^^^^^^^^^^^^^^^^

::

    client_id = 'YOUR ID HERE'
    client_secret = 'YOUR SECRET HERE'
    pin = 1234

    oauth_scope = 'Send|Transactions|Balance|Request|Contacts|AccountInfoFull|Funding|ManageAccount'
    access_token = 'OAUTH TOKENS GO HERE'

    # Hostnames, endpoints
    production_host = 'https://www.dwolla.com/'
    sandbox_host = 'https://uat.dwolla.com/'
    default_postfix = 'oauth/rest'

    # Client behavior
    sandbox = True
    debug = True
    host = None
    rest_timeout = 15
    proxy = False

Proxies
^^^^^^^

``dwolla-python`` also supports proxies. In order to set proxies, you must assign a python dictionary to the proxy constant in the following format:

::

    proxy = {
        'http': 'http://someproxy:someport',
        'https': 'https://anotherproxy:anotherport'
    }

Changing Settings
^^^^^^^^^^^^^^^^^

In order to use the library, you must use your own ``client_id``, ``client_secret``, or ``access_token``. It is generally recommended to modify ``constants`` as shown below, but client control flags also expose this functionality.

::

    # Import everything from the dwolla package
    from dwolla import *

    # Configure the library (change these)
    constants.sandbox=False

    constants.client_id = "zbDwIC0dWCVU7cQtfvGwVwVjvxwQfjaTgkVi+FZOmKqPBzK5JG"
    constants.client_secret = "ckmgwJz9h/fZ09unyXxpupCyrmAMe0bnUiMHF/0+SDaR9RHe99"
    constants.access_token = "aK6DdCVlIsR1hKvTbp8VCwnvci8cwaTLlW9edtbHJVmKoopnoe"


    # Example 1: Get basic information for a user via
    # their Dwolla ID.

    print accounts.basic('812-202-3784')

Specifying additional parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For the API
^^^^^^^^^^^

As of version ``2.2.0``, you are no longer required to pass in additional API parameters in a ``params={...}`` dictionary. You can just simply specify the name of the parameter and its value as in the example below.

Example; Fetch a user's contacts, limit results to 5
''''''''''''''''''''''''''''''''''''''''''''''''''''

``python def get(**kwargs):`` \`\`\`python from dwolla import contacts

contacts.get(limit=5) \`\`\`

**NOTE**: If a ``params={...}`` dictionary is passed, it will be used instead of any additional ``**kwargs`` parameters. This excludes the client control flags noted in the next session. This is done to preserve function calls made to versions prior to ``2.2.0``. The ``params`` parameter behavior will be deprecated as of ``3.x`` releases.

Client Control Flags
^^^^^^^^^^^^^^^^^^^^

``dwolla-python`` supports the following client control flags. They override any applicable settings in the ``constants`` module for the call which they are present in. They do not get sent to the Dwolla API and are popped out of ``**kwargs``.

-  ``dwollaparse``

   -  *Parses the API response obtained from the Dwolla API and returns data to the user.*
   -  Default: ``dwolla``
   -  Acceptable Values: ``raw`` (JSON-ify'd string), ``dict`` (Dictionary/Parsed JSON data), ``dwolla`` (an extension of ``default``, where the contents of the ``Response`` key are returned and the rest disposed).

-  ``client_id``

   -  *Overrides the ``client_id`` set in ``constants`` for the call which it is present in.*
   -  Acceptable Values: (any valid client\_id)

-  ``client_secret``

   -  *Overrides the ``client_secret`` set in ``constants`` for the call which it is present in.*
   -  Acceptable Values: (any valid client\_secret)

-  ``alternate_token``

   -  *Overrides the ``access_token`` set in ``constants`` for the call which it is present in.*
   -  Acceptable Values: (any valid OAuth token)

-  ``alternate_pin``

   -  *Overrides the ``pin`` set in ``constants`` for the call which it is present in.*
   -  Acceptable Values: (any valid PIN)

Example; Fetch a user's contacts, limit results to 5, provide alternate OAuth token.
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

``python def get(**kwargs):`` \`\`\`python from dwolla import contacts

contacts.get(limit=5, alternate\_token="Some alternate token.") \`\`\`

--------------

There are 9 quick-start files which will walk you through working with ``dwolla-python``'s classes/endpoint groupings.

-  ``changeSettings.py``: Instantiate library with custom settings.
-  ``accounts.py``: Retrieve account information, such as balance.
-  ``checkouts.py``: Offsite-gateway endpoints, server-to-server checkout example.
-  ``contacts.py``: Retrieve/sort through user contacts.
-  ``fundingsources.py``: Modify and get information with regards to funding sources.
-  ``masspay.py``: Create and retrieve jobs/data regarding MassPay jobs.
-  ``oauth.py``: Examples on retrieving OAuth access/refresh token pairs.
-  ``request.py``: Create and retrieve money requests/information regarding money requests.
-  ``transactions.py``: Send money, get transaction info by ID, etc.

Structure
---------

``dwolla-python`` is a conglomerate of multiple modules; each module in the ``dwolla/`` directory is named after a the endpoints that it covers (`similar to Dwolla's developer documentation <https://developers.dwolla.com/dev/docs>`_).

Endpoint Modules
~~~~~~~~~~~~~~~~

Each endpoint module depends on ``Rest()`` in ``rest.py`` to fulfill ``GET``, ``DELETE``, ``POST``, and ``PUT`` requests.

-  ``accounts.py``:
-  ``basic()``: Retrieves basic account information
-  ``full()``: Retrieve full account information
-  ``balance()``: Get user balance
-  ``nearby()``: Get nearby users
-  ``autowithdrawalstatus()``: Get auto-withdrawal status
-  ``toggleautowithdrawalstatus()``: Toggle auto-withdrawal
-  ``checkouts.py``:
-  ``create()``: Creates a checkout session.
-  ``get()``: Gets status of existing checkout session.
-  ``complete()``: Completes a checkout session.
-  ``verify()``: Verifies a checkout session.
-  ``contacts.py``:
-  ``get()``: Retrieve a user's contacts.
-  ``nearby()``: Get spots near a location.
-  ``fundingsources.py``:
-  ``info()``: Retrieve information regarding a funding source via ID.
-  ``get()``: List all funding sources.
-  ``add()``: Add a funding source.
-  ``verify()``: Verify a funding source.
-  ``withdraw()``: Withdraw from Dwolla into funding source.
-  ``deposit()``: Deposit to Dwolla from funding source.
-  ``masspay.py``:
-  ``create()``: Creates a MassPay job.
-  ``getjob()``: Gets a MassPay job.
-  ``getjobitems()``: Gets all items for a specific job.
-  ``getitem()``: Gets an item from a specific job.
-  ``listjobs()``: Lists all MassPay jobs.
-  ``oauth.py``:
-  ``genauthurl()``: Generates OAuth permission link URL
-  ``get()``: Retrieves OAuth + Refresh token pair from Dwolla servers.
-  ``refresh()``: Retrieves OAuth + Refresh pair with refresh token.
-  ``catalog()``: Returns a "catalog" of endpoints that are available for use with the current/passed OAuth token.
-  ``request.py``:
-  ``create()``: Request money from user.
-  ``get()``: Lists all pending money requests.
-  ``info()``: Retrieves info for a pending money request.
-  ``cancel()``: Cancels a money request.
-  ``fulfill()``: Fulfills a money request.
-  ``transactions.py``:
-  ``send()``: Sends money
-  ``refund()``: Refunds money
-  ``get()``: Lists transactions for user
-  ``info()``: Get information for transaction by ID.
-  ``stats()``: Get transaction statistics for current user.
-  ``schedule()``: Schedule a transaction for a later date.
-  ``scheduled()``: Get all scheduled transactions.
-  ``scheduledbyid()``: Get a scheduled transaction by its ID.
-  ``editscheduledbyid()``: Edit scheduled transaction by its ID.
-  ``deletescheduledbyid()``: Delete a scheduled transaction by its ID.
-  ``deleteallscheduled()``: Delete all scheduled transactions.

Unit Testing
------------

``dwolla-python`` uses `unittest <https://docs.python.org/2/library/unittest.html>`_ for unit testing. Integration testing is planned sometime in the future.

To run the tests, install ``dwolla-python`` as per the aforementioned instructions and run:

::

    cd location/of/the/library
    pip install unittest
    python -m unittest discover tests/

README
------

In order for the library's README file to display nicely on PyPi, we must use the ``*.rst`` file format. When making changes to this README file, please `use this tool <http://johnmacfarlane.net/pandoc/try/>`_ to convert the ``*.md`` file to ``*.rst``, and make sure to keep both files updated.

Changelog
---------

2.3.1 \* Fix bug that prevented a code from being exchanged for a token.

2.3.0 \* Pass authorization token through headers

2.2.2 \* Fix to pass unit tests for python3

2.2.1 \* Support for Google App Engine added (thanks, @gae123)!

2.2.0 \* **Potentially breaking changes!** \* Additional parameters are now passed in via ``**kwargs`` for both API and client control. \* API responses can now be specified in *any* endpoint using the ``dwollaparse`` flag. Supported responses are ``raw``, ``dict``, and ``dwolla``. \* ``customSettings.py`` renamed to ``changeSettings.py`` as it is more appropriate for the file's contents.

2.1.2 \* Merged bugfix for exception as ``e.message`` has been deprecated (thanks, @ka7eh)! \* Added ``_decimal_default`` function as default for ``json.dumps`` serialization. \* Whenever ``json.loads`` is called, ``int`` and ``float`` types will now be returned as ``Decimal``. \* Exposed ``dwollaparse`` option in ``constants`` module for greater granularity. \* Added two new unit tests for ``PUT`` and ``DELETE`` HTTP calls to ``requests``.

2.1.1 \* Small packaging error damaged v2.1.1, re-release of 2.1.0

2.1.0 \* Added ``verified_account`` parameter to OAuth authorization URL function.

2.0.9 \* Added ``/oauth/rest/catalog`` endpoint as ``oauth.catalog()`` with appropriate unit tests and examples. \* Added ``/oauth/transactions/scheduled`` endpoints with appropriate unit tests and examples.

2.0.8 \* Fixed exception member-access issue (thanks again, @melinath)!

2.0.7 \* Added better exceptions (thanks, @melinath)!

2.0.6 \* Fixed request.fulfill, added missing ``amount`` param in data and ``alternate_pin`` parameter.

2.0.5 \* Added Python 3 compatibility (thanks @ka7eh)!

2.0.4 \* Fixed a bug with postnomial ``/`` characters causing endpoint requests to fail (thanks for letting us know, @ankitpopli1891).

2.0.3 \* Fixed OAuth handshake bug involving ``redirect_uri`` (thanks @melinath for the bug submission)!

2.0.2 \* Added a webhooks module for ``verify()`` (thanks @mez). \* Fixed bug in offsite-gateway checkouts (also thanks, @mez!).

2.0.1 \* Added MANIFEST.in to resolve issues with README failing retrieval from PyPi.

2.0.0 \* Initial release.

Credits
-------

This wrapper is based on `requests <http://docs.python-requests.org/>`_ for REST capability and uses `unittest <https://docs.python.org/2/library/unittest.html>`_ for unit testing and `Travis <https://travis-ci.org/>`_ for automagical build verification.

Version ``2.x`` initially written by `David Stancu <http://davidstancu.me>`_ (david@dwolla.com).

Versions ``1.x``: The old wrapper is a forked extension of Thomas Hansen's 'dwolla-python' module.

-  Thomas Hansen <thomas.hansen@gmail.com>
-  Jordan Bouvier <jbouvier@gmail.com>
-  Michael Schonfeld <michael@dwolla.com>
-  George Sibble <george.sibble@ultapay.com>
-  Andrey Fedorov <anfedorov@gmail.com>

License
-------

Copyright (c) 2014 Dwolla Inc, David Stancu

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

.. |Join the chat at https://gitter.im/Dwolla/dwolla-python| image:: https://badges.gitter.im/Join%20Chat.svg
.. |Build Status| image:: https://travis-ci.org/Dwolla/dwolla-python.svg?branch=master
