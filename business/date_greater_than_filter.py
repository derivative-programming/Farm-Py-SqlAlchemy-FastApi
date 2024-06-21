# business/date_greater_than_filter.py
"""
This module contains the DateGreaterThanFilterBusObj class,
which represents the business object for a DateGreaterThanFilter.
"""
from decimal import Decimal
import random
import uuid
from typing import List
from datetime import datetime, date
from helpers.session_context import SessionContext
from managers import DateGreaterThanFilterManager
from models import DateGreaterThanFilter
import models
import managers as managers_and_enums
from .base_bus_obj import BaseBusObj

NOT_INITIALIZED_ERROR_MESSAGE = (
    "DateGreaterThanFilter object is not initialized")
class DateGreaterThanFilterInvalidInitError(Exception):
    """
    Exception raised when the DateGreaterThanFilter object is not initialized properly.
    """
class DateGreaterThanFilterBusObj(BaseBusObj):
    """
    This class represents the business object for a DateGreaterThanFilter.
    It requires a valid session context for initialization.
    """
    def __init__(self, session_context: SessionContext):
        """
        Initializes a new instance of the DateGreaterThanFilterBusObj class.
        :param session_context: The session context.
        :raises ValueError: If the session is not provided.
        """
        if not session_context.session:
            raise ValueError("session required")
        self._session_context = session_context
        self.date_greater_than_filter = DateGreaterThanFilter()
    @property
    def date_greater_than_filter_id(self) -> int:
        """
        Get the date_greater_than_filter ID from the DateGreaterThanFilter object.
        :return: The date_greater_than_filter ID.
        :raises AttributeError: If the DateGreaterThanFilter object is not initialized.
        """
        if not self.date_greater_than_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.date_greater_than_filter.date_greater_than_filter_id
    # code
    @property
    def code(self):
        """
        Get the code from the DateGreaterThanFilter object.
        :return: The code.
        :raises AttributeError: If the DateGreaterThanFilter object is not initialized.
        """
        if not self.date_greater_than_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.date_greater_than_filter.code
    @code.setter
    def code(self, value: uuid.UUID):  # type: ignore
        """
        Set the code for the DateGreaterThanFilter object.
        :param value: The code value.
        :raises AttributeError: If the DateGreaterThanFilter object is not initialized.
        :raises ValueError: If the code is not a UUID.
        """
        if not self.date_greater_than_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if not isinstance(value, uuid.UUID):
            raise ValueError("code must be a UUID.")
        self.date_greater_than_filter.code = value
    # last_change_code
    @property
    def last_change_code(self):
        """
        Get the last change code from the DateGreaterThanFilter object.
        :return: The last change code.
        :raises AttributeError: If the DateGreaterThanFilter object is not initialized.
        """
        if not self.date_greater_than_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.date_greater_than_filter.last_change_code
    @last_change_code.setter
    def last_change_code(self, value: int):
        """
        Set the last change code for the DateGreaterThanFilter object.
        :param value: The last change code value.
        :raises AttributeError: If the DateGreaterThanFilter object is not initialized.
        :raises ValueError: If the last change code is not an integer.
        """
        if not self.date_greater_than_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if not isinstance(value, int):
            raise ValueError("last_change_code must be an integer.")
        self.date_greater_than_filter.last_change_code = value
    # insert_user_id
    @property
    def insert_user_id(self):
        """
        Get the insert user ID from the DateGreaterThanFilter object.
        :return: The insert user ID.
        :raises AttributeError: If the DateGreaterThanFilter object is not initialized.
        """
        if not self.date_greater_than_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.date_greater_than_filter.insert_user_id
    @insert_user_id.setter
    def insert_user_id(self, value: uuid.UUID):
        """
        Set the insert user ID for the DateGreaterThanFilter object.
        :param value: The insert user ID value.
        :raises AttributeError: If the DateGreaterThanFilter object is not initialized.
        :raises ValueError: If the insert user ID is not a UUID.
        """
        if not self.date_greater_than_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if not isinstance(value, uuid.UUID):
            raise ValueError("insert_user_id must be a UUID.")
        self.date_greater_than_filter.insert_user_id = value
    # last_update_user_id
    @property
    def last_update_user_id(self):
        """
        Get the last update user ID from the DateGreaterThanFilter object.
        :return: The last update user ID.
        :raises AttributeError: If the DateGreaterThanFilter object is not initialized.
        """
        if not self.date_greater_than_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.date_greater_than_filter.last_update_user_id
    @last_update_user_id.setter
    def last_update_user_id(self, value: uuid.UUID):
        """
        Set the last update user ID for the DateGreaterThanFilter object.
        :param value: The last update user ID value.
        :raises AttributeError: If the DateGreaterThanFilter object is not initialized.
        :raises ValueError: If the last update user ID is not a UUID.
        """
        if not self.date_greater_than_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if not isinstance(value, uuid.UUID):
            raise ValueError("last_update_user_id must be a UUID.")
        self.date_greater_than_filter.last_update_user_id = value
