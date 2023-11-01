from datetime import datetime, date 
from marshmallow import Schema, fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from sqlalchemy import Index, event, BigInteger, Boolean, Column, Date, DateTime, Float, Integer, Numeric, String, ForeignKey, Uuid, func
from sqlalchemy.dialects.postgresql import UUID 
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.ext.hybrid import hybrid_property
from utils.common_functions import snake_case
from .base import Base  # Importing the Base from central module
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


class Plant(Base):
    __tablename__ = snake_case('Plant')

    plant_id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(UUIDType, unique=True, default=generate_uuid, nullable=True)
    last_change_code = Column(Integer, nullable=True)
    insert_user_id = Column(UUIDType, default=generate_uuid, nullable=True)
    last_update_user_id = Column(UUIDType, default=generate_uuid, nullable=True)
    flvr_foreign_key_id = Column(Integer, ForeignKey(snake_case('Flavor') + '.flavor_id'), nullable=True)
    is_delete_allowed = Column(Boolean, default=False, nullable=True)
    is_edit_allowed = Column(Boolean, default=False, nullable=True)
    land_id = Column(Integer, ForeignKey(snake_case('Land') + '.land_id'), nullable=True)
    other_flavor = Column(String, default="", nullable=True)
    some_big_int_val = Column(BigInteger, default=0, nullable=True)
    some_bit_val = Column(Boolean, default=False, nullable=True)
    some_date_val = Column(Date, default=date(1753, 1, 1), nullable=True)
    some_decimal_val = Column(Numeric(precision=18, scale=6), default=0, nullable=True)
    some_email_address = Column(String, default="", nullable=True)
    some_float_val = Column(Float, default=0.0, nullable=True)
    some_int_val = Column(Integer, default=0, nullable=True)
    some_money_val = Column(Numeric(precision=18, scale=2), default=0, nullable=True)
    some_n_var_char_val = Column(String, default="", nullable=True)
    some_phone_number = Column(String, default="", nullable=True)
    some_text_val = Column(String, default="", nullable=True)
    some_uniqueidentifier_val = Column(UUIDType, default=generate_uuid,  nullable=True)
    some_utc_date_time_val = Column(DateTime, default=datetime(1753, 1, 1), nullable=True)
    some_var_char_val = Column(String, default="", nullable=True)
    flvr_foreign_key_code_peek = UUIDType  # FlvrForeignKeyID
    land_code_peek = UUIDType # LandID
    insert_utc_date_time = Column(DateTime, nullable=True)
    last_update_utc_date_time = Column(DateTime, nullable=True)


    #no relationsip properties. they are not updated immediately if the id prop is updated directly
    # land = relationship('Land', back_populates=snake_case('Land'))
    # flavor = relationship('Flavor', back_populates=snake_case('Flavor'))
 
    __mapper_args__ = {
        'version_id_col': last_change_code
    }

    
    def __init__(self, **kwargs):
        super().__init__(**kwargs) 

        self.code = kwargs.get('code', generate_uuid())
        self.last_change_code = kwargs.get('last_change_code', 0)
        self.insert_user_id = kwargs.get('insert_user_id', None)
        self.last_update_user_id = kwargs.get('last_update_user_id', None)
        self.flvr_foreign_key_id = kwargs.get('flvr_foreign_key_id', 0)
        self.is_delete_allowed = kwargs.get('is_delete_allowed', False)
        self.is_edit_allowed = kwargs.get('is_edit_allowed', False)
        self.land_id = kwargs.get('land_id', 0)
        self.other_flavor = kwargs.get('other_flavor', "")
        self.some_big_int_val = kwargs.get('some_big_int_val', 0)
        self.some_bit_val = kwargs.get('some_bit_val', False)
        self.some_date_val = kwargs.get('some_date_val', date(1753, 1, 1))
        self.some_decimal_val = kwargs.get('some_decimal_val', 0)
        self.some_email_address = kwargs.get('some_email_address', "")
        self.some_float_val = kwargs.get('some_float_val', 0.0)
        self.some_int_val = kwargs.get('some_int_val', 0)
        self.some_money_val = kwargs.get('some_money_val', 0)
        self.some_n_var_char_val = kwargs.get('some_n_var_char_val', "")
        self.some_phone_number = kwargs.get('some_phone_number', "")
        self.some_text_val = kwargs.get('some_text_val', "")
        self.some_uniqueidentifier_val = kwargs.get('some_uniqueidentifier_val', generate_uuid())
        self.some_utc_date_time_val = kwargs.get('some_utc_date_time_val', datetime(1753, 1, 1))
        self.some_var_char_val = kwargs.get('some_var_char_val', "")
        self.insert_utc_date_time = kwargs.get('insert_utc_date_time', datetime(1753, 1, 1))
        self.last_update_utc_date_time = kwargs.get('last_update_utc_date_time', datetime(1753, 1, 1))
#endset
        self.flvr_foreign_key_code_peek = kwargs.get('flvr_foreign_key_code_peek', generate_uuid()) # FlvrForeignKeyID
        self.land_code_peek = kwargs.get('land_code_peek', generate_uuid())# LandID
#endset 

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