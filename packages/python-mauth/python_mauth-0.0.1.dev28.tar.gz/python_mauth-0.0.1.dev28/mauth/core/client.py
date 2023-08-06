from typing import Dict
from functools import partial

import requests


__all__ = (
    'APIConnector',
    'APIClient',
    'APIAdaptor'
)


class APIConnector():
    """
    Base class to work with remote API server. Use this one in your
    APIClient's variants.
    """
    API_BASE_URL = ''
    API_VERSION = 1

    def __init__(
            self, api_base_url: str=None, api_version: str=None, *args,
            **kwargs
        ):
        """
        Initializes api connector. Received parameters required to
        connect remote server.

        Args:
            api_base_url (str, optional): Base url used to construct url.
            api_version (str, optional): API version to use.
        """
        self.api_base_url = api_base_url or self.API_BASE_URL
        self.api_version = api_version or self.API_VERSION

        super().__init__(*args, **kwargs)

    def __getattribute__(self, name: str):
        """
        Override default __getattribute__ to shortner request sending
        on remote server.
        For example instead of:
            >>>> object._send('get', 'url/path', data, headers)
        You can use:
            >>>> object.get('url/path', data, headers)

        Args:
            name (str): Property to get.
        """
        if name in ['get', 'post', 'put', 'delete']:
            return partial(self._send, name)
        return super().__getattribute__(name)

    def construct_url(self, *args) -> str:
        """
        Returns url with joined args as parts of url.

        Args:
            *args: part of url.

        Returns:
            str: URL
        """
        url = f'{self.api_base_url}v{self.api_version}/'

        if not args:
            return url

        joined_args = '/'.join([x.strip('/') for x in args]) + '/'

        return f'{url}{joined_args}'

    def get_auth_headers(self) -> Dict:
        """
        Returns params need to authorizate your requests on remote
        server. Params passed as headers.
        Override it if you need.
        """
        return {}

    def _send(
            self, method: str, path: str, data: Dict=None, files: Dict=None,
            headers: Dict=None
        ):
        """
        Private method used to send request to the remote REST API
        server.

        Args:
            method (str): REST method to use.
            path (str): Corresponding relative path to send request.
            data (Dict, optional): Params to send.
            files (Dict, optional): Files to send.
            headers (Dict, optional): Request headers.

        Returns:
            Response: requests' response instance.

        Raises:
            AttributeError: Unsupported method was used.
        """
        url = self.construct_url(path)
        request_method = getattr(requests, method, None)

        if not request_method:
            raise AttributeError(f'{method} is not supported')

        if headers is None:
            headers = {}

        headers.update(self.get_auth_headers())

        # Delete method accespts only path, without extra params
        if method == 'delete':
            response = request_method(url, headers=headers)
        else:
            response = request_method(url, data, files=files, headers=headers)

        # Raise HTTPError if received such one
        response.raise_for_status()

        return response


class APIClient(APIConnector):
    """
    API client class that implements basic REST methods to talk with the
    server.

    Attributes:
        API_KEY (str): Default API key used when no API key is passed.
        api_key (str): Unique API key passed on init.

    """
    API_KEY = ''

    def __init__(self, api_key: str=None, *args, **kwargs):
        self.api_key = api_key or self.API_KEY

        super().__init__(*args, **kwargs)

    def get_auth_headers(self) -> Dict:
        """
        Returns headers required to authenticate on the authorization
        server.

        Returns:
            Dict: Headers to authenticate request.
        """
        return {
            'API-KEY': self.api_key
        }


class APIAdaptor():
    """
    Base class that should be inherited by each class that has to work
    the API.

    Attributes:
        api_client (APIClient): APIClient instance to work with the API.
        api_client_class (APIClient): APIClient default class to use
            when no api_client passed on initialization stage.
    """
    api_client_class = APIClient

    def __init__(self, api_client=None, *args, **kwargs):
        """
        Initializes new api adaptor instance to use in classes that
        work with API.

        Args:
            api_client (None, optional): Custom APIClient instance, if
                you need to pass special params or even your own class.
        """
        if api_client:
            self.api_client = api_client
        else:
            self.api_client = self.api_client_class()

        super().__init__(*args, **kwargs)
