import colander
from typing import List


__all__ = (
    'SchemaFields',
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
