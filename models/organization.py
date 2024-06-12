# models/organization.py
"""
    #TODO add comment
"""
from datetime import date, datetime
from sqlalchemy import (BigInteger, Boolean, Column, Date, DateTime, Float,
                        ForeignKey, Index, Integer, Numeric, String, Uuid,
                        event, func)
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.dialects.postgresql import UUID
import models.constants.organization as organization_constants
from services.db_config import DB_DIALECT, generate_uuid, get_uuid_type
from utils.common_functions import snake_case
from .base import Base, EncryptedType
UUIDType = get_uuid_type(DB_DIALECT)
class Organization(Base):
    """
    #TODO add comment
    """
    __tablename__ = 'farm_' + snake_case('Organization')
    organization_id = Column(
        'organization_id',
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
    name = Column(
        'name',

        String,

        default="",
        index=organization_constants.name_calculatedIsDBColumnIndexed,
        nullable=True)
    tac_id = Column('tac_id',
                     Integer,
                     ForeignKey('farm_' + snake_case('Tac') + '.tac_id'),
                     index=organization_constants.tac_id_calculatedIsDBColumnIndexed,
                     nullable=True)
    tac_code_peek = UUIDType  # TacID
    insert_utc_date_time = Column(
        'insert_utc_date_time',
        DateTime,
        nullable=True)
    last_update_utc_date_time = Column(
        'last_update_utc_date_time',
        DateTime,
        nullable=True)
    #no relationsip properties. they are not updated immediately if the id prop is updated directly
    # tac = relationship('Tac', back_populates=snake_case('Tac'))
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
        self.name = kwargs.get(
            'name', "")
        self.tac_id = kwargs.get(
            'tac_id', 0)
        self.insert_utc_date_time = kwargs.get(
            'insert_utc_date_time', datetime(1753, 1, 1))
        self.last_update_utc_date_time = kwargs.get(
            'last_update_utc_date_time', datetime(1753, 1, 1))
# endset
        self.tac_code_peek = kwargs.get(  # TacID
            'tac_code_peek', generate_uuid())
# endset
    @staticmethod
    def property_list():
        result = [
            "name",
            "tac_id",
# endset
            "code"
            ]
        return result
# Define the index separately from the column
# Index('index_code', Organization.code)
# Index('farm_organization_index_tac_id', Organization.tac_id)  # TacID
@event.listens_for(Organization, 'before_insert')
def set_created_on(mapper, connection, target):
    target.insert_utc_date_time = datetime.utcnow()
    target.last_update_utc_date_time = datetime.utcnow()
@event.listens_for(Organization, 'before_update')
def set_updated_on(mapper, connection, target):
    target.last_update_utc_date_time = datetime.utcnow()
