Client library for Mauth project
================================

Install library through pypi

.. code-block:: python

    pipenv install python_mauth

Simple usecase of creating application

.. code-block:: python

    from mauth.applications import Application

    app = Application(
        api_base_url='http://auth.ob-auth.com', api_key='some_key'
    )
    app.title = 'title'
    app.create()
    print(app.id)
