=====
Wixot Auth
=====

Wixot Auth

Quick start
-----------

1. Settings::
    INSTALLED_APPS = [
        ...
        'wAuth',
    ]


1. Add "wAuth" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'wAuth',
    ]

2. Include the polls URLconf in your project urls.py like this::

    url(r'^',include('wAuth.urls')),

3. Run `python manage.py migrate` to create the polls models.

4. Start the development server and visit http://127.0.0.1:8000/wlogin/
   to auth with wixot mail.

