# models/serialization_schema/error_log.py
"""
This module contains the ErrorLogSchema class, which is responsible
for serializing and deserializing ErrorLog objects.
"""
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import ErrorLog
class ErrorLogSchema(SQLAlchemyAutoSchema):
    """
    Schema class for serializing and deserializing ErrorLog objects.
    """
    class Meta:
        """
        Meta class for defining the schema's metadata.
        """
        model = ErrorLog
        exclude = (
            "_error_log_id",
            "_code",
            "_insert_user_id",
            "_last_update_user_id",
            "_last_change_code",
            "_insert_utc_date_time",
            "_last_update_utc_date_time",
            "_browser_code",  # browserCode
            "_context_code",  # contextCode
            "_created_utc_date_time",  # createdUTCDateTime
            "_description",  # description
            "_is_client_side_error",  # isClientSideError
            "_is_resolved",  # isResolved
            "_pac_id",  # PacID
            "_url",  # url
# endset  # noqa E122
        )
    error_log_id = fields.Int()
    code = fields.UUID()
    last_change_code = fields.Int()
    insert_user_id = fields.UUID()
    last_update_user_id = fields.UUID()
    browser_code = fields.UUID()
    context_code = fields.UUID()
    created_utc_date_time = fields.DateTime()  # (format="%Y-%m-%dT%H:%M:%S")
    description = fields.Str()
    is_client_side_error = fields.Bool()
    is_resolved = fields.Bool()
    pac_id = fields.Int()
    url = fields.Str()
    insert_utc_date_time = fields.DateTime()
    last_update_utc_date_time = fields.DateTime()
    pac_code_peek = fields.UUID()  # PacID
# endset
