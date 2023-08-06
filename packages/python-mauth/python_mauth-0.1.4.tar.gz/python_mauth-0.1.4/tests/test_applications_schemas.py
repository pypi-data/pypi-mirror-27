from mauth.applications.schemas import (
    ApplicationSchema,
    ApplicationAddressSchema,
    ApplicationPatternSchema,
    ApplicationPrivilegeSchema
)


class TestApplicationSchema():
    def setup(self):
        self.fields = ApplicationSchema.get_fields_names()

    def test_fields_simple_output(self):
        assert [_.name for _ in ApplicationSchema.__class_schema_nodes__] == self.fields


class TestApplicationAddressSchema():
    def setup(self):
        self.fields = ApplicationAddressSchema.get_fields_names()

    def test_fields_simple_output(self):
        assert [_.name for _ in ApplicationAddressSchema.__class_schema_nodes__] == self.fields


class TestApplicationPatternSchema():
    def setup(self):
        self.fields = ApplicationPatternSchema.get_fields_names()

    def test_fields_simple_output(self):
        assert [_.name for _ in ApplicationPatternSchema.__class_schema_nodes__] == self.fields


class TestApplicationPrivilegeSchema():
    def setup(self):
        self.fields = ApplicationPrivilegeSchema.get_fields_names()

    def test_fields_simple_output(self):
        assert [_.name for _ in ApplicationPrivilegeSchema.__class_schema_nodes__] == self.fields