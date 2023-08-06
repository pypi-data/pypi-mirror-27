from mauth.core.client import APIAdaptor
from mauth.core.schemas import SchemaObject
from mauth.core.mixins import (
    CRUDMixin, ListObjectMixin,
    RetreiveObjectMixin, UpdateObjectMixin,
    PathMixin
)
from .schemas import UserSchema, ProviderAccountSchema


__all__ = (
    'User',
    'UserList',
    'ProviderAccount',
    'ProviderAccountList',
)


class ProviderAccount(CRUDMixin, SchemaObject, PathMixin, APIAdaptor):
    """
    Wrapper of ProviderAccount to work with object over the API.

    Attributes:
        path (str): API url part to work over methods.
        schema_class (MappingSchema): Mapping schema to serialize object.
    """
    path = 'providers-accounts/{id}'
    path_create = 'providers-accounts/create/'
    schema_class = ProviderAccountSchema


class ProviderAccountList(ListObjectMixin, APIAdaptor, PathMixin):
    """
    Wrapper over list of ProviderAccount to work over the API with
    multiple ProviderAccount objects at the same time.

    Attributes:
        instance_class (object): Instance to serialize objects in the
            list.
        path (str): API url part to work over methods.
    """
    path = 'providers-accounts/'
    instance_class = ProviderAccount


class User(CRUDMixin, SchemaObject, PathMixin, APIAdaptor):
    """
    Wrapper of User to work with object over the API.

    Attributes:
        path (str): API url part to work over methods.
        schema_class (MappingSchema): Mapping schema to serialize object.
    """
    path = 'users/{id}'
    path_create = 'users/create/'
    schema_class = UserSchema


class UserList(ListObjectMixin, APIAdaptor, PathMixin):
    """
    Wrapper over list of User to work over the API with
    multiple User objects at the same time.

    Attributes:
        instance_class (object): Instance to serialize objects in the
            list.
        path (str): API url part to work over methods.
    """
    path = 'users/'
    instance_class = User
