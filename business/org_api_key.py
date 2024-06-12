# business/org_api_key.py
"""
    #TODO add comment
"""
import random
import uuid
from typing import List
from datetime import datetime, date
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from helpers.session_context import SessionContext
from services.db_config import DB_DIALECT, generate_uuid, get_uuid_type
from managers import OrgApiKeyManager
from models import OrgApiKey
import models
import managers as managers_and_enums
from .base_bus_obj import BaseBusObj

UUIDType = get_uuid_type(DB_DIALECT)
class OrgApiKeyInvalidInitError(Exception):
    """
    #TODO add comment
    """
    pass
class OrgApiKeyBusObj(BaseBusObj):
    """
    #TODO add comment
    """
    def __init__(self, session_context: SessionContext):
        if not session_context.session:
            raise ValueError("session required")
        self._session_context = session_context
        self.org_api_key = OrgApiKey()
    @property
    def org_api_key_id(self):
        """
        #TODO add comment
        """
        return self.org_api_key.org_api_key_id
    @org_api_key_id.setter
    def code(self, value: int):
        """
        #TODO add comment
        """
        if not isinstance(value, int):
            raise ValueError("org_api_key_id must be a int.")
        self.org_api_key.org_api_key_id = value
    # code
    @property
    def code(self):
        """
        #TODO add comment
        """
        return self.org_api_key.code
    @code.setter
    def code(self, value: UUIDType):  # type: ignore
        """
        #TODO add comment
        """
        #if not isinstance(value, UUIDType):
        #raise ValueError("code must be a UUID.")
        self.org_api_key.code = value
    # last_change_code
    @property
    def last_change_code(self):
        """
        #TODO add comment
        """
        return self.org_api_key.last_change_code
    @last_change_code.setter
    def last_change_code(self, value: int):
        """
        #TODO add comment
        """
        if not isinstance(value, int):
            raise ValueError("last_change_code must be an integer.")
        self.org_api_key.last_change_code = value
    # insert_user_id
    @property
    def insert_user_id(self):
        """
        #TODO add comment
        """
        return self.org_api_key.insert_user_id
    @insert_user_id.setter
    def insert_user_id(self, value: uuid.UUID):
        """
        #TODO add comment
        """
        if not isinstance(value, uuid.UUID):
            raise ValueError("insert_user_id must be a UUID.")
        self.org_api_key.insert_user_id = value
    def set_prop_insert_user_id(self, value: uuid.UUID):
        """
        #TODO add comment
        """
        self.insert_user_id = value
        return self
    # last_update_user_id
    @property
    def last_update_user_id(self):
        """
        #TODO add comment
        """
        return self.org_api_key.last_update_user_id
    @last_update_user_id.setter
    def last_update_user_id(self, value: uuid.UUID):
        """
        #TODO add comment
        """
        if not isinstance(value, uuid.UUID):
            raise ValueError("last_update_user_id must be a UUID.")
        self.org_api_key.last_update_user_id = value
    def set_prop_last_update_user_id(self, value: uuid.UUID):
        """
        #TODO add comment
        """
        self.last_update_user_id = value
        return self
