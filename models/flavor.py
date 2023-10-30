from datetime import datetime
import uuid
from sqlalchemy import Index, event, BigInteger, Boolean, Column, DateTime, Float, Integer, Numeric, String, ForeignKey, Uuid, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from utils.common_functions import snake_case
from .base import Base  # Importing the Base from central module
class Flavor(Base):
    __tablename__ = snake_case('Flavor')
    flavor_id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(UUID(as_uuid=True), unique=True, default=uuid.uuid4, nullable=True)
    last_change_code = Column(UUID(as_uuid=True), default=uuid.uuid4, nullable=True)
    insert_user_id = Column(UUID(as_uuid=True), default=uuid.uuid4, nullable=True)
    last_update_user_id = Column(UUID(as_uuid=True), default=uuid.uuid4, nullable=True)
    description = Column(String, default="", nullable=True)
    display_order = Column(Integer, default=0, nullable=True)
    is_active = Column(Boolean, default=False, nullable=True)
    lookup_enum_name = Column(String, default="", nullable=True)
    name = Column(String, default="", nullable=True)
    pac_id = Column(Integer, ForeignKey(snake_case('Pac') + '.id'), nullable=True)
    pac_code_peek = uuid.UUID  # PacID
    insert_utc_date_time = Column(DateTime, default=func.now(), nullable=True)
    last_update_utc_date_time = Column(DateTime, onupdate=func.now(), nullable=True)
    #no relationsip properties. they are not updated immediately if the id prop is updated directly
    # pac = relationship('Pac', back_populates=snake_case('Pac'))
    # flavor = relationship('Flavor', back_populates=snake_case('Flavor'))
    __mapper_args__ = {
        'version_id_col': last_change_code
    }
# Define the index separately from the column
Index('index_code', Flavor.code)
Index('index_pac_id', Flavor.pac_id) #PacID
@event.listens_for(Flavor, 'before_insert')
def set_created_on(mapper, connection, target):
    target.insert_utc_date_time = func.now()
    target.last_update_utc_date_time = func.now()
@event.listens_for(Flavor, 'before_update')
def set_updated_on(mapper, connection, target):
    target.last_update_utc_date_time = func.now()
    target.last_change_code = uuid.uuid4()
