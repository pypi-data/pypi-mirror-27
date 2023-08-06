import colander
import pytest
from requests import HTTPError

from mauth.applications import ApplicationPrivilege, ApplicationPrivilegeList
from tests.base import test_api_client, BaseTestCase


class TestApplicationPrivilege(BaseTestCase):
    def setup(self):
        super().setup()

    def test_create(self):
        with pytest.raises(colander.Invalid):
            ApplicationPrivilege(api_client=test_api_client).create()

        application_privilege = ApplicationPrivilege(api_client=test_api_client)
        application_privilege.application = self.application_id
        application_privilege.title = 'some title'
        application_privilege.create()

        assert application_privilege.id is not None

    def test_read_update_destroy(self):
        with pytest.raises(colander.Invalid):
            ApplicationPrivilege(api_client=test_api_client).create()

        application_privilege = ApplicationPrivilege(api_client=test_api_client)
        application_privilege.application = self.application_id
        application_privilege.title = 'some title'
        application_privilege.create()

        read_application_privilege = ApplicationPrivilege(api_client=test_api_client)
        read_application_privilege.id = application_privilege.id
        read_application_privilege.application = self.application_id
        read_application_privilege.read()
        assert read_application_privilege.title != None
        # assert application_address.title == 'Privilege'

        application_privilege.title = 'New privilege'
        application_privilege.update()
        assert application_privilege.title == 'New privilege'

        application_privilege.destroy()
        privilege = ApplicationPrivilege(api_client=test_api_client)
        privilege.id = application_privilege.id
        privilege.application = self.application_id
        with pytest.raises(colander.Invalid):
            privilege.read()


class TestApplicationPrivilegeList():
    def setup(self):
        self.application_privilege_list = ApplicationPrivilegeList(api_client=test_api_client)

    def test_list(self):
        assert isinstance(self.application_privilege_list.list(), list)