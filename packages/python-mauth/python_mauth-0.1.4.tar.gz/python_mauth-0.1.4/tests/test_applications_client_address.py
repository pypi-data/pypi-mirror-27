import colander
import pytest
from requests import HTTPError

from mauth.applications import ApplicationAddress, ApplicationAddressList
from tests.base import test_api_client, BaseTestCase


class TestApplicationAddress(BaseTestCase):
    def setup(self):
        super().setup()

    def test_create(self):
        with pytest.raises(colander.Invalid):
            ApplicationAddress(api_client=test_api_client).create()

        application_address = ApplicationAddress(api_client=test_api_client)
        application_address.application = self.application_id
        application_address.address = '127.0.0.1'
        application_address.mask = 32
        application_address.create()

        assert application_address.id is not None

    def test_read_update_destroy(self):
        application_address = ApplicationAddress(api_client=test_api_client)
        application_address.application = self.application_id
        application_address.address = '127.0.0.1'
        application_address.mask = 32
        application_address.create()

        read_application_address = ApplicationAddress(api_client=test_api_client)
        read_application_address.id = application_address.id
        read_application_address.application = self.application_id
        read_application_address.read()
        assert read_application_address.address != None
        # assert application_address.address == '127.0.0.1'

        application_address.mask = 24
        application_address.update()
        assert application_address.mask == 24

        application_address.destroy()
        address = ApplicationAddress(api_client=test_api_client)
        address.id = application_address.id
        address.application = self.application_id
        with pytest.raises(colander.Invalid):
            address.read()


class TestApplicationAddressList():
    def setup(self):
        self.application_list = ApplicationAddressList(api_client=test_api_client)

    def test_list(self):
        assert isinstance(self.application_list.list(), list)
