from ..core.client import APIAdaptor
from ..core.schemas import SchemaObject
from ..core.mixins import CRUDMixin, ListObjectMixin, PathMixin
from .schemas import (
    ApplicationSchema, ApplicationPatternSchema, ApplicationAddressSchema,
    ApplicationPrivilegeSchema
)


__all__ = (
    'Application',
    'ApplicationList',
    'ApplicationPattern',
    'ApplicationPatternList',
    'ApplicationAddress',
    'ApplicationAddressList',
    'ApplicationPrivilege',
    'ApplicationPrivilegeList',
)


class Application(CRUDMixin, SchemaObject, PathMixin, APIAdaptor):
    """
    Wrapper of Application to work with object over the API.

    Attributes:
        path (str): API url part to work over methods.
        path_create (str): API url part to create.
        schema_class (MappingSchema): Mapping schema to serialize object.
    """
    path = 'applications/{id}/'
    path_create = 'applications/create/'
    path_delete = 'applications/delete/{id}/'
    schema_class = ApplicationSchema


class ApplicationList(APIAdaptor, ListObjectMixin, PathMixin):
    """
    Wrapper over list of Applications to work over the API with multiple
    Application objects at the same time.

    Attributes:
        instance_class (object): Instance to serialize objects in the
            list.
        path (str): API url part to work over methods.
    """
    path = 'applications/'
    instance_class = Application


class ApplicationPattern(CRUDMixin, SchemaObject, PathMixin, APIAdaptor):
    """
    Wrapper of ApplicationPattern to work with object over the API.

    Attributes:
        path (str): API url part to work over methods.
        schema_class (MappingSchema): Mapping schema to serialize object.
    """
    path = 'patterns/{id}/'
    path_create = 'patterns/create/'
    schema_class = ApplicationPatternSchema


class ApplicationPatternList(APIAdaptor, ListObjectMixin, PathMixin):
    """
    Wrapper over list of ApplicationPatterns to work over the API with
    multiple ApplicationPattern objects at the same time.

    Attributes:
        instance_class (object): Instance to serialize objects in the
            list.
        path (str): API url part to work over methods.
    """
    path = 'patterns/'
    instance_class = ApplicationPattern


class ApplicationAddress(CRUDMixin, SchemaObject, PathMixin, APIAdaptor):
    """
    Wrapper of ApplicationAddress to work with object over the API.

    Attributes:
        path (str): API url part to work over methods.
        schema_class (MappingSchema): Mapping schema to serialize object.
    """
    path = 'addresses/{id}/'
    path_create = 'addresses/create/'
    schema_class = ApplicationAddressSchema


class ApplicationAddressList(APIAdaptor, ListObjectMixin, PathMixin):
    """
    Wrapper over list of ApplicationAddresses to work over the API with
    multiple ApplicationAddress objects at the same time.

    Attributes:
        instance_class (object): Instance to serialize objects in the
            list.
        path (str): API url part to work over methods.
    """
    path = 'addresses/'
    instance_class = ApplicationAddress


class ApplicationPrivilege(APIAdaptor, CRUDMixin, SchemaObject, PathMixin):
    """
    Wrapper of ApplicationPrivilege to work with object over the API.

    Attributes:
        path (str): API url part to work over methods.
        schema_class (MappingSchema): Mapping schema to serialize object.
    """
    path = 'privileges/{id}/'
    path_create = 'privileges/create/'
    schema_class = ApplicationPrivilegeSchema


class ApplicationPrivilegeList(APIAdaptor, ListObjectMixin, PathMixin):
    """
    Wrapper over list of ApplicationPrivilege to work over the API with
    multiple ApplicationPrivilege objects at the same time.

    Attributes:
        instance_class (object): Instance to serialize objects in the
            list.
        path (str): API url part to work over methods.
    """
    path = 'privileges/'
    instance_class = ApplicationPrivilege
