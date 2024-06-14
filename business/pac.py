# business/pac.py
"""
    #TODO add comment
"""
import random
import uuid
from typing import List
from datetime import datetime, date
from helpers.session_context import SessionContext
from managers import PacManager
from models import Pac
import models
import managers as managers_and_enums
from .base_bus_obj import BaseBusObj

from business.tri_state_filter import TriStateFilterBusObj

from business.tac import TacBusObj

from business.role import RoleBusObj

from business.land import LandBusObj

from business.flavor import FlavorBusObj

from business.error_log import ErrorLogBusObj

from business.date_greater_than_filter import DateGreaterThanFilterBusObj

class PacInvalidInitError(Exception):
    """
    #TODO add comment
    """
    pass
class PacBusObj(BaseBusObj):
    """
    This class represents the business object for a Pac.
    It requires a valid session context for initialization.
    """
    def __init__(self, session_context: SessionContext):
        if not session_context.session:
            raise ValueError("session required")
        self._session_context = session_context
        self.pac = Pac()
    @property
    def pac_id(self):
        """
        Get the pac ID from the Pac object.
        :return: The pac ID.
        """
        if not self.pac:
            raise AttributeError("Pac object is not initialized")
        return self.pac.pac_id
    @pac_id.setter
    def pac_id(self, value: int):
        """
        #TODO add comment
        """
        if not isinstance(value, int):
            raise ValueError("pac_id must be a int.")
        self.pac.pac_id = value
    # code
    @property
    def code(self):
        """
        #TODO add comment
        """
        if not self.pac:
            raise AttributeError("Pac object is not initialized")
        return self.pac.code
    @code.setter
    def code(self, value: uuid.UUID):  # type: ignore
        """
        #TODO add comment
        """
        if not self.pac:
            raise AttributeError("Pac object is not initialized")
        if not isinstance(value, uuid.UUID):
            raise ValueError("code must be a UUID.")
        self.pac.code = value
    # last_change_code
    @property
    def last_change_code(self):
        """
        #TODO add comment
        """
        if not self.pac:
            raise AttributeError("Pac object is not initialized")
        return self.pac.last_change_code
    @last_change_code.setter
    def last_change_code(self, value: int):
        """
        #TODO add comment
        """
        if not self.pac:
            raise AttributeError("Pac object is not initialized")
        if not isinstance(value, int):
            raise ValueError("last_change_code must be an integer.")
        self.pac.last_change_code = value
    # insert_user_id
    @property
    def insert_user_id(self):
        """
        #TODO add comment
        """
        if not self.pac:
            raise AttributeError("Pac object is not initialized")
        return self.pac.insert_user_id
    @insert_user_id.setter
    def insert_user_id(self, value: uuid.UUID):
        """
        #TODO add comment
        """
        if not self.pac:
            raise AttributeError("Pac object is not initialized")
        if not isinstance(value, uuid.UUID):
            raise ValueError("insert_user_id must be a UUID.")
        self.pac.insert_user_id = value
    # def set_prop_insert_user_id(self, value: uuid.UUID):
    #     """
    #     #TODO add comment
    #     """
    #     if not self.pac:
    #         raise AttributeError("Pac object is not initialized")
    #     self.insert_user_id = value
    #     return self
    # last_update_user_id
    @property
    def last_update_user_id(self):
        """
        #TODO add comment
        """
        if not self.pac:
            raise AttributeError("Pac object is not initialized")
        return self.pac.last_update_user_id
    @last_update_user_id.setter
    def last_update_user_id(self, value: uuid.UUID):
        """
        #TODO add comment
        """
        if not self.pac:
            raise AttributeError("Pac object is not initialized")
        if not isinstance(value, uuid.UUID):
            raise ValueError("last_update_user_id must be a UUID.")
        self.pac.last_update_user_id = value
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
        if not self.pac:
            raise AttributeError("Pac object is not initialized")
        if self.pac.description is None:
            return ""
        return self.pac.description
    @description.setter
    def description(self, value):
        """
        #TODO add comment
        """
        if not self.pac:
            raise AttributeError("Pac object is not initialized")
        assert isinstance(value, str), "description must be a string"
        self.pac.description = value
    # def set_prop_description(self, value):
    #     """
    #     #TODO add comment
    #     """
    #     self.description = value
    #     return self
    # displayOrder
    @property
    def display_order(self):
        """
        #TODO add comment
        """
        if not self.pac:
            raise AttributeError("Pac object is not initialized")
        return self.pac.display_order
    @display_order.setter
    def display_order(self, value):
        """
        #TODO add comment
        """
        if not self.pac:
            raise AttributeError("Pac object is not initialized")
        assert isinstance(value, int), (
            "display_order must be an integer")
        self.pac.display_order = value
    # def set_prop_display_order(self, value):
    #     """
    #     #TODO add comment
    #     """
    #     self.display_order = value
    #     return self
    # isActive
    @property
    def is_active(self):
        """
        #TODO add comment
        """
        if not self.pac:
            raise AttributeError("Pac object is not initialized")
        return self.pac.is_active
    @is_active.setter
    def is_active(self, value: bool):
        """
        #TODO add comment
        """
        if not self.pac:
            raise AttributeError("Pac object is not initialized")
        if not isinstance(value, bool):
            raise ValueError("is_active must be a boolean.")
        self.pac.is_active = value
    # def set_prop_is_active(self, value: bool):
    #     """
    #     #TODO add comment
    #     """
    #     self.is_active = value
    #     return self
    # lookupEnumName
    @property
    def lookup_enum_name(self):
        """
        #TODO add comment
        """
        if not self.pac:
            raise AttributeError("Pac object is not initialized")
        if self.pac.lookup_enum_name is None:
            return ""
        return self.pac.lookup_enum_name
    @lookup_enum_name.setter
    def lookup_enum_name(self, value):
        """
        #TODO add comment
        """
        if not self.pac:
            raise AttributeError("Pac object is not initialized")
        assert isinstance(value, str), "lookup_enum_name must be a string"
        self.pac.lookup_enum_name = value
    # def set_prop_lookup_enum_name(self, value):
    #     """
    #     #TODO add comment
    #     """
    #     self.lookup_enum_name = value
    #     return self
    # name
    @property
    def name(self):
        """
        #TODO add comment
        """
        if not self.pac:
            raise AttributeError("Pac object is not initialized")
        if self.pac.name is None:
            return ""
        return self.pac.name
    @name.setter
    def name(self, value):
        """
        #TODO add comment
        """
        if not self.pac:
            raise AttributeError("Pac object is not initialized")
        assert isinstance(value, str), "name must be a string"
        self.pac.name = value
    # def set_prop_name(self, value):
    #     """
    #     #TODO add comment
    #     """
    #     self.name = value
    #     return self
