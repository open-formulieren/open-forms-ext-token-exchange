
===================================
Open Forms extension token exchange
===================================

:Version: 0.3.0
:Source: https://github.com/open-formulieren/open-forms-ext-token-exchange
:Keywords: Open Forms Extension, Keycloak token exchange

|build-status| |code-quality| |black| |coverage|

|python-versions| |django-versions| |pypi-version|

Open Forms extension to use Keycloak access tokens when requesting prefill data from external APIs.

.. contents::

.. section-numbering::

Features
========

* Signal receiver which extracts the Keycloak access token from the session and caches it.
* Pre-request hook that adds a custom `authentication class`_ to the request kwargs.
* Custom authentication class that performs the token exchange with Keycloak and adds the exchanged token to the ``Authorization`` header.


.. note::

   The token exchange has a `standard`_, but Keycloak mentions in its `documentation`_ that they
   "*extended it a little, ignored some of it, and loosely interpreted other parts of the specification*".


.. _authentication class: https://requests.readthedocs.io/en/latest/user/advanced/#custom-authentication
.. _standard: https://www.rfc-editor.org/rfc/rfc8693.html
.. _documentation: https://www.keycloak.org/docs/latest/securing_apps/#how-token-exchange-works

Installation
============

Requirements
------------

* Python 3.7 or above
* setuptools 30.3.0 or above
* Django 3.2


Usage
=====

For an explanation of this how this extension works, look at the Open Forms `developer documentation`_.

To see how to build and distribute an image with this extension, look at the Open Forms documentation about
`building and distributing extensions`_.

.. _developer documentation: https://open-forms.readthedocs.io/en/latest/developers/extensions.html#keycloak-token-exchange-extension
.. _building and distributing extensions: https://open-forms.readthedocs.io/en/latest/developers/extensions.html#keycloak-token-exchange-extension

Configuration
=============

In the Open Forms Admin, go to **Miscellaneous** > **Token exchange plugin configurations**.
Click on **Add Token exchange plugin configuration** and fill in the details:

* Select the service for which you want the token authorisation to be performed.
* Add the Keycloak audience.

Save the configuration.

.. |build-status| image:: https://github.com/open-formulieren/open-forms-ext-token-exchange/workflows/Run%20CI/badge.svg
    :alt: Build status
    :target: https://github.com/open-formulieren/open-forms-ext-token-exchange/actions?query=workflow%3A%22Run+CI%22

.. |code-quality| image:: https://github.com/open-formulieren/open-forms-ext-token-exchange/workflows/Code%20quality%20checks/badge.svg
     :alt: Code quality checks
     :target: https://github.com/open-formulieren/open-forms-ext-token-exchange/actions?query=workflow%3A%22Code+quality+checks%22

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

.. |coverage| image:: https://codecov.io/gh/open-formulieren/open-forms-ext-token-exchange/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/open-formulieren/open-forms-ext-token-exchange
    :alt: Coverage status

.. |python-versions| image:: https://img.shields.io/pypi/pyversions/open-forms-ext-token-exchange.svg

.. |django-versions| image:: https://img.shields.io/pypi/djversions/open-forms-ext-token-exchange.svg

.. |pypi-version| image:: https://img.shields.io/pypi/v/open-forms-ext-token-exchange.svg
    :target: https://pypi.org/project/open-forms-ext-token-exchange/
