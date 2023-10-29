import uuid
from sqlalchemy import Index, event, BigInteger, Boolean, Column, DateTime, Float, Integer, Numeric, String, ForeignKey, Uuid, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from utils.common_functions import snake_case
Base = declarative_base()
class ErrorLog(Base):
    __tablename__ = snake_case('ErrorLog')
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(UUID(as_uuid=True), unique=True, default=uuid.uuid4)
    last_change_code = Column(UUID(as_uuid=True))
    browser_code = Column(UUID(as_uuid=True))
    context_code = Column(UUID(as_uuid=True))
    created_utc_date_time = Column(DateTime)
    description = Column(String)
    is_client_side_error = Column(Boolean)
    is_resolved = Column(Boolean)
    pac_id = Column(Integer, ForeignKey(snake_case('Pac') + '.id'))
    url = Column(String)
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
Index('index_code', ErrorLog.code)
Index('index_pac_id', ErrorLog.pac_id) #PacID
@event.listens_for(ErrorLog, 'before_insert')
def set_created_on(mapper, connection, target):
    target.insert_utc_date_time = func.now()
@event.listens_for(ErrorLog, 'before_update')
def set_updated_on(mapper, connection, target):
    target.last_update_utc_date_time = func.now()
    target.last_change_code = uuid.uuid4()
