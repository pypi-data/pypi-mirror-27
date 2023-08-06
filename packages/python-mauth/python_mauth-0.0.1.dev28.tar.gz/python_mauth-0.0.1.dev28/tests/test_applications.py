import json
import pytest
import mauth
from requests.exceptions import HTTPError

from mauth.applications import Application, ApplicationList
from mauth.applications.schemas import ApplicationSchema
from .base import test_api_client


class TestApplication():
    def setup(self):
        self.application = Application(api_client=test_api_client)

    def test_create(self):
        with pytest.raises(HTTPError):
            self.application.create()

        # TODO: Only admin application can change internal_type.
        application = Application(api_client=test_api_client)
        application.title = 'title'
        new_application = application.create()
        assert type(new_application) == Application

    def test_update_read(self):
        application = Application(api_client=test_api_client)
        application.title = 'title1'

        new_application = application.create()

        assert new_application.title == 'title1'

        new_application.title = 'title2'
        new_application.update()
        assert new_application.title == 'title2'

        app = Application(api_client=test_api_client)
        app.id = new_application.id
        app.read()
        assert app.title == 'title2'

    def test_destroy(self):
        application = Application(api_client=test_api_client)
        application.title = 'title1'

        new_application = application.create()
        new_application.destroy()
        app = Application(api_client=test_api_client)
        assert not app.id
        assert not app.title

    def test_fields_is_readable_without_any_data_passed(self):
        application = Application(api_client=test_api_client)
        assert not application.id
        assert not application.title
        assert not application.url
        assert not application.client_id
        assert not application.internal_type
        assert not application.auth_status
        assert application.has_referrals is True
        assert not application.api_key

    def test_fields_is_readable_with_data_passed(self):
        fields = {
            'id': 1, 'title': 'title', 'url': None, 'client_id': '',
            'internal_type': 'admin', 'auth_status': '',
            'has_referrals': False, 'api_key': '1231232'
        }
        application = Application(api_client=test_api_client, object_dict=fields)
        assert application.id == 1
        assert application.title == 'title'
        assert application.url == ''
        assert application.client_id == ''
        assert application.internal_type == 'admin'
        assert application.auth_status == ''
        assert application.has_referrals is False
        assert application.api_key == '1231232'


class TestApplicationList():
    def setup(self):
        self.application_list = ApplicationList(api_client=test_api_client)

    def test_list(self):
        assert isinstance(self.application_list.list(), list)


class TestApplicationSchema():
    def setup(self):
        self.fields = ApplicationSchema.get_fields_names()

    def test_fields_simple_output(self):
        assert [_.name for _ in ApplicationSchema.__class_schema_nodes__] == self.fields
