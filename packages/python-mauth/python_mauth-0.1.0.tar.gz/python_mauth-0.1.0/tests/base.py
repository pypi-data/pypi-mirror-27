from mauth.core.client import APIClient


__all__ = (
    'test_api_client',
)

test_api_client = APIClient(
    api_key='e154cd3878e56278cfc595a719370590',
    api_base_url='http://localhost:8000/api/'
)
