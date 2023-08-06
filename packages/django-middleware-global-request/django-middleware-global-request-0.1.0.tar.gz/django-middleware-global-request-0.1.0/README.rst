DJANGO MIDDLEWARE GLOBAL REQUEST
================================


Django middleware that keep request instance for every thread.


Usage:
------

1. Add django application django_global_request to INSTALLED_APPS in settings.py

::

    INSTALLED_APPS = [
        ...
        'django_global_request',
        ...
    ]

2. Add GlobalRequestMiddleware to MIDDLEWARE in settings.py

::

    MIDDLEWARE = [
        ...
        'django_global_request.middleware.GlobalRequestMiddleware',
        ...
    ]

3. Get request instance with from django_global_request.middleware import get_request

::

    from django_global_request.middleware import get_request

    class TestModel(models.Model):

        field1 = models.CharField(max_length=32)

        def hello(self):
            request = get_request()
            ...
