import uuid
from datetime import datetime, date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Index, event, BigInteger, Boolean, Column, Date, DateTime, Float, Integer, Numeric, String, ForeignKey, Uuid, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from services.db_config import db_dialect,generate_uuid
from managers import TacManager as TacIDManager #TacID
from managers import OrganizationManager
from models import Organization
class OrganizationSessionNotFoundError(Exception):
    pass
class OrganizationInvalidInitError(Exception):
    pass
#Conditionally set the UUID column type
if db_dialect == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif db_dialect == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  #This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)
class OrganizationBusObj:
    def __init__(self, session:AsyncSession=None):
        if not session:
            raise OrganizationSessionNotFoundError("session required")
        self.session = session
        self.organization = Organization()
    @property
    def organization_id(self):
        return self.organization.organization_id
    @organization_id.setter
    def code(self, value: int):
        if not isinstance(value, int):
            raise ValueError("organization_id must be a int.")
        self.organization.organization_id = value
    #code
    @property
    def code(self):
        return self.organization.code
    @code.setter
    def code(self, value: UUIDType):
        #if not isinstance(value, UUIDType):
        #raise ValueError("code must be a UUID.")
        self.organization.code = value
    #last_change_code
    @property
    def last_change_code(self):
        return self.organization.last_change_code
    @last_change_code.setter
    def last_change_code(self, value: int):
        if not isinstance(value, int):
            raise ValueError("last_change_code must be an integer.")
        self.organization.last_change_code = value
    #insert_user_id
    @property
    def insert_user_id(self):
        return self.organization.insert_user_id
    @insert_user_id.setter
    def insert_user_id(self, value: uuid.UUID):
        if not isinstance(value, uuid.UUID):
            raise ValueError("insert_user_id must be a UUID.")
        self.organization.insert_user_id = value
    #last_update_user_id
    @property
    def last_update_user_id(self):
        return self.organization.last_update_user_id
    @last_update_user_id.setter
    def last_update_user_id(self, value: uuid.UUID):
        if not isinstance(value, uuid.UUID):
            raise ValueError("last_update_user_id must be a UUID.")
        self.organization.last_update_user_id = value

    #Name
    @property
    def name(self):
        return self.organization.name
    @name.setter
    def name(self, value):
        assert isinstance(value, str), "name must be a string"
        self.organization.name = value
    #TacID

    #name,
    #TacID
    @property
    def tac_id(self):
        return self.organization.tac_id
    @tac_id.setter
    def tac_id(self, value):
        assert isinstance(value, int) or value is None, "tac_id must be an integer or None"
        self.organization.tac_id = value
    @property
    def tac_code_peek(self):
        return self.organization.tac_code_peek
    @tac_code_peek.setter
    def tac_code_peek(self, value):
        assert isinstance(value, UUIDType), "tac_code_peek must be a UUID"
        self.organization.tac_code_peek = value

    #insert_utc_date_time
    @property
    def insert_utc_date_time(self):
        return self.organization.insert_utc_date_time
    @insert_utc_date_time.setter
    def insert_utc_date_time(self, value):
        assert isinstance(value, datetime) or value is None, "insert_utc_date_time must be a datetime object or None"
        self.organization.insert_utc_date_time = value
    #update_utc_date_time
    @property
    def last_update_utc_date_time(self):
        return self.organization.last_update_utc_date_time
    @last_update_utc_date_time.setter
    def last_update_utc_date_time(self, value):
        assert isinstance(value, datetime) or value is None, "last_update_utc_date_time must be a datetime object or None"
        self.organization.last_update_utc_date_time = value
    async def load(self, json_data:str=None, code:uuid.UUID=None, organization_id:int=None, organization_obj_instance:Organization=None, organization_dict:dict=None):
        if organization_id and self.organization.organization_id is None:
            organization_manager = OrganizationManager(self.session)
            organization_obj = await organization_manager.get_by_id(organization_id)
            self.organization = organization_obj
        if code and self.organization.organization_id is None:
            organization_manager = OrganizationManager(self.session)
            organization_obj = await organization_manager.get_by_code(code)
            self.organization = organization_obj
        if organization_obj_instance and self.organization.organization_id is None:
            organization_manager = OrganizationManager(self.session)
            organization_obj = await organization_manager.get_by_id(organization_obj_instance.organization_id)
            self.organization = organization_obj
        if json_data and self.organization.organization_id is None:
            organization_manager = OrganizationManager(self.session)
            self.organization = organization_manager.from_json(json_data)
        if organization_dict and self.organization.organization_id is None:
            organization_manager = OrganizationManager(self.session)
            self.organization = organization_manager.from_dict(organization_dict)
    async def refresh(self):
        organization_manager = OrganizationManager(self.session)
        self.organization = await organization_manager.refresh(self.organization)
    def to_dict(self):
        organization_manager = OrganizationManager(self.session)
        return organization_manager.to_dict(self.organization)
    def to_json(self):
        organization_manager = OrganizationManager(self.session)
        return organization_manager.to_json(self.organization)
    async def save(self):
        if self.organization.organization_id > 0:
            organization_manager = OrganizationManager(self.session)
            self.organization = await organization_manager.update(self.organization)
        if self.organization.organization_id == 0:
            organization_manager = OrganizationManager(self.session)
            self.organization = await organization_manager.add(self.organization)
    async def delete(self):
        if self.organization.organization_id > 0:
            organization_manager = OrganizationManager(self.session)
            self.organization = await organization_manager.delete(self.organization.organization_id)
    def get_organization_obj(self) -> Organization:
        return self.organization
    def is_equal(self,organization:Organization) -> Organization:
        organization_manager = OrganizationManager(self.session)
        my_organization = self.get_organization_obj()
        return organization_manager.is_equal(organization, my_organization)

    async def get_tac_id_rel_obj(self, tac_id: int): #TacID
        tac_manager = TacIDManager(self.session)
        return await tac_manager.get_by_id(self.organization.tac_id)