# endset
    # dayCount
    @property
    def day_count(self):
        """
        Returns the value of day_count attribute of the date_greater_than_filter.
        Raises:
            AttributeError: If the date_greater_than_filter is not initialized.
        Returns:
            int: The value of day_count attribute.
        """
        if not self.date_greater_than_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.date_greater_than_filter.day_count
    @day_count.setter
    def day_count(self, value):
        """
        Sets the value of day_count for the date_greater_than_filter.
        Args:
            value (int): The integer value to set for day_count.
        Raises:
            AttributeError: If the date_greater_than_filter is not initialized.
        """
        if not self.date_greater_than_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, int), (
            "day_count must be an integer")
        self.date_greater_than_filter.day_count = value
    def set_prop_day_count(self, value: int):
        """
        Set the value of day_count property.
        Args:
            value (int): The value to set for day_count.
        Returns:
            self: Returns the instance of the class.
        """
        self.day_count = value
        return self
    # description
    @property
    def description(self):
        """
        Get the Description from the DateGreaterThanFilter object.
        :return: The Description.
        :raises AttributeError: If the DateGreaterThanFilter object is not initialized.
        """
        if not self.date_greater_than_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if self.date_greater_than_filter.description is None:
            return ""
        return self.date_greater_than_filter.description
    @description.setter
    def description(self, value):
        """
        Set the Description for the DateGreaterThanFilter object.
        :param value: The Description value.
        :raises AttributeError: If the DateGreaterThanFilter object is not initialized.
        :raises AssertionError: If the Description is not a string.
        """
        if not self.date_greater_than_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, str), "description must be a string"
        self.date_greater_than_filter.description = value
    def set_prop_description(self, value: str):
        """
        Set the Description for the DateGreaterThanFilter object.
        :param value: The Description value.
        :return: The updated DateGreaterThanFilterBusObj instance.
        """
        self.description = value
        return self
    # displayOrder
    @property
    def display_order(self):
        """
        Returns the value of display_order attribute of the date_greater_than_filter.
        Raises:
            AttributeError: If the date_greater_than_filter is not initialized.
        Returns:
            int: The value of display_order attribute.
        """
        if not self.date_greater_than_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.date_greater_than_filter.display_order
    @display_order.setter
    def display_order(self, value):
        """
        Sets the value of display_order for the date_greater_than_filter.
        Args:
            value (int): The integer value to set for display_order.
        Raises:
            AttributeError: If the date_greater_than_filter is not initialized.
        """
        if not self.date_greater_than_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, int), (
            "display_order must be an integer")
        self.date_greater_than_filter.display_order = value
    def set_prop_display_order(self, value: int):
        """
        Set the value of display_order property.
        Args:
            value (int): The value to set for display_order.
        Returns:
            self: Returns the instance of the class.
        """
        self.display_order = value
        return self
    # isActive
    @property
    def is_active(self):
        """
        Get the Is Active flag from the DateGreaterThanFilter object.
        :return: The Is Active flag.
        :raises AttributeError: If the DateGreaterThanFilter object is not initialized.
        """
        if not self.date_greater_than_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.date_greater_than_filter.is_active
    @is_active.setter
    def is_active(self, value: bool):
        """
        Set the Is Active flag for the DateGreaterThanFilter object.
        :param value: The Is Active flag value.
        :raises AttributeError: If the DateGreaterThanFilter object is not initialized.
        :raises ValueError: If the Is Active flag is not a boolean.
        """
        if not self.date_greater_than_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if not isinstance(value, bool):
            raise ValueError("is_active must be a boolean.")
        self.date_greater_than_filter.is_active = value
    def set_prop_is_active(self, value: bool):
        """
        Set the Is Active flag for the DateGreaterThanFilter object.
        :param value: The Is Active flag value.
        :return: The updated DateGreaterThanFilterBusObj instance.
        """
        self.is_active = value
        return self
    # lookupEnumName
    @property
    def lookup_enum_name(self):
        """
        Get the Lookup Enum Name from the DateGreaterThanFilter object.
        :return: The Lookup Enum Name.
        :raises AttributeError: If the DateGreaterThanFilter object is not initialized.
        """
        if not self.date_greater_than_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if self.date_greater_than_filter.lookup_enum_name is None:
            return ""
        return self.date_greater_than_filter.lookup_enum_name
    @lookup_enum_name.setter
    def lookup_enum_name(self, value):
        """
        Set the Lookup Enum Name for the DateGreaterThanFilter object.
        :param value: The Lookup Enum Name value.
        :raises AttributeError: If the DateGreaterThanFilter object is not initialized.
        :raises AssertionError: If the Lookup Enum Name is not a string.
        """
        if not self.date_greater_than_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, str), "lookup_enum_name must be a string"
        self.date_greater_than_filter.lookup_enum_name = value
    def set_prop_lookup_enum_name(self, value: str):
        """
        Set the Lookup Enum Name for the DateGreaterThanFilter object.
        :param value: The Lookup Enum Name value.
        :return: The updated DateGreaterThanFilterBusObj instance.
        """
        self.lookup_enum_name = value
        return self
    # name
    @property
    def name(self):
        """
        Get the Name from the DateGreaterThanFilter object.
        :return: The Name.
        :raises AttributeError: If the DateGreaterThanFilter object is not initialized.
        """
        if not self.date_greater_than_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if self.date_greater_than_filter.name is None:
            return ""
        return self.date_greater_than_filter.name
    @name.setter
    def name(self, value):
        """
        Set the Name for the DateGreaterThanFilter object.
        :param value: The Name value.
        :raises AttributeError: If the DateGreaterThanFilter object is not initialized.
        :raises AssertionError: If the Name is not a string.
        """
        if not self.date_greater_than_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, str), "name must be a string"
        self.date_greater_than_filter.name = value
    def set_prop_name(self, value: str):
        """
        Set the Name for the DateGreaterThanFilter object.
        :param value: The Name value.
        :return: The updated DateGreaterThanFilterBusObj instance.
        """
        self.name = value
        return self
    # PacID
