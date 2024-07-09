# models/serialization_schema/df_maintenance.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import

"""
This module contains the
DFMaintenanceSchema
class, which is responsible
for serializing and deserializing
DFMaintenance objects.
"""

from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from models import DFMaintenance


class DFMaintenanceSchema(SQLAlchemyAutoSchema):
    """
    Schema class for serializing and deserializing
    DFMaintenance objects.
    """

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Meta class for defining the schema's metadata.
        """

        model = DFMaintenance
        exclude = (
            "_df_maintenance_id",
            "_code",
            "_insert_user_id",
            "_last_update_user_id",
            "_last_change_code",
            "_insert_utc_date_time",
            "_last_update_utc_date_time",
            "_is_paused",  # isPaused
            "_is_scheduled_df_process_request_completed",  # isScheduledDFProcessRequestCompleted
            "_is_scheduled_df_process_request_started",  # isScheduledDFProcessRequestStarted
            "_last_scheduled_df_process_request_utc_date_time",  # lastScheduledDFProcessRequestUTCDateTime
            "_next_scheduled_df_process_request_utc_date_time",  # nextScheduledDFProcessRequestUTCDateTime
            "_pac_id",  # PacID
            "_paused_by_username",  # pausedByUsername
            "_paused_utc_date_time",  # pausedUTCDateTime
            "_scheduled_df_process_request_processor_identifier",  # scheduledDFProcessRequestProcessorIdentifier
# endset  # noqa E122
        )

    df_maintenance_id = fields.Int()
    code = fields.UUID()
    last_change_code = fields.Int()
    insert_user_id = fields.UUID()
    last_update_user_id = fields.UUID()
    is_paused = fields.Bool()
    is_scheduled_df_process_request_completed = fields.Bool()
    is_scheduled_df_process_request_started = fields.Bool()
    last_scheduled_df_process_request_utc_date_time = \
        fields.DateTime()  # (format="%Y-%m-%dT%H:%M:%S")
    next_scheduled_df_process_request_utc_date_time = \
        fields.DateTime()  # (format="%Y-%m-%dT%H:%M:%S")
    pac_id = fields.Int()
    paused_by_username = fields.Str()
    paused_utc_date_time = \
        fields.DateTime()  # (format="%Y-%m-%dT%H:%M:%S")
    scheduled_df_process_request_processor_identifier = fields.Str()
    insert_utc_date_time = fields.DateTime()
    last_update_utc_date_time = fields.DateTime()
    pac_code_peek = fields.UUID()  # PacID
