# business/land.py
"""
    #TODO add comment
"""
from decimal import Decimal
import random
import uuid
from typing import List
from datetime import datetime, date
from helpers.session_context import SessionContext
from managers import LandManager
from models import Land
import models
import managers as managers_and_enums
from .base_bus_obj import BaseBusObj

from business.plant import PlantBusObj

NOT_INITIALIZED_ERROR_MESSAGE = (
    "Land object is not initialized")
class LandInvalidInitError(Exception):
    """
    #TODO add comment
    """
class LandBusObj(BaseBusObj):
    """
    This class represents the business object for a Land.
    It requires a valid session context for initialization.
    """
    def __init__(self, session_context: SessionContext):
        if not session_context.session:
            raise ValueError("session required")
        self._session_context = session_context
        self.land = Land()
    @property
    def land_id(self) -> int:
        """
        Get the land ID from the Land object.
        :return: The land ID.
        """
        if not self.land:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.land.land_id
    # @land_id.setter
    # def land_id(self, value: int):
    #     """
    #     #TODO add comment
    #     """
    #     if not isinstance(value, int):
    #         raise ValueError("land_id must be a int.")
    #     self.land.land_id = value
    # code
    @property
    def code(self):
        """
        #TODO add comment
        """
        if not self.land:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.land.code
    @code.setter
    def code(self, value: uuid.UUID):  # type: ignore
        """
        #TODO add comment
        """
        if not self.land:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if not isinstance(value, uuid.UUID):
            raise ValueError("code must be a UUID.")
        self.land.code = value
    # last_change_code
    @property
    def last_change_code(self):
        """
        #TODO add comment
        """
        if not self.land:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.land.last_change_code
    @last_change_code.setter
    def last_change_code(self, value: int):
        """
        #TODO add comment
        """
        if not self.land:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if not isinstance(value, int):
            raise ValueError("last_change_code must be an integer.")
        self.land.last_change_code = value
    # insert_user_id
    @property
    def insert_user_id(self):
        """
        #TODO add comment
        """
        if not self.land:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.land.insert_user_id
    @insert_user_id.setter
    def insert_user_id(self, value: uuid.UUID):
        """
        #TODO add comment
        """
        if not self.land:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if not isinstance(value, uuid.UUID):
            raise ValueError("insert_user_id must be a UUID.")
        self.land.insert_user_id = value
    # def set_prop_insert_user_id(self, value: uuid.UUID):
    #     """
    #     #TODO add comment
    #     """
    #     if not self.land:
    #         raise AttributeError(NOT_INITIALIZED_ERROR_MESSAGE)
    #     self.insert_user_id = value
    #     return self
    # last_update_user_id
    @property
    def last_update_user_id(self):
        """
        #TODO add comment
        """
        if not self.land:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.land.last_update_user_id
    @last_update_user_id.setter
    def last_update_user_id(self, value: uuid.UUID):
        """
        #TODO add comment
        """
        if not self.land:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if not isinstance(value, uuid.UUID):
            raise ValueError("last_update_user_id must be a UUID.")
        self.land.last_update_user_id = value
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
        if not self.land:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if self.land.description is None:
            return ""
        return self.land.description
    @description.setter
    def description(self, value):
        """
        #TODO add comment
        """
        if not self.land:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, str), "description must be a string"
        self.land.description = value
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
        if not self.land:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.land.display_order
    @display_order.setter
    def display_order(self, value):
        """
        #TODO add comment
        """
        if not self.land:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, int), (
            "display_order must be an integer")
        self.land.display_order = value
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
        if not self.land:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.land.is_active
    @is_active.setter
    def is_active(self, value: bool):
        """
        #TODO add comment
        """
        if not self.land:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if not isinstance(value, bool):
            raise ValueError("is_active must be a boolean.")
        self.land.is_active = value
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
        if not self.land:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if self.land.lookup_enum_name is None:
            return ""
        return self.land.lookup_enum_name
    @lookup_enum_name.setter
    def lookup_enum_name(self, value):
        """
        #TODO add comment
        """
        if not self.land:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, str), "lookup_enum_name must be a string"
        self.land.lookup_enum_name = value
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
        if not self.land:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if self.land.name is None:
            return ""
        return self.land.name
    @name.setter
    def name(self, value):
        """
        #TODO add comment
        """
        if not self.land:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, str), "name must be a string"
        self.land.name = value
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
        if not self.land:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.land.pac_id
    @pac_id.setter
    def pac_id(self, value):
        """
        #TODO add comment
        """
        if not self.land:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, int) or value is None, (
            "pac_id must be an integer or None")
        self.land.pac_id = value
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
        if not self.land:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.land.pac_code_peek
    # @pac_code_peek.setter
    # def pac_code_peek(self, value):
    #     assert isinstance(value, uuid.UUID),
    #           "pac_code_peek must be a UUID"
    #     self.land.pac_code_peek = value
