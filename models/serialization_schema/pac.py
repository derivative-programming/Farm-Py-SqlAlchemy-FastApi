# models/serialization_schema/pac.py
"""
This module contains the PacSchema class, which is responsible
for serializing and deserializing Pac objects.
"""
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import Pac
class PacSchema(SQLAlchemyAutoSchema):
    """
    Schema class for serializing and deserializing Pac objects.
    """
    class Meta:
        """
        Meta class for defining the schema's metadata.
        """
        model = Pac
        exclude = (
            "_pac_id",
            "_code",
            "_insert_user_id",
            "_last_update_user_id",
            "_last_change_code",
            "_insert_utc_date_time",
            "_last_update_utc_date_time",
            "_description",  # description
            "_display_order",  # displayOrder
            "_is_active",  # isActive
            "_lookup_enum_name",  # lookupEnumName
            "_name",  # name
# endset  # noqa E122
        )
    pac_id = fields.Int()
    code = fields.UUID()
    last_change_code = fields.Int()
    insert_user_id = fields.UUID()
    last_update_user_id = fields.UUID()
    description = fields.Str()
    display_order = fields.Int()
    is_active = fields.Bool()
    lookup_enum_name = fields.Str()
    name = fields.Str()
    insert_utc_date_time = fields.DateTime()
    last_update_utc_date_time = fields.DateTime()

# endset
