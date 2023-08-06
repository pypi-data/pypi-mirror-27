Django orders flavor
====================

|Pypi| |Wheel| |Build Status| |Codecov| |Code Climate|


Django orders app.

Dependencies
------------

* Python ≥ 3.4
* Django ≥ 1.11

Installation
------------

Install last stable version from Pypi.

.. code:: sh

    pip install django-orders-flavor


Add ``orders`` to your INSTALLED_APPS setting.

.. code:: python

    INSTALLED_APPS = (
        ...
        'django_filters',
        'oauth2_provider',
        'paypal.standard.ipn',
        'rest_framework',
        ...
        'core_flavor.apps.CoreAppConfig',
        'countries.apps.CountriesAppConfig',
        'orders.apps.OrdersAppConfig'
    )

Hook the Django urls into your URLconf.

.. code:: python

    from django.conf.urls import include, url

    urlpatterns = [
        url(r'^', include(
            'orders.api.urls',
            namespace='orders-flavor-api')),

        url(r'^paypal/', include('paypal.standard.ipn.urls'))
    ]

Apply migrations.

.. code:: python

    python manage.py migrate

.. |Pypi| image:: https://img.shields.io/pypi/v/django-orders-flavor.svg
   :target: https://pypi.python.org/pypi/django-orders-flavor

.. |Wheel| image:: https://img.shields.io/pypi/wheel/django-orders-flavor.svg
   :target: https://pypi.python.org/pypi/django-orders-flavor

.. |Build Status| image:: https://travis-ci.org/flavors/orders.svg?branch=master
   :target: https://travis-ci.org/flavors/orders

.. |Codecov| image:: https://img.shields.io/codecov/c/github/flavors/orders.svg
   :target: https://codecov.io/gh/flavors/orders

.. |Code Climate| image:: https://codeclimate.com/github/flavors/orders/badges/gpa.svg
   :target: https://codeclimate.com/github/flavors/orders
