from mauth.users.schemas import (
    ProviderAccountSchema,
    UserSchema
)


class TestProviderAccountSchema():
    def setup(self):
        self.fields = ProviderAccountSchema.get_fields_names()

    def test_fields_simple_output(self):
        assert [_.name for _ in ProviderAccountSchema.__class_schema_nodes__] == self.fields


class TestUserSchema():
    def setup(self):
        self.fields = UserSchema.get_fields_names()

    def test_fields_simple_output(self):
        assert [_.name for _ in UserSchema.__class_schema_nodes__] == self.fields