# endset
    # description,
    # displayOrder,
    # isActive,
    # lookupEnumName,
    # name,
# endset
    # insert_utc_date_time
    @property
    def insert_utc_date_time(self):
        """
        #TODO add comment
        """
        if not self.pac:
            raise AttributeError("Pac object is not initialized")
        return self.pac.insert_utc_date_time
    @insert_utc_date_time.setter
    def insert_utc_date_time(self, value):
        """
        #TODO add comment
        """
        if not self.pac:
            raise AttributeError("Pac object is not initialized")
        assert isinstance(value, datetime) or value is None, (
            "insert_utc_date_time must be a datetime object or None")
        self.pac.insert_utc_date_time = value
    # update_utc_date_time
    @property
    def last_update_utc_date_time(self):
        """
        #TODO add comment
        """
        if not self.pac:
            raise AttributeError("Pac object is not initialized")
        return self.pac.last_update_utc_date_time
    @last_update_utc_date_time.setter
    def last_update_utc_date_time(self, value):
        """
        #TODO add comment
        """
        if not self.pac:
            raise AttributeError("Pac object is not initialized")
        assert isinstance(value, datetime) or value is None, (
            "last_update_utc_date_time must be a datetime object or None")
        self.pac.last_update_utc_date_time = value
    async def load_from_json(
        self,
        json_data: str
    ):
        """
        Load pac data from JSON string.
        :param json_data: JSON string containing pac data.
        :raises ValueError: If json_data is not a string or if no pac data is found.
        """
        if not isinstance(json_data, str):
            raise ValueError("json_data must be a string")
        pac_manager = PacManager(self._session_context)
        self.pac = pac_manager.from_json(json_data)
        return self
    async def load_from_code(
        self,
        code: uuid.UUID
    ):
        """
        Load pac data from UUID code.
        :param code: UUID code for loading a specific pac.
        :raises ValueError: If code is not a UUID or if no pac data is found.
        """
        if not isinstance(code, uuid.UUID):
            raise ValueError("code must be a UUID")
        pac_manager = PacManager(self._session_context)
        pac_obj = await pac_manager.get_by_code(code)
        self.pac = pac_obj
        return self
    async def load_from_id(
        self,
        pac_id: int
    ):
        """
        Load pac data from pac ID.
        :param pac_id: Integer ID for loading a specific pac.
        :raises ValueError: If pac_id is not an integer or if no pac data is found.
        """
        if not isinstance(pac_id, int):
            raise ValueError("pac_id must be an integer")
        pac_manager = PacManager(self._session_context)
        pac_obj = await pac_manager.get_by_id(pac_id)
        self.pac = pac_obj
        return self
    async def load_from_obj_instance(
        self,
        pac_obj_instance: Pac
    ):
        """
        Use the provided Pac instance.
        :param pac_obj_instance: Instance of the Pac class.
        :raises ValueError: If pac_obj_instance is not an instance of Pac.
        """
        if not isinstance(pac_obj_instance, Pac):
            raise ValueError("pac_obj_instance must be an instance of Pac")
        pac_manager = PacManager(self._session_context)
        pac_obj_instance_pac_id = pac_obj_instance.pac_id
        pac_obj = await pac_manager.get_by_id(
            pac_obj_instance_pac_id
        )
        self.pac = pac_obj
        return self
    async def load_from_dict(
        self,
        pac_dict: dict
    ):
        """
        Load pac data from dictionary.
        :param pac_dict: Dictionary containing pac data.
        :raises ValueError: If pac_dict is not a dictionary or if no pac data is found.
        """
        if not isinstance(pac_dict, dict):
            raise ValueError("pac_dict must be a dictionary")
        pac_manager = PacManager(self._session_context)
        self.pac = pac_manager.from_dict(pac_dict)
        return self

    @property
    def lookup_enum(self) -> managers_and_enums.PacEnum:
        return managers_and_enums.PacEnum[self.pac.lookup_enum_name]
    async def load_from_enum(
        self,
        pac_enum:
            managers_and_enums.PacEnum
    ):
        """
        Load plant data from dictionary.
        :param plant_dict: Dictionary containing plant data.
        :raises ValueError: If plant_dict is not a dictionary or if no plant data is found.
        """
        if not isinstance(pac_enum, managers_and_enums.PacEnum):
            raise ValueError("pac_enum must be a enum")
        pac_manager = PacManager(self._session_context)
        self.pac = await pac_manager.from_enum(pac_enum)

    def get_session_context(self):
        """
        #TODO add comment
        """
        return self._session_context
    async def refresh(self):
        """
        #TODO add comment
        """
        pac_manager = PacManager(self._session_context)
        self.pac = await pac_manager.refresh(self.pac)
        return self
    def is_valid(self):
        """
        #TODO add comment
        """
        return (self.pac is not None)
    def to_dict(self):
        """
        #TODO add comment
        """
        pac_manager = PacManager(self._session_context)
        return pac_manager.to_dict(self.pac)
    def to_json(self):
        """
        #TODO add comment
        """
        pac_manager = PacManager(self._session_context)
        return pac_manager.to_json(self.pac)
    async def save(self):
        """
        #TODO add comment
        """
        if not self.pac:
            raise AttributeError("Pac object is not initialized")
        if self.pac.pac_id is not None and self.pac.pac_id > 0:
            pac_manager = PacManager(self._session_context)
            self.pac = await pac_manager.update(self.pac)
        if self.pac.pac_id is None or self.pac.pac_id == 0:
            pac_manager = PacManager(self._session_context)
            self.pac = await pac_manager.add(self.pac)
        return self
    async def delete(self):
        """
        #TODO add comment
        """
        if not self.pac:
            raise AttributeError("Pac object is not initialized")
        if self.pac.pac_id > 0:
            pac_manager = PacManager(self._session_context)
            await pac_manager.delete(self.pac.pac_id)
            self.pac = None
    async def randomize_properties(self):
        """
        #TODO add comment
        """
        if not self.pac:
            raise AttributeError("Pac object is not initialized")
        self.pac.description = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        self.pac.display_order = random.randint(0, 100)
        self.pac.is_active = random.choice([True, False])
        self.pac.lookup_enum_name = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        self.pac.name = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