# endset
    # dayCount,
    # description,
    # displayOrder,
    # isActive,
    # lookupEnumName,
    # name,
    # PacID
    @property
    def pac_id(self):
        """
        Returns the pac ID associated with the date_greater_than_filter.
        Raises:
            AttributeError: If the date_greater_than_filter is not initialized.
        Returns:
            int: The pac ID of the date_greater_than_filter.
        """
        if not self.date_greater_than_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.date_greater_than_filter.pac_id
    @pac_id.setter
    def pac_id(self, value):
        """
        Sets the pac ID for the date_greater_than_filter.
        Args:
            value (int or None): The pac ID to be set.
                Must be an integer or None.
        Raises:
            AttributeError: If the date_greater_than_filter is not initialized.
        """
        if not self.date_greater_than_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, int) or value is None, (
            "pac_id must be an integer or None")
        self.date_greater_than_filter.pac_id = value
    def set_prop_pac_id(self, value: int):
        """
        Set the pac ID for the date_greater_than_filter.
        Args:
            value (int): The ID of the pac.
        Returns:
            DateGreaterThanFilter: The updated DateGreaterThanFilter object.
        """
        self.pac_id = value
        return self
    @property
    def pac_code_peek(self) -> uuid.UUID:
        """
        Returns the pac code peek of the date_greater_than_filter.
        Raises:
            AttributeError: If the date_greater_than_filter is not initialized.
        Returns:
            uuid.UUID: The pac code peek of the date_greater_than_filter.
        """
        if not self.date_greater_than_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.date_greater_than_filter.pac_code_peek
    # @pac_code_peek.setter
    # def pac_code_peek(self, value):
    #     assert isinstance(value, uuid.UUID),
    #           "pac_code_peek must be a UUID"
    #     self.date_greater_than_filter.pac_code_peek = value
