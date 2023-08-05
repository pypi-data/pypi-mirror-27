================
django-basicauth
================

Basic auth utilities for Django.

Requires
========

Tested under...

* Python

  * 2.7
  * 3.6

* Django

  * 1.8
  * 1.10
  * 1.11

Installation
============

::

    pip install django-basicauth


Usage
=====

.. code-block:: python

    from basicauth.decorators import basic_auth_required

    @basic_auth_required
    def myview(request):
        ...

or by a middleware.

.. code-block:: python

    MIDDLEWARE_CLASSES = (
        'basicauth.middleware.BasicAuthMiddleware',
        ...
    )

Basic Auth for specific requestno only
--------------------------------------

To apply basic auth for specific requests,
Use ``target_test`` argument.

In the below code, anonymous users will be required Basic Auth
Authenticated users can pass it without `Basic ...` header.

.. code-block:: python

    from basicauth.decorators import basic_auth_required

    @basic_auth_required(
        target_test=lambda request: not request.user.is_authenticated
    )
    def myview(request):
        ...

``target_test`` accepts ``typing.Callable[[HttpRequest], bool]``,
and if the callable returns ``True``, Basic Auth will be required.

Applying decorator to CBVs
==========================

To apply ``@basic_auth_requried`` decorator to Class Based Views,
use ``django.utils.decorators.method_decorator``.

.. code-block:: python

    from django.utils.decorators import method_decorator
    from basicauth.decorators import basic_auth_required

    @method_decorator(basic_auth_required, name='dispatch')
    class YourView(TemplateView):
        template_name = "my-template.html"

Settings
========

* ``BASICAUTH_USERS`` (required): Dictionary including keys as username and values as passwords.
* ``BASICAUTH_REALM``: realm string, default is "Secure resource".
* ``BASICAUTH_DISABLE``: Disable all of barriers by this library.


Changes
=======

0.4.2 (2017-11-27)
------------------
* Fixed to avoid timing attacks
    * Lots of thanks for Hugo Castilho

0.4.1 (2017-10-20)
------------------
* Added ``target_test`` argument for the decorator.

0.4 (2017-09-30)
----------------

* Supported Python 2.7
* Dropped Django1.9
* Supported Django 1.10+ style middleware

0.3 (2017-08-28)
----------------

* Added ``BASICAUTH_DISABLE`` setting
* Changed API of ``basicauthutils.validate_request``
    * Fixed to return True/False
    * Adding REMOTE_USER by this function

0.2.1 (2017-08-28)
------------------

* Officially supported Django 1.11, 1.10, 1.9

0.2 (2016-03-31)
----------------

* Added BasicAuthMiddleware https://github.com/hirokiky/django-basicauth/pull/3

0.1 (2015-04-20)
----------------

* Initial


