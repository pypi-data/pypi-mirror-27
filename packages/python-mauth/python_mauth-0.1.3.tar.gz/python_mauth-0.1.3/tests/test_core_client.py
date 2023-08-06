import pytest
from requests.exceptions import HTTPError

from mauth.core.client import APIClient
from .base import test_api_client


class TestAPIClient():
    def setup(self):
        self.api_client = test_api_client
        self.api_base_url = 'http://localhost:8000/api/'

    def test_construct_url(self):
        assert (
            self.api_client.construct_url() ==
            f'{self.api_base_url}v1/'
        )

        assert (
            self.api_client.construct_url('/method/url/') ==
            f'{self.api_base_url}v1/method/url/'
        )

        assert (
            self.api_client.construct_url('/method/url/', 'path') ==
            f'{self.api_base_url}v1/method/url/path/'
        )

        assert (
            self.api_client.construct_url('/method/url/', '/path') ==
            f'{self.api_base_url}v1/method/url/path/'
        )

        assert (
            self.api_client.construct_url('/method/url/', '/path/') ==
            f'{self.api_base_url}v1/method/url/path/'
        )

    def test_send(self):
        with pytest.raises(AttributeError):
            self.api_client._send('unknown_method', 'path')

        assert self.api_client._send('get', 'providers').status_code == 200

        with pytest.raises(HTTPError) as e:
            self.api_client._send('get', '')
            assert e.status_code == 404

    def test_getattr(self):
        with pytest.raises(AttributeError):
            self.api_client.method('unknown_method', 'path')

        assert self.api_client.get('providers').status_code == 200

        with pytest.raises(HTTPError):
            assert self.api_client.post('').status_code == 404

    def test_get_auth_headers(self):
        assert self.api_client.get_auth_headers().get('API-KEY') == self.api_client.api_key