import pytest
import colander
from requests import HTTPError

from mauth.applications import ApplicationPattern, ApplicationPatternList
from tests.base import test_api_client, BaseTestCase


class TestApplicationPattern(BaseTestCase):
    def setup(self):
        super().setup()

    def test_create(self):
        with pytest.raises(colander.Invalid):
            ApplicationPattern(api_client=test_api_client).create()

        application_pattern = ApplicationPattern(api_client=test_api_client)
        application_pattern.application = self.application_id
        application_pattern.regex = '127.0.0.1'
        application_pattern.create()
        assert application_pattern.id is not None

    def test_read_update_destroy(self):
        application_pattern = ApplicationPattern(api_client=test_api_client)
        application_pattern.application = self.application_id
        application_pattern.regex = '127.0.0.1'
        application_pattern.create()

        read_application_pattern = ApplicationPattern(api_client=test_api_client)
        read_application_pattern.id = application_pattern.id
        read_application_pattern.application = self.application_id
        read_application_pattern.read()
        assert read_application_pattern.regex != None
        # assert application_pattern.regex == '/([0-9a-z]+)/'

        application_pattern.regex = '/([0-9A-Za-z]+)/'
        application_pattern.update()
        assert application_pattern.regex == '/([0-9A-Za-z]+)/'

        application_pattern.destroy()
        pattern = ApplicationPattern(api_client=test_api_client)
        pattern.id = application_pattern.id
        pattern.application = self.application_id
        with pytest.raises(colander.Invalid):
            pattern.read()


class TestApplicationPatternList():
    def setup(self):
        self.application_list = ApplicationPatternList(api_client=test_api_client)

    def test_list(self):
        assert isinstance(self.application_list.list(), list)
