# business/pac.py
"""
This module contains the PacBusObj class,
which represents the business object for a Pac.
"""
from decimal import Decimal
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

NOT_INITIALIZED_ERROR_MESSAGE = (
    "Pac object is not initialized")
class PacInvalidInitError(Exception):
    """
    Exception raised when the
    Pac object
    is not initialized properly.
    """
class PacBusObj(BaseBusObj):
    """
    This class represents the business object for a Pac.
    It requires a valid session context for initialization.
    """
    def __init__(self, session_context: SessionContext):
        """
        Initializes a new instance of the
        PacBusObj class.
        :param session_context: The session context.
        :raises ValueError: If the session is not provided.
        """
        if not session_context.session:
            raise ValueError("session required")
        self._session_context = session_context
        self.pac = Pac()
    @property
    def pac_id(self) -> int:
        """
        Get the pac ID from the
        Pac object.
        :return: The pac ID.
        :raises AttributeError: If the
            Pac object is not initialized.
        """
        if not self.pac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.pac.pac_id
    # code
    @property
    def code(self):
        """
        Get the code from the
        Pac object.
        :return: The code.
        :raises AttributeError: If the
            Pac object is not initialized.
        """
        if not self.pac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.pac.code
    @code.setter
    def code(self, value: uuid.UUID):  # type: ignore
        """
        Set the code for the Pac object.
        :param value: The code value.
        :raises AttributeError: If the
            Pac object is not initialized.
        :raises ValueError: If the code is not a UUID.
        """
        if not self.pac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if not isinstance(value, uuid.UUID):
            raise ValueError("code must be a UUID.")
        self.pac.code = value
    # last_change_code
    @property
    def last_change_code(self):
        """
        Get the last change code from the
        Pac object.
        :return: The last change code.
        :raises AttributeError: If the
            Pac object is not initialized.
        """
        if not self.pac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.pac.last_change_code
    @last_change_code.setter
    def last_change_code(self, value: int):
        """
        Set the last change code for the
        Pac object.
        :param value: The last change code value.
        :raises AttributeError: If the
            Pac object is not initialized.
        :raises ValueError: If the last change code is not an integer.
        """
        if not self.pac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if not isinstance(value, int):
            raise ValueError("last_change_code must be an integer.")
        self.pac.last_change_code = value
    # insert_user_id
    @property
    def insert_user_id(self):
        """
        Get the insert user ID from the
        Pac object.
        :return: The insert user ID.
        :raises AttributeError: If the
            Pac object is not initialized.
        """
        if not self.pac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.pac.insert_user_id
    @insert_user_id.setter
    def insert_user_id(self, value: uuid.UUID):
        """
        Set the insert user ID for the
        Pac object.
        :param value: The insert user ID value.
        :raises AttributeError: If the
            Pac object is not initialized.
        :raises ValueError: If the insert user ID is not a UUID.
        """
        if not self.pac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if not isinstance(value, uuid.UUID):
            raise ValueError("insert_user_id must be a UUID.")
        self.pac.insert_user_id = value
    # last_update_user_id
    @property
    def last_update_user_id(self):
        """
        Get the last update user ID from the
        Pac object.
        :return: The last update user ID.
        :raises AttributeError: If the
            Pac object is not initialized.
        """
        if not self.pac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.pac.last_update_user_id
    @last_update_user_id.setter
    def last_update_user_id(self, value: uuid.UUID):
        """
        Set the last update user ID for the
        Pac object.
        :param value: The last update user ID value.
        :raises AttributeError: If the
            Pac object is not initialized.
        :raises ValueError: If the last update user ID is not a UUID.
        """
        if not self.pac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if not isinstance(value, uuid.UUID):
            raise ValueError("last_update_user_id must be a UUID.")
        self.pac.last_update_user_id = value
# endset
    # description
    @property
    def description(self):
        """
        Get the Description from the
        Pac object.
        :return: The Description.
        :raises AttributeError: If the
            Pac object is not initialized.
        """
        if not self.pac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if self.pac.description is None:
            return ""
        return self.pac.description
    @description.setter
    def description(self, value):
        """
        Set the Description for the
        Pac object.
        :param value: The Description value.
        :raises AttributeError: If the
            Pac object is not initialized.
        :raises AssertionError: If the Description is not a string.
        """
        if not self.pac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, str), "description must be a string"
        self.pac.description = value
    def set_prop_description(self, value: str):
        """
        Set the Description for the
        Pac object.
        :param value: The Description value.
        :return: The updated
            PacBusObj instance.
        """
        self.description = value
        return self
    # displayOrder
    @property
    def display_order(self):
        """
        Returns the value of
        display_order attribute of the
        pac.
        Raises:
            AttributeError: If the
                pac is not initialized.
        Returns:
            int: The value of
                display_order attribute.
        """
        if not self.pac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.pac.display_order
    @display_order.setter
    def display_order(self, value):
        """
        Sets the value of
        display_order for the
        pac.
        Args:
            value (int): The integer value to set for
                display_order.
        Raises:
            AttributeError: If the
                pac is not initialized.
        """
        if not self.pac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, int), (
            "display_order must be an integer")
        self.pac.display_order = value
    def set_prop_display_order(self, value: int):
        """
        Set the value of
        display_order property.
        Args:
            value (int): The value to set for
                display_order.
        Returns:
            self: Returns the instance of the class.
        """
        self.display_order = value
        return self
    # isActive
    @property
    def is_active(self):
        """
        Get the Is Active flag from the
        Pac object.
        :return: The Is Active flag.
        :raises AttributeError: If the
            Pac object is not initialized.
        """
        if not self.pac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.pac.is_active
    @is_active.setter
    def is_active(self, value: bool):
        """
        Set the Is Active flag for the
        Pac object.
        :param value: The Is Active flag value.
        :raises AttributeError: If the
            Pac object is not initialized.
        :raises ValueError: If the Is Active flag is not a boolean.
        """
        if not self.pac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if not isinstance(value, bool):
            raise ValueError("is_active must be a boolean.")
        self.pac.is_active = value
    def set_prop_is_active(self, value: bool):
        """
        Set the Is Active flag for the
        Pac object.
        :param value: The Is Active flag value.
        :return: The updated
            PacBusObj instance.
        """
        self.is_active = value
        return self
    # lookupEnumName
    @property
    def lookup_enum_name(self):
        """
        Get the Lookup Enum Name from the
        Pac object.
        :return: The Lookup Enum Name.
        :raises AttributeError: If the
            Pac object is not initialized.
        """
        if not self.pac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if self.pac.lookup_enum_name is None:
            return ""
        return self.pac.lookup_enum_name
    @lookup_enum_name.setter
    def lookup_enum_name(self, value):
        """
        Set the Lookup Enum Name for the
        Pac object.
        :param value: The Lookup Enum Name value.
        :raises AttributeError: If the
            Pac object is not initialized.
        :raises AssertionError: If the Lookup Enum Name is not a string.
        """
        if not self.pac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, str), "lookup_enum_name must be a string"
        self.pac.lookup_enum_name = value
    def set_prop_lookup_enum_name(self, value: str):
        """
        Set the Lookup Enum Name for the
        Pac object.
        :param value: The Lookup Enum Name value.
        :return: The updated
            PacBusObj instance.
        """
        self.lookup_enum_name = value
        return self
    # name
    @property
    def name(self):
        """
        Get the Name from the
        Pac object.
        :return: The Name.
        :raises AttributeError: If the
            Pac object is not initialized.
        """
        if not self.pac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if self.pac.name is None:
            return ""
        return self.pac.name
    @name.setter
    def name(self, value):
        """
        Set the Name for the
        Pac object.
        :param value: The Name value.
        :raises AttributeError: If the
            Pac object is not initialized.
        :raises AssertionError: If the Name is not a string.
        """
        if not self.pac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, str), "name must be a string"
        self.pac.name = value
    def set_prop_name(self, value: str):
        """
        Set the Name for the
        Pac object.
        :param value: The Name value.
        :return: The updated
            PacBusObj instance.
        """
        self.name = value
        return self
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
        Inserts the UTC date and time into
        the pac object.
        Raises:
            AttributeError: If the
                pac object is not initialized.
        Returns:
            The UTC date and time inserted into the
            pac object.
        """
        if not self.pac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.pac.insert_utc_date_time
    @insert_utc_date_time.setter
    def insert_utc_date_time(self, value):
        """
        Inserts the UTC date and time for the
        pac.
        Args:
            value (datetime): The UTC date and time to be inserted.
                It should be a datetime object or None.
        Raises:
            AttributeError: If the
                pac is not initialized.
        """
        if not self.pac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, datetime) or value is None, (
            "insert_utc_date_time must be a datetime object or None")
        self.pac.insert_utc_date_time = value
    # update_utc_date_time
    @property
    def last_update_utc_date_time(self):
        """
        Returns the last update UTC date and time
        of the pac.
        Raises:
            AttributeError: If the
                pac is not initialized.
        Returns:
            datetime: The last update UTC date and time
                of the pac.
        """
        if not self.pac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.pac.last_update_utc_date_time
    @last_update_utc_date_time.setter
    def last_update_utc_date_time(self, value):
        """
        Sets the last update UTC date and time
        for the pac.
        Args:
            value (datetime): The datetime object
                representing the last update UTC date and time.
                Pass None to unset the value.
        Raises:
            AttributeError: If the
                pac is not initialized.
        """
        if not self.pac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, datetime) or value is None, (
            "last_update_utc_date_time must be a datetime object or None")
        self.pac.last_update_utc_date_time = value
    async def load_from_json(
        self,
        json_data: str
    ):
        """
        Load pac data
        from JSON string.
        :param json_data: JSON string containing
            pac data.
        :raises ValueError: If json_data is not a string
            or if no pac
            data is found.
        """
        if not isinstance(json_data, str):
            raise ValueError("json_data must be a string")
        pac_manager = PacManager(
            self._session_context)
        self.pac = pac_manager.from_json(json_data)
        return self
    async def load_from_code(
        self,
        code: uuid.UUID
    ):
        """
        Load pac
        data from UUID code.
        :param code: UUID code for loading a specific
            pac.
        :raises ValueError: If code is not a UUID or if no
            pac data is found.
        """
        if not isinstance(code, uuid.UUID):
            raise ValueError("code must be a UUID")
        pac_manager = PacManager(
            self._session_context)
        pac_obj = await pac_manager.get_by_code(
            code)
        self.pac = pac_obj
        return self
    async def load_from_id(
        self,
        pac_id: int
    ):
        """
        Load pac data from
        pac ID.
        :param pac_id: Integer ID for loading a specific
            pac.
        :raises ValueError: If pac_id
            is not an integer or
            if no pac
            data is found.
        """
        if not isinstance(pac_id, int):
            raise ValueError("pac_id must be an integer")
        pac_manager = PacManager(
            self._session_context)
        pac_obj = await pac_manager.get_by_id(
            pac_id)
        self.pac = pac_obj
        return self
    async def load_from_obj_instance(
        self,
        pac_obj_instance: Pac
    ):
        """
        Use the provided
        Pac instance.
        :param pac_obj_instance: Instance of the
            Pac class.
        :raises ValueError: If pac_obj_instance
            is not an instance of
            Pac.
        """
        if not isinstance(pac_obj_instance,
                          Pac):
            raise ValueError("pac_obj_instance must be an instance of Pac")
        pac_manager = PacManager(
            self._session_context)
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
        Load pac data
        from dictionary.
        :param pac_dict: Dictionary containing
            pac data.
        :raises ValueError: If pac_dict
            is not a
            dictionary or if no
            pac data is found.
        """
        if not isinstance(pac_dict, dict):
            raise ValueError("pac_dict must be a dictionary")
        pac_manager = PacManager(
            self._session_context)
        self.pac = pac_manager.from_dict(
            pac_dict)
        return self

    @property
    def lookup_enum(self) -> managers_and_enums.PacEnum:
        """
        Returns the corresponding PacEnum
        value based on the lookup_enum_name.
        Raises:
            AttributeError: If the pac
                attribute is not initialized.
        Returns:
            managers_and_enums.PacEnum:
                The corresponding PacEnum value.
        """
        if not self.pac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return (
            managers_and_enums.PacEnum[
                self.pac.lookup_enum_name
            ]
        )
    async def load_from_enum(
        self,
        pac_enum:
            managers_and_enums.PacEnum
    ):
        """
        Load pac data from dictionary.
        :param pac_dict: Dictionary
            containing pac data.
        :raises ValueError: If pac_dict
            is not a dictionary or if no
            pac data is found.
        """
        if not isinstance(
            pac_enum,
            managers_and_enums.PacEnum
        ):
            raise ValueError("pac_enum must be a enum")
        pac_manager = PacManager(
            self._session_context
        )
        self.pac = await (
            pac_manager.
            from_enum(pac_enum)
        )

    def get_session_context(self):
        """
        Returns the session context.
        :return: The session context.
        :rtype: SessionContext
        """
        return self._session_context
    async def refresh(self):
        """
        Refreshes the pac
        object by fetching
        the latest data from the database.
        Returns:
            The updated
            pac object.
        """
        pac_manager = PacManager(
            self._session_context)
        self.pac = await pac_manager.refresh(
            self.pac)
        return self
    def is_valid(self):
        """
        Check if the pac
        is valid.
        Returns:
            bool: True if the pac
                is valid, False otherwise.
        """
        return self.pac is not None
    def to_dict(self):
        """
        Converts the Pac
        object to a dictionary representation.
        Returns:
            dict: A dictionary representation of the
                Pac object.
        """
        pac_manager = PacManager(
            self._session_context)
        return pac_manager.to_dict(
            self.pac)
    def to_json(self):
        """
        Converts the pac
        object to a JSON representation.
        Returns:
            str: The JSON representation of the
                pac object.
        """
        pac_manager = PacManager(
            self._session_context)
        return pac_manager.to_json(
            self.pac)
    async def save(self):
        """
        Saves the pac object
        to the database.
        If the pac object
        is not initialized, an AttributeError is raised.
        If the pac_id
        is greater than 0, the
        pac is
        updated in the database.
        If the pac_id is 0,
        the pac is
        added to the database.
        Returns:
            The updated or added
            pac object.
        Raises:
            AttributeError: If the pac
            object is not initialized.
        """
        if not self.pac:
            raise AttributeError(NOT_INITIALIZED_ERROR_MESSAGE)
        pac_id = self.pac.pac_id
        if pac_id > 0:
            pac_manager = PacManager(
                self._session_context)
            self.pac = await pac_manager.update(
                self.pac)
        if pac_id == 0:
            pac_manager = PacManager(
                self._session_context)
            self.pac = await pac_manager.add(
                self.pac)
        return self
    async def delete(self):
        """
        Deletes the pac
        from the database.
        Raises:
            AttributeError: If the pac
                is not initialized.
        """
        if not self.pac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if self.pac.pac_id > 0:
            pac_manager = PacManager(
                self._session_context)
            await pac_manager.delete(
                self.pac.pac_id)
            self.pac = None
    async def randomize_properties(self):
        """
        Randomizes the properties of the
        pac object.
        This method generates random values for various
        properties of the pac
        object
        Returns:
            self: The current instance of the
                Pac class.
        Raises:
            AttributeError: If the pac
                object is not initialized.
        """
        if not self.pac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        self.pac.description = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        self.pac.display_order = (
            random.randint(0, 100))
        self.pac.is_active = (
            random.choice([True, False]))
        self.pac.lookup_enum_name = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        self.pac.name = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
# endset
        return self
    def get_pac_obj(self) -> Pac:
        """
        Returns the pac
        object.
        Raises:
            AttributeError: If the pac
                object is not initialized.
        Returns:
            Pac: The pac
                object.
        """
        if not self.pac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.pac
    def is_equal(
        self,
        pac: Pac
    ) -> bool:
        """
        Checks if the current pac
        is equal to the given pac.
        Args:
            pac (Pac): The
                pac to compare with.
        Returns:
            bool: True if the pacs
                are equal, False otherwise.
        """
        pac_manager = PacManager(
            self._session_context)
        my_pac = self.get_pac_obj()
        return pac_manager.is_equal(
            pac, my_pac)
# endset
    # description,
    # displayOrder,
    # isActive,
    # lookupEnumName,
    # name,
# endset
    def get_obj(self) -> Pac:
        """
        Returns the Pac object.
        :return: The Pac object.
        :rtype: Pac
        """
        return self.pac
    def get_object_name(self) -> str:
        """
        Returns the name of the object.
        :return: The name of the object.
        :rtype: str
        """
        return "pac"
    def get_id(self) -> int:
        """
        Returns the ID of the pac.
        :return: The ID of the pac.
        :rtype: int
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
        Convert a list of Pac
        objects to a list of
        PacBusObj objects.
        Args:
            session_context (SessionContext): The session context.
            obj_list (List[Pac]): The
                list of Pac objects to convert.
        Returns:
            List[PacBusObj]: The
                list of converted PacBusObj
                objects.
        """
        result = list()
        for pac in obj_list:
            pac_bus_obj = PacBusObj(session_context)
            await pac_bus_obj.load_from_obj_instance(
                pac)
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

