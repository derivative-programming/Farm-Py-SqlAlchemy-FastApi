# business/tac.py
"""
    #TODO add comment
"""
from decimal import Decimal
import random
import uuid
from typing import List
from datetime import datetime, date
from helpers.session_context import SessionContext
from managers import TacManager
from models import Tac
import models
import managers as managers_and_enums
from .base_bus_obj import BaseBusObj

from business.organization import OrganizationBusObj

from business.customer import CustomerBusObj

NOT_INITIALIZED_ERROR_MESSAGE = (
    "Tac object is not initialized")
class TacInvalidInitError(Exception):
    """
    #TODO add comment
    """
class TacBusObj(BaseBusObj):
    """
    This class represents the business object for a Tac.
    It requires a valid session context for initialization.
    """
    def __init__(self, session_context: SessionContext):
        if not session_context.session:
            raise ValueError("session required")
        self._session_context = session_context
        self.tac = Tac()
    @property
    def tac_id(self) -> int:
        """
        Get the tac ID from the Tac object.
        :return: The tac ID.
        """
        if not self.tac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.tac.tac_id
    # @tac_id.setter
    # def tac_id(self, value: int):
    #     """
    #     #TODO add comment
    #     """
    #     if not isinstance(value, int):
    #         raise ValueError("tac_id must be a int.")
    #     self.tac.tac_id = value
    # code
    @property
    def code(self):
        """
        #TODO add comment
        """
        if not self.tac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.tac.code
    @code.setter
    def code(self, value: uuid.UUID):  # type: ignore
        """
        #TODO add comment
        """
        if not self.tac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if not isinstance(value, uuid.UUID):
            raise ValueError("code must be a UUID.")
        self.tac.code = value
    # last_change_code
    @property
    def last_change_code(self):
        """
        #TODO add comment
        """
        if not self.tac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.tac.last_change_code
    @last_change_code.setter
    def last_change_code(self, value: int):
        """
        #TODO add comment
        """
        if not self.tac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if not isinstance(value, int):
            raise ValueError("last_change_code must be an integer.")
        self.tac.last_change_code = value
    # insert_user_id
    @property
    def insert_user_id(self):
        """
        #TODO add comment
        """
        if not self.tac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.tac.insert_user_id
    @insert_user_id.setter
    def insert_user_id(self, value: uuid.UUID):
        """
        #TODO add comment
        """
        if not self.tac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if not isinstance(value, uuid.UUID):
            raise ValueError("insert_user_id must be a UUID.")
        self.tac.insert_user_id = value
    # def set_prop_insert_user_id(self, value: uuid.UUID):
    #     """
    #     #TODO add comment
    #     """
    #     if not self.tac:
    #         raise AttributeError(NOT_INITIALIZED_ERROR_MESSAGE)
    #     self.insert_user_id = value
    #     return self
    # last_update_user_id
    @property
    def last_update_user_id(self):
        """
        #TODO add comment
        """
        if not self.tac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.tac.last_update_user_id
    @last_update_user_id.setter
    def last_update_user_id(self, value: uuid.UUID):
        """
        #TODO add comment
        """
        if not self.tac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if not isinstance(value, uuid.UUID):
            raise ValueError("last_update_user_id must be a UUID.")
        self.tac.last_update_user_id = value
    # def set_prop_last_update_user_id(self, value: uuid.UUID):
    #     """
    #     #TODO add comment
    #     """
    #     self.last_update_user_id = value
    #     return self
