from typing import List, Dict


__all__ = (
    'SchemaFields',
    'SchemaObject'
)


class SchemaFields():
    """
    Mixin that allows to work with schema fields.
    """

    @classmethod
    def get_fields_names(cls) -> List[str]:
        """
        Returns all the fields names defined in the schema.
        """
        # NOTE: Cache for _fields.

        return [_.name for _ in cls.__class_schema_nodes__]


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
