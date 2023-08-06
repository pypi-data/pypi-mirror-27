import pytest
from requests import HTTPError

from mauth.applications import ApplicationPrivilege, ApplicationPrivilegeList
from tests.base import test_api_client


class TestApplicationPrivilege():
    def setup(self):
        self.application_id = 1
        self.application_privilege_id = 1  # object id in DB

    @pytest.mark.skip(
        reason="Remove this decorator if ApplicationPrivilege object exists in DB."
    )
    def test_read_update_destroy(self):
        application_address = ApplicationPrivilege(api_client=test_api_client)
        application_address.id = self.application_privilege_id
        application_address.application = self.application_id
        application_address.read()
        assert application_address.title != None
        # assert application_address.title == 'Privilege'

        application_address.title = 'New privilege'
        application_address.update()
        assert application_address.title == 'New privilege'

        application_address.destroy()
        privilege = ApplicationPrivilege(api_client=test_api_client)
        privilege.id = self.application_privilege_id
        privilege.application = self.application_id
        with pytest.raises(HTTPError):
            privilege.read()


class TestApplicationPrivilegeList():
    def setup(self):
        self.application_list = ApplicationPrivilegeList(api_client=test_api_client)

    def test_list(self):
        assert isinstance(self.application_list.list(), list)