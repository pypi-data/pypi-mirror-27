import colander

from mauth.core.schemas import SchemaFields


__all__ = (
    'ProviderAccountSchema',
    'UserSchema'
)


class ProviderAccountSchema(colander.MappingSchema, SchemaFields):
    """
    Provider account serialization schema.

    Attributes:
        id (Int): Provider Account primary key.
        application (Int): Application id.
        login (String): Provider account login.
        password (String): Provider account password.
        provider_id (Int): Provider id.
        user_id (Int): Provider user id.
    """
    id = colander.SchemaNode(colander.Int(), missing=None)

    login = colander.SchemaNode(
        colander.String(), validator=colander.Length(0, 255),
        missing=''
    )
    password = colander.SchemaNode(
        colander.String(),
        validator=colander.Length(0, 255),
        missing=''
    )

    provider = colander.SchemaNode(colander.Int(), missing=None)
    user = colander.SchemaNode(colander.Int(), missing=None)
    application = colander.SchemaNode(colander.Int(), missing=None)


class UserSchema(colander.MappingSchema, SchemaFields):
    """
    User object serialization schema.

    Attributes:
        id (Int): User primary key.
        date_joined (DateTime): User date joined.
        email (String): User email.
        first_name (String): User first name.
        gender (String): User gender.
        is_active (Boolean): Whether the user is active.
        is_staff (Boolean): Whether the user is staff.
        last_name (String): User last name.
        username (String): User system username.
    """

    id = colander.SchemaNode(colander.Int(), missing=None)

    username = colander.SchemaNode(colander.String(), missing='')
    email = colander.SchemaNode(colander.String(), missing='')
    is_staff = colander.SchemaNode(colander.Boolean(), missing=False)
    is_active = colander.SchemaNode(colander.Boolean(), missing=True)
    date_joined = colander.SchemaNode(colander.DateTime(), missing=None)
    first_name = colander.SchemaNode(colander.String(), missing='')
    last_name = colander.SchemaNode(colander.String(), missing='')
    gender = colander.SchemaNode(colander.String(), missing='')
