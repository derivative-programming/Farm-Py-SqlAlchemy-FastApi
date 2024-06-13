# models/pac.py
"""
    #TODO add comment
"""
import uuid
from datetime import date, datetime
from sqlalchemy_utils import UUIDType
from sqlalchemy import (BigInteger, Boolean, Column, Date, DateTime, Float,
                        ForeignKey, Index, Integer, Numeric, String,
                        event, func)
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.dialects.postgresql import UUID
import models.constants.pac as pac_constants
from utils.common_functions import snake_case
from .base import Base, EncryptedType
class Pac(Base):
    """
    #TODO add comment
    """
    __tablename__ = 'farm_' + snake_case('Pac')
    pac_id = Column(
        'pac_id',
        Integer,
        primary_key=True,
        autoincrement=True)
    _code = Column(
        'code',
        UUIDType(binary=False),
        unique=True,
        default=uuid.uuid4,
        nullable=True)
    last_change_code = Column(
        'last_change_code',
        Integer,
        nullable=True)
    _insert_user_id = Column(
        'insert_user_id',
        UUIDType(binary=False),
        default=uuid.uuid4,
        nullable=True)
    _last_update_user_id = Column(
        'last_update_user_id',
        UUIDType(binary=False),
        default=uuid.uuid4,
        nullable=True)
    description = Column(
        'description',

        String,

        default="",
        index=pac_constants.description_calculatedIsDBColumnIndexed,
        nullable=True)
    display_order = Column(
        'display_order',
        Integer,
        default=0,
        index=pac_constants.display_order_calculatedIsDBColumnIndexed,
        nullable=True)
    is_active = Column(
        'is_active',
        Boolean,
        default=False,
        index=pac_constants.is_active_calculatedIsDBColumnIndexed,
        nullable=True)
    lookup_enum_name = Column(
        'lookup_enum_name',

        String,

        default="",
        index=pac_constants.lookup_enum_name_calculatedIsDBColumnIndexed,
        nullable=True)
    name = Column(
        'name',

        String,

        default="",
        index=pac_constants.name_calculatedIsDBColumnIndexed,
        nullable=True)

    insert_utc_date_time = Column(
        'insert_utc_date_time',
        DateTime,
        nullable=True)
    last_update_utc_date_time = Column(
        'last_update_utc_date_time',
        DateTime,
        nullable=True)
    #no relationsip properties. they are not updated immediately if the id prop is updated directly
    #  = relationship('', back_populates=snake_case(''))
    # flavor = relationship('Flavor', back_populates=snake_case('Flavor'))
    __mapper_args__ = {
        'version_id_col': last_change_code
    }
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.code = kwargs.get('code', uuid.uuid4())
        self.last_change_code = kwargs.get(
            'last_change_code', 0)
        self.insert_user_id = kwargs.get(
            'insert_user_id', uuid.UUID(int=0))
        self.last_update_user_id = kwargs.get(
            'last_update_user_id', uuid.UUID(int=0))
        self.description = kwargs.get(
            'description', "")
        self.display_order = kwargs.get(
            'display_order', 0)
        self.is_active = kwargs.get(
            'is_active', False)
        self.lookup_enum_name = kwargs.get(
            'lookup_enum_name', "")
        self.name = kwargs.get(
            'name', "")
        self.insert_utc_date_time = kwargs.get(
            'insert_utc_date_time', datetime(1753, 1, 1))
        self.last_update_utc_date_time = kwargs.get(
            'last_update_utc_date_time', datetime(1753, 1, 1))
# endset

# endset
    @property
    def code(self):
        return uuid.UUID(str(self._code))
    @code.setter
    def code(self, value):
        if isinstance(value, uuid.UUID):
            self._code = value
        else:
            self._code = uuid.UUID(value)
        self.last_update_utc_date_time = datetime.utcnow()
    @property
    def insert_user_id(self):
        return uuid.UUID(str(self._insert_user_id))
    @insert_user_id.setter
    def insert_user_id(self, value):
        if isinstance(value, uuid.UUID):
            self._insert_user_id = value
        else:
            self._insert_user_id = uuid.UUID(value)
        self.last_update_utc_date_time = datetime.utcnow()
    @property
    def last_update_user_id(self):
        return uuid.UUID(str(self._last_update_user_id))
    @last_update_user_id.setter
    def last_update_user_id(self, value):
        if isinstance(value, uuid.UUID):
            self._last_update_user_id = value
        else:
            self._last_update_user_id = uuid.UUID(value)
        self.last_update_utc_date_time = datetime.utcnow()
    # description,
    # displayOrder,
    # isActive,
    # lookupEnumName,
    # name,
# endset
    @staticmethod
    def property_list():
        result = [
            "description",
            "display_order",
            "is_active",
            "lookup_enum_name",
            "name",
# endset
            "code"
            ]
        return result
# Define the index separately from the column
# Index('index_code', Pac.code)

@event.listens_for(Pac, 'before_insert')
def set_created_on(mapper, connection, target):
    target.insert_utc_date_time = datetime.utcnow()
    target.last_update_utc_date_time = datetime.utcnow()
@event.listens_for(Pac, 'before_update')
def set_updated_on(mapper, connection, target):
    target.last_update_utc_date_time = datetime.utcnow()
