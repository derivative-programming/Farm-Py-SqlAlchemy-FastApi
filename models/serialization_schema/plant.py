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
    UUIDType = UUID(as_uuid=True)
elif db_dialect == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  # This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)
 
class PlantSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Plant
    
    plant_id = fields.Int()
    code = fields.UUID()
    last_change_code = fields.Int()
    insert_user_id = fields.UUID()
    last_update_user_id = fields.UUID()
    flvr_foreign_key_id = fields.Int()
    is_delete_allowed = fields.Bool()
    is_edit_allowed = fields.Bool()
    land_id = fields.Int()
    other_flavor = fields.Str()
    some_big_int_val = fields.Int()
    some_bit_val = fields.Bool()
    some_date_val = fields.DateTime()
    some_decimal_val = fields.Decimal(as_string=True)  # This will serialize Decimal as string
    some_email_address = fields.Str()
    some_float_val = fields.Float()
    some_int_val = fields.Int()
    some_money_val = fields.Decimal(as_string=True)  # This will serialize Decimal as string
    some_n_var_char_val = fields.Str()
    some_phone_number = fields.Str()
    some_text_val = fields.Str()
    some_uniqueidentifier_val = fields.UUID()
    some_utc_date_time_val = fields.DateTime()
    some_var_char_val = fields.Str()
    insert_utc_date_time = fields.DateTime()
    last_update_utc_date_time = fields.DateTime()
 

# Define the index separately from the column
# Index('index_code', Plant.code)
Index('plant_index_land_id', Plant.land_id) #LandID
Index('plant_index_flvr_foreign_key_id', Plant.flvr_foreign_key_id) #FlvrForeignKeyID

    
@event.listens_for(Plant, 'before_insert')
def set_created_on(mapper, connection, target):
    target.insert_utc_date_time = func.now()
    target.last_update_utc_date_time = func.now()

@event.listens_for(Plant, 'before_update')
def set_updated_on(mapper, connection, target):
    target.last_update_utc_date_time = func.now() 