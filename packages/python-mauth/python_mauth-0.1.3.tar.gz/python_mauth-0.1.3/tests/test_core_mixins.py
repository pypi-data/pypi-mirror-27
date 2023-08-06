import colander
import pytest
from requests.exceptions import HTTPError
from mauth.core.schemas import SchemaFields
from mauth.core.mixins import PathMixin, CRUDMixin
from mauth.core.schemas import SchemaObject

from .base import test_api_client


class DummySchemaClass(colander.MappingSchema, SchemaFields):
    title = colander.SchemaNode(
        colander.String(), validator=colander.Length(0, 255),
        missing=''
    )


class DummyClient(SchemaObject):
    schema_class = DummySchemaClass


class TestSchemaObject():
    def setup(self):
        self.object_data = {'title': 'some title'}
        self.client = DummyClient(self.object_data)

    def test_init(self):
        assert type(self.client.schema) == DummySchemaClass
        assert self.client.serialized_data == self.object_data
        assert self.client.title == 'some title'

    def test_get_fields_data(self):
        assert self.client.get_fields_data() == self.object_data


class DummyClientPathMixin(DummyClient, PathMixin):
    path = '/path/'
    path_create = '/path/create/'


class TestPathMixin():
    def setup(self):
        self.client = DummyClientPathMixin()

    def test_get_path(self):
        assert self.client.get_path('unknown_method') == '/path/'
        assert self.client.get_path('create') == '/path/create/'


class DummyClientRetrieveObjectMixin(DummyClient, PathMixin, CRUDMixin):
    path = '/path/'
    path_create = '/path/read/'


class TestCRUDMixin():
    def setup(self):
        self.object_data = {'title': 'some title', 'id': 1}
        self.client = DummyClientRetrieveObjectMixin(self.object_data)

    def test_read_without_pk(self):
        with pytest.raises(ValueError):
            self.client.read()

    def test_update_without_pk(self):
        with pytest.raises(ValueError):
            self.client.update()

    def test_create_without_pk(self):
        with pytest.raises(KeyError):
            self.client.create()

    def test_destroy_without_pk(self):
        with pytest.raises(ValueError):
            self.client.destroy()
