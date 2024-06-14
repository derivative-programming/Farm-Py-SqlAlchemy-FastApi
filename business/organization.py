# business/organization.py
"""
    #TODO add comment
"""
import random
import uuid
from typing import List
from datetime import datetime, date
from helpers.session_context import SessionContext
from managers import OrganizationManager
from models import Organization
import models
import managers as managers_and_enums
from .base_bus_obj import BaseBusObj

from business.org_customer import OrgCustomerBusObj

from business.org_api_key import OrgApiKeyBusObj

class OrganizationInvalidInitError(Exception):
    """
    #TODO add comment
    """
    pass
class OrganizationBusObj(BaseBusObj):
    """
    This class represents the business object for a Organization.
    It requires a valid session context for initialization.
    """
    def __init__(self, session_context: SessionContext):
        if not session_context.session:
            raise ValueError("session required")
        self._session_context = session_context
        self.organization = Organization()
    @property
    def organization_id(self):
        """
        Get the organization ID from the Organization object.
        :return: The organization ID.
        """
        if not self.organization:
            raise AttributeError("Organization object is not initialized")
        return self.organization.organization_id
    @organization_id.setter
    def organization_id(self, value: int):
        """
        #TODO add comment
        """
        if not isinstance(value, int):
            raise ValueError("organization_id must be a int.")
        self.organization.organization_id = value
    # code
    @property
    def code(self):
        """
        #TODO add comment
        """
        if not self.organization:
            raise AttributeError("Organization object is not initialized")
        return self.organization.code
    @code.setter
    def code(self, value: uuid.UUID):  # type: ignore
        """
        #TODO add comment
        """
        if not self.organization:
            raise AttributeError("Organization object is not initialized")
        if not isinstance(value, uuid.UUID):
            raise ValueError("code must be a UUID.")
        self.organization.code = value
    # last_change_code
    @property
    def last_change_code(self):
        """
        #TODO add comment
        """
        if not self.organization:
            raise AttributeError("Organization object is not initialized")
        return self.organization.last_change_code
    @last_change_code.setter
    def last_change_code(self, value: int):
        """
        #TODO add comment
        """
        if not self.organization:
            raise AttributeError("Organization object is not initialized")
        if not isinstance(value, int):
            raise ValueError("last_change_code must be an integer.")
        self.organization.last_change_code = value
    # insert_user_id
    @property
    def insert_user_id(self):
        """
        #TODO add comment
        """
        if not self.organization:
            raise AttributeError("Organization object is not initialized")
        return self.organization.insert_user_id
    @insert_user_id.setter
    def insert_user_id(self, value: uuid.UUID):
        """
        #TODO add comment
        """
        if not self.organization:
            raise AttributeError("Organization object is not initialized")
        if not isinstance(value, uuid.UUID):
            raise ValueError("insert_user_id must be a UUID.")
        self.organization.insert_user_id = value
    # def set_prop_insert_user_id(self, value: uuid.UUID):
    #     """
    #     #TODO add comment
    #     """
    #     if not self.organization:
    #         raise AttributeError("Organization object is not initialized")
    #     self.insert_user_id = value
    #     return self
    # last_update_user_id
    @property
    def last_update_user_id(self):
        """
        #TODO add comment
        """
        if not self.organization:
            raise AttributeError("Organization object is not initialized")
        return self.organization.last_update_user_id
    @last_update_user_id.setter
    def last_update_user_id(self, value: uuid.UUID):
        """
        #TODO add comment
        """
        if not self.organization:
            raise AttributeError("Organization object is not initialized")
        if not isinstance(value, uuid.UUID):
            raise ValueError("last_update_user_id must be a UUID.")
        self.organization.last_update_user_id = value
    # def set_prop_last_update_user_id(self, value: uuid.UUID):
    #     """
    #     #TODO add comment
    #     """
    #     self.last_update_user_id = value
    #     return self
# endset
    # name
    @property
    def name(self):
        """
        #TODO add comment
        """
        if not self.organization:
            raise AttributeError("Organization object is not initialized")
        if self.organization.name is None:
            return ""
        return self.organization.name
    @name.setter
    def name(self, value):
        """
        #TODO add comment
        """
        if not self.organization:
            raise AttributeError("Organization object is not initialized")
        assert isinstance(value, str), "name must be a string"
        self.organization.name = value
    # def set_prop_name(self, value):
    #     """
    #     #TODO add comment
    #     """
    #     self.name = value
    #     return self
    # TacID
