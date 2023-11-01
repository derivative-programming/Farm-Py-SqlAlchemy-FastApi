from datetime import datetime 
from marshmallow import Schema, fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from sqlalchemy import Index, event, BigInteger, Boolean, Column, DateTime, Float, Integer, Numeric, String, ForeignKey, Uuid, func
from sqlalchemy.dialects.postgresql import UUID 
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.ext.hybrid import hybrid_property
from utils.common_functions import snake_case
from ..base import Base  # Importing the Base from central module
from models import Plant
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
 
class PlantSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Plant
    
    plant_id = fields.Int()
    code = schema_UUIDType
    last_change_code = fields.Int()
    insert_user_id = schema_UUIDType
    last_update_user_id = schema_UUIDType
    flvr_foreign_key_id = fields.Int()
    is_delete_allowed = fields.Bool()
    is_edit_allowed = fields.Bool()
    land_id = fields.Int()
    other_flavor = fields.Str()
    some_big_int_val = fields.Int()
    some_bit_val = fields.Bool()
    some_date_val = fields.Date()
    some_decimal_val = fields.Decimal(as_string=True)  # This will serialize Decimal as string
    some_email_address = fields.Str()
    some_float_val = fields.Float()
    some_int_val = fields.Int()
    some_money_val = fields.Decimal(as_string=True)  # This will serialize Decimal as string
    some_n_var_char_val = fields.Str()
    some_phone_number = fields.Str()
    some_text_val = fields.Str()
    some_uniqueidentifier_val = schema_UUIDType
    some_utc_date_time_val = fields.DateTime()
    some_var_char_val = fields.Str()
    insert_utc_date_time = fields.DateTime()
    last_update_utc_date_time = fields.DateTime()
  
    flvr_foreign_key_code_peek = schema_UUIDType  #FlvrForeignKeyID
    land_code_peek = schema_UUIDType #LandID
#endset