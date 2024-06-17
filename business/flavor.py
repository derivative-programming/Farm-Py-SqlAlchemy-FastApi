# business/flavor.py
"""
    #TODO add comment
"""
from decimal import Decimal
import random
import uuid
from typing import List
from datetime import datetime, date
from helpers.session_context import SessionContext
from managers import FlavorManager
from models import Flavor
import models
import managers as managers_and_enums
from .base_bus_obj import BaseBusObj

NOT_INITIALIZED_ERROR_MESSAGE = (
    "Flavor object is not initialized")
class FlavorInvalidInitError(Exception):
    """
    #TODO add comment
    """
class FlavorBusObj(BaseBusObj):
    """
    This class represents the business object for a Flavor.
    It requires a valid session context for initialization.
    """
    def __init__(self, session_context: SessionContext):
        if not session_context.session:
            raise ValueError("session required")
        self._session_context = session_context
        self.flavor = Flavor()
    @property
    def flavor_id(self) -> int:
        """
        Get the flavor ID from the Flavor object.
        :return: The flavor ID.
        """
        if not self.flavor:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.flavor.flavor_id
    # @flavor_id.setter
    # def flavor_id(self, value: int):
    #     """
    #     #TODO add comment
    #     """
    #     if not isinstance(value, int):
    #         raise ValueError("flavor_id must be a int.")
    #     self.flavor.flavor_id = value
    # code
    @property
    def code(self):
        """
        #TODO add comment
        """
        if not self.flavor:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.flavor.code
    @code.setter
    def code(self, value: uuid.UUID):  # type: ignore
        """
        #TODO add comment
        """
        if not self.flavor:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if not isinstance(value, uuid.UUID):
            raise ValueError("code must be a UUID.")
        self.flavor.code = value
    # last_change_code
    @property
    def last_change_code(self):
        """
        #TODO add comment
        """
        if not self.flavor:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.flavor.last_change_code
    @last_change_code.setter
    def last_change_code(self, value: int):
        """
        #TODO add comment
        """
        if not self.flavor:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if not isinstance(value, int):
            raise ValueError("last_change_code must be an integer.")
        self.flavor.last_change_code = value
    # insert_user_id
    @property
    def insert_user_id(self):
        """
        #TODO add comment
        """
        if not self.flavor:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.flavor.insert_user_id
    @insert_user_id.setter
    def insert_user_id(self, value: uuid.UUID):
        """
        #TODO add comment
        """
        if not self.flavor:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if not isinstance(value, uuid.UUID):
            raise ValueError("insert_user_id must be a UUID.")
        self.flavor.insert_user_id = value
    # def set_prop_insert_user_id(self, value: uuid.UUID):
    #     """
    #     #TODO add comment
    #     """
    #     if not self.flavor:
    #         raise AttributeError(NOT_INITIALIZED_ERROR_MESSAGE)
    #     self.insert_user_id = value
    #     return self
    # last_update_user_id
    @property
    def last_update_user_id(self):
        """
        #TODO add comment
        """
        if not self.flavor:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.flavor.last_update_user_id
    @last_update_user_id.setter
    def last_update_user_id(self, value: uuid.UUID):
        """
        #TODO add comment
        """
        if not self.flavor:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if not isinstance(value, uuid.UUID):
            raise ValueError("last_update_user_id must be a UUID.")
        self.flavor.last_update_user_id = value
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
        if not self.flavor:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if self.flavor.description is None:
            return ""
        return self.flavor.description
    @description.setter
    def description(self, value):
        """
        #TODO add comment
        """
        if not self.flavor:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, str), "description must be a string"
        self.flavor.description = value
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
        if not self.flavor:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.flavor.display_order
    @display_order.setter
    def display_order(self, value):
        """
        #TODO add comment
        """
        if not self.flavor:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, int), (
            "display_order must be an integer")
        self.flavor.display_order = value
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
        if not self.flavor:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.flavor.is_active
    @is_active.setter
    def is_active(self, value: bool):
        """
        #TODO add comment
        """
        if not self.flavor:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if not isinstance(value, bool):
            raise ValueError("is_active must be a boolean.")
        self.flavor.is_active = value
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
        if not self.flavor:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if self.flavor.lookup_enum_name is None:
            return ""
        return self.flavor.lookup_enum_name
    @lookup_enum_name.setter
    def lookup_enum_name(self, value):
        """
        #TODO add comment
        """
        if not self.flavor:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, str), "lookup_enum_name must be a string"
        self.flavor.lookup_enum_name = value
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
        if not self.flavor:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if self.flavor.name is None:
            return ""
        return self.flavor.name
    @name.setter
    def name(self, value):
        """
        #TODO add comment
        """
        if not self.flavor:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, str), "name must be a string"
        self.flavor.name = value
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
        if not self.flavor:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.flavor.pac_id
    @pac_id.setter
    def pac_id(self, value):
        """
        #TODO add comment
        """
        if not self.flavor:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, int) or value is None, (
            "pac_id must be an integer or None")
        self.flavor.pac_id = value
    def set_prop_pac_id(self, value: int):
        """
        #TODO add comment
        """
        self.pac_id = value
        return self
    @property
    def pac_code_peek(self):
        """
        #TODO add comment
        """
        if not self.flavor:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.flavor.pac_code_peek
    # @pac_code_peek.setter
    # def pac_code_peek(self, value):
    #     assert isinstance(value, uuid.UUID),
    #           "pac_code_peek must be a UUID"
    #     self.flavor.pac_code_peek = value
