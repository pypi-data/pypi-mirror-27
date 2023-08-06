from .client import APIClient
from .mixins import CRUDMixin, ListObjectMixin


class User(APIClient, CRUDMixin):
    pass


class UserList(APIClient, ListObjectMixin):
    instance_class = User