# endset
    # description
    @property
    def description(self):
        """
        #TODO add comment
        """
        if not self.tac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if self.tac.description is None:
            return ""
        return self.tac.description
    @description.setter
    def description(self, value):
        """
        #TODO add comment
        """
        if not self.tac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, str), "description must be a string"
        self.tac.description = value
    def set_prop_description(self, value: str):
        """
        #TODO add comment
        """
        self.description = value
        return self
    # displayOrder
    @property
    def display_order(self):
        """
        #TODO add comment
        """
        if not self.tac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.tac.display_order
    @display_order.setter
    def display_order(self, value):
        """
        #TODO add comment
        """
        if not self.tac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, int), (
            "display_order must be an integer")
        self.tac.display_order = value
    def set_prop_display_order(self, value: int):
        """
        #TODO add comment
        """
        self.display_order = value
        return self
    # isActive
    @property
    def is_active(self):
        """
        #TODO add comment
        """
        if not self.tac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.tac.is_active
    @is_active.setter
    def is_active(self, value: bool):
        """
        #TODO add comment
        """
        if not self.tac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if not isinstance(value, bool):
            raise ValueError("is_active must be a boolean.")
        self.tac.is_active = value
    def set_prop_is_active(self, value: bool):
        """
        #TODO add comment
        """
        self.is_active = value
        return self
    # lookupEnumName
    @property
    def lookup_enum_name(self):
        """
        #TODO add comment
        """
        if not self.tac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if self.tac.lookup_enum_name is None:
            return ""
        return self.tac.lookup_enum_name
    @lookup_enum_name.setter
    def lookup_enum_name(self, value):
        """
        #TODO add comment
        """
        if not self.tac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, str), "lookup_enum_name must be a string"
        self.tac.lookup_enum_name = value
    def set_prop_lookup_enum_name(self, value: str):
        """
        #TODO add comment
        """
        self.lookup_enum_name = value
        return self
    # name
    @property
    def name(self):
        """
        #TODO add comment
        """
        if not self.tac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if self.tac.name is None:
            return ""
        return self.tac.name
    @name.setter
    def name(self, value):
        """
        #TODO add comment
        """
        if not self.tac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, str), "name must be a string"
        self.tac.name = value
    def set_prop_name(self, value: str):
        """
        #TODO add comment
        """
        self.name = value
        return self
    # PacID
# endset
    # description,
    # displayOrder,
    # isActive,
    # lookupEnumName,
    # name,
    # PacID
    @property
    def pac_id(self):
        """
        #TODO add comment
        """
        if not self.tac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.tac.pac_id
    @pac_id.setter
    def pac_id(self, value):
        """
        #TODO add comment
        """
        if not self.tac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, int) or value is None, (
            "pac_id must be an integer or None")
        self.tac.pac_id = value
    def set_prop_pac_id(self, value: int):
        """
        #TODO add comment
        """
        self.pac_id = value
        return self
    @property
    def pac_code_peek(self) -> uuid.UUID:
        """
        #TODO add comment
        """
        if not self.tac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.tac.pac_code_peek
    # @pac_code_peek.setter
    # def pac_code_peek(self, value):
    #     assert isinstance(value, uuid.UUID),
    #           "pac_code_peek must be a UUID"
    #     self.tac.pac_code_peek = value
