Client library for Mauth project
================================

Install library through pypi

.. code-block:: python

    pipenv install python_mauth

Simple usecase of creating application

.. code-block:: python

    from mauth.applications import Application
    from mauth.core.client import APIClient

    api_client = APIClient(
        api_key='',
        api_base_url='http://localhost:8000/api/'
    )
    app = Application(api_client=api_client)
    app.title = 'title'

    # NOTE. Creation allowed only for admin application.
    app.create()
    print(app.id)