# endset
    # apiKeyValue
    @property
    def api_key_value(self):
        """
        #TODO add comment
        """
        return self.org_api_key.api_key_value
    @api_key_value.setter
    def api_key_value(self, value):
        """
        #TODO add comment
        """
        assert isinstance(value, str), "api_key_value must be a string"
        self.org_api_key.api_key_value = value
    def set_prop_api_key_value(self, value):
        """
        #TODO add comment
        """
        self.api_key_value = value
        return self
    # createdBy
    @property
    def created_by(self):
        """
        #TODO add comment
        """
        return self.org_api_key.created_by
    @created_by.setter
    def created_by(self, value):
        """
        #TODO add comment
        """
        assert isinstance(value, str), "created_by must be a string"
        self.org_api_key.created_by = value
    def set_prop_created_by(self, value):
        """
        #TODO add comment
        """
        self.created_by = value
        return self
    # createdUTCDateTime
    @property
    def created_utc_date_time(self):
        """
        #TODO add comment
        """
        return self.org_api_key.created_utc_date_time
    @created_utc_date_time.setter
    def created_utc_date_time(self, value):
        """
        #TODO add comment
        """
        assert isinstance(value, datetime), (
            "created_utc_date_time must be a datetime object")
        self.org_api_key.created_utc_date_time = value
    def set_prop_created_utc_date_time(self, value):
        """
        #TODO add comment
        """
        self.created_utc_date_time = value
        return self
    # expirationUTCDateTime
    @property
    def expiration_utc_date_time(self):
        """
        #TODO add comment
        """
        return self.org_api_key.expiration_utc_date_time
    @expiration_utc_date_time.setter
    def expiration_utc_date_time(self, value):
        """
        #TODO add comment
        """
        assert isinstance(value, datetime), (
            "expiration_utc_date_time must be a datetime object")
        self.org_api_key.expiration_utc_date_time = value
    def set_prop_expiration_utc_date_time(self, value):
        """
        #TODO add comment
        """
        self.expiration_utc_date_time = value
        return self
    # isActive
    @property
    def is_active(self):
        """
        #TODO add comment
        """
        return self.org_api_key.is_active
    @is_active.setter
    def is_active(self, value: bool):
        """
        #TODO add comment
        """
        if not isinstance(value, bool):
            raise ValueError("is_active must be a boolean.")
        self.org_api_key.is_active = value
    def set_prop_is_active(self, value: bool):
        """
        #TODO add comment
        """
        self.is_active = value
        return self
    # isTempUserKey
    @property
    def is_temp_user_key(self):
        """
        #TODO add comment
        """
        return self.org_api_key.is_temp_user_key
    @is_temp_user_key.setter
    def is_temp_user_key(self, value: bool):
        """
        #TODO add comment
        """
        if not isinstance(value, bool):
            raise ValueError("is_temp_user_key must be a boolean.")
        self.org_api_key.is_temp_user_key = value
    def set_prop_is_temp_user_key(self, value: bool):
        """
        #TODO add comment
        """
        self.is_temp_user_key = value
        return self
    # name
    @property
    def name(self):
        """
        #TODO add comment
        """
        return self.org_api_key.name
    @name.setter
    def name(self, value):
        """
        #TODO add comment
        """
        assert isinstance(value, str), "name must be a string"
        self.org_api_key.name = value
    def set_prop_name(self, value):
        """
        #TODO add comment
        """
        self.name = value
        return self
    # OrganizationID
    # OrgCustomerID
# endset
    # apiKeyValue,
    # createdBy,
    # createdUTCDateTime
    # expirationUTCDateTime
    # isActive,
    # isTempUserKey,
    # name,
    # OrganizationID
    @property
    def organization_id(self):
        """
        #TODO add comment
        """
        return self.org_api_key.organization_id
    @organization_id.setter
    def organization_id(self, value):
        """
        #TODO add comment
        """
        assert isinstance(value, int) or value is None, (
            "organization_id must be an integer or None")
        self.org_api_key.organization_id = value
    def set_prop_organization_id(self, value):
        """
        #TODO add comment
        """
        self.organization_id = value
        return self
    @property
    def organization_code_peek(self):
        """
        #TODO add comment
        """
        return self.org_api_key.organization_code_peek
    # @organization_code_peek.setter
    # def organization_code_peek(self, value):
    #     assert isinstance(value, UUIDType),
    #           "organization_code_peek must be a UUID"
    #     self.org_api_key.organization_code_peek = value
    # OrgCustomerID
    @property
    def org_customer_id(self):
        """
        #TODO add comment
        """
        return self.org_api_key.org_customer_id
    @org_customer_id.setter
    def org_customer_id(self, value: int):
        """
        #TODO add comment
        """
        if not isinstance(value, int):
            raise ValueError("org_customer_id must be an integer.")
        self.org_api_key.org_customer_id = value
    def set_prop_org_customer_id(self, value):
        """
        #TODO add comment
        """
        self.org_customer_id = value
        return self
    @property
    def org_customer_code_peek(self):
        """
        #TODO add comment
        """
        return self.org_api_key.org_customer_code_peek
    # @org_customer_code_peek.setter
    # def org_customer_code_peek(self, value):
    #     assert isinstance(
    #       value, UUIDType),
    #       "org_customer_code_peek must be a UUID"
    #     self.org_api_key.org_customer_code_peek = value
