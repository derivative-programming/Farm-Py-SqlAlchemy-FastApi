# models/serialization_schema/organization.py
# pylint: disable=unused-import

"""
This module contains the
OrganizationSchema
class, which is responsible
for serializing and deserializing
Organization objects.
"""

from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import Organization


class OrganizationSchema(SQLAlchemyAutoSchema):
    """
    Schema class for serializing and deserializing
    Organization objects.
    """

    class Meta:
        """
        Meta class for defining the schema's metadata.
        """

        model = Organization
        exclude = (
            "_organization_id",
            "_code",
            "_insert_user_id",
            "_last_update_user_id",
            "_last_change_code",
            "_insert_utc_date_time",
            "_last_update_utc_date_time",
            "_name",  # name
            "_tac_id",  # TacID
# endset  # noqa E122
        )

    organization_id = fields.Int()
    code = fields.UUID()
    last_change_code = fields.Int()
    insert_user_id = fields.UUID()
    last_update_user_id = fields.UUID()
    name = fields.Str()
    tac_id = fields.Int()
    insert_utc_date_time = fields.DateTime()
    last_update_utc_date_time = fields.DateTime()
    tac_code_peek = fields.UUID()  # TacID
