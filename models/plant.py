from datetime import datetime
import uuid
from sqlalchemy import Index, event, BigInteger, Boolean, Column, DateTime, Float, Integer, Numeric, String, ForeignKey, Uuid, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from utils.common_functions import snake_case
from .base import Base  # Importing the Base from central module


class Plant(Base):
    __tablename__ = snake_case('Plant')

    plant_id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(UUID(as_uuid=True), unique=True, default=uuid.uuid4, nullable=True)
    last_change_code = Column(UUID(as_uuid=True), default=uuid.uuid4, nullable=True)
    insert_user_id = Column(UUID(as_uuid=True), default=uuid.uuid4, nullable=True)
    last_update_user_id = Column(UUID(as_uuid=True), default=uuid.uuid4, nullable=True)
    flvr_foreign_key_id = Column(Integer, ForeignKey(snake_case('Flavor') + '.id'), nullable=True)
    is_delete_allowed = Column(Boolean, default=False, nullable=True)
    is_edit_allowed = Column(Boolean, default=False, nullable=True)
    land_id = Column(Integer, ForeignKey(snake_case('Land') + '.id'), nullable=True)
    other_flavor = Column(String, default="", nullable=True)
    some_big_int_val = Column(BigInteger, default=0, nullable=True)
    some_bit_val = Column(Boolean, default=False, nullable=True)
    some_date_val = Column(DateTime, default=datetime(1753, 1, 1), nullable=True)
    some_decimal_val = Column(Numeric, default=0, nullable=True)
    some_email_address = Column(String, default="", nullable=True)
    some_float_val = Column(Float, default=0.0, nullable=True)
    some_int_val = Column(Integer, default=0, nullable=True)
    some_money_val = Column(Numeric, default=0, nullable=True)
    some_n_varchar_val = Column(String, default="", nullable=True)
    some_phone_number = Column(String, default="", nullable=True)
    some_text_val = Column(String, default="", nullable=True)
    some_uniqueidentifier_val = Column(UUID(as_uuid=True), nullable=True)
    some_utc_date_time_val = Column(DateTime, default=datetime(1753, 1, 1), nullable=True)
    some_varchar_val = Column(String, default="", nullable=True)
    flvr_foreign_key_code_peek = uuid.UUID  # FlvrForeignKeyID
    land_code_peek = uuid.UUID  # LandID
    insert_utc_date_time = Column(DateTime, default=func.now(), nullable=True)
    last_update_utc_date_time = Column(DateTime, onupdate=func.now(), nullable=True)


    #no relationsip properties. they are not updated immediately if the id prop is updated directly
    # land = relationship('Land', back_populates=snake_case('Land'))
    # flavor = relationship('Flavor', back_populates=snake_case('Flavor'))

 
    __mapper_args__ = {
        'version_id_col': last_change_code
    }


# Define the index separately from the column
Index('index_code', Plant.code)
Index('index_land_id', Plant.land_id) #LandID
Index('index_flvr_foreign_key_id', Plant.flvr_foreign_key_id) #FlvrForeignKeyID

    
@event.listens_for(Plant, 'before_insert')
def set_created_on(mapper, connection, target):
    target.insert_utc_date_time = func.now()
    target.last_update_utc_date_time = func.now()

@event.listens_for(Plant, 'before_update')
def set_updated_on(mapper, connection, target):
    target.last_update_utc_date_time = func.now()
    target.last_change_code = uuid.uuid4()