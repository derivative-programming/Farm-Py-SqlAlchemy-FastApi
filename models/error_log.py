from datetime import datetime
from sqlalchemy import Index, event, BigInteger, Boolean, Column, DateTime, Float, Integer, Numeric, String, ForeignKey, Uuid, func
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
class ErrorLog(Base):
    __tablename__ = snake_case('ErrorLog')
    error_log_id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(UUIDType, unique=True, default=generate_uuid, nullable=True)
    last_change_code = Column(Integer, nullable=True)
    insert_user_id = Column(UUIDType, default=generate_uuid, nullable=True)
    last_update_user_id = Column(UUIDType, default=generate_uuid, nullable=True)
    browser_code = Column(UUIDType, default=generate_uuid,  nullable=True)
    context_code = Column(UUIDType, default=generate_uuid,  nullable=True)
    created_utc_date_time = Column(DateTime, default=datetime(1753, 1, 1), nullable=True)
    description = Column(String, default="", nullable=True)
    is_client_side_error = Column(Boolean, default=False, nullable=True)
    is_resolved = Column(Boolean, default=False, nullable=True)
    pac_id = Column(Integer, ForeignKey(snake_case('Pac') + '.pac_id'), nullable=True)
    url = Column(String, default="", nullable=True)
    pac_code_peek = UUIDType # PacID
    insert_utc_date_time = Column(DateTime, nullable=True)
    last_update_utc_date_time = Column(DateTime, nullable=True)
    #no relationsip properties. they are not updated immediately if the id prop is updated directly
    # pac = relationship('Pac', back_populates=snake_case('Pac'))
    # flavor = relationship('Flavor', back_populates=snake_case('Flavor'))
    __mapper_args__ = {
        'version_id_col': last_change_code
    }
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.error_log_id = 0
        self.code = generate_uuid()
        self.last_change_code = 0
        insert_user_id = None
        last_update_user_id = None
        self.browser_code = generate_uuid()
        self.context_code = generate_uuid()
        self.created_utc_date_time = datetime(1753, 1, 1)
        self.description = ""
        self.is_client_side_error = False
        self.is_resolved = False
        self.pac_id = 0
        self.url = ""
        self.insert_utc_date_time = datetime(1753, 1, 1)
        self.last_update_utc_date_time = datetime(1753, 1, 1)
        self.pac_code_peek = generate_uuid() # PacID
# Define the index separately from the column
# Index('index_code', ErrorLog.code)
Index('error_log_index_pac_id', ErrorLog.pac_id) #PacID
@event.listens_for(ErrorLog, 'before_insert')
def set_created_on(mapper, connection, target):
    target.insert_utc_date_time = func.now()
    target.last_update_utc_date_time = func.now()
@event.listens_for(ErrorLog, 'before_update')
def set_updated_on(mapper, connection, target):
    target.last_update_utc_date_time = func.now()
