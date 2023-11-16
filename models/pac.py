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
import models.constants.pac as pac_constants
# Conditionally set the UUID column type
if db_dialect == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif db_dialect == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  # This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)
class Pac(Base):
    __tablename__ = 'farm_' + snake_case('Pac')
    pac_id = Column('pac_id', Integer, primary_key=True, autoincrement=True)
    code = Column('code', UUIDType, unique=True, default=generate_uuid, nullable=True)
    last_change_code = Column('last_change_code', Integer, nullable=True)
    insert_user_id = Column('insert_user_id', UUIDType, default=generate_uuid, nullable=True)
    last_update_user_id = Column('last_update_user_id', UUIDType, default=generate_uuid, nullable=True)
    description = Column('description',
                            String,
                          default="",
                                index=pac_constants.description_calculatedIsDBColumnIndexed,
                          nullable=True)
    display_order = Column('display_order',
                          Integer,
                          default=0,
                                index=pac_constants.display_order_calculatedIsDBColumnIndexed,
                          nullable=True)
    is_active = Column('is_active',
                               Boolean,
                               default=False,
                                index=pac_constants.is_active_calculatedIsDBColumnIndexed,
                               nullable=True)
    lookup_enum_name = Column('lookup_enum_name',
                            String,
                          default="",
                                index=pac_constants.lookup_enum_name_calculatedIsDBColumnIndexed,
                          nullable=True)
    name = Column('name',
                            String,
                          default="",
                                index=pac_constants.name_calculatedIsDBColumnIndexed,
                          nullable=True)

    insert_utc_date_time = Column('insert_utc_date_time', DateTime, nullable=True)
    last_update_utc_date_time = Column('last_update_utc_date_time', DateTime, nullable=True)
    #no relationsip properties. they are not updated immediately if the id prop is updated directly
    #  = relationship('', back_populates=snake_case(''))
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
        self.description = kwargs.get('description', "")
        self.display_order = kwargs.get('display_order', 0)
        self.is_active = kwargs.get('is_active', False)
        self.lookup_enum_name = kwargs.get('lookup_enum_name', "")
        self.name = kwargs.get('name', "")
        self.insert_utc_date_time = kwargs.get('insert_utc_date_time', datetime(1753, 1, 1))
        self.last_update_utc_date_time = kwargs.get('last_update_utc_date_time', datetime(1753, 1, 1))

# Define the index separately from the column
# Index('index_code', Pac.code)

@event.listens_for(Pac, 'before_insert')
def set_created_on(mapper, connection, target):
    target.insert_utc_date_time = datetime.utcnow()
    target.last_update_utc_date_time = datetime.utcnow()
@event.listens_for(Pac, 'before_update')
def set_updated_on(mapper, connection, target):
    target.last_update_utc_date_time = datetime.utcnow()
