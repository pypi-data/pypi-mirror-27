import pytest
import colander
from requests import HTTPError

from mauth.applications import ApplicationPattern, ApplicationPatternList
from tests.base import test_api_client, BaseTestCase


class TestApplicationPattern(BaseTestCase):
    def setup(self):
        self.application_id = 1
        self.application_pattern_id = 5  # object id in DB
        super().setup()

    def test_create(self):
        with pytest.raises(colander.Invalid):
            ApplicationPattern(api_client=test_api_client).create()

        application_address = ApplicationPattern(api_client=test_api_client)

        application_address.application = self.application_id
        application_address.regex = '127.0.0.1'
        application_address.create()
        assert application_address.id is not None

    @pytest.mark.skip(
        reason="Remove this decorator if ApplicationPattern object exists in DB."
    )
    def test_read_update_destroy(self):
        application_pattern = ApplicationPattern(api_client=test_api_client)
        application_pattern.id = self.application_pattern_id
        application_pattern.application = self.application_id
        application_pattern.read()
        assert application_pattern.regex != None
        # assert application_pattern.regex == '/([0-9a-z]+)/'

        application_pattern.regex = '/([0-9A-Za-z]+)/'
        application_pattern.update()
        assert application_pattern.regex == '/([0-9A-Za-z]+)/'

        application_pattern.destroy()
        pattern = ApplicationPattern(api_client=test_api_client)
        pattern.id = self.application_pattern_id
        pattern.application = self.application_id
        with pytest.raises(HTTPError):
            pattern.read()


class TestApplicationPatternList():
    def setup(self):
        self.application_list = ApplicationPatternList(api_client=test_api_client)

    def test_list(self):
        assert isinstance(self.application_list.list(), list)
