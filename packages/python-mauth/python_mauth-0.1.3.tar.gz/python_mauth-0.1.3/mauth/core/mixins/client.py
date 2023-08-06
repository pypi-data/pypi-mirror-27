__all__ = (
    'CreateObjectMixin',
    'UpdateObjectMixin',
    'RetreiveObjectMixin',
    'DestroyObjectMixin',
    'ListObjectMixin',
    'CRUDMixin',
)


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

        # Create instance class with inherited currenct api_client.
        self.serialized_data = self.schema.deserialize(response.json())
        self.set_fields_data(self.serialized_data)
        return


class UpdateObjectMixin():
    """
    Mixin that provides logic for object updating.
    """

    def update(self):
        """
        Sends update request on the remote server.
        """
        data = self.get_fields_data()
        serialized_data = self.schema.serialize(data)
        pk = serialized_data.get('id')

        if not pk:
            raise ValueError("Cannot update object without primary key")

        # NOTE: A good idea would be to store object state to limit
        # requests when actually no updates were made.
        response = self.api_client.put(
            self.get_path('update', id=pk), serialized_data
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

        response = self.api_client.get(self.get_path('read', id=pk))

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
        data = self.get_fields_data()
        serialized_data = self.schema.serialize(data)
        pk = serialized_data.get('id')

        if not pk:
            raise ValueError("Cannot destroy object without primary key")

        response = self.api_client.delete(self.get_path('delete', id=pk))
        self.id = None

        return None


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