# endset
    # insert_utc_date_time
    @property
    def insert_utc_date_time(self):
        """
        #TODO add comment
        """
        if not self.tac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.tac.insert_utc_date_time
    @insert_utc_date_time.setter
    def insert_utc_date_time(self, value):
        """
        #TODO add comment
        """
        if not self.tac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, datetime) or value is None, (
            "insert_utc_date_time must be a datetime object or None")
        self.tac.insert_utc_date_time = value
    # update_utc_date_time
    @property
    def last_update_utc_date_time(self):
        """
        #TODO add comment
        """
        if not self.tac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.tac.last_update_utc_date_time
    @last_update_utc_date_time.setter
    def last_update_utc_date_time(self, value):
        """
        #TODO add comment
        """
        if not self.tac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, datetime) or value is None, (
            "last_update_utc_date_time must be a datetime object or None")
        self.tac.last_update_utc_date_time = value
    async def load_from_json(
        self,
        json_data: str
    ):
        """
        Load tac data from JSON string.
        :param json_data: JSON string containing tac data.
        :raises ValueError: If json_data is not a string
            or if no tac data is found.
        """
        if not isinstance(json_data, str):
            raise ValueError("json_data must be a string")
        tac_manager = TacManager(self._session_context)
        self.tac = tac_manager.from_json(json_data)
        return self
    async def load_from_code(
        self,
        code: uuid.UUID
    ):
        """
        Load tac data from UUID code.
        :param code: UUID code for loading a specific tac.
        :raises ValueError: If code is not a UUID or if no tac data is found.
        """
        if not isinstance(code, uuid.UUID):
            raise ValueError("code must be a UUID")
        tac_manager = TacManager(self._session_context)
        tac_obj = await tac_manager.get_by_code(code)
        self.tac = tac_obj
        return self
    async def load_from_id(
        self,
        tac_id: int
    ):
        """
        Load tac data from tac ID.
        :param tac_id: Integer ID for loading a specific tac.
        :raises ValueError: If tac_id is not an integer or
            if no tac data is found.
        """
        if not isinstance(tac_id, int):
            raise ValueError("tac_id must be an integer")
        tac_manager = TacManager(self._session_context)
        tac_obj = await tac_manager.get_by_id(tac_id)
        self.tac = tac_obj
        return self
    async def load_from_obj_instance(
        self,
        tac_obj_instance: Tac
    ):
        """
        Use the provided Tac instance.
        :param tac_obj_instance: Instance of the Tac class.
        :raises ValueError: If tac_obj_instance is not an instance of Tac.
        """
        if not isinstance(tac_obj_instance, Tac):
            raise ValueError("tac_obj_instance must be an instance of Tac")
        tac_manager = TacManager(self._session_context)
        tac_obj_instance_tac_id = tac_obj_instance.tac_id
        tac_obj = await tac_manager.get_by_id(
            tac_obj_instance_tac_id
        )
        self.tac = tac_obj
        return self
    async def load_from_dict(
        self,
        tac_dict: dict
    ):
        """
        Load tac data from dictionary.
        :param tac_dict: Dictionary containing tac data.
        :raises ValueError: If tac_dict is not a
            dictionary or if no tac data is found.
        """
        if not isinstance(tac_dict, dict):
            raise ValueError("tac_dict must be a dictionary")
        tac_manager = TacManager(self._session_context)
        self.tac = tac_manager.from_dict(tac_dict)
        return self

    @property
    def lookup_enum(self) -> managers_and_enums.TacEnum:
        """
        #TODO add comment
        """
        return (
            managers_and_enums.TacEnum[
                self.tac.lookup_enum_name
            ]
        )
    async def load_from_enum(
        self,
        tac_enum:
            managers_and_enums.TacEnum
    ):
        """
        Load tac data from dictionary.
        :param tac_dict: Dictionary
            containing tac data.
        :raises ValueError: If tac_dict
            is not a dictionary or if no
            tac data is found.
        """
        if not isinstance(
            tac_enum,
            managers_and_enums.TacEnum
        ):
            raise ValueError("tac_enum must be a enum")
        tac_manager = TacManager(
            self._session_context
        )
        self.tac = await (
            tac_manager.
            from_enum(tac_enum)
        )

    def get_session_context(self):
        """
        #TODO add comment
        """
        return self._session_context
    async def refresh(self):
        """
        #TODO add comment
        """
        tac_manager = TacManager(self._session_context)
        self.tac = await tac_manager.refresh(self.tac)
        return self
    def is_valid(self):
        """
        #TODO add comment
        """
        return self.tac is not None
    def to_dict(self):
        """
        #TODO add comment
        """
        tac_manager = TacManager(self._session_context)
        return tac_manager.to_dict(self.tac)
    def to_json(self):
        """
        #TODO add comment
        """
        tac_manager = TacManager(self._session_context)
        return tac_manager.to_json(self.tac)
    async def save(self):
        """
        #TODO add comment
        """
        if not self.tac:
            raise AttributeError(NOT_INITIALIZED_ERROR_MESSAGE)
        if self.tac.tac_id > 0:
            tac_manager = TacManager(self._session_context)
            self.tac = await tac_manager.update(self.tac)
        if self.tac.tac_id == 0:
            tac_manager = TacManager(self._session_context)
            self.tac = await tac_manager.add(self.tac)
        return self
    async def delete(self):
        """
        #TODO add comment
        """
        if not self.tac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if self.tac.tac_id > 0:
            tac_manager = TacManager(self._session_context)
            await tac_manager.delete(self.tac.tac_id)
            self.tac = None
    async def randomize_properties(self):
        """
        #TODO add comment
        """
        if not self.tac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        self.tac.description = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        self.tac.display_order = random.randint(0, 100)
        self.tac.is_active = random.choice([True, False])
        self.tac.lookup_enum_name = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        self.tac.name = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        # self.tac.pac_id = random.randint(0, 100)
