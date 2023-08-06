from mauth.applications import Application
from mauth.core.client import APIClient


__all__ = (
    'test_api_client',
)

test_api_client = APIClient(
    api_key='06d88fec4fbbff0483445c6400e52e36',
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
        print(self.application_id, 123123131)

    def teardown(self):
        self.application.destroy()
