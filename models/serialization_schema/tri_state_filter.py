from datetime import datetime
from marshmallow import Schema, fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from sqlalchemy import Index, event, BigInteger, Boolean, Column, DateTime, Float, Integer, Numeric, String, ForeignKey, Uuid, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.ext.hybrid import hybrid_property
from utils.common_functions import snake_case
from ..base import Base  # Importing the Base from central module
from models import TriStateFilter
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from services.db_config import db_dialect,generate_uuid
# Conditionally set the UUID column type
if db_dialect == 'postgresql':
    schema_UUIDType = fields.UUID()
elif db_dialect == 'mssql':
    schema_UUIDType = UNIQUEIDENTIFIER
else:  # This will cover SQLite, MySQL, and other databases
    schema_UUIDType = fields.Str()
class TriStateFilterSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = TriStateFilter
    tri_state_filter_id = fields.Int()
    code = schema_UUIDType
    last_change_code = fields.Int()
    insert_user_id = schema_UUIDType
    last_update_user_id = schema_UUIDType
    description = fields.Str()
    display_order = fields.Int()
    is_active = fields.Bool()
    lookup_enum_name = fields.Str()
    name = fields.Str()
    pac_id = fields.Int()
    state_int_value = fields.Int()
    insert_utc_date_time = fields.DateTime()
    last_update_utc_date_time = fields.DateTime()
    pac_code_peek = schema_UUIDType #PacID