# endset
        return self
    def get_pac_obj(self) -> Pac:
        """
        #TODO add comment
        """
        if not self.pac:
            raise AttributeError("Pac object is not initialized")
        return self.pac
    def is_equal(self, pac: Pac) -> bool:
        """
        #TODO add comment
        """
        pac_manager = PacManager(self._session_context)
        my_pac = self.get_pac_obj()
        return pac_manager.is_equal(pac, my_pac)
# endset
    # description,
    # displayOrder,
    # isActive,
    # lookupEnumName,
    # name,
# endset
    def get_obj(self) -> Pac:
        """
        #TODO add comment
        """
        return self.pac
    def get_object_name(self) -> str:
        """
        #TODO add comment
        """
        return "pac"
    def get_id(self) -> int:
        """
        #TODO add comment
        """
        return self.pac_id
    # description,
    # displayOrder,
    # isActive,
    # lookupEnumName,
    # name,
# endset
    @staticmethod
    async def to_bus_obj_list(
        session_context: SessionContext,
        obj_list: List[Pac]
    ):
        """
        #TODO add comment
        """
        result = list()
        for pac in obj_list:
            pac_bus_obj = PacBusObj(session_context)
            await pac_bus_obj.load_from_obj_instance(pac)
            result.append(pac_bus_obj)
        return result

    async def build_tri_state_filter(self) -> TriStateFilterBusObj:
        item = TriStateFilterBusObj(self._session_context)

        item.pac_id = self.pac_id
        item.tri_state_filter.pac_code_peek = self.code

        return item

    async def get_all_tri_state_filter(self) -> List[TriStateFilterBusObj]:
        results = list()
        tri_state_filter_manager = managers_and_enums.TriStateFilterManager(self._session_context)
        obj_list = await tri_state_filter_manager.get_by_pac_id(self.pac_id)
        for obj_item in obj_list:
            bus_obj_item = TriStateFilterBusObj(self._session_context)
            await bus_obj_item.load_from_obj_instance(obj_item)
            results.append(bus_obj_item)
        return results

    async def build_tac(self) -> TacBusObj:
        item = TacBusObj(self._session_context)

        item.pac_id = self.pac_id
        item.tac.pac_code_peek = self.code

        return item

    async def get_all_tac(self) -> List[TacBusObj]:
        results = list()
        tac_manager = managers_and_enums.TacManager(self._session_context)
        obj_list = await tac_manager.get_by_pac_id(self.pac_id)
        for obj_item in obj_list:
            bus_obj_item = TacBusObj(self._session_context)
            await bus_obj_item.load_from_obj_instance(obj_item)
            results.append(bus_obj_item)
        return results

    async def build_role(self) -> RoleBusObj:
        item = RoleBusObj(self._session_context)

        item.pac_id = self.pac_id
        item.role.pac_code_peek = self.code

        return item

    async def get_all_role(self) -> List[RoleBusObj]:
        results = list()
        role_manager = managers_and_enums.RoleManager(self._session_context)
        obj_list = await role_manager.get_by_pac_id(self.pac_id)
        for obj_item in obj_list:
            bus_obj_item = RoleBusObj(self._session_context)
            await bus_obj_item.load_from_obj_instance(obj_item)
            results.append(bus_obj_item)
        return results

    async def build_land(self) -> LandBusObj:
        item = LandBusObj(self._session_context)

        item.pac_id = self.pac_id
        item.land.pac_code_peek = self.code

        return item

    async def get_all_land(self) -> List[LandBusObj]:
        results = list()
        land_manager = managers_and_enums.LandManager(self._session_context)
        obj_list = await land_manager.get_by_pac_id(self.pac_id)
        for obj_item in obj_list:
            bus_obj_item = LandBusObj(self._session_context)
            await bus_obj_item.load_from_obj_instance(obj_item)
            results.append(bus_obj_item)
        return results

    async def build_flavor(self) -> FlavorBusObj:
        item = FlavorBusObj(self._session_context)

        item.pac_id = self.pac_id
        item.flavor.pac_code_peek = self.code

        return item

    async def get_all_flavor(self) -> List[FlavorBusObj]:
        results = list()
        flavor_manager = managers_and_enums.FlavorManager(self._session_context)
        obj_list = await flavor_manager.get_by_pac_id(self.pac_id)
        for obj_item in obj_list:
            bus_obj_item = FlavorBusObj(self._session_context)
            await bus_obj_item.load_from_obj_instance(obj_item)
            results.append(bus_obj_item)
        return results

    async def build_error_log(self) -> ErrorLogBusObj:
        item = ErrorLogBusObj(self._session_context)

        item.pac_id = self.pac_id
        item.error_log.pac_code_peek = self.code

        return item

    async def get_all_error_log(self) -> List[ErrorLogBusObj]:
        results = list()
        error_log_manager = managers_and_enums.ErrorLogManager(self._session_context)
        obj_list = await error_log_manager.get_by_pac_id(self.pac_id)
        for obj_item in obj_list:
            bus_obj_item = ErrorLogBusObj(self._session_context)
            await bus_obj_item.load_from_obj_instance(obj_item)
            results.append(bus_obj_item)
        return results

    async def build_date_greater_than_filter(self) -> DateGreaterThanFilterBusObj:
        item = DateGreaterThanFilterBusObj(self._session_context)

        item.pac_id = self.pac_id
        item.date_greater_than_filter.pac_code_peek = self.code

        return item

    async def get_all_date_greater_than_filter(self) -> List[DateGreaterThanFilterBusObj]:
        results = list()
        date_greater_than_filter_manager = managers_and_enums.DateGreaterThanFilterManager(self._session_context)
        obj_list = await date_greater_than_filter_manager.get_by_pac_id(self.pac_id)
        for obj_item in obj_list:
            bus_obj_item = DateGreaterThanFilterBusObj(self._session_context)
            await bus_obj_item.load_from_obj_instance(obj_item)
            results.append(bus_obj_item)
        return results

