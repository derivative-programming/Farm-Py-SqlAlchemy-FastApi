# models/serialization_schema/date_greater_than_filter.py
# pylint: disable=unused-import

"""
This module contains the
DateGreaterThanFilterSchema
class, which is responsible
for serializing and deserializing
DateGreaterThanFilter objects.
"""

from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import DateGreaterThanFilter


class DateGreaterThanFilterSchema(SQLAlchemyAutoSchema):
    """
    Schema class for serializing and deserializing
    DateGreaterThanFilter objects.
    """

    class Meta:
        """
        Meta class for defining the schema's metadata.
        """

        model = DateGreaterThanFilter
        exclude = (
            "_date_greater_than_filter_id",
            "_code",
            "_insert_user_id",
            "_last_update_user_id",
            "_last_change_code",
            "_insert_utc_date_time",
            "_last_update_utc_date_time",
            "_day_count",  # dayCount
            "_description",  # description
            "_display_order",  # displayOrder
            "_is_active",  # isActive
            "_lookup_enum_name",  # lookupEnumName
            "_name",  # name
            "_pac_id",  # PacID
# endset  # noqa E122
        )

    date_greater_than_filter_id = fields.Int()
    code = fields.UUID()
    last_change_code = fields.Int()
    insert_user_id = fields.UUID()
    last_update_user_id = fields.UUID()
    day_count = fields.Int()
    description = fields.Str()
    display_order = fields.Int()
    is_active = fields.Bool()
    lookup_enum_name = fields.Str()
    name = fields.Str()
    pac_id = fields.Int()
    insert_utc_date_time = fields.DateTime()
    last_update_utc_date_time = fields.DateTime()
    pac_code_peek = fields.UUID()  # PacID
