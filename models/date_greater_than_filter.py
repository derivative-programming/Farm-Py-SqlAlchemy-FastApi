import uuid
from sqlalchemy import Index, event, BigInteger, Boolean, Column, DateTime, Float, Integer, Numeric, String, ForeignKey, Uuid, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from utils.common_functions import snake_case
Base = declarative_base()
class DateGreaterThanFilter(Base):
    __tablename__ = snake_case('DateGreaterThanFilter')
    date_greater_than_filter_id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(UUID(as_uuid=True), unique=True, default=uuid.uuid4)
    last_change_code = Column(UUID(as_uuid=True))
    day_count = Column(Integer)
    description = Column(String)
    display_order = Column(Integer)
    is_active = Column(Boolean)
    lookup_enum_name = Column(String)
    name = Column(String)
    pac_id = Column(Integer, ForeignKey(snake_case('Pac') + '.id'))
    pac_code_peek = uuid.UUID #PacID
    insert_utc_date_time = Column(DateTime, default=func.now())
    last_update_utc_date_time = Column(DateTime, onupdate=func.now())
    #no relationsip properties. they are not updated immediately if the id prop is updated directly
    # pac = relationship('Pac', back_populates=snake_case('Pac'))
    # flavor = relationship('Flavor', back_populates=snake_case('Flavor'))
    __mapper_args__ = {
        'version_id_col': last_change_code
    }
# Define the index separately from the column
Index('index_code', DateGreaterThanFilter.code)
Index('index_pac_id', DateGreaterThanFilter.pac_id) #PacID
@event.listens_for(DateGreaterThanFilter, 'before_insert')
def set_created_on(mapper, connection, target):
    target.insert_utc_date_time = func.now()
@event.listens_for(DateGreaterThanFilter, 'before_update')
def set_updated_on(mapper, connection, target):
    target.last_update_utc_date_time = func.now()
    target.last_change_code = uuid.uuid4()
