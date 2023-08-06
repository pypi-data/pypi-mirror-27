import colander

from mauth.core.schemas import SchemaFields


__all__ = (
    'ApplicationSchema',
    'ApplicationPatternSchema',
    'ApplicationAddressSchema'
)


class ApplicationSchema(colander.MappingSchema, SchemaFields):
    """
    Application object serialization object.

    Attributes:
        api_key (TYPE): Description
        auth_status (TYPE): Description
        client_id (TYPE): Description
        has_referrals (TYPE): Description
        internal_type (TYPE): Description
        title (TYPE): Description
        url (TYPE): Description
    """
    id = colander.SchemaNode(colander.Int(), missing=None)
    title = colander.SchemaNode(
        colander.String(), validator=colander.Length(0, 255),
        missing=''
    )
    url = colander.SchemaNode(
        colander.String(allow_empty=True),
        validator=colander.Length(0, 255),
        missing=''
    )
    client_id = colander.SchemaNode(colander.String(), missing='')
    internal_type = colander.SchemaNode(colander.String(), missing='')
    auth_status = colander.SchemaNode(colander.String(), missing='')
    has_referrals = colander.SchemaNode(colander.Boolean(), missing=True)
    api_key = colander.SchemaNode(colander.String(), missing='')


class ApplicationPatternSchema(colander.MappingSchema, SchemaFields):
    """
    Application's pattern serialization schema.

    Attributes:
        application_id (TYPE): Description
        id (TYPE): Description
        regex (TYPE): Description
    """

    id = colander.SchemaNode(colander.Int(), missing=None)

    application_id = colander.SchemaNode(colander.Int(), missing=None)
    regex = colander.SchemaNode(colander.String(), missing='')


class ApplicationAddressSchema(colander.MappingSchema, SchemaFields):
    """
    Application's address serialization schema.

    Attributes:
        address (TYPE): Description
        application_id (TYPE): Description
        id (TYPE): Description
        mask (TYPE): Description
    """

    id = colander.SchemaNode(colander.Int(), missing=None)

    application_id = colander.SchemaNode(colander.Int(), missing=None)
    address = colander.SchemaNode(colander.String(), missing='')
    mask = colander.SchemaNode(colander.Int(), missing=None)