# endset
    # name,
    # TacID
    @property
    def tac_id(self):
        """
        #TODO add comment
        """
        if not self.organization:
            raise AttributeError("Organization object is not initialized")
        return self.organization.tac_id
    @tac_id.setter
    def tac_id(self, value):
        """
        #TODO add comment
        """
        if not self.organization:
            raise AttributeError("Organization object is not initialized")
        assert isinstance(value, int) or value is None, (
            "tac_id must be an integer or None")
        self.organization.tac_id = value
    # def set_prop_tac_id(self, value):
    #     """
    #     #TODO add comment
    #     """
    #     self.tac_id = value
    #     return self
    @property
    def tac_code_peek(self):
        """
        #TODO add comment
        """
        if not self.organization:
            raise AttributeError("Organization object is not initialized")
        return self.organization.tac_code_peek
    # @tac_code_peek.setter
    # def tac_code_peek(self, value):
    #     assert isinstance(value, uuid.UUID),
    #           "tac_code_peek must be a UUID"
    #     self.organization.tac_code_peek = value
# endset
    # insert_utc_date_time
    @property
    def insert_utc_date_time(self):
        """
        #TODO add comment
        """
        if not self.organization:
            raise AttributeError("Organization object is not initialized")
        return self.organization.insert_utc_date_time
    @insert_utc_date_time.setter
    def insert_utc_date_time(self, value):
        """
        #TODO add comment
        """
        if not self.organization:
            raise AttributeError("Organization object is not initialized")
        assert isinstance(value, datetime) or value is None, (
            "insert_utc_date_time must be a datetime object or None")
        self.organization.insert_utc_date_time = value
    # update_utc_date_time
    @property
    def last_update_utc_date_time(self):
        """
        #TODO add comment
        """
        if not self.organization:
            raise AttributeError("Organization object is not initialized")
        return self.organization.last_update_utc_date_time
    @last_update_utc_date_time.setter
    def last_update_utc_date_time(self, value):
        """
        #TODO add comment
        """
        if not self.organization:
            raise AttributeError("Organization object is not initialized")
        assert isinstance(value, datetime) or value is None, (
            "last_update_utc_date_time must be a datetime object or None")
        self.organization.last_update_utc_date_time = value
    async def load_from_json(
        self,
        json_data: str
    ):
        """
        Load organization data from JSON string.
        :param json_data: JSON string containing organization data.
        :raises ValueError: If json_data is not a string or if no organization data is found.
        """
        if not isinstance(json_data, str):
            raise ValueError("json_data must be a string")
        organization_manager = OrganizationManager(self._session_context)
        self.organization = organization_manager.from_json(json_data)
        return self
    async def load_from_code(
        self,
        code: uuid.UUID
    ):
        """
        Load organization data from UUID code.
        :param code: UUID code for loading a specific organization.
        :raises ValueError: If code is not a UUID or if no organization data is found.
        """
        if not isinstance(code, uuid.UUID):
            raise ValueError("code must be a UUID")
        organization_manager = OrganizationManager(self._session_context)
        organization_obj = await organization_manager.get_by_code(code)
        self.organization = organization_obj
        return self
    async def load_from_id(
        self,
        organization_id: int
    ):
        """
        Load organization data from organization ID.
        :param organization_id: Integer ID for loading a specific organization.
        :raises ValueError: If organization_id is not an integer or if no organization data is found.
        """
        if not isinstance(organization_id, int):
            raise ValueError("organization_id must be an integer")
        organization_manager = OrganizationManager(self._session_context)
        organization_obj = await organization_manager.get_by_id(organization_id)
        self.organization = organization_obj
        return self
    async def load_from_obj_instance(
        self,
        organization_obj_instance: Organization
    ):
        """
        Use the provided Organization instance.
        :param organization_obj_instance: Instance of the Organization class.
        :raises ValueError: If organization_obj_instance is not an instance of Organization.
        """
        if not isinstance(organization_obj_instance, Organization):
            raise ValueError("organization_obj_instance must be an instance of Organization")
        organization_manager = OrganizationManager(self._session_context)
        organization_obj_instance_organization_id = organization_obj_instance.organization_id
        organization_obj = await organization_manager.get_by_id(
            organization_obj_instance_organization_id
        )
        self.organization = organization_obj
        return self
    async def load_from_dict(
        self,
        organization_dict: dict
    ):
        """
        Load organization data from dictionary.
        :param organization_dict: Dictionary containing organization data.
        :raises ValueError: If organization_dict is not a dictionary or if no organization data is found.
        """
        if not isinstance(organization_dict, dict):
            raise ValueError("organization_dict must be a dictionary")
        organization_manager = OrganizationManager(self._session_context)
        self.organization = organization_manager.from_dict(organization_dict)
        return self

    async def refresh(self):
        """
        #TODO add comment
        """
        organization_manager = OrganizationManager(self._session_context)
        self.organization = await organization_manager.refresh(self.organization)
        return self
    def is_valid(self):
        """
        #TODO add comment
        """
        return (self.organization is not None)
    def to_dict(self):
        """
        #TODO add comment
        """
        organization_manager = OrganizationManager(self._session_context)
        return organization_manager.to_dict(self.organization)
    def to_json(self):
        """
        #TODO add comment
        """
        organization_manager = OrganizationManager(self._session_context)
        return organization_manager.to_json(self.organization)
    async def save(self):
        """
        #TODO add comment
        """
        if not self.organization:
            raise AttributeError("Organization object is not initialized")
        if self.organization.organization_id is not None and self.organization.organization_id > 0:
            organization_manager = OrganizationManager(self._session_context)
            self.organization = await organization_manager.update(self.organization)
        if self.organization.organization_id is None or self.organization.organization_id == 0:
            organization_manager = OrganizationManager(self._session_context)
            self.organization = await organization_manager.add(self.organization)
        return self
    async def delete(self):
        """
        #TODO add comment
        """
        if not self.organization:
            raise AttributeError("Organization object is not initialized")
        if self.organization.organization_id > 0:
            organization_manager = OrganizationManager(self._session_context)
            await organization_manager.delete(self.organization.organization_id)
            self.organization = None
    async def randomize_properties(self):
        """
        #TODO add comment
        """
        if not self.organization:
            raise AttributeError("Organization object is not initialized")
        self.organization.name = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        # self.organization.tac_id = random.randint(0, 100)