# endset
    # insert_utc_date_time
    @property
    def insert_utc_date_time(self):
        """
        #TODO add comment
        """
        return self.org_api_key.insert_utc_date_time
    @insert_utc_date_time.setter
    def insert_utc_date_time(self, value):
        """
        #TODO add comment
        """
        assert isinstance(value, datetime) or value is None, (
            "insert_utc_date_time must be a datetime object or None")
        self.org_api_key.insert_utc_date_time = value
    # update_utc_date_time
    @property
    def last_update_utc_date_time(self):
        """
        #TODO add comment
        """
        return self.org_api_key.last_update_utc_date_time
    @last_update_utc_date_time.setter
    def last_update_utc_date_time(self, value):
        """
        #TODO add comment
        """
        assert isinstance(value, datetime) or value is None, (
            "last_update_utc_date_time must be a datetime object or None")
        self.org_api_key.last_update_utc_date_time = value

    async def load(self, json_data: str = None,
                   code: uuid.UUID = None,
                   org_api_key_id: int = None,
                   org_api_key_obj_instance: OrgApiKey = None,
                   org_api_key_dict: dict = None):
        """
        #TODO add comment
        """
        if org_api_key_id and self.org_api_key.org_api_key_id is None:
            org_api_key_manager = OrgApiKeyManager(self._session_context)
            org_api_key_obj = await org_api_key_manager.get_by_id(org_api_key_id)
            self.org_api_key = org_api_key_obj
        if code and self.org_api_key.org_api_key_id is None:
            org_api_key_manager = OrgApiKeyManager(self._session_context)
            org_api_key_obj = await org_api_key_manager.get_by_code(code)
            self.org_api_key = org_api_key_obj
        if org_api_key_obj_instance and self.org_api_key.org_api_key_id is None:
            org_api_key_manager = OrgApiKeyManager(self._session_context)
            org_api_key_obj = await org_api_key_manager.get_by_id(
                org_api_key_obj_instance.org_api_key_id
            )
            self.org_api_key = org_api_key_obj
        if json_data and self.org_api_key.org_api_key_id is None:
            org_api_key_manager = OrgApiKeyManager(self._session_context)
            self.org_api_key = org_api_key_manager.from_json(json_data)
        if org_api_key_dict and self.org_api_key.org_api_key_id is None:
            org_api_key_manager = OrgApiKeyManager(self._session_context)
            self.org_api_key = org_api_key_manager.from_dict(org_api_key_dict)
        return self
    @staticmethod
    async def get(
        session_context: SessionContext,
        json_data: str = None,
        code: uuid.UUID = None,
        org_api_key_id: int = None,
        org_api_key_obj_instance: OrgApiKey = None,
        org_api_key_dict: dict = None
    ):
        """
        #TODO add comment
        """
        result = OrgApiKeyBusObj(session_context)
        await result.load(
            json_data,
            code,
            org_api_key_id,
            org_api_key_obj_instance,
            org_api_key_dict
        )
        return result

    async def refresh(self):
        """
        #TODO add comment
        """
        org_api_key_manager = OrgApiKeyManager(self._session_context)
        self.org_api_key = await org_api_key_manager.refresh(self.org_api_key)
        return self
    def is_valid(self):
        """
        #TODO add comment
        """
        return (self.org_api_key is not None)
    def to_dict(self):
        """
        #TODO add comment
        """
        org_api_key_manager = OrgApiKeyManager(self._session_context)
        return org_api_key_manager.to_dict(self.org_api_key)
    def to_json(self):
        """
        #TODO add comment
        """
        org_api_key_manager = OrgApiKeyManager(self._session_context)
        return org_api_key_manager.to_json(self.org_api_key)
    async def save(self):
        """
        #TODO add comment
        """
        if self.org_api_key.org_api_key_id is not None and self.org_api_key.org_api_key_id > 0:
            org_api_key_manager = OrgApiKeyManager(self._session_context)
            self.org_api_key = await org_api_key_manager.update(self.org_api_key)
        if self.org_api_key.org_api_key_id is None or self.org_api_key.org_api_key_id == 0:
            org_api_key_manager = OrgApiKeyManager(self._session_context)
            self.org_api_key = await org_api_key_manager.add(self.org_api_key)
        return self
    async def delete(self):
        """
        #TODO add comment
        """
        if self.org_api_key.org_api_key_id > 0:
            org_api_key_manager = OrgApiKeyManager(self._session_context)
            await org_api_key_manager.delete(self.org_api_key.org_api_key_id)
            self.org_api_key = None
    async def randomize_properties(self):
        """
        #TODO add comment
        """
        self.org_api_key.api_key_value = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        self.org_api_key.created_by = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        self.org_api_key.created_utc_date_time = datetime(
            random.randint(2000, 2023),
            random.randint(1, 12),
            random.randint(1, 28))
        self.org_api_key.expiration_utc_date_time = datetime(
            random.randint(2000, 2023),
            random.randint(1, 12),
            random.randint(1, 28))
        self.org_api_key.is_active = random.choice([True, False])
        self.org_api_key.is_temp_user_key = random.choice([True, False])
        self.org_api_key.name = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        # self.org_api_key.organization_id = random.randint(0, 100)
        self.org_api_key.org_customer_id = random.choice(
            await managers_and_enums.OrgCustomerManager(
                self._session_context).get_list()).org_customer_id
