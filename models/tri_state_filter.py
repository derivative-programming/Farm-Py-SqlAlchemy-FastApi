# models/tri_state_filter.py
"""
    #TODO add comment
"""
from datetime import date, datetime
from sqlalchemy import (BigInteger, Boolean, Column, Date, DateTime, Float,
                        ForeignKey, Index, Integer, Numeric, String, Uuid,
                        event, func)
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.dialects.postgresql import UUID
import models.constants.tri_state_filter as tri_state_filter_constants
from services.db_config import DB_DIALECT, generate_uuid, get_uuid_type
from utils.common_functions import snake_case
from .base import Base, EncryptedType
UUIDType = get_uuid_type(DB_DIALECT)
class TriStateFilter(Base):
    """
    #TODO add comment
    """
    __tablename__ = 'farm_' + snake_case('TriStateFilter')
    tri_state_filter_id = Column(
        'tri_state_filter_id',
        Integer,
        primary_key=True,
        autoincrement=True)
    code = Column('code',
                  UUIDType,
                  unique=True,
                  default=generate_uuid,
                  nullable=True)
    last_change_code = Column(
        'last_change_code',
        Integer,
        nullable=True)
    insert_user_id = Column(
        'insert_user_id',
        UUIDType,
        default=generate_uuid,
        nullable=True)
    last_update_user_id = Column(
        'last_update_user_id',
        UUIDType,
        default=generate_uuid,
        nullable=True)
    description = Column(
        'description',

        String,

        default="",
        index=tri_state_filter_constants.description_calculatedIsDBColumnIndexed,
        nullable=True)
    display_order = Column(
        'display_order',
        Integer,
        default=0,
        index=tri_state_filter_constants.display_order_calculatedIsDBColumnIndexed,
        nullable=True)
    is_active = Column(
        'is_active',
        Boolean,
        default=False,
        index=tri_state_filter_constants.is_active_calculatedIsDBColumnIndexed,
        nullable=True)
    lookup_enum_name = Column(
        'lookup_enum_name',

        String,

        default="",
        index=tri_state_filter_constants.lookup_enum_name_calculatedIsDBColumnIndexed,
        nullable=True)
    name = Column(
        'name',

        String,

        default="",
        index=tri_state_filter_constants.name_calculatedIsDBColumnIndexed,
        nullable=True)
    pac_id = Column('pac_id',
                     Integer,
                     ForeignKey('farm_' + snake_case('Pac') + '.pac_id'),
                     index=tri_state_filter_constants.pac_id_calculatedIsDBColumnIndexed,
                     nullable=True)
    state_int_value = Column(
        'state_int_value',
        Integer,
        default=0,
        index=tri_state_filter_constants.state_int_value_calculatedIsDBColumnIndexed,
        nullable=True)
    pac_code_peek = UUIDType  # PacID
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
        self.code = kwargs.get('code', generate_uuid())
        self.last_change_code = kwargs.get(
            'last_change_code', 0)
        self.insert_user_id = kwargs.get(
            'insert_user_id', None)
        self.last_update_user_id = kwargs.get(
            'last_update_user_id', None)
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
        self.pac_id = kwargs.get(
            'pac_id', 0)
        self.state_int_value = kwargs.get(
            'state_int_value', 0)
        self.insert_utc_date_time = kwargs.get(
            'insert_utc_date_time', datetime(1753, 1, 1))
        self.last_update_utc_date_time = kwargs.get(
            'last_update_utc_date_time', datetime(1753, 1, 1))
# endset
        self.pac_code_peek = kwargs.get(  # PacID
            'pac_code_peek', generate_uuid())
# endset
    @staticmethod
    def property_list():
        result = [
            "description",
            "display_order",
            "is_active",
            "lookup_enum_name",
            "name",
            "pac_id",
            "state_int_value",
# endset
            "code"
            ]
        return result
# Define the index separately from the column
# Index('index_code', TriStateFilter.code)
# Index('farm_tri_state_filter_index_pac_id', TriStateFilter.pac_id)  # PacID
@event.listens_for(TriStateFilter, 'before_insert')
def set_created_on(mapper, connection, target):
    target.insert_utc_date_time = datetime.utcnow()
    target.last_update_utc_date_time = datetime.utcnow()
@event.listens_for(TriStateFilter, 'before_update')
def set_updated_on(mapper, connection, target):
    target.last_update_utc_date_time = datetime.utcnow()
