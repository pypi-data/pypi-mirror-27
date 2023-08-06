from mauth.core.client import APIClient


__all__ = (
    'test_api_client',
)

test_api_client = APIClient(
    api_key='06d88fec4fbbff0483445c6400e52e36',
    api_base_url='http://localhost:8000/api/'
)
