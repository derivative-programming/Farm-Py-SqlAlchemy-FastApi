# models/error_log.py
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
import models.constants.error_log as error_log_constants
from utils.common_functions import snake_case
from .base import Base, EncryptedType
class ErrorLog(Base):
    """
    #TODO add comment
    """
    __tablename__ = 'farm_' + snake_case('ErrorLog')
    error_log_id = Column(
        'error_log_id',
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
    _browser_code = Column(
        'browser_code',
        UUIDType(binary=False),
        default=uuid.uuid4,
        index=error_log_constants.browser_code_calculatedIsDBColumnIndexed,
        nullable=True)
    _context_code = Column(
        'context_code',
        UUIDType(binary=False),
        default=uuid.uuid4,
        index=error_log_constants.context_code_calculatedIsDBColumnIndexed,
        nullable=True)
    created_utc_date_time = Column(
        'created_utc_date_time',
        DateTime,
        default=datetime(1753, 1, 1),
        index=error_log_constants.created_utc_date_time_calculatedIsDBColumnIndexed,
        nullable=True)
    description = Column(
        'description',

        String,

        default="",
        index=error_log_constants.description_calculatedIsDBColumnIndexed,
        nullable=True)
    is_client_side_error = Column(
        'is_client_side_error',
        Boolean,
        default=False,
        index=error_log_constants.is_client_side_error_calculatedIsDBColumnIndexed,
        nullable=True)
    is_resolved = Column(
        'is_resolved',
        Boolean,
        default=False,
        index=error_log_constants.is_resolved_calculatedIsDBColumnIndexed,
        nullable=True)
    pac_id = Column('pac_id',
                     Integer,
                     ForeignKey('farm_' + snake_case('Pac') + '.pac_id'),
                     index=error_log_constants.pac_id_calculatedIsDBColumnIndexed,
                     nullable=True)
    url = Column(
        'url',

        String,

        default="",
        index=error_log_constants.url_calculatedIsDBColumnIndexed,
        nullable=True)
    _pac_code_peek = UUIDType  # PacID
    insert_utc_date_time = Column(
        'insert_utc_date_time',
        DateTime,
        nullable=True)
    last_update_utc_date_time = Column(
        'last_update_utc_date_time',
        DateTime,
        nullable=True)
    #no relationsip properties. they are not updated immediately if the id prop is updated directly
    # pac = relationship('Pac', back_populates=snake_case('Pac'))
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
        self.browser_code = kwargs.get(
            'browser_code', uuid.uuid4())
        self.context_code = kwargs.get(
            'context_code', uuid.uuid4())
        self.created_utc_date_time = kwargs.get(
            'created_utc_date_time', datetime(1753, 1, 1))
        self.description = kwargs.get(
            'description', "")
        self.is_client_side_error = kwargs.get(
            'is_client_side_error', False)
        self.is_resolved = kwargs.get(
            'is_resolved', False)
        self.pac_id = kwargs.get(
            'pac_id', 0)
        self.url = kwargs.get(
            'url', "")
        self.insert_utc_date_time = kwargs.get(
            'insert_utc_date_time', datetime(1753, 1, 1))
        self.last_update_utc_date_time = kwargs.get(
            'last_update_utc_date_time', datetime(1753, 1, 1))
# endset
        self.pac_code_peek = kwargs.get(  # PacID
            'pac_code_peek', uuid.uuid4())
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
    # browserCode,
    @property
    def browser_code(self):
        return uuid.UUID(str(self._browser_code))
    @code.setter
    def browser_code(self, value):
        if isinstance(value, uuid.UUID):
            self._browser_code = value
        else:
            self._browser_code = uuid.UUID(value)
        self.last_update_utc_date_time = datetime.utcnow()
    # contextCode,
    @property
    def context_code(self):
        return uuid.UUID(str(self._context_code))
    @code.setter
    def context_code(self, value):
        if isinstance(value, uuid.UUID):
            self._context_code = value
        else:
            self._context_code = uuid.UUID(value)
        self.last_update_utc_date_time = datetime.utcnow()
    # createdUTCDateTime
    # description,
    # isClientSideError,
    # isResolved,
    # PacID
    @property
    def pac_code_peek(self):
        return uuid.UUID(str(self._pac_code_peek))
    @code.setter
    def pac_code_peek(self, value):
        if isinstance(value, uuid.UUID):
            self._pac_code_peek = value
        else:
            self._pac_code_peek = uuid.UUID(value)
    # url,
# endset
    @staticmethod
    def property_list():
        result = [
            "browser_code",
            "context_code",
            "created_utc_date_time",
            "description",
            "is_client_side_error",
            "is_resolved",
            "pac_id",
            "url",
# endset
            "code"
            ]
        return result
# Define the index separately from the column
# Index('index_code', ErrorLog.code)
# Index('farm_error_log_index_pac_id', ErrorLog.pac_id)  # PacID
@event.listens_for(ErrorLog, 'before_insert')
def set_created_on(mapper, connection, target):
    target.insert_utc_date_time = datetime.utcnow()
    target.last_update_utc_date_time = datetime.utcnow()
@event.listens_for(ErrorLog, 'before_update')
def set_updated_on(mapper, connection, target):
    target.last_update_utc_date_time = datetime.utcnow()
