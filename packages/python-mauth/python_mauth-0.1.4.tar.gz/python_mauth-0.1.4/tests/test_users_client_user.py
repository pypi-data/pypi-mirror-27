from uuid import uuid4
import colander
import pytest

from mauth.users import User, UserList
from tests.base import test_api_client


class TestProviderAccount():
    def setup(self):
        self.user_id = 1

    def test_read_update(self):
        user = User(api_client=test_api_client)
        user.username = 'super_usear28'
        user.email = 'ad@ad.ads28'
        user.password = 'qwerty123'
        user.first_name = 'first'
        user.last_name = 'last'
        user.create()
        user.read()
        assert user.username != None
        assert user.email != None

        new_value = 'new last name'
        user.last_name = new_value
        user.update()
        assert user.last_name == new_value

        user.destroy()


class TestUserList():
    def setup(self):
        self.user_list = UserList(api_client=test_api_client)

    def test_list(self):
        assert isinstance(self.user_list.list(), list)
