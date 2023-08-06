social-auth-backend-b2access
============================

B2ACCESS_ is an easy-to-use and secure Authentication and
Authorization platform developed by EUDAT. B2ACCESS offers
authentication of users to applications using OAuth 2.0, OpenID
Connect and SAML.

``social-auth-backend-b2access`` is an OAuth2 client for B2ACCESS
that depends on social-auth-core_.

This is a Python 3 based project. No attempts
have been made to make it backwards compatible with Python 2.


Installation
------------

Install with ``pip install social-auth-backend-b2access`` or by
downloading the source and running ``setup.py``.


Usage
-----

Set up a service at B2ACCESS
.............................

There needs to exist an entry for your site/app/service at
B2ACCESS. Go to `B2ACCESS`_ but do not log in. Click on ``Register
a new account``. In the popup, click on ``OAuth 2.0 Client
Registration Form``. This will bring up a new popup, "Registration
Form".

The ``username`` and ``password`` will be used later to change
information about the app, but will also be used as the OAuth2
``KEY`` and ``SECRET``. ``mail`` is the correct contact email
address for the person responsible for the service. ``OAuth client
return URL`` is what B2ACCESS calls the endpoints to the service.
``social-auth`` calls these ``redirect uris``, and there can be
more than one. ``Admin`` is the name of the person responsible for
the service. The ``usage``-field must be filled with at least
30 characters.

The redirect uri is of the form ``<type>://<domainpath>/<suffix>/``,
where ``<type>`` is one of ``http`` or ``https``, ``<domainpath>``
is the domain name of your site and an optional path, and the
``<suffix>`` is backend-dependent. See the examples under
**Backends**.

Set up your site
................

You'll need to set the client id (username) and client secret
(password) you chose for B2ACCESS in the settings of your
app/site.

Both the name of the settings and the redirect uris depend on the
backends used. Add at least one of the backends below.

See `social's documentation`_ for more.

Django
......

In your ``settings.py``:

* Add ``'social_django'`` to ``INSTALLED_APPS``.
* Add one or more of the backend names below to the start of
  ``AUTHENTICATION_BACKENDS``. If you're also using user-models
  à la Django, ``'django.contrib.auth.backends.ModelBackend'``
  must be in the same list, following the backends.
* Set ``SOCIAL_AUTH_B2ACCESS_SSL_PROTOCOL`` to ``True`` to force
  use of SSL.
* ``SOCIAL_AUTH_LOGIN_REDIRECT_URL``,
  ``SOCIAL_AUTH_NEW_USER_REDIRECT_URL`` and
  ``SOCIAL_AUTH_REDIRECT_IS_HTTPS`` will have to be set depending
  on the needs of your site.
* If you use the Django admin, you might want to set
  ``SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS``, for instance to
  ``['username', 'email']``.

In your site's ``urls.py``, include:

``url(PREFIX, include('social_django.urls', namespace='social')),``

... where PREFIX is a string to start off the urls with. Empty
string, ``''``, is fine.


Generating usernames
--------------------

By default, the username that is returned is B2ACCESS'
"name"-field, which holds a full name of a person. Also, the name
is cleaned via a regular expression, see the table of results below:

+------------+---------+
| Before     | After   |
+------------+---------+
| John Doe   | JohnDoe |
+------------+---------+
| Schültz    | Schltz  |
+------------+---------+

If you don't want the username to be cleaned, set
``SOCIAL_AUTH_CLEAN_USERNAMES`` to ``False`` in settings.

If you want to make the username very url-friendly, set
``SOCIAL_AUTH_SLUGIFY_USERNAMES`` to ``True``. "John Doe" will
then be converted to "john-doe". This will also strip away
non-ASCII letters.

If you want to use email-addresses for the username, set
``SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL`` to ``True`` in settings.

If there already is a user with that username registered, the
username will have a random alpahnumeric string appended in order
to make it unique.

You might want to let users change this generated username. The
backend only cares that a username exists and is unique and won't
change the username back.


Backends
--------

b2access.B2ACCESSOAuth2
.......................

This is for services in production.

Register service at
    `B2ACCESS`_

Backend name
    ``b2access.B2ACCESSOAuth2``

Settings
    Client id: ``SOCIAL_AUTH_B2ACCESS_KEY``

    Client secret: ``SOCIAL_AUTH_B2ACCESS_SECRET``

Scopes needed
    ``email`` and ``profile``

Redirect-uri ends with
    /complete/b2access/

Example redirect uri:
    http://127.0.0.1/complete/b2access/

b2access.B2ACCESSIntegrationOAuth2
..................................

This is for services not yet fully in production.

Register service at
    https://b2access-integration.fz-juelich.de/home/

Backend name
    ``b2access.B2ACCESSIntegrationOAuth2``

Settings
    Client id: ``SOCIAL_AUTH_B2ACCESS_TEST_KEY``

    Client secret: ``SOCIAL_AUTH_B2ACCESS_TEST_SECRET``

Scopes needed
    ``email`` and ``profile``

Redirect-uri ends with
    /complete/b2access-test/

Example redirect uri:
    http://127.0.0.1/complete/b2access-test/

.. _B2ACCESS: https://b2access.eudat.eu/
.. _social-auth-core: https://python-social-auth.readthedocs.io/en/latest/
.. _social's documentation: https://python-social-auth.readthedocs.io/en/latest/
.. _python-social-auth: https://pypi.python.org/pypi/social-auth


:Version: 1.0.0
