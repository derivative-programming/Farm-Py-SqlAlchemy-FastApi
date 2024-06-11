# plant.py

"""
    #TODO add comment
"""

from datetime import datetime, date
from marshmallow import Schema, fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from sqlalchemy import Index, event, BigInteger, Boolean, Column, Date, DateTime, Float, Integer, Numeric, String, ForeignKey, Uuid, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.ext.hybrid import hybrid_property
from utils.common_functions import snake_case
from .base import Base,EncryptedType  # Importing the Base from central module
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from services.db_config import db_dialect,generate_uuid
import models.constants.plant as plant_constants

# Conditionally set the UUID column type
if db_dialect == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif db_dialect == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  # This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)



class Plant(Base):
    __tablename__ = 'farm_' + snake_case('Plant')

    plant_id = Column('plant_id', Integer, primary_key=True, autoincrement=True)
    code = Column('code', UUIDType, unique=True, default=generate_uuid, nullable=True)
    last_change_code = Column('last_change_code', Integer, nullable=True)
    insert_user_id = Column('insert_user_id', UUIDType, default=generate_uuid, nullable=True)
    last_update_user_id = Column('last_update_user_id', UUIDType, default=generate_uuid, nullable=True)
    flvr_foreign_key_id = Column('flvr_foreign_key_id',
                                 Integer,
                                 ForeignKey('farm_' + snake_case('Flavor') + '.flavor_id'),
                                index=plant_constants.flvr_foreign_key_id_calculatedIsDBColumnIndexed,
                                 nullable=True)
    is_delete_allowed = Column('is_delete_allowed',
                               Boolean,
                               default=False,
                                index=plant_constants.is_delete_allowed_calculatedIsDBColumnIndexed,
                               nullable=True)
    is_edit_allowed = Column('is_edit_allowed',
                             Boolean,
                             default=False,
                                index=plant_constants.is_edit_allowed_calculatedIsDBColumnIndexed,
                             nullable=True)
    land_id = Column('land_id',
                     Integer,
                     ForeignKey('farm_' + snake_case('Land') + '.land_id'),
                     index=plant_constants.land_id_calculatedIsDBColumnIndexed,
                     nullable=True)
    other_flavor = Column('other_flavor',
                            ##GENIF[isEncrypted=false]Start
                            String,
                            ##GENIF[isEncrypted=false]End
                            ##GENIF[isEncrypted=true]Start
                            ##GENREMOVECOMMENTEncryptedType(),
                            ##GENIF[isEncrypted=true]End
                          default="",
                                index=plant_constants.other_flavor_calculatedIsDBColumnIndexed,
                          nullable=True)
    some_big_int_val = Column('some_big_int_val',
                              BigInteger,
                              default=0,
                                index=plant_constants.some_big_int_val_calculatedIsDBColumnIndexed,
                              nullable=True)
    some_bit_val = Column('some_bit_val',
                          Boolean,
                          default=False,
                                index=plant_constants.some_bit_val_calculatedIsDBColumnIndexed,
                          nullable=True)
    some_date_val = Column('some_date_val',
                           Date,
                           default=date(1753, 1, 1),
                                index=plant_constants.some_date_val_calculatedIsDBColumnIndexed,
                           nullable=True)
    some_decimal_val = Column('some_decimal_val',
                              Numeric(precision=18, scale=6),
                              default=0,
                                index=plant_constants.some_decimal_val_calculatedIsDBColumnIndexed,
                              nullable=True)
    some_email_address = Column('some_email_address',
                                 ##GENIF[isEncrypted=false]Start
                                 String,
                                 ##GENIF[isEncrypted=false]End
                                 ##GENIF[isEncrypted=true]Start
                                 ##GENREMOVECOMMENTEncryptedType(),
                                 ##GENIF[isEncrypted=true]End
                                default="",
                                index=plant_constants.some_email_address_calculatedIsDBColumnIndexed,
                                nullable=True)
    some_float_val = Column('some_float_val',
                            Float,
                            default=0.0,
                                index=plant_constants.some_float_val_calculatedIsDBColumnIndexed,
                            nullable=True)
    some_int_val = Column('some_int_val',
                          Integer,
                          default=0,
                                index=plant_constants.some_int_val_calculatedIsDBColumnIndexed,
                          nullable=True)
    some_money_val = Column('some_money_val',
                            Numeric(precision=18, scale=2),
                            default=0,
                                index=plant_constants.some_money_val_calculatedIsDBColumnIndexed,
                            nullable=True)
    some_n_var_char_val = Column('some_n_var_char_val',
                                 ##GENIF[isEncrypted=false]Start
                                 String,
                                 ##GENIF[isEncrypted=false]End
                                 ##GENIF[isEncrypted=true]Start
                                 ##GENREMOVECOMMENTEncryptedType(),
                                 ##GENIF[isEncrypted=true]End
                                 default="",
                                index=plant_constants.some_n_var_char_val_calculatedIsDBColumnIndexed,
                                 nullable=True)
    some_phone_number = Column('some_phone_number',
                                 ##GENIF[isEncrypted=false]Start
                                 String,
                                 ##GENIF[isEncrypted=false]End
                                 ##GENIF[isEncrypted=true]Start
                                 ##GENREMOVECOMMENTEncryptedType(),
                                 ##GENIF[isEncrypted=true]End
                               default="",
                                index=plant_constants.some_phone_number_calculatedIsDBColumnIndexed,
                               nullable=True)
    some_text_val = Column('some_text_val',
                           String,
                           default="",
                                index=plant_constants.some_text_val_calculatedIsDBColumnIndexed,
                           nullable=True)
    some_uniqueidentifier_val = Column('some_uniqueidentifier_val',
                                       UUIDType,
                                       default=generate_uuid,
                                index=plant_constants.some_uniqueidentifier_val_calculatedIsDBColumnIndexed,
                                       nullable=True)
    some_utc_date_time_val = Column('some_utc_date_time_val',
                                    DateTime,
                                    default=datetime(1753, 1, 1),
                                index=plant_constants.some_utc_date_time_val_calculatedIsDBColumnIndexed,
                                    nullable=True)
    some_var_char_val = Column('some_var_char_val',
                                 ##GENIF[isEncrypted=false]Start
                                 String,
                                 ##GENIF[isEncrypted=false]End
                                 ##GENIF[isEncrypted=true]Start
                                 ##GENREMOVECOMMENTEncryptedType(),
                                 ##GENIF[isEncrypted=true]End
                               default="",
                                index=plant_constants.some_var_char_val_calculatedIsDBColumnIndexed,
                               nullable=True)
    flvr_foreign_key_code_peek = UUIDType  # FlvrForeignKeyID
    land_code_peek = UUIDType # LandID
    insert_utc_date_time = Column('insert_utc_date_time', DateTime, nullable=True)
    last_update_utc_date_time = Column('last_update_utc_date_time', DateTime, nullable=True)


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

    @staticmethod
    def property_list():
        result = [
            "flvr_foreign_key_id",
            "is_delete_allowed",
            "is_edit_allowed",
            "land_id",
            "other_flavor",
            "some_big_int_val",
            "some_bit_val",
            "some_date_val",
            "some_decimal_val",
            "some_email_address",
            "some_float_val",
            "some_int_val",
            "some_money_val",
            "some_n_var_char_val",
            "some_phone_number",
            "some_text_val",
            "some_uniqueidentifier_val",
            "some_utc_date_time_val",
            "some_var_char_val",
#endset
            "code"
            ]
        return result

# Define the index separately from the column
# Index('index_code', Plant.code)
# Index('farm_plant_index_land_id', Plant.land_id)  # LandID
# Index('farm_plant_index_flvr_foreign_key_id', Plant.flvr_foreign_key_id)  # FlvrForeignKeyID


@event.listens_for(Plant, 'before_insert')
def set_created_on(mapper, connection, target):
    target.insert_utc_date_time = datetime.utcnow()
    target.last_update_utc_date_time = datetime.utcnow()

@event.listens_for(Plant, 'before_update')
def set_updated_on(mapper, connection, target):
    target.last_update_utc_date_time = datetime.utcnow()
