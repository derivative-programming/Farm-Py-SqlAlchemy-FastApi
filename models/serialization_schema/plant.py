# plant.py

"""
    #TODO add comment
"""

from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from models import Plant
from services.db_config import DB_DIALECT

# Conditionally set the UUID column type
if DB_DIALECT == 'postgresql':
    schema_UUIDType = fields.UUID()
elif DB_DIALECT == 'mssql':
    schema_UUIDType = UNIQUEIDENTIFIER
else:  # This will cover SQLite, MySQL, and other databases
    schema_UUIDType = fields.Str()


class PlantSchema(SQLAlchemyAutoSchema):
    """
    #TODO add comment
    """

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
    some_decimal_val = fields.Decimal(as_string=True)
    some_email_address = fields.Str()
    some_float_val = fields.Float()
    some_int_val = fields.Int()
    some_money_val = fields.Decimal(as_string=True)
    some_n_var_char_val = fields.Str()
    some_phone_number = fields.Str()
    some_text_val = fields.Str()
    some_uniqueidentifier_val = schema_UUIDType
    some_utc_date_time_val = fields.DateTime()  # (format="%Y-%m-%dT%H:%M:%S")
    some_var_char_val = fields.Str()
    insert_utc_date_time = fields.DateTime()
    last_update_utc_date_time = fields.DateTime()

    flvr_foreign_key_code_peek = schema_UUIDType   # FlvrForeignKeyID
    land_code_peek = schema_UUIDType  # LandID
# endset