# endset
    # insert_utc_date_time
    @property
    def insert_utc_date_time(self):
        """
        #TODO add comment
        """
        if not self.land:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.land.insert_utc_date_time
    @insert_utc_date_time.setter
    def insert_utc_date_time(self, value):
        """
        #TODO add comment
        """
        if not self.land:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, datetime) or value is None, (
            "insert_utc_date_time must be a datetime object or None")
        self.land.insert_utc_date_time = value
    # update_utc_date_time
    @property
    def last_update_utc_date_time(self):
        """
        #TODO add comment
        """
        if not self.land:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.land.last_update_utc_date_time
    @last_update_utc_date_time.setter
    def last_update_utc_date_time(self, value):
        """
        #TODO add comment
        """
        if not self.land:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, datetime) or value is None, (
            "last_update_utc_date_time must be a datetime object or None")
        self.land.last_update_utc_date_time = value
    async def load_from_json(
        self,
        json_data: str
    ):
        """
        Load land data from JSON string.
        :param json_data: JSON string containing land data.
        :raises ValueError: If json_data is not a string
            or if no land data is found.
        """
        if not isinstance(json_data, str):
            raise ValueError("json_data must be a string")
        land_manager = LandManager(self._session_context)
        self.land = land_manager.from_json(json_data)
        return self
    async def load_from_code(
        self,
        code: uuid.UUID
    ):
        """
        Load land data from UUID code.
        :param code: UUID code for loading a specific land.
        :raises ValueError: If code is not a UUID or if no land data is found.
        """
        if not isinstance(code, uuid.UUID):
            raise ValueError("code must be a UUID")
        land_manager = LandManager(self._session_context)
        land_obj = await land_manager.get_by_code(code)
        self.land = land_obj
        return self
    async def load_from_id(
        self,
        land_id: int
    ):
        """
        Load land data from land ID.
        :param land_id: Integer ID for loading a specific land.
        :raises ValueError: If land_id is not an integer or
            if no land data is found.
        """
        if not isinstance(land_id, int):
            raise ValueError("land_id must be an integer")
        land_manager = LandManager(self._session_context)
        land_obj = await land_manager.get_by_id(land_id)
        self.land = land_obj
        return self
    async def load_from_obj_instance(
        self,
        land_obj_instance: Land
    ):
        """
        Use the provided Land instance.
        :param land_obj_instance: Instance of the Land class.
        :raises ValueError: If land_obj_instance is not an instance of Land.
        """
        if not isinstance(land_obj_instance, Land):
            raise ValueError("land_obj_instance must be an instance of Land")
        land_manager = LandManager(self._session_context)
        land_obj_instance_land_id = land_obj_instance.land_id
        land_obj = await land_manager.get_by_id(
            land_obj_instance_land_id
        )
        self.land = land_obj
        return self
    async def load_from_dict(
        self,
        land_dict: dict
    ):
        """
        Load land data from dictionary.
        :param land_dict: Dictionary containing land data.
        :raises ValueError: If land_dict is not a
            dictionary or if no land data is found.
        """
        if not isinstance(land_dict, dict):
            raise ValueError("land_dict must be a dictionary")
        land_manager = LandManager(self._session_context)
        self.land = land_manager.from_dict(land_dict)
        return self

    @property
    def lookup_enum(self) -> managers_and_enums.LandEnum:
        """
        #TODO add comment
        """
        return (
            managers_and_enums.LandEnum[
                self.land.lookup_enum_name
            ]
        )
    async def load_from_enum(
        self,
        land_enum:
            managers_and_enums.LandEnum
    ):
        """
        Load plant data from dictionary.
        :param plant_dict: Dictionary containing plant data.
        :raises ValueError: If plant_dict is not a dictionary or
            if no plant data is found.
        """
        if not isinstance(
            land_enum,
            managers_and_enums.LandEnum
        ):
            raise ValueError("land_enum must be a enum")
        land_manager = LandManager(
            self._session_context
        )
        self.land = await (
            land_manager.
            from_enum(land_enum)
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
        land_manager = LandManager(self._session_context)
        self.land = await land_manager.refresh(self.land)
        return self
    def is_valid(self):
        """
        #TODO add comment
        """
        return self.land is not None
    def to_dict(self):
        """
        #TODO add comment
        """
        land_manager = LandManager(self._session_context)
        return land_manager.to_dict(self.land)
    def to_json(self):
        """
        #TODO add comment
        """
        land_manager = LandManager(self._session_context)
        return land_manager.to_json(self.land)
    async def save(self):
        """
        #TODO add comment
        """
        if not self.land:
            raise AttributeError(NOT_INITIALIZED_ERROR_MESSAGE)
        if self.land.land_id > 0:
            land_manager = LandManager(self._session_context)
            self.land = await land_manager.update(self.land)
        if self.land.land_id == 0:
            land_manager = LandManager(self._session_context)
            self.land = await land_manager.add(self.land)
        return self
    async def delete(self):
        """
        #TODO add comment
        """
        if not self.land:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if self.land.land_id > 0:
            land_manager = LandManager(self._session_context)
            await land_manager.delete(self.land.land_id)
            self.land = None
    async def randomize_properties(self):
        """
        #TODO add comment
        """
        if not self.land:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        self.land.description = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        self.land.display_order = random.randint(0, 100)
        self.land.is_active = random.choice([True, False])
        self.land.lookup_enum_name = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        self.land.name = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        # self.land.pac_id = random.randint(0, 100)
# endset
        return self
    def get_land_obj(self) -> Land:
        """
        #TODO add comment
        """
        if not self.land:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.land
    def is_equal(self, land: Land) -> bool:
        """
        #TODO add comment
        """
        land_manager = LandManager(self._session_context)
        my_land = self.get_land_obj()
        return land_manager.is_equal(land, my_land)
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
    def get_obj(self) -> Land:
        """
        #TODO add comment
        """
        return self.land
    def get_object_name(self) -> str:
        """
        #TODO add comment
        """
        return "land"
    def get_id(self) -> int:
        """
        #TODO add comment
        """
        return self.land_id
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
        obj_list: List[Land]
    ):
        """
        #TODO add comment
        """
        result = list()
        for land in obj_list:
            land_bus_obj = LandBusObj(session_context)
            await land_bus_obj.load_from_obj_instance(land)
            result.append(land_bus_obj)
        return result

    async def build_plant(self) -> PlantBusObj:
        item = PlantBusObj(self._session_context)
        flavor_manager = managers_and_enums.FlavorManager(self._session_context)
        flvr_foreign_key_id_flavor = await flavor_manager.from_enum(
            managers_and_enums.FlavorEnum.Unknown)
        item.flvr_foreign_key_id = flvr_foreign_key_id_flavor.flavor_id
        item.plant.flvr_foreign_key_id_code_peek = flvr_foreign_key_id_flavor.code

        item.land_id = self.land_id
        item.plant.land_code_peek = self.code

        return item

    async def get_all_plant(self) -> List[PlantBusObj]:
        results = list()
        plant_manager = managers_and_enums.PlantManager(self._session_context)
        obj_list = await plant_manager.get_by_land_id(self.land_id)
        for obj_item in obj_list:
            bus_obj_item = PlantBusObj(self._session_context)
            await bus_obj_item.load_from_obj_instance(obj_item)
            results.append(bus_obj_item)
        return results