# endset
        return self
    def get_org_api_key_obj(self) -> OrgApiKey:
        """
        #TODO add comment
        """
        return self.org_api_key
    def is_equal(self, org_api_key: OrgApiKey) -> OrgApiKey:
        """
        #TODO add comment
        """
        org_api_key_manager = OrgApiKeyManager(self._session_context)
        my_org_api_key = self.get_org_api_key_obj()
        return org_api_key_manager.is_equal(org_api_key, my_org_api_key)
# endset
    # apiKeyValue,
    # createdBy,
    # createdUTCDateTime
    # expirationUTCDateTime
    # isActive,
    # isTempUserKey,
    # name,
    # OrganizationID
    async def get_organization_id_rel_obj(self) -> models.Organization:
        """
        #TODO add comment
        """
        organization_manager = managers_and_enums.OrganizationManager(self._session_context)
        organization_obj = await organization_manager.get_by_id(self.organization_id)
        return organization_obj
    # OrgCustomerID
    async def get_org_customer_id_rel_obj(self) -> models.OrgCustomer:
        """
        #TODO add comment
        """
        org_customer_manager = managers_and_enums.OrgCustomerManager(
            self._session_context)
        org_customer_obj = await org_customer_manager.get_by_id(
            self.org_customer_id
        )
        return org_customer_obj
# endset
    def get_obj(self) -> OrgApiKey:
        """
        #TODO add comment
        """
        return self.org_api_key
    def get_object_name(self) -> str:
        """
        #TODO add comment
        """
        return "org_api_key"
    def get_id(self) -> int:
        """
        #TODO add comment
        """
        return self.org_api_key_id
    # apiKeyValue,
    # createdBy,
    # createdUTCDateTime
    # expirationUTCDateTime
    # isActive,
    # isTempUserKey,
    # name,
    # OrganizationID
    async def get_parent_name(self) -> str:
        """
        #TODO add comment
        """
        return 'Organization'
    async def get_parent_code(self) -> uuid.UUID:
        """
        #TODO add comment
        """
        return self.organization_code_peek
    async def get_parent_obj(self) -> models.Organization:
        """
        #TODO add comment
        """
        return self.get_organization_id_rel_obj()
    # OrgCustomerID
# endset
    @staticmethod
    async def to_bus_obj_list(
        session_context: SessionContext,
        obj_list: List[OrgApiKey]
    ):
        """
        #TODO add comment
        """
        result = list()
        for org_api_key in obj_list:
            org_api_key_bus_obj = OrgApiKeyBusObj.get(
                session_context,
                org_api_key_obj_instance=org_api_key
            )
            result.append(org_api_key_bus_obj)
        return result