# endset
    # insert_utc_date_time
    @property
    def insert_utc_date_time(self):
        """
        Inserts the UTC date and time into the date_greater_than_filter object.
        Raises:
            AttributeError: If the date_greater_than_filter object is not initialized.
        Returns:
            The UTC date and time inserted into the date_greater_than_filter object.
        """
        if not self.date_greater_than_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.date_greater_than_filter.insert_utc_date_time
    @insert_utc_date_time.setter
    def insert_utc_date_time(self, value):
        """
        Inserts the UTC date and time for the date_greater_than_filter.
        Args:
            value (datetime): The UTC date and time to be inserted.
                It should be a datetime object or None.
        Raises:
            AttributeError: If the date_greater_than_filter is not initialized.
        """
        if not self.date_greater_than_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, datetime) or value is None, (
            "insert_utc_date_time must be a datetime object or None")
        self.date_greater_than_filter.insert_utc_date_time = value
    # update_utc_date_time
    @property
    def last_update_utc_date_time(self):
        """
        Returns the last update UTC date and time of the date_greater_than_filter.
        Raises:
            AttributeError: If the date_greater_than_filter is not initialized.
        Returns:
            datetime: The last update UTC date and time of the date_greater_than_filter.
        """
        if not self.date_greater_than_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.date_greater_than_filter.last_update_utc_date_time
    @last_update_utc_date_time.setter
    def last_update_utc_date_time(self, value):
        """
        Sets the last update UTC date and time for the date_greater_than_filter.
        Args:
            value (datetime): The datetime object
                representing the last update UTC date and time.
                Pass None to unset the value.
        Raises:
            AttributeError: If the date_greater_than_filter is not initialized.
        """
        if not self.date_greater_than_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, datetime) or value is None, (
            "last_update_utc_date_time must be a datetime object or None")
        self.date_greater_than_filter.last_update_utc_date_time = value
    async def load_from_json(
        self,
        json_data: str
    ):
        """
        Load date_greater_than_filter data from JSON string.
        :param json_data: JSON string containing date_greater_than_filter data.
        :raises ValueError: If json_data is not a string
            or if no date_greater_than_filter data is found.
        """
        if not isinstance(json_data, str):
            raise ValueError("json_data must be a string")
        date_greater_than_filter_manager = DateGreaterThanFilterManager(self._session_context)
        self.date_greater_than_filter = date_greater_than_filter_manager.from_json(json_data)
        return self
    async def load_from_code(
        self,
        code: uuid.UUID
    ):
        """
        Load date_greater_than_filter data from UUID code.
        :param code: UUID code for loading a specific date_greater_than_filter.
        :raises ValueError: If code is not a UUID or if no date_greater_than_filter data is found.
        """
        if not isinstance(code, uuid.UUID):
            raise ValueError("code must be a UUID")
        date_greater_than_filter_manager = DateGreaterThanFilterManager(self._session_context)
        date_greater_than_filter_obj = await date_greater_than_filter_manager.get_by_code(code)
        self.date_greater_than_filter = date_greater_than_filter_obj
        return self
    async def load_from_id(
        self,
        date_greater_than_filter_id: int
    ):
        """
        Load date_greater_than_filter data from date_greater_than_filter ID.
        :param date_greater_than_filter_id: Integer ID for loading a specific date_greater_than_filter.
        :raises ValueError: If date_greater_than_filter_id is not an integer or
            if no date_greater_than_filter data is found.
        """
        if not isinstance(date_greater_than_filter_id, int):
            raise ValueError("date_greater_than_filter_id must be an integer")
        date_greater_than_filter_manager = DateGreaterThanFilterManager(self._session_context)
        date_greater_than_filter_obj = await date_greater_than_filter_manager.get_by_id(date_greater_than_filter_id)
        self.date_greater_than_filter = date_greater_than_filter_obj
        return self
    async def load_from_obj_instance(
        self,
        date_greater_than_filter_obj_instance: DateGreaterThanFilter
    ):
        """
        Use the provided DateGreaterThanFilter instance.
        :param date_greater_than_filter_obj_instance: Instance of the DateGreaterThanFilter class.
        :raises ValueError: If date_greater_than_filter_obj_instance is not an instance of DateGreaterThanFilter.
        """
        if not isinstance(date_greater_than_filter_obj_instance, DateGreaterThanFilter):
            raise ValueError("date_greater_than_filter_obj_instance must be an instance of DateGreaterThanFilter")
        date_greater_than_filter_manager = DateGreaterThanFilterManager(self._session_context)
        date_greater_than_filter_obj_instance_date_greater_than_filter_id = date_greater_than_filter_obj_instance.date_greater_than_filter_id
        date_greater_than_filter_obj = await date_greater_than_filter_manager.get_by_id(
            date_greater_than_filter_obj_instance_date_greater_than_filter_id
        )
        self.date_greater_than_filter = date_greater_than_filter_obj
        return self
    async def load_from_dict(
        self,
        date_greater_than_filter_dict: dict
    ):
        """
        Load date_greater_than_filter data from dictionary.
        :param date_greater_than_filter_dict: Dictionary containing date_greater_than_filter data.
        :raises ValueError: If date_greater_than_filter_dict is not a
            dictionary or if no date_greater_than_filter data is found.
        """
        if not isinstance(date_greater_than_filter_dict, dict):
            raise ValueError("date_greater_than_filter_dict must be a dictionary")
        date_greater_than_filter_manager = DateGreaterThanFilterManager(self._session_context)
        self.date_greater_than_filter = date_greater_than_filter_manager.from_dict(date_greater_than_filter_dict)
        return self

