import uuid
from typing import List
from datetime import datetime, date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Index, event, BigInteger, Boolean, Column, Date, DateTime, Float, Integer, Numeric, String, ForeignKey, Uuid, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
# from business.organization import OrganizationBusObj #OrganizationID
from business.org_customer import OrgCustomerBusObj #OrgCustomerID
from services.db_config import db_dialect,generate_uuid
# from managers import OrganizationManager as OrganizationIDManager #OrganizationID
# from managers import OrgCustomerManager as OrgCustomerIDManager #OrgCustomerID
from managers import OrgApiKeyManager
from models import OrgApiKey
import models
import managers as managers_and_enums
from .base_bus_obj import BaseBusObj

class OrgApiKeySessionNotFoundError(Exception):
    pass
class OrgApiKeyInvalidInitError(Exception):
    pass
#Conditionally set the UUID column type
if db_dialect == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif db_dialect == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  #This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)
class OrgApiKeyBusObj(BaseBusObj):
    def __init__(self, session:AsyncSession=None):
        if not session:
            raise OrgApiKeySessionNotFoundError("session required")
        self.session = session
        self.org_api_key = OrgApiKey()
    @property
    def org_api_key_id(self):
        return self.org_api_key.org_api_key_id
    @org_api_key_id.setter
    def code(self, value: int):
        if not isinstance(value, int):
            raise ValueError("org_api_key_id must be a int.")
        self.org_api_key.org_api_key_id = value
    #code
    @property
    def code(self):
        return self.org_api_key.code
    @code.setter
    def code(self, value: UUIDType):
        #if not isinstance(value, UUIDType):
        #raise ValueError("code must be a UUID.")
        self.org_api_key.code = value
    #last_change_code
    @property
    def last_change_code(self):
        return self.org_api_key.last_change_code
    @last_change_code.setter
    def last_change_code(self, value: int):
        if not isinstance(value, int):
            raise ValueError("last_change_code must be an integer.")
        self.org_api_key.last_change_code = value
    #insert_user_id
    @property
    def insert_user_id(self):
        return self.org_api_key.insert_user_id
    @insert_user_id.setter
    def insert_user_id(self, value: uuid.UUID):
        if not isinstance(value, uuid.UUID):
            raise ValueError("insert_user_id must be a UUID.")
        self.org_api_key.insert_user_id = value
    def set_prop_insert_user_id(self, value: uuid.UUID):
        self.insert_user_id = value
        return self
    #last_update_user_id
    @property
    def last_update_user_id(self):
        return self.org_api_key.last_update_user_id
    @last_update_user_id.setter
    def last_update_user_id(self, value: uuid.UUID):
        if not isinstance(value, uuid.UUID):
            raise ValueError("last_update_user_id must be a UUID.")
        self.org_api_key.last_update_user_id = value
    def set_prop_last_update_user_id(self, value: uuid.UUID):
        self.last_update_user_id = value
        return self

    #ApiKeyValue
    @property
    def api_key_value(self):
        return self.org_api_key.api_key_value
    @api_key_value.setter
    def api_key_value(self, value):
        assert isinstance(value, str), "api_key_value must be a string"
        self.org_api_key.api_key_value = value
    def set_prop_api_key_value(self, value):
        self.api_key_value = value
        return self
    #CreatedBy
    @property
    def created_by(self):
        return self.org_api_key.created_by
    @created_by.setter
    def created_by(self, value):
        assert isinstance(value, str), "created_by must be a string"
        self.org_api_key.created_by = value
    def set_prop_created_by(self, value):
        self.created_by = value
        return self
    #CreatedUTCDateTime
    @property
    def created_utc_date_time(self):
        return self.org_api_key.created_utc_date_time
    @created_utc_date_time.setter
    def created_utc_date_time(self, value):
        assert isinstance(value, datetime), "created_utc_date_time must be a datetime object"
        self.org_api_key.created_utc_date_time = value
    def set_prop_created_utc_date_time(self, value):
        self.created_utc_date_time = value
        return self
    #ExpirationUTCDateTime
    @property
    def expiration_utc_date_time(self):
        return self.org_api_key.expiration_utc_date_time
    @expiration_utc_date_time.setter
    def expiration_utc_date_time(self, value):
        assert isinstance(value, datetime), "expiration_utc_date_time must be a datetime object"
        self.org_api_key.expiration_utc_date_time = value
    def set_prop_expiration_utc_date_time(self, value):
        self.expiration_utc_date_time = value
        return self
    #IsActive
    @property
    def is_active(self):
        return self.org_api_key.is_active
    @is_active.setter
    def is_active(self, value: bool):
        if not isinstance(value, bool):
            raise ValueError("is_active must be a boolean.")
        self.org_api_key.is_active = value
    def set_prop_is_active(self, value: bool):
        self.is_active = value
        return self
    #IsTempUserKey
    @property
    def is_temp_user_key(self):
        return self.org_api_key.is_temp_user_key
    @is_temp_user_key.setter
    def is_temp_user_key(self, value: bool):
        if not isinstance(value, bool):
            raise ValueError("is_temp_user_key must be a boolean.")
        self.org_api_key.is_temp_user_key = value
    def set_prop_is_temp_user_key(self, value: bool):
        self.is_temp_user_key = value
        return self
    #Name
    @property
    def name(self):
        return self.org_api_key.name
    @name.setter
    def name(self, value):
        assert isinstance(value, str), "name must be a string"
        self.org_api_key.name = value
    def set_prop_name(self, value):
        self.name = value
        return self
    #OrganizationID
    #OrgCustomerID

    #apiKeyValue,
    #createdBy,
    #createdUTCDateTime
    #expirationUTCDateTime
    #isActive,
    #isTempUserKey,
    #name,
    #OrganizationID
    @property
    def organization_id(self):
        return self.org_api_key.organization_id
    @organization_id.setter
    def organization_id(self, value):
        assert isinstance(value, int) or value is None, "organization_id must be an integer or None"
        self.org_api_key.organization_id = value
    def set_prop_organization_id(self, value):
        self.organization_id = value
        return self
    @property
    def organization_code_peek(self):
        return self.org_api_key.organization_code_peek
    # @organization_code_peek.setter
    # def organization_code_peek(self, value):
    #     assert isinstance(value, UUIDType), "organization_code_peek must be a UUID"
    #     self.org_api_key.organization_code_peek = value
    #OrgCustomerID
    @property
    def org_customer_id(self):
        return self.org_api_key.org_customer_id
    @org_customer_id.setter
    def org_customer_id(self, value: int):
        if not isinstance(value, int):
            raise ValueError("org_customer_id must be an integer.")
        self.org_api_key.org_customer_id = value
    def set_prop_org_customer_id(self, value):
        self.org_customer_id = value
        return self
    @property
    def org_customer_code_peek(self):
        return self.org_api_key.org_customer_code_peek
    # @org_customer_code_peek.setter
    # def org_customer_code_peek(self, value):
    #     assert isinstance(value, UUIDType), "org_customer_code_peek must be a UUID"
    #     self.org_api_key.org_customer_code_peek = value

    #insert_utc_date_time
    @property
    def insert_utc_date_time(self):
        return self.org_api_key.insert_utc_date_time
    @insert_utc_date_time.setter
    def insert_utc_date_time(self, value):
        assert isinstance(value, datetime) or value is None, "insert_utc_date_time must be a datetime object or None"
        self.org_api_key.insert_utc_date_time = value
    #update_utc_date_time
    @property
    def last_update_utc_date_time(self):
        return self.org_api_key.last_update_utc_date_time
    @last_update_utc_date_time.setter
    def last_update_utc_date_time(self, value):
        assert isinstance(value, datetime) or value is None, "last_update_utc_date_time must be a datetime object or None"
        self.org_api_key.last_update_utc_date_time = value

    async def load(self, json_data:str=None,
                   code:uuid.UUID=None,
                   org_api_key_id:int=None,
                   org_api_key_obj_instance:OrgApiKey=None,
                   org_api_key_dict:dict=None):
        if org_api_key_id and self.org_api_key.org_api_key_id is None:
            org_api_key_manager = OrgApiKeyManager(self.session)
            org_api_key_obj = await org_api_key_manager.get_by_id(org_api_key_id)
            self.org_api_key = org_api_key_obj
        if code and self.org_api_key.org_api_key_id is None:
            org_api_key_manager = OrgApiKeyManager(self.session)
            org_api_key_obj = await org_api_key_manager.get_by_code(code)
            self.org_api_key = org_api_key_obj
        if org_api_key_obj_instance and self.org_api_key.org_api_key_id is None:
            org_api_key_manager = OrgApiKeyManager(self.session)
            org_api_key_obj = await org_api_key_manager.get_by_id(org_api_key_obj_instance.org_api_key_id)
            self.org_api_key = org_api_key_obj
        if json_data and self.org_api_key.org_api_key_id is None:
            org_api_key_manager = OrgApiKeyManager(self.session)
            self.org_api_key = org_api_key_manager.from_json(json_data)
        if org_api_key_dict and self.org_api_key.org_api_key_id is None:
            org_api_key_manager = OrgApiKeyManager(self.session)
            self.org_api_key = org_api_key_manager.from_dict(org_api_key_dict)

    async def refresh(self):
        org_api_key_manager = OrgApiKeyManager(self.session)
        self.org_api_key = await org_api_key_manager.refresh(self.org_api_key)
    def to_dict(self):
        org_api_key_manager = OrgApiKeyManager(self.session)
        return org_api_key_manager.to_dict(self.org_api_key)
    def to_json(self):
        org_api_key_manager = OrgApiKeyManager(self.session)
        return org_api_key_manager.to_json(self.org_api_key)
    async def save(self):
        if self.org_api_key.org_api_key_id > 0:
            org_api_key_manager = OrgApiKeyManager(self.session)
            self.org_api_key = await org_api_key_manager.update(self.org_api_key)
        if self.org_api_key.org_api_key_id == 0:
            org_api_key_manager = OrgApiKeyManager(self.session)
            self.org_api_key = await org_api_key_manager.add(self.org_api_key)
    async def delete(self):
        if self.org_api_key.org_api_key_id > 0:
            org_api_key_manager = OrgApiKeyManager(self.session)
            self.org_api_key = await org_api_key_manager.delete(self.org_api_key.org_api_key_id)
    def get_org_api_key_obj(self) -> OrgApiKey:
        return self.org_api_key
    def is_equal(self,org_api_key:OrgApiKey) -> OrgApiKey:
        org_api_key_manager = OrgApiKeyManager(self.session)
        my_org_api_key = self.get_org_api_key_obj()
        return org_api_key_manager.is_equal(org_api_key, my_org_api_key)

    #apiKeyValue,
    #createdBy,
    #createdUTCDateTime
    #expirationUTCDateTime
    #isActive,
    #isTempUserKey,
    #name,
    #OrganizationID
    async def get_organization_id_rel_obj(self) -> models.Organization:
        organization_manager = managers_and_enums.OrganizationManager(self.session)
        organization_obj = await organization_manager.get_by_id(self.organization_id)
        return organization_obj
    #OrgCustomerID
    async def get_org_customer_id_rel_obj(self) -> models.OrgCustomer:
        org_customer_manager = managers_and_enums.OrgCustomerManager(self.session)
        org_customer_obj = await org_customer_manager.get_by_id(self.org_customer_id)
        return org_customer_obj

    def get_obj(self) -> OrgApiKey:
        return self.org_api_key
    def get_object_name(self) -> str:
        return "org_api_key"
    def get_id(self) -> int:
        return self.org_api_key_id
    #apiKeyValue,
    #createdBy,
    #createdUTCDateTime
    #expirationUTCDateTime
    #isActive,
    #isTempUserKey,
    #name,
    #OrganizationID
    # async def get_parent_obj(self) -> OrganizationBusObj:
    #     return await self.get_organization_id_rel_bus_obj()
    async def get_parent_name(self) -> str:
        return 'Organization'
    async def get_parent_code(self) -> uuid.UUID:
        return self.organization_code_peek
    #OrgCustomerID