# endset
    # insert_utc_date_time
    @property
    def insert_utc_date_time(self):
        """
        #TODO add comment
        """
        if not self.flavor:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.flavor.insert_utc_date_time
    @insert_utc_date_time.setter
    def insert_utc_date_time(self, value):
        """
        #TODO add comment
        """
        if not self.flavor:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, datetime) or value is None, (
            "insert_utc_date_time must be a datetime object or None")
        self.flavor.insert_utc_date_time = value
    # update_utc_date_time
    @property
    def last_update_utc_date_time(self):
        """
        #TODO add comment
        """
        if not self.flavor:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.flavor.last_update_utc_date_time
    @last_update_utc_date_time.setter
    def last_update_utc_date_time(self, value):
        """
        #TODO add comment
        """
        if not self.flavor:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, datetime) or value is None, (
            "last_update_utc_date_time must be a datetime object or None")
        self.flavor.last_update_utc_date_time = value
    async def load_from_json(
        self,
        json_data: str
    ):
        """
        Load flavor data from JSON string.
        :param json_data: JSON string containing flavor data.
        :raises ValueError: If json_data is not a string
            or if no flavor data is found.
        """
        if not isinstance(json_data, str):
            raise ValueError("json_data must be a string")
        flavor_manager = FlavorManager(self._session_context)
        self.flavor = flavor_manager.from_json(json_data)
        return self
    async def load_from_code(
        self,
        code: uuid.UUID
    ):
        """
        Load flavor data from UUID code.
        :param code: UUID code for loading a specific flavor.
        :raises ValueError: If code is not a UUID or if no flavor data is found.
        """
        if not isinstance(code, uuid.UUID):
            raise ValueError("code must be a UUID")
        flavor_manager = FlavorManager(self._session_context)
        flavor_obj = await flavor_manager.get_by_code(code)
        self.flavor = flavor_obj
        return self
    async def load_from_id(
        self,
        flavor_id: int
    ):
        """
        Load flavor data from flavor ID.
        :param flavor_id: Integer ID for loading a specific flavor.
        :raises ValueError: If flavor_id is not an integer or
            if no flavor data is found.
        """
        if not isinstance(flavor_id, int):
            raise ValueError("flavor_id must be an integer")
        flavor_manager = FlavorManager(self._session_context)
        flavor_obj = await flavor_manager.get_by_id(flavor_id)
        self.flavor = flavor_obj
        return self
    async def load_from_obj_instance(
        self,
        flavor_obj_instance: Flavor
    ):
        """
        Use the provided Flavor instance.
        :param flavor_obj_instance: Instance of the Flavor class.
        :raises ValueError: If flavor_obj_instance is not an instance of Flavor.
        """
        if not isinstance(flavor_obj_instance, Flavor):
            raise ValueError("flavor_obj_instance must be an instance of Flavor")
        flavor_manager = FlavorManager(self._session_context)
        flavor_obj_instance_flavor_id = flavor_obj_instance.flavor_id
        flavor_obj = await flavor_manager.get_by_id(
            flavor_obj_instance_flavor_id
        )
        self.flavor = flavor_obj
        return self
    async def load_from_dict(
        self,
        flavor_dict: dict
    ):
        """
        Load flavor data from dictionary.
        :param flavor_dict: Dictionary containing flavor data.
        :raises ValueError: If flavor_dict is not a
            dictionary or if no flavor data is found.
        """
        if not isinstance(flavor_dict, dict):
            raise ValueError("flavor_dict must be a dictionary")
        flavor_manager = FlavorManager(self._session_context)
        self.flavor = flavor_manager.from_dict(flavor_dict)
        return self

    @property
    def lookup_enum(self) -> managers_and_enums.FlavorEnum:
        """
        #TODO add comment
        """
        return (
            managers_and_enums.FlavorEnum[
                self.flavor.lookup_enum_name
            ]
        )
    async def load_from_enum(
        self,
        flavor_enum:
            managers_and_enums.FlavorEnum
    ):
        """
        Load plant data from dictionary.
        :param plant_dict: Dictionary containing plant data.
        :raises ValueError: If plant_dict is not a dictionary or
            if no plant data is found.
        """
        if not isinstance(
            flavor_enum,
            managers_and_enums.FlavorEnum
        ):
            raise ValueError("flavor_enum must be a enum")
        flavor_manager = FlavorManager(
            self._session_context
        )
        self.flavor = await (
            flavor_manager.
            from_enum(flavor_enum)
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
        flavor_manager = FlavorManager(self._session_context)
        self.flavor = await flavor_manager.refresh(self.flavor)
        return self
    def is_valid(self):
        """
        #TODO add comment
        """
        return self.flavor is not None
    def to_dict(self):
        """
        #TODO add comment
        """
        flavor_manager = FlavorManager(self._session_context)
        return flavor_manager.to_dict(self.flavor)
    def to_json(self):
        """
        #TODO add comment
        """
        flavor_manager = FlavorManager(self._session_context)
        return flavor_manager.to_json(self.flavor)
    async def save(self):
        """
        #TODO add comment
        """
        if not self.flavor:
            raise AttributeError(NOT_INITIALIZED_ERROR_MESSAGE)
        if self.flavor.flavor_id > 0:
            flavor_manager = FlavorManager(self._session_context)
            self.flavor = await flavor_manager.update(self.flavor)
        if self.flavor.flavor_id == 0:
            flavor_manager = FlavorManager(self._session_context)
            self.flavor = await flavor_manager.add(self.flavor)
        return self
    async def delete(self):
        """
        #TODO add comment
        """
        if not self.flavor:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if self.flavor.flavor_id > 0:
            flavor_manager = FlavorManager(self._session_context)
            await flavor_manager.delete(self.flavor.flavor_id)
            self.flavor = None
    async def randomize_properties(self):
        """
        #TODO add comment
        """
        if not self.flavor:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        self.flavor.description = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        self.flavor.display_order = random.randint(0, 100)
        self.flavor.is_active = random.choice([True, False])
        self.flavor.lookup_enum_name = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        self.flavor.name = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        # self.flavor.pac_id = random.randint(0, 100)
# endset
        return self
    def get_flavor_obj(self) -> Flavor:
        """
        #TODO add comment
        """
        if not self.flavor:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.flavor
    def is_equal(self, flavor: Flavor) -> bool:
        """
        #TODO add comment
        """
        flavor_manager = FlavorManager(self._session_context)
        my_flavor = self.get_flavor_obj()
        return flavor_manager.is_equal(flavor, my_flavor)
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
    def get_obj(self) -> Flavor:
        """
        #TODO add comment
        """
        return self.flavor
    def get_object_name(self) -> str:
        """
        #TODO add comment
        """
        return "flavor"
    def get_id(self) -> int:
        """
        #TODO add comment
        """
        return self.flavor_id
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
        obj_list: List[Flavor]
    ):
        """
        #TODO add comment
        """
        result = list()
        for flavor in obj_list:
            flavor_bus_obj = FlavorBusObj(session_context)
            await flavor_bus_obj.load_from_obj_instance(flavor)
            result.append(flavor_bus_obj)
        return result

