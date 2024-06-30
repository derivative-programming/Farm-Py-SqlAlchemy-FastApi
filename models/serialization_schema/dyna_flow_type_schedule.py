# models/serialization_schema/dyna_flow_type_schedule.py
# pylint: disable=unused-import

"""
This module contains the
DynaFlowTypeScheduleSchema
class, which is responsible
for serializing and deserializing
DynaFlowTypeSchedule objects.
"""

from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import DynaFlowTypeSchedule


class DynaFlowTypeScheduleSchema(SQLAlchemyAutoSchema):
    """
    Schema class for serializing and deserializing
    DynaFlowTypeSchedule objects.
    """

    class Meta:
        """
        Meta class for defining the schema's metadata.
        """

        model = DynaFlowTypeSchedule
        exclude = (
            "_dyna_flow_type_schedule_id",
            "_code",
            "_insert_user_id",
            "_last_update_user_id",
            "_last_change_code",
            "_insert_utc_date_time",
            "_last_update_utc_date_time",
            "_dyna_flow_type_id",  # dynaFlowTypeID
            "_frequency_in_hours",  # frequencyInHours
            "_is_active",  # isActive
            "_last_utc_date_time",  # lastUTCDateTime
            "_next_utc_date_time",  # nextUTCDateTime
            "_pac_id",  # PacID
# endset  # noqa E122
        )

    dyna_flow_type_schedule_id = fields.Int()
    code = fields.UUID()
    last_change_code = fields.Int()
    insert_user_id = fields.UUID()
    last_update_user_id = fields.UUID()
    dyna_flow_type_id = fields.Int()
    frequency_in_hours = fields.Int()
    is_active = fields.Bool()
    last_utc_date_time = \
        fields.DateTime()  # (format="%Y-%m-%dT%H:%M:%S")
    next_utc_date_time = \
        fields.DateTime()  # (format="%Y-%m-%dT%H:%M:%S")
    pac_id = fields.Int()
    insert_utc_date_time = fields.DateTime()
    last_update_utc_date_time = fields.DateTime()
    dyna_flow_type_code_peek = fields.UUID()   # DynaFlowTypeID
    pac_code_peek = fields.UUID()  # PacID
