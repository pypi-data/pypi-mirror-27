import colander
import pytest
from requests import HTTPError

from mauth.applications import Application, ApplicationList
from tests.base import test_api_client


class TestApplication():
    def setup(self):
        self.application = Application(api_client=test_api_client)

    def test_create(self):
        with pytest.raises(HTTPError):
            self.application.create()

        # TODO: Only admin application can change internal_type.
        application = Application(api_client=test_api_client)
        application.title = 'title'
        application.create()
        assert application.id is not None

        application.destroy()
        app = Application(api_client=test_api_client)
        with pytest.raises(colander.Invalid):
            app.read()

    def test_update_read_destroy(self):
        application = Application(api_client=test_api_client)
        application.title = 'title1'
        application.create()

        assert application.title == 'title1'

        application.title = 'title2'
        application.update()
        assert application.title == 'title2'

        app = Application(api_client=test_api_client)
        app.id = application.id
        app.read()
        assert app.title == 'title2'

        app.destroy()
        app = Application(api_client=test_api_client)
        with pytest.raises(colander.Invalid):
            app.read()

    def test_destroy(self):
        application = Application(api_client=test_api_client)
        application.title = 'title_destroy'

        application.create()
        application.destroy()
        app = Application(api_client=test_api_client)
        with pytest.raises(colander.Invalid):
            app.read()

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