# endset
        return self
    def get_organization_obj(self) -> Organization:
        """
        #TODO add comment
        """
        if not self.organization:
            raise AttributeError("Organization object is not initialized")
        return self.organization
    def is_equal(self, organization: Organization) -> bool:
        """
        #TODO add comment
        """
        organization_manager = OrganizationManager(self._session_context)
        my_organization = self.get_organization_obj()
        return organization_manager.is_equal(organization, my_organization)
# endset
    # name,
    # TacID
    async def get_tac_id_rel_obj(self) -> models.Tac:
        """
        #TODO add comment
        """
        tac_manager = managers_and_enums.TacManager(self._session_context)
        tac_obj = await tac_manager.get_by_id(self.tac_id)
        return tac_obj
# endset
    def get_obj(self) -> Organization:
        """
        #TODO add comment
        """
        return self.organization
    def get_object_name(self) -> str:
        """
        #TODO add comment
        """
        return "organization"
    def get_id(self) -> int:
        """
        #TODO add comment
        """
        return self.organization_id
    # name,
    # TacID
    async def get_parent_name(self) -> str:
        """
        #TODO add comment
        """
        return 'Tac'
    async def get_parent_code(self) -> uuid.UUID:
        """
        #TODO add comment
        """
        return self.tac_code_peek
    async def get_parent_obj(self) -> models.Tac:
        """
        #TODO add comment
        """
        return self.get_tac_id_rel_obj()
# endset
    @staticmethod
    async def to_bus_obj_list(
        session_context: SessionContext,
        obj_list: List[Organization]
    ):
        """
        #TODO add comment
        """
        result = list()
        for organization in obj_list:
            organization_bus_obj = OrganizationBusObj.get(
                session_context,
                organization_obj_instance=organization
            )
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

