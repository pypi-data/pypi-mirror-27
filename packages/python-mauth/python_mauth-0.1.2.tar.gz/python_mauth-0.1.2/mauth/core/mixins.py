from typing import Dict

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
    """
    Schema object mixin. Provides a few shortcuts to process data using
    declared schema_class.

    Attributes:
        schema (object): schema_class instance.
        schema_class (object): Schema class to process data.
        serialized_data (Dict): Object data.
    """
    schema_class = None

    def __init__(self, object_dict: Dict=None, *args, **kwargs):
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

    def set_fields_data(self, fields_data: Dict):
        """
        Sets variables specified in schema.

        Args:
            fields_data (Dict): Fields data.
        """
        for field, value in fields_data.items():
            setattr(self, field, value)

    def get_fields_data(self) -> Dict:
        """
        Returns fields data as dictionary.

        Returns:
            Dict: Fields data.
        """
        return {
            field: getattr(self, field, None)
            for field in self.schema_class.get_fields_names()
        }


class PathMixin():
    """
    Mixin to define separate pathes for different REST methods.

    Attributes:
        path (str): Url path
    """
    path = ''

    def get_path(self, method: str, *args, **kwargs) -> str:
        """
        Returns path to process request for currect method.
        If there is no such path_variable, e.g. - `path_{method}`, uses
        `path`

        Args:
            method (str): Method, e.g. - create, update

        Returns:
            str: URL path to process request.
        """
        method_path = f'path_{method}'

        if hasattr(self, method_path):
            path = getattr(self, method_path, '')
        else:
            path = self.path

        return path.format(*args, **kwargs)


class CreateObjectMixin():
    """
    Mixins that provides logic of object creation.
    """

    def create(self):
        """
        Sends create request on the remote server and returns instance
        of instance_class with data inherited from current instance.
        """
        data = self.get_fields_data()

        # Created object has no id
        data.pop('id')
        serialized_data = self.schema.serialize(data)

        response = self.api_client.post(
            self.get_path('create'), serialized_data
        )
        instance_class = getattr(self, 'instance_class', self.__class__)
        # Create instance class with inherited currenct api_client.
        return instance_class(
            api_client=self.api_client, object_dict=response.json()
        )


class UpdateObjectMixin():
    """
    Mixin that provides logic for object updating.
    """

    def update(self):
        """
        Sends update request on the remote server.
        """
        data = self.get_fields_data()

        # Currenct object data.
        serialized_data = self.schema.serialize(data)

        # NOTE: A good idea would be to store object state to limit
        # requests when actually no updates were made.
        response = self.api_client.put(
            self.get_path('update', id=self.id), serialized_data
        )

        return None


class RetreiveObjectMixin():
    """
    Mixin that provides logic for object data retreiving.
    """

    def read(self):
        """
        Returns corresponding object from the remote server.
        """
        data = self.get_fields_data()
        serialized_data = self.schema.serialize(data)
        pk = serialized_data.get('id')

        if not pk:
            raise ValueError("Cannot get object without primary key")

        response = self.api_client.get(self.get_path('read', id=self.id))

        self.set_fields_data(self.schema.deserialize(response.json()))
        return None


class DestroyObjectMixin():
    """
    Mixin that provides logic to destroy object.
    """

    def destroy(self):
        """
        Sends delete request on the remote server.
        """
        pk = self.serialized_data.get('id')

        if not pk:
            raise ValueError("Cannot destroy object without primary key")

        return self.api_client.delete(self.get_path('delete', id=pk))


class ListObjectMixin():
    """
    Mixin that provides logic of retreiving multiple objects at the same
    time.
    """

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
    Implements full CRUD API over object.
    """
