# business/organization.py
"""
    #TODO add comment
"""
import random
import uuid
from typing import List
from datetime import datetime, date
from sqlalchemy import Index, event, BigInteger, Boolean, Column, Date, DateTime, Float, Integer, Numeric, String, ForeignKey, Uuid, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from helpers.session_context import SessionContext
from services.db_config import db_dialect,generate_uuid
from managers import OrganizationManager
from models import Organization
import models
import managers as managers_and_enums
from .base_bus_obj import BaseBusObj

from business.org_customer import OrgCustomerBusObj

from business.org_api_key import OrgApiKeyBusObj

class OrganizationInvalidInitError(Exception):
    pass
# Conditionally set the UUID column type
if db_dialect == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif db_dialect == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  #This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)
class OrganizationBusObj(BaseBusObj):
    def __init__(self, session_context: SessionContext):
        if not session_context.session:
            raise ValueError("session required")
        self._session_context = session_context
        self.organization = Organization()
    @property
    def organization_id(self):
        return self.organization.organization_id
    @organization_id.setter
    def code(self, value: int):
        if not isinstance(value, int):
            raise ValueError("organization_id must be a int.")
        self.organization.organization_id = value
    # code
    @property
    def code(self):
        return self.organization.code
    @code.setter
    def code(self, value: UUIDType):
        #if not isinstance(value, UUIDType):
        #raise ValueError("code must be a UUID.")
        self.organization.code = value
    # last_change_code
    @property
    def last_change_code(self):
        return self.organization.last_change_code
    @last_change_code.setter
    def last_change_code(self, value: int):
        if not isinstance(value, int):
            raise ValueError("last_change_code must be an integer.")
        self.organization.last_change_code = value
    # insert_user_id
    @property
    def insert_user_id(self):
        return self.organization.insert_user_id
    @insert_user_id.setter
    def insert_user_id(self, value: uuid.UUID):
        if not isinstance(value, uuid.UUID):
            raise ValueError("insert_user_id must be a UUID.")
        self.organization.insert_user_id = value
    def set_prop_insert_user_id(self, value: uuid.UUID):
        self.insert_user_id = value
        return self
    # last_update_user_id
    @property
    def last_update_user_id(self):
        return self.organization.last_update_user_id
    @last_update_user_id.setter
    def last_update_user_id(self, value: uuid.UUID):
        if not isinstance(value, uuid.UUID):
            raise ValueError("last_update_user_id must be a UUID.")
        self.organization.last_update_user_id = value
    def set_prop_last_update_user_id(self, value: uuid.UUID):
        self.last_update_user_id = value
        return self

    # name
    @property
    def name(self):
        return self.organization.name
    @name.setter
    def name(self, value):
        assert isinstance(value, str), "name must be a string"
        self.organization.name = value
    def set_prop_name(self, value):
        self.name = value
        return self
    # TacID

    # name,
    # TacID
    @property
    def tac_id(self):
        return self.organization.tac_id
    @tac_id.setter
    def tac_id(self, value):
        assert isinstance(value, int) or value is None, "tac_id must be an integer or None"
        self.organization.tac_id = value
    def set_prop_tac_id(self, value):
        self.tac_id = value
        return self
    @property
    def tac_code_peek(self):
        return self.organization.tac_code_peek
    # @tac_code_peek.setter
    # def tac_code_peek(self, value):
    #     assert isinstance(value, UUIDType), "tac_code_peek must be a UUID"
    #     self.organization.tac_code_peek = value

    # insert_utc_date_time
    @property
    def insert_utc_date_time(self):
        return self.organization.insert_utc_date_time
    @insert_utc_date_time.setter
    def insert_utc_date_time(self, value):
        assert isinstance(value, datetime) or value is None, "insert_utc_date_time must be a datetime object or None"
        self.organization.insert_utc_date_time = value
    # update_utc_date_time
    @property
    def last_update_utc_date_time(self):
        return self.organization.last_update_utc_date_time
    @last_update_utc_date_time.setter
    def last_update_utc_date_time(self, value):
        assert isinstance(value, datetime) or value is None, "last_update_utc_date_time must be a datetime object or None"
        self.organization.last_update_utc_date_time = value

    async def load(self, json_data: str = None,
                   code: uuid.UUID = None,
                   organization_id: int = None,
                   organization_obj_instance: Organization = None,
                   organization_dict: dict = None):
        if organization_id and self.organization.organization_id is None:
            organization_manager = OrganizationManager(self._session_context)
            organization_obj = await organization_manager.get_by_id(organization_id)
            self.organization = organization_obj
        if code and self.organization.organization_id is None:
            organization_manager = OrganizationManager(self._session_context)
            organization_obj = await organization_manager.get_by_code(code)
            self.organization = organization_obj
        if organization_obj_instance and self.organization.organization_id is None:
            organization_manager = OrganizationManager(self._session_context)
            organization_obj = await organization_manager.get_by_id(organization_obj_instance.organization_id)
            self.organization = organization_obj
        if json_data and self.organization.organization_id is None:
            organization_manager = OrganizationManager(self._session_context)
            self.organization = organization_manager.from_json(json_data)
        if organization_dict and self.organization.organization_id is None:
            organization_manager = OrganizationManager(self._session_context)
            self.organization = organization_manager.from_dict(organization_dict)
        return self
    @staticmethod
    async def get(session_context: SessionContext,
                    json_data: str = None,
                   code: uuid.UUID = None,
                   organization_id: int = None,
                   organization_obj_instance: Organization = None,
                   organization_dict: dict = None):
        result = OrganizationBusObj(session_context)
        await result.load(
            json_data,
            code,
            organization_id,
            organization_obj_instance,
            organization_dict
        )
        return result

    async def refresh(self):
        organization_manager = OrganizationManager(self._session_context)
        self.organization = await organization_manager.refresh(self.organization)
        return self
    def is_valid(self):
        return (self.organization is not None)
    def to_dict(self):
        organization_manager = OrganizationManager(self._session_context)
        return organization_manager.to_dict(self.organization)
    def to_json(self):
        organization_manager = OrganizationManager(self._session_context)
        return organization_manager.to_json(self.organization)
    async def save(self):
        if self.organization.organization_id is not None and self.organization.organization_id > 0:
            organization_manager = OrganizationManager(self._session_context)
            self.organization = await organization_manager.update(self.organization)
        if self.organization.organization_id is None or self.organization.organization_id == 0:
            organization_manager = OrganizationManager(self._session_context)
            self.organization = await organization_manager.add(self.organization)
        return self
    async def delete(self):
        if self.organization.organization_id > 0:
            organization_manager = OrganizationManager(self._session_context)
            await organization_manager.delete(self.organization.organization_id)
            self.organization = None
    async def randomize_properties(self):
        self.organization.name = "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        # self.organization.tac_id = random.randint(0, 100)

        return self
    def get_organization_obj(self) -> Organization:
        return self.organization
    def is_equal(self, organization: Organization) -> Organization:
        organization_manager = OrganizationManager(self._session_context)
        my_organization = self.get_organization_obj()
        return organization_manager.is_equal(organization, my_organization)

    # name,
    # TacID
    async def get_tac_id_rel_obj(self) -> models.Tac:
        tac_manager = managers_and_enums.TacManager(self._session_context)
        tac_obj = await tac_manager.get_by_id(self.tac_id)
        return tac_obj

    def get_obj(self) -> Organization:
        return self.organization
    def get_object_name(self) -> str:
        return "organization"
    def get_id(self) -> int:
        return self.organization_id
    # name,
    # TacID
    async def get_parent_name(self) -> str:
        return 'Tac'
    async def get_parent_code(self) -> uuid.UUID:
        return self.tac_code_peek
    async def get_parent_obj(self) -> models.Tac:
        return self.get_tac_id_rel_obj()

    @staticmethod
    async def to_bus_obj_list(session_context: SessionContext, obj_list: List[Organization]):
        result = list()
        for organization in obj_list:
            organization_bus_obj = OrganizationBusObj.get(session_context, organization_obj_instance=organization)
            result.append(organization_bus_obj)
        return result

    async def build_org_customer(self) -> OrgCustomerBusObj:
        item = OrgCustomerBusObj(self._session_context)

        item.organization_id = self.organization_id
        item.org_customer.organization_code_peek = self.code

        return item

    async def get_all_org_customer(self) -> List[OrgCustomerBusObj]:
        results = list()
        org_customer_manager = managers_and_enums.OrgCustomerManager(self._session_context)
        obj_list = await org_customer_manager.get_by_organization_id(self.organization_id)
        for obj_item in obj_list:
            bus_obj_item = OrgCustomerBusObj(self._session_context)
            await bus_obj_item.load(org_customer_obj_instance=obj_item)
            results.append(bus_obj_item)
        return results

    async def build_org_api_key(self) -> OrgApiKeyBusObj:
        item = OrgApiKeyBusObj(self._session_context)

        item.organization_id = self.organization_id
        item.org_api_key.organization_code_peek = self.code

        return item

    async def get_all_org_api_key(self) -> List[OrgApiKeyBusObj]:
        results = list()
        org_api_key_manager = managers_and_enums.OrgApiKeyManager(self._session_context)
        obj_list = await org_api_key_manager.get_by_organization_id(self.organization_id)
        for obj_item in obj_list:
            bus_obj_item = OrgApiKeyBusObj(self._session_context)
            await bus_obj_item.load(org_api_key_obj_instance=obj_item)
            results.append(bus_obj_item)
        return results