##GENTrainingBlock[caseLookupEnums]Start
##GENLearn[isLookup=true]Start
    @property
    def lookup_enum(self) -> managers_and_enums.DateGreaterThanFilterEnum:
        """
        Returns the corresponding DateGreaterThanFilterEnum
        value based on the lookup_enum_name.
        Raises:
            AttributeError: If the date_greater_than_filter
                attribute is not initialized.
        Returns:
            managers_and_enums.DateGreaterThanFilterEnum:
                The corresponding DateGreaterThanFilterEnum value.
        """
        if not self.date_greater_than_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return (
            managers_and_enums.DateGreaterThanFilterEnum[
                self.date_greater_than_filter.lookup_enum_name
            ]
        )
    async def load_from_enum(
        self,
        date_greater_than_filter_enum:
            managers_and_enums.DateGreaterThanFilterEnum
    ):
        """
        Load date_greater_than_filter data from dictionary.
        :param date_greater_than_filter_dict: Dictionary
            containing date_greater_than_filter data.
        :raises ValueError: If date_greater_than_filter_dict
            is not a dictionary or if no
            date_greater_than_filter data is found.
        """
        if not isinstance(
            date_greater_than_filter_enum,
            managers_and_enums.DateGreaterThanFilterEnum
        ):
            raise ValueError("date_greater_than_filter_enum must be a enum")
        date_greater_than_filter_manager = DateGreaterThanFilterManager(
            self._session_context
        )
        self.date_greater_than_filter = await (
            date_greater_than_filter_manager.
            from_enum(date_greater_than_filter_enum)
        )

##GENLearn[isLookup=true]End
##GENTrainingBlock[caseLookupEnums]End

    def get_session_context(self):
        """
        Returns the session context.
        :return: The session context.
        :rtype: SessionContext
        """
        return self._session_context
    async def refresh(self):
        """
        Refreshes the date_greater_than_filter object by fetching
        the latest data from the database.
        Returns:
            The updated date_greater_than_filter object.
        """
        date_greater_than_filter_manager = DateGreaterThanFilterManager(self._session_context)
        self.date_greater_than_filter = await date_greater_than_filter_manager.refresh(self.date_greater_than_filter)
        return self
    def is_valid(self):
        """
        Check if the date_greater_than_filter is valid.
        Returns:
            bool: True if the date_greater_than_filter is valid, False otherwise.
        """
        return self.date_greater_than_filter is not None
    def to_dict(self):
        """
        Converts the DateGreaterThanFilter object to a dictionary representation.
        Returns:
            dict: A dictionary representation of the DateGreaterThanFilter object.
        """
        date_greater_than_filter_manager = DateGreaterThanFilterManager(self._session_context)
        return date_greater_than_filter_manager.to_dict(self.date_greater_than_filter)
    def to_json(self):
        """
        Converts the date_greater_than_filter object to a JSON representation.
        Returns:
            str: The JSON representation of the date_greater_than_filter object.
        """
        date_greater_than_filter_manager = DateGreaterThanFilterManager(self._session_context)
        return date_greater_than_filter_manager.to_json(self.date_greater_than_filter)
    async def save(self):
        """
        Saves the date_greater_than_filter object to the database.
        If the date_greater_than_filter object is not initialized, an AttributeError is raised.
        If the date_greater_than_filter_id is greater than 0, the date_greater_than_filter is
        updated in the database.
        If the date_greater_than_filter_id is 0, the date_greater_than_filter is added to the database.
        Returns:
            The updated or added date_greater_than_filter object.
        Raises:
            AttributeError: If the date_greater_than_filter object is not initialized.
        """
        if not self.date_greater_than_filter:
            raise AttributeError(NOT_INITIALIZED_ERROR_MESSAGE)
        date_greater_than_filter_id = self.date_greater_than_filter.date_greater_than_filter_id
        if date_greater_than_filter_id > 0:
            date_greater_than_filter_manager = DateGreaterThanFilterManager(self._session_context)
            self.date_greater_than_filter = await date_greater_than_filter_manager.update(self.date_greater_than_filter)
        if date_greater_than_filter_id == 0:
            date_greater_than_filter_manager = DateGreaterThanFilterManager(self._session_context)
            self.date_greater_than_filter = await date_greater_than_filter_manager.add(self.date_greater_than_filter)
        return self
    async def delete(self):
        """
        Deletes the date_greater_than_filter from the database.
        Raises:
            AttributeError: If the date_greater_than_filter is not initialized.
        """
        if not self.date_greater_than_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if self.date_greater_than_filter.date_greater_than_filter_id > 0:
            date_greater_than_filter_manager = DateGreaterThanFilterManager(self._session_context)
            await date_greater_than_filter_manager.delete(self.date_greater_than_filter.date_greater_than_filter_id)
            self.date_greater_than_filter = None
    async def randomize_properties(self):
        """
        Randomizes the properties of the date_greater_than_filter object.
        This method generates random values for various
        properties of the date_greater_than_filter object
        Returns:
            self: The current instance of the DateGreaterThanFilter class.
        Raises:
            AttributeError: If the date_greater_than_filter object is not initialized.
        """
        if not self.date_greater_than_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        self.date_greater_than_filter.day_count = (
            random.randint(0, 100))
        self.date_greater_than_filter.description = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        self.date_greater_than_filter.display_order = (
            random.randint(0, 100))
        self.date_greater_than_filter.is_active = (
            random.choice([True, False]))
        self.date_greater_than_filter.lookup_enum_name = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        self.date_greater_than_filter.name = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        # self.date_greater_than_filter.pac_id = random.randint(0, 100)
# endset
        return self
    def get_date_greater_than_filter_obj(self) -> DateGreaterThanFilter:
        """
        Returns the date_greater_than_filter object.
        Raises:
            AttributeError: If the date_greater_than_filter object is not initialized.
        Returns:
            DateGreaterThanFilter: The date_greater_than_filter object.
        """
        if not self.date_greater_than_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.date_greater_than_filter
    def is_equal(self, date_greater_than_filter: DateGreaterThanFilter) -> bool:
        """
        Checks if the current date_greater_than_filter is equal to the given date_greater_than_filter.
        Args:
            date_greater_than_filter (DateGreaterThanFilter): The date_greater_than_filter to compare with.
        Returns:
            bool: True if the date_greater_than_filters are equal, False otherwise.
        """
        date_greater_than_filter_manager = DateGreaterThanFilterManager(self._session_context)
        my_date_greater_than_filter = self.get_date_greater_than_filter_obj()
        return date_greater_than_filter_manager.is_equal(date_greater_than_filter, my_date_greater_than_filter)
# endset
    # dayCount,
    # description,
    # displayOrder,
    # isActive,
    # lookupEnumName,
    # name,
    # PacID
    async def get_pac_id_rel_obj(self) -> models.Pac:
        """
        Retrieves the related Pac object based on the pac_id.
        Returns:
            An instance of the Pac model representing the related pac.
        """
        pac_manager = managers_and_enums.PacManager(self._session_context)
        pac_obj = await pac_manager.get_by_id(self.pac_id)
        return pac_obj
# endset
    def get_obj(self) -> DateGreaterThanFilter:
        """
        Returns the DateGreaterThanFilter object.
        :return: The DateGreaterThanFilter object.
        :rtype: DateGreaterThanFilter
        """
        return self.date_greater_than_filter
    def get_object_name(self) -> str:
        """
        Returns the name of the object.
        :return: The name of the object.
        :rtype: str
        """
        return "date_greater_than_filter"
    def get_id(self) -> int:
        """
        Returns the ID of the date_greater_than_filter.
        :return: The ID of the date_greater_than_filter.
        :rtype: int
        """
        return self.date_greater_than_filter_id
    # dayCount,
    # description,
    # displayOrder,
    # isActive,
    # lookupEnumName,
    # name,
    # PacID
    async def get_parent_name(self) -> str:
        """
        Get the name of the parent date_greater_than_filter.
        Returns:
            str: The name of the parent date_greater_than_filter.
        """
        return 'Pac'
    async def get_parent_code(self) -> uuid.UUID:
        """
        Get the parent code of the date_greater_than_filter.
        Returns:
            The parent code of the date_greater_than_filter as a UUID.
        """
        return self.pac_code_peek
    async def get_parent_obj(self) -> models.Pac:
        """
        Get the parent object of the current date_greater_than_filter.
        Returns:
            The parent object of the current date_greater_than_filter,
            which is an instance of the Pac model.
        """
        pac = await self.get_pac_id_rel_obj()
        return pac
# endset
    @staticmethod
    async def to_bus_obj_list(
        session_context: SessionContext,
        obj_list: List[DateGreaterThanFilter]
    ):
        """
        Convert a list of DateGreaterThanFilter objects to a list of DateGreaterThanFilterBusObj objects.
        Args:
            session_context (SessionContext): The session context.
            obj_list (List[DateGreaterThanFilter]): The list of DateGreaterThanFilter objects to convert.
        Returns:
            List[DateGreaterThanFilterBusObj]: The list of converted DateGreaterThanFilterBusObj objects.
        """
        result = list()
        for date_greater_than_filter in obj_list:
            date_greater_than_filter_bus_obj = DateGreaterThanFilterBusObj(session_context)
            await date_greater_than_filter_bus_obj.load_from_obj_instance(date_greater_than_filter)
            result.append(date_greater_than_filter_bus_obj)
        return result

