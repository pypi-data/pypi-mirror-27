import colander


__all__ = (
    'SchemaFields',
)


class SchemaFields():

    @classmethod
    def get_fields_names(cls):
        # TODO: add cache in _fields
        cls._fields = []

        for attr in cls.__class_schema_nodes__:
            if isinstance(attr, colander.SchemaNode):
                cls._fields.append(attr)

        return cls._fields
