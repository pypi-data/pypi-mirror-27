from mauth.applications import Application
from mauth.core.client import APIClient


__all__ = (
    'test_api_client',
)

test_api_client = APIClient(
    api_key='cb2b52271b4392f23971aedb48404fe7',
    api_base_url='http://localhost:8000/api/'
)


class BaseTestCase():
    def setup(self):
        self.application = Application(api_client=test_api_client)
        self.application.title = 'Admin app'
        self.application.internal_type = 'admin'
        self.application.auth_status = 'available'
        self.application.create()
        self.application_id = self.application.id

    def teardown(self):
        self.application.destroy()