# endset
        return self
    def get_tac_obj(self) -> Tac:
        """
        #TODO add comment
        """
        if not self.tac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.tac
    def is_equal(self, tac: Tac) -> bool:
        """
        #TODO add comment
        """
        tac_manager = TacManager(self._session_context)
        my_tac = self.get_tac_obj()
        return tac_manager.is_equal(tac, my_tac)
# endset
    # description,
    # displayOrder,
    # isActive,
    # lookupEnumName,
    # name,
    # PacID
    async def get_pac_id_rel_obj(self) -> models.Pac:
        """
        #TODO add comment
        """
        pac_manager = managers_and_enums.PacManager(self._session_context)
        pac_obj = await pac_manager.get_by_id(self.pac_id)
        return pac_obj
# endset
    def get_obj(self) -> Tac:
        """
        #TODO add comment
        """
        return self.tac
    def get_object_name(self) -> str:
        """
        #TODO add comment
        """
        return "tac"
    def get_id(self) -> int:
        """
        #TODO add comment
        """
        return self.tac_id
    # description,
    # displayOrder,
    # isActive,
    # lookupEnumName,
    # name,
    # PacID
    async def get_parent_name(self) -> str:
        """
        #TODO add comment
        """
        return 'Pac'
    async def get_parent_code(self) -> uuid.UUID:
        """
        #TODO add comment
        """
        return self.pac_code_peek
    async def get_parent_obj(self) -> models.Pac:
        """
        #TODO add comment
        """
        return self.get_pac_id_rel_obj()
# endset
    @staticmethod
    async def to_bus_obj_list(
        session_context: SessionContext,
        obj_list: List[Tac]
    ):
        """
        #TODO add comment
        """
        result = list()
        for tac in obj_list:
            tac_bus_obj = TacBusObj(session_context)
            await tac_bus_obj.load_from_obj_instance(tac)
            result.append(tac_bus_obj)
        return result

    async def build_organization(self) -> OrganizationBusObj:
        item = OrganizationBusObj(self._session_context)

        item.tac_id = self.tac_id
        item.organization.tac_code_peek = self.code

        return item

    async def get_all_organization(self) -> List[OrganizationBusObj]:
        results = list()
        organization_manager = managers_and_enums.OrganizationManager(self._session_context)
        obj_list = await organization_manager.get_by_tac_id(self.tac_id)
        for obj_item in obj_list:
            bus_obj_item = OrganizationBusObj(self._session_context)
            await bus_obj_item.load_from_obj_instance(obj_item)
            results.append(bus_obj_item)
        return results

    async def build_customer(self) -> CustomerBusObj:
        item = CustomerBusObj(self._session_context)

        item.tac_id = self.tac_id
        item.customer.tac_code_peek = self.code

        return item

    async def get_all_customer(self) -> List[CustomerBusObj]:
        results = list()
        customer_manager = managers_and_enums.CustomerManager(self._session_context)
        obj_list = await customer_manager.get_by_tac_id(self.tac_id)
        for obj_item in obj_list:
            bus_obj_item = CustomerBusObj(self._session_context)
            await bus_obj_item.load_from_obj_instance(obj_item)
            results.append(bus_obj_item)
        return results
    async def get_customer_by_email_prop(self, email) -> List[CustomerBusObj]:
        results = list()
        customer_manager = managers_and_enums.CustomerManager(self._session_context)
        obj_list = await customer_manager.get_by_email_prop(email)
        for obj_item in obj_list:
            bus_obj_item = CustomerBusObj(self._session_context)
            await bus_obj_item.load_from_obj_instance(obj_item)
            results.append(bus_obj_item)
        return results
    async def get_customer_by_fs_user_code_value_prop(self, fs_user_code_value) -> List[CustomerBusObj]:
        results = list()
        customer_manager = managers_and_enums.CustomerManager(self._session_context)
        obj_list = await customer_manager.get_by_fs_user_code_value_prop(fs_user_code_value)
        for obj_item in obj_list:
            bus_obj_item = CustomerBusObj(self._session_context)
            await bus_obj_item.load_from_obj_instance(obj_item)
            results.append(bus_obj_item)
        return results

