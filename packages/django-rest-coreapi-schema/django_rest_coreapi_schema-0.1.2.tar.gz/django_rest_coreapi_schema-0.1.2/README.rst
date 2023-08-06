Django restframework schema
===========================

This package is a schema for django restframework.

How to use
==========

Installation
------------

.. code:: bash

    $ pip install django-rest-coreapi-schema

.. code:: bash

    $ pip install -e git+https://github.com/emilioag/django_rest_coreapi_schema.git#egg=django_rest_coreapi_schema

Configuration
-------------

django settings
~~~~~~~~~~~~~~~

Add the next configuration in your settings.py file.

.. code:: python

    REST_FRAMEWORK = {
        'DEFAULT_SCHEMA_CLASS': 'django_rest_coreapi_schema.schema.CoreAPIAutoSchema',
    }

Restframework docs (urls)
~~~~~~~~~~~~~~~~~~~~~~~~~

Add to your urls.py the restframework docs

.. code:: python

    from django.conf.urls import url
    from rest_framework.documentation import include_docs_urls

    urlpatterns = [
        url(r'^docs/', include_docs_urls(title='My API title', description='API description', public=False)),
    ]

Create your serializers
~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from rest_framework import serializers


    class UserSerializer(serializers.Serializer):
        email = serializers.CharField(
            required=False,
            help_text="User email")
        address = serializers.CharField(
            required=False,
            help_text="User address")


    class FilterSerializer(serializers.Serializer):
        order = serializers.ChoiceField(
            required=False,
            choices=[("asc", "Asc"), ("desc", "desc")],
            help_text="Order")
        username = serializers.CharField(
            required=False,
            help_text="Username pattern")


    class PathSerializer(serializers.Serializer):
        username = serializers.CharField(
            required=True,
            help_text="Username")

Create your pagination
~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from rest_framework.pagination import PageNumberPagination


    class LargeResultsSetPagination(PageNumberPagination):
        page_size = 1000
        page_size_query_param = 'page_size'
        max_page_size = 10000

Create your view
----------------

Documenting path variables
~~~~~~~~~~~~~~~~~~~~~~~~~~

You have to use the class variable: ``queryset``

.. code:: python

    from django_rest_coreapi_schema.views import DocumentedBaseView

    class UserView(DocumentedBaseView):
        queryset = PathSerializer

Url args
~~~~~~~~

You have to use the class variables: ``filter_backends`` and
``filter_fields``

-  **filter\_backends** is a list of serializers which contains all the
   possible url args.
-  **filter\_fields** is a list of arg names that will be appear in the
   coreapi documentation.

.. code:: python

    from django_rest_coreapi_schema.views import DocumentedBaseView

    class UserListView(DocumentedBaseView):
        filter_backends = [FilterSerializer]
        filter_fields = ('order', 'username')

Body
~~~~

Http put, post, etc. body.

.. code:: python

    from django_rest_coreapi_schema.views import DocumentedBaseView

    class UserView(DocumentedBaseView):
        body_serializer_class = UserSerializer

Pagination (for large results)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from django_rest_coreapi_schema.views import DocumentedBaseView

    class UserListView(DocumentedBaseView):
        pagination_class = LargeResultsSetPagination

You can see a whole example in examples/restAPI folder inside this
repository.
