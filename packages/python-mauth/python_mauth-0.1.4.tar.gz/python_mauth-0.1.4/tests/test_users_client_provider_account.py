from uuid import uuid4
import colander
import pytest

from mauth.users import ProviderAccount, ProviderAccountList
from tests.base import test_api_client, BaseTestCase


class TestProviderAccount(BaseTestCase):
    def setup(self):
        super().setup()
        self.provider_acc_id = 1

    def test_read_update(self):
        # TODO: add client for provider
        provider_acc = ProviderAccount(api_client=test_api_client)
        # provider_acc.id = self.provider_acc_id
        provider_acc.application = self.application_id
        provider_acc.provider = 1
        provider_acc.user = 1
        provider_acc.create()
        provider_acc.read()
        assert provider_acc.application != None
        assert provider_acc.provider != None
        assert provider_acc.user != None

        new_value = uuid4()
        provider_acc.login = new_value
        provider_acc.update()
        assert provider_acc.login == new_value




class TestProviderAccountList():
    def setup(self):
        self.provider_account_list = ProviderAccountList(api_client=test_api_client)

    def test_list(self):
        assert isinstance(self.provider_account_list.list(), list)

