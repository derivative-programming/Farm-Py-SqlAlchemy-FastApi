# models/serialization_schema/dyna_flow_task_type.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import

"""
This module contains the
DynaFlowTaskTypeSchema
class, which is responsible
for serializing and deserializing
DynaFlowTaskType objects.
"""

from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from models import DynaFlowTaskType


class DynaFlowTaskTypeSchema(SQLAlchemyAutoSchema):
    """
    Schema class for serializing and deserializing
    DynaFlowTaskType objects.
    """

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Meta class for defining the schema's metadata.
        """

        model = DynaFlowTaskType
        exclude = (
            "_dyna_flow_task_type_id",
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
            "_max_retry_count",  # maxRetryCount
            "_name",  # name
            "_pac_id",  # PacID
# endset  # noqa E122
        )

    dyna_flow_task_type_id = fields.Int()
    code = fields.UUID()
    last_change_code = fields.Int()
    insert_user_id = fields.UUID()
    last_update_user_id = fields.UUID()
    description = fields.Str()
    display_order = fields.Int()
    is_active = fields.Bool()
    lookup_enum_name = fields.Str()
    max_retry_count = fields.Int()
    name = fields.Str()
    pac_id = fields.Int()
    insert_utc_date_time = fields.DateTime()
    last_update_utc_date_time = fields.DateTime()
    pac_code_peek = fields.UUID()  # PacID
