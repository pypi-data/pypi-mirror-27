__all__ = (
    'CreateObjectMixin',
    'UpdateObjectMixin',
    'RetreiveObjectMixin',
    'DestroyObjectMixin',
    'ListObjectMixin',
    'CRUDMixin',
    'PathMixin',
    'SchemaObject'
)


class SchemaObject():
    schema_class = None

    def __init__(self, object_dict=None, *args, **kwargs):
        """
        Args:
            object_dict (None, optional): Data received from API server.
        """
        self.schema = self.schema_class()

        if not object_dict:
            object_dict = {}

        # Validate received data.
        self.serialized_data = self.schema.deserialize(object_dict)
        self.set_fields_data(self.serialized_data)

        super().__init__(*args, **kwargs)

    def set_fields_data(self, fields_values):
        for field, value in fields_values.items():
            setattr(self, field, value)

    def get_fields_data(self):
        return {
            field: getattr(self, field, None)
            for field in self.serialized_data.keys()
        }


class PathMixin():
    path = ''

    def get_path(self, method: str, *args, **kwargs) -> str:
        method_path = f'path_{method}'

        if hasattr(self, method_path):
            path = getattr(self, method_path, '')
        else:
            path = self.path

        return path.format(*args, **kwargs)


class CreateObjectMixin():

    def create(self):
        """
        Sends create request on the remote server.
        """
        data = self.get_fields_data()

        # Created object has no id
        data.pop('id')
        serialized_data = self.schema.serialize(data)

        response = self.api_client.post(
            self.get_path('create'), serialized_data
        )
        instance_class = getattr(self, 'instance_class', self.__class__)
        return instance_class(
            api_client=self.api_client, object_dict=response.json()
        )


class UpdateObjectMixin():

    def update(self):
        """
        Sends update request on the remote server.
        """
        data = self.get_fields_data()
        serialized_data = self.schema.serialize(data)
        response = self.api_client.put(
            self.get_path('update', id=self.id), serialized_data
        )

        return None


class RetreiveObjectMixin():

    def read(self):
        """
        Returns corresponding object from the remote server.
        """
        pk = self.serialized_data.get('id')
        response = self.api_client.get(self.get_path('read', id=self.id))

        self.set_fields_data(self.schema.deserialize(response.json()))
        return


class DestroyObjectMixin():

    def destroy(self):
        """
        Sends delete request on the remote server.
        """
        pk = self.serialized_data.get('id')

        return self.api_client.delete(self.get_path('delete', id=pk))


class ListObjectMixin():

    def list(self, data=None):
        """
        Returns the list of corresponding instance_class.
        """
        if not data:
            data = {}

        response = self.api_client.get(self.get_path('list'), data)
        data = response.json()

        return [self.instance_class(x) for x in data]


class CRUDMixin(
        RetreiveObjectMixin, UpdateObjectMixin, DestroyObjectMixin,
        CreateObjectMixin
    ):
    """
    Implements full CRUD API on one path
    """
