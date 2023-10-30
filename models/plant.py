import uuid
from sqlalchemy import Index, event, BigInteger, Boolean, Column, DateTime, Float, Integer, Numeric, String, ForeignKey, Uuid, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from utils.common_functions import snake_case

Base = declarative_base()

class Plant(Base):
    __tablename__ = snake_case('Plant')

    plant_id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(UUID(as_uuid=True), unique=True, default=uuid.uuid4)
    last_change_code = Column(UUID(as_uuid=True))
    flvr_foreign_key_id = Column(Integer, ForeignKey(snake_case('Flavor') + '.id'))
    is_delete_allowed = Column(Boolean)
    is_edit_allowed = Column(Boolean)
    land_id = Column(Integer, ForeignKey(snake_case('Land') + '.id'))
    other_flavor = Column(String)
    some_big_int_val = Column(BigInteger)
    some_bit_val = Column(Boolean)
    some_date_val = Column(DateTime)
    some_decimal_val = Column(Numeric)
    some_email_address = Column(String)
    some_float_val = Column(Float)
    some_int_val = Column(Integer)
    some_money_val = Column(Numeric)
    some_n_varchar_val = Column(String)
    some_phone_number = Column(String)
    some_text_val = Column(String)
    some_uniqueidentifier_val = Column(UUID(as_uuid=True))
    some_utc_date_time_val = Column(DateTime)
    some_varchar_val = Column(String)
    flvr_foreign_key_code_peek = uuid.UUID #FlvrForeignKeyID
    land_code_peek = uuid.UUID #LandID
    insert_utc_date_time = Column(DateTime, default=func.now())
    last_update_utc_date_time = Column(DateTime, onupdate=func.now())

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

@event.listens_for(Plant, 'before_update')
def set_updated_on(mapper, connection, target):
    target.last_update_utc_date_time = func.now()
    target.last_change_code = uuid.uuid4()