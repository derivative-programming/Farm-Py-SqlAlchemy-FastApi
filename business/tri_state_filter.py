# business/tri_state_filter.py
"""
    #TODO add comment
"""
import random
import uuid
from typing import List
from datetime import datetime, date
from helpers.session_context import SessionContext
from managers import TriStateFilterManager
from models import TriStateFilter
import models
import managers as managers_and_enums
from .base_bus_obj import BaseBusObj

class TriStateFilterInvalidInitError(Exception):
    """
    #TODO add comment
    """
    pass
class TriStateFilterBusObj(BaseBusObj):
    """
    This class represents the business object for a TriStateFilter.
    It requires a valid session context for initialization.
    """
    def __init__(self, session_context: SessionContext):
        if not session_context.session:
            raise ValueError("session required")
        self._session_context = session_context
        self.tri_state_filter = TriStateFilter()
    @property
    def tri_state_filter_id(self):
        """
        Get the tri_state_filter ID from the TriStateFilter object.
        :return: The tri_state_filter ID.
        """
        if not self.tri_state_filter:
            raise AttributeError("TriStateFilter object is not initialized")
        return self.tri_state_filter.tri_state_filter_id
    # @tri_state_filter_id.setter
    # def tri_state_filter_id(self, value: int):
    #     """
    #     #TODO add comment
    #     """
    #     if not isinstance(value, int):
    #         raise ValueError("tri_state_filter_id must be a int.")
    #     self.tri_state_filter.tri_state_filter_id = value
    # code
    @property
    def code(self):
        """
        #TODO add comment
        """
        if not self.tri_state_filter:
            raise AttributeError("TriStateFilter object is not initialized")
        return self.tri_state_filter.code
    @code.setter
    def code(self, value: uuid.UUID):  # type: ignore
        """
        #TODO add comment
        """
        if not self.tri_state_filter:
            raise AttributeError("TriStateFilter object is not initialized")
        if not isinstance(value, uuid.UUID):
            raise ValueError("code must be a UUID.")
        self.tri_state_filter.code = value
    # last_change_code
    @property
    def last_change_code(self):
        """
        #TODO add comment
        """
        if not self.tri_state_filter:
            raise AttributeError("TriStateFilter object is not initialized")
        return self.tri_state_filter.last_change_code
    @last_change_code.setter
    def last_change_code(self, value: int):
        """
        #TODO add comment
        """
        if not self.tri_state_filter:
            raise AttributeError("TriStateFilter object is not initialized")
        if not isinstance(value, int):
            raise ValueError("last_change_code must be an integer.")
        self.tri_state_filter.last_change_code = value
    # insert_user_id
    @property
    def insert_user_id(self):
        """
        #TODO add comment
        """
        if not self.tri_state_filter:
            raise AttributeError("TriStateFilter object is not initialized")
        return self.tri_state_filter.insert_user_id
    @insert_user_id.setter
    def insert_user_id(self, value: uuid.UUID):
        """
        #TODO add comment
        """
        if not self.tri_state_filter:
            raise AttributeError("TriStateFilter object is not initialized")
        if not isinstance(value, uuid.UUID):
            raise ValueError("insert_user_id must be a UUID.")
        self.tri_state_filter.insert_user_id = value
    # def set_prop_insert_user_id(self, value: uuid.UUID):
    #     """
    #     #TODO add comment
    #     """
    #     if not self.tri_state_filter:
    #         raise AttributeError("TriStateFilter object is not initialized")
    #     self.insert_user_id = value
    #     return self
    # last_update_user_id
    @property
    def last_update_user_id(self):
        """
        #TODO add comment
        """
        if not self.tri_state_filter:
            raise AttributeError("TriStateFilter object is not initialized")
        return self.tri_state_filter.last_update_user_id
    @last_update_user_id.setter
    def last_update_user_id(self, value: uuid.UUID):
        """
        #TODO add comment
        """
        if not self.tri_state_filter:
            raise AttributeError("TriStateFilter object is not initialized")
        if not isinstance(value, uuid.UUID):
            raise ValueError("last_update_user_id must be a UUID.")
        self.tri_state_filter.last_update_user_id = value
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
        if not self.tri_state_filter:
            raise AttributeError("TriStateFilter object is not initialized")
        if self.tri_state_filter.description is None:
            return ""
        return self.tri_state_filter.description
    @description.setter
    def description(self, value):
        """
        #TODO add comment
        """
        if not self.tri_state_filter:
            raise AttributeError("TriStateFilter object is not initialized")
        assert isinstance(value, str), "description must be a string"
        self.tri_state_filter.description = value
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
        if not self.tri_state_filter:
            raise AttributeError("TriStateFilter object is not initialized")
        return self.tri_state_filter.display_order
    @display_order.setter
    def display_order(self, value):
        """
        #TODO add comment
        """
        if not self.tri_state_filter:
            raise AttributeError("TriStateFilter object is not initialized")
        assert isinstance(value, int), (
            "display_order must be an integer")
        self.tri_state_filter.display_order = value
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
        if not self.tri_state_filter:
            raise AttributeError("TriStateFilter object is not initialized")
        return self.tri_state_filter.is_active
    @is_active.setter
    def is_active(self, value: bool):
        """
        #TODO add comment
        """
        if not self.tri_state_filter:
            raise AttributeError("TriStateFilter object is not initialized")
        if not isinstance(value, bool):
            raise ValueError("is_active must be a boolean.")
        self.tri_state_filter.is_active = value
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
        if not self.tri_state_filter:
            raise AttributeError("TriStateFilter object is not initialized")
        if self.tri_state_filter.lookup_enum_name is None:
            return ""
        return self.tri_state_filter.lookup_enum_name
    @lookup_enum_name.setter
    def lookup_enum_name(self, value):
        """
        #TODO add comment
        """
        if not self.tri_state_filter:
            raise AttributeError("TriStateFilter object is not initialized")
        assert isinstance(value, str), "lookup_enum_name must be a string"
        self.tri_state_filter.lookup_enum_name = value
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
        if not self.tri_state_filter:
            raise AttributeError("TriStateFilter object is not initialized")
        if self.tri_state_filter.name is None:
            return ""
        return self.tri_state_filter.name
    @name.setter
    def name(self, value):
        """
        #TODO add comment
        """
        if not self.tri_state_filter:
            raise AttributeError("TriStateFilter object is not initialized")
        assert isinstance(value, str), "name must be a string"
        self.tri_state_filter.name = value
    # def set_prop_name(self, value):
    #     """
    #     #TODO add comment
    #     """
    #     self.name = value
    #     return self
    # PacID
    # stateIntValue
    @property
    def state_int_value(self):
        """
        #TODO add comment
        """
        if not self.tri_state_filter:
            raise AttributeError("TriStateFilter object is not initialized")
        return self.tri_state_filter.state_int_value
    @state_int_value.setter
    def state_int_value(self, value):
        """
        #TODO add comment
        """
        if not self.tri_state_filter:
            raise AttributeError("TriStateFilter object is not initialized")
        assert isinstance(value, int), (
            "state_int_value must be an integer")
        self.tri_state_filter.state_int_value = value
    # def set_prop_state_int_value(self, value):
    #     """
    #     #TODO add comment
    #     """
    #     self.state_int_value = value
    #     return self
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
        if not self.tri_state_filter:
            raise AttributeError("TriStateFilter object is not initialized")
        return self.tri_state_filter.pac_id
    @pac_id.setter
    def pac_id(self, value):
        """
        #TODO add comment
        """
        if not self.tri_state_filter:
            raise AttributeError("TriStateFilter object is not initialized")
        assert isinstance(value, int) or value is None, (
            "pac_id must be an integer or None")
        self.tri_state_filter.pac_id = value
    # def set_prop_pac_id(self, value):
    #     """
    #     #TODO add comment
    #     """
    #     self.pac_id = value
    #     return self
    @property
    def pac_code_peek(self):
        """
        #TODO add comment
        """
        if not self.tri_state_filter:
            raise AttributeError("TriStateFilter object is not initialized")
        return self.tri_state_filter.pac_code_peek
    # @pac_code_peek.setter
    # def pac_code_peek(self, value):
    #     assert isinstance(value, uuid.UUID),
    #           "pac_code_peek must be a UUID"
    #     self.tri_state_filter.pac_code_peek = value
    # stateIntValue,
# endset
    # insert_utc_date_time
    @property
    def insert_utc_date_time(self):
        """
        #TODO add comment
        """
        if not self.tri_state_filter:
            raise AttributeError("TriStateFilter object is not initialized")
        return self.tri_state_filter.insert_utc_date_time
    @insert_utc_date_time.setter
    def insert_utc_date_time(self, value):
        """
        #TODO add comment
        """
        if not self.tri_state_filter:
            raise AttributeError("TriStateFilter object is not initialized")
        assert isinstance(value, datetime) or value is None, (
            "insert_utc_date_time must be a datetime object or None")
        self.tri_state_filter.insert_utc_date_time = value
    # update_utc_date_time
    @property
    def last_update_utc_date_time(self):
        """
        #TODO add comment
        """
        if not self.tri_state_filter:
            raise AttributeError("TriStateFilter object is not initialized")
        return self.tri_state_filter.last_update_utc_date_time
    @last_update_utc_date_time.setter
    def last_update_utc_date_time(self, value):
        """
        #TODO add comment
        """
        if not self.tri_state_filter:
            raise AttributeError("TriStateFilter object is not initialized")
        assert isinstance(value, datetime) or value is None, (
            "last_update_utc_date_time must be a datetime object or None")
        self.tri_state_filter.last_update_utc_date_time = value
    async def load_from_json(
        self,
        json_data: str
    ):
        """
        Load tri_state_filter data from JSON string.
        :param json_data: JSON string containing tri_state_filter data.
        :raises ValueError: If json_data is not a string or if no tri_state_filter data is found.
        """
        if not isinstance(json_data, str):
            raise ValueError("json_data must be a string")
        tri_state_filter_manager = TriStateFilterManager(self._session_context)
        self.tri_state_filter = tri_state_filter_manager.from_json(json_data)
        return self
    async def load_from_code(
        self,
        code: uuid.UUID
    ):
        """
        Load tri_state_filter data from UUID code.
        :param code: UUID code for loading a specific tri_state_filter.
        :raises ValueError: If code is not a UUID or if no tri_state_filter data is found.
        """
        if not isinstance(code, uuid.UUID):
            raise ValueError("code must be a UUID")
        tri_state_filter_manager = TriStateFilterManager(self._session_context)
        tri_state_filter_obj = await tri_state_filter_manager.get_by_code(code)
        self.tri_state_filter = tri_state_filter_obj
        return self
    async def load_from_id(
        self,
        tri_state_filter_id: int
    ):
        """
        Load tri_state_filter data from tri_state_filter ID.
        :param tri_state_filter_id: Integer ID for loading a specific tri_state_filter.
        :raises ValueError: If tri_state_filter_id is not an integer or if no tri_state_filter data is found.
        """
        if not isinstance(tri_state_filter_id, int):
            raise ValueError("tri_state_filter_id must be an integer")
        tri_state_filter_manager = TriStateFilterManager(self._session_context)
        tri_state_filter_obj = await tri_state_filter_manager.get_by_id(tri_state_filter_id)
        self.tri_state_filter = tri_state_filter_obj
        return self
    async def load_from_obj_instance(
        self,
        tri_state_filter_obj_instance: TriStateFilter
    ):
        """
        Use the provided TriStateFilter instance.
        :param tri_state_filter_obj_instance: Instance of the TriStateFilter class.
        :raises ValueError: If tri_state_filter_obj_instance is not an instance of TriStateFilter.
        """
        if not isinstance(tri_state_filter_obj_instance, TriStateFilter):
            raise ValueError("tri_state_filter_obj_instance must be an instance of TriStateFilter")
        tri_state_filter_manager = TriStateFilterManager(self._session_context)
        tri_state_filter_obj_instance_tri_state_filter_id = tri_state_filter_obj_instance.tri_state_filter_id
        tri_state_filter_obj = await tri_state_filter_manager.get_by_id(
            tri_state_filter_obj_instance_tri_state_filter_id
        )
        self.tri_state_filter = tri_state_filter_obj
        return self
    async def load_from_dict(
        self,
        tri_state_filter_dict: dict
    ):
        """
        Load tri_state_filter data from dictionary.
        :param tri_state_filter_dict: Dictionary containing tri_state_filter data.
        :raises ValueError: If tri_state_filter_dict is not a dictionary or if no tri_state_filter data is found.
        """
        if not isinstance(tri_state_filter_dict, dict):
            raise ValueError("tri_state_filter_dict must be a dictionary")
        tri_state_filter_manager = TriStateFilterManager(self._session_context)
        self.tri_state_filter = tri_state_filter_manager.from_dict(tri_state_filter_dict)
        return self

    @property
    def lookup_enum(self) -> managers_and_enums.TriStateFilterEnum:
        return managers_and_enums.TriStateFilterEnum[self.tri_state_filter.lookup_enum_name]
    async def load_from_enum(
        self,
        tri_state_filter_enum:
            managers_and_enums.TriStateFilterEnum
    ):
        """
        Load plant data from dictionary.
        :param plant_dict: Dictionary containing plant data.
        :raises ValueError: If plant_dict is not a dictionary or if no plant data is found.
        """
        if not isinstance(tri_state_filter_enum, managers_and_enums.TriStateFilterEnum):
            raise ValueError("tri_state_filter_enum must be a enum")
        tri_state_filter_manager = TriStateFilterManager(self._session_context)
        self.tri_state_filter = await tri_state_filter_manager.from_enum(tri_state_filter_enum)

    def get_session_context(self):
        """
        #TODO add comment
        """
        return self._session_context
    async def refresh(self):
        """
        #TODO add comment
        """
        tri_state_filter_manager = TriStateFilterManager(self._session_context)
        self.tri_state_filter = await tri_state_filter_manager.refresh(self.tri_state_filter)
        return self
    def is_valid(self):
        """
        #TODO add comment
        """
        return (self.tri_state_filter is not None)
    def to_dict(self):
        """
        #TODO add comment
        """
        tri_state_filter_manager = TriStateFilterManager(self._session_context)
        return tri_state_filter_manager.to_dict(self.tri_state_filter)
    def to_json(self):
        """
        #TODO add comment
        """
        tri_state_filter_manager = TriStateFilterManager(self._session_context)
        return tri_state_filter_manager.to_json(self.tri_state_filter)
    async def save(self):
        """
        #TODO add comment
        """
        if not self.tri_state_filter:
            raise AttributeError("TriStateFilter object is not initialized")
        if self.tri_state_filter.tri_state_filter_id is not None and self.tri_state_filter.tri_state_filter_id > 0:
            tri_state_filter_manager = TriStateFilterManager(self._session_context)
            self.tri_state_filter = await tri_state_filter_manager.update(self.tri_state_filter)
        if self.tri_state_filter.tri_state_filter_id is None or self.tri_state_filter.tri_state_filter_id == 0:
            tri_state_filter_manager = TriStateFilterManager(self._session_context)
            self.tri_state_filter = await tri_state_filter_manager.add(self.tri_state_filter)
        return self
    async def delete(self):
        """
        #TODO add comment
        """
        if not self.tri_state_filter:
            raise AttributeError("TriStateFilter object is not initialized")
        if self.tri_state_filter.tri_state_filter_id > 0:
            tri_state_filter_manager = TriStateFilterManager(self._session_context)
            await tri_state_filter_manager.delete(self.tri_state_filter.tri_state_filter_id)
            self.tri_state_filter = None
    async def randomize_properties(self):
        """
        #TODO add comment
        """
        if not self.tri_state_filter:
            raise AttributeError("TriStateFilter object is not initialized")
        self.tri_state_filter.description = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        self.tri_state_filter.display_order = random.randint(0, 100)
        self.tri_state_filter.is_active = random.choice([True, False])
        self.tri_state_filter.lookup_enum_name = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        self.tri_state_filter.name = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        # self.tri_state_filter.pac_id = random.randint(0, 100)
        self.tri_state_filter.state_int_value = random.randint(0, 100)
