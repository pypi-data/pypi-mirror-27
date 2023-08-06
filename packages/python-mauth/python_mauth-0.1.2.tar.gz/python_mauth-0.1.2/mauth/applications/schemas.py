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
        api_key (Int): Application primary key.
        auth_status (String): Application authentication status.
        client_id (String): Application client id.
        has_referrals (Boolean): Application has referral program or not.
        internal_type (String): Application internal type.
        title (String): Application title.
        url (String): Application url for internal applications.
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
        id (Int): Application pattern primary key.
        application_id (Int): Application pattern application id(FK).
        regex (String): Application regex or full url to the server.
    """

    id = colander.SchemaNode(colander.Int(), missing=None)

    application_id = colander.SchemaNode(colander.Int(), missing=None)
    regex = colander.SchemaNode(colander.String(), missing='')


class ApplicationAddressSchema(colander.MappingSchema, SchemaFields):
    """
    Application's address serialization schema.

    Attributes:
        id (Int): Application address primary key
        application_id (Int): Application address application id.
        address (String): Application IP address.
        mask (Int): Application IP address mask
    """

    id = colander.SchemaNode(colander.Int(), missing=None)

    application_id = colander.SchemaNode(colander.Int(), missing=None)
    address = colander.SchemaNode(colander.String(), missing='')
    mask = colander.SchemaNode(colander.Int(), missing=None)
