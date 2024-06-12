# error_log.py
"""
    #TODO add comment
"""
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from models import ErrorLog
from services.db_config import DB_DIALECT
# Conditionally set the UUID column type
if DB_DIALECT == 'postgresql':
    schema_UUIDType = fields.UUID()
elif DB_DIALECT == 'mssql':
    schema_UUIDType = UNIQUEIDENTIFIER
else:  # This will cover SQLite, MySQL, and other databases
    schema_UUIDType = fields.Str()
class ErrorLogSchema(SQLAlchemyAutoSchema):
    """
    #TODO add comment
    """
    class Meta:
        model = ErrorLog
    error_log_id = fields.Int()
    code = schema_UUIDType
    last_change_code = fields.Int()
    insert_user_id = schema_UUIDType
    last_update_user_id = schema_UUIDType
    browser_code = schema_UUIDType
    context_code = schema_UUIDType
    created_utc_date_time = fields.DateTime()  # (format="%Y-%m-%dT%H:%M:%S")
    description = fields.Str()
    is_client_side_error = fields.Bool()
    is_resolved = fields.Bool()
    pac_id = fields.Int()
    url = fields.Str()
    insert_utc_date_time = fields.DateTime()
    last_update_utc_date_time = fields.DateTime()
    pac_code_peek = schema_UUIDType  # PacID
# endset