# endset
        return self
    def get_tri_state_filter_obj(self) -> TriStateFilter:
        """
        #TODO add comment
        """
        if not self.tri_state_filter:
            raise AttributeError("TriStateFilter object is not initialized")
        return self.tri_state_filter
    def is_equal(self, tri_state_filter: TriStateFilter) -> bool:
        """
        #TODO add comment
        """
        tri_state_filter_manager = TriStateFilterManager(self._session_context)
        my_tri_state_filter = self.get_tri_state_filter_obj()
        return tri_state_filter_manager.is_equal(tri_state_filter, my_tri_state_filter)
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
    # stateIntValue,
# endset
    def get_obj(self) -> TriStateFilter:
        """
        #TODO add comment
        """
        return self.tri_state_filter
    def get_object_name(self) -> str:
        """
        #TODO add comment
        """
        return "tri_state_filter"
    def get_id(self) -> int:
        """
        #TODO add comment
        """
        return self.tri_state_filter_id
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
    # stateIntValue,
# endset
    @staticmethod
    async def to_bus_obj_list(
        session_context: SessionContext,
        obj_list: List[TriStateFilter]
    ):
        """
        #TODO add comment
        """
        result = list()
        for tri_state_filter in obj_list:
            tri_state_filter_bus_obj = TriStateFilterBusObj(session_context)
            await tri_state_filter_bus_obj.load_from_obj_instance(tri_state_filter)
            result.append(tri_state_filter_bus_obj)
        return result

