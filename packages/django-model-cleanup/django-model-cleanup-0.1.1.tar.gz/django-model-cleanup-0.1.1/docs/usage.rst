=====
Usage
=====

To use Django Model Cleanup in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_model_cleanup.apps.DjangoModelCleanupConfig',
        ...
    )

Add Django Model Cleanup's URL patterns:

.. code-block:: python

    from django_model_cleanup import urls as django_model_cleanup_urls


    urlpatterns = [
        ...
        url(r'^', include(django_model_cleanup_urls)),
        ...
    ]
