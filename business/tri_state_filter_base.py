# business/tri_state_filter_base.py
"""
This module contains the TriStateFilterBaseBusObj class,
which represents the base business object for a TriStateFilter.
"""
from decimal import Decimal
import random
import uuid
from datetime import datetime, date
from helpers.session_context import SessionContext
from managers import TriStateFilterManager
from models import TriStateFilter
import models
import managers as managers_and_enums
from .base_bus_obj import BaseBusObj
NOT_INITIALIZED_ERROR_MESSAGE = (
    "TriStateFilter object is not initialized")
class TriStateFilterInvalidInitError(Exception):
    """
    Exception raised when the
    TriStateFilter object
    is not initialized properly.
    """
class TriStateFilterBaseBusObj(BaseBusObj):
    """
    This class represents the base business object
    for a TriStateFilter.
    It requires a valid session context for initialization.
    """
    def __init__(self, session_context: SessionContext):
        """
        Initializes a new instance of the
        TriStateFilterBusObj class.
        :param session_context: The session context.
        :raises ValueError: If the session is not provided.
        """
        if not session_context.session:
            raise ValueError("session required")
        self._session_context = session_context
        self.tri_state_filter = TriStateFilter()
    @property
    def tri_state_filter_id(self) -> int:
        """
        Get the tri_state_filter ID from the
        TriStateFilter object.
        :return: The tri_state_filter ID.
        :raises AttributeError: If the
            TriStateFilter object is not initialized.
        """
        if not self.tri_state_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.tri_state_filter.tri_state_filter_id
    # code
    @property
    def code(self):
        """
        Get the code from the
        TriStateFilter object.
        :return: The code.
        :raises AttributeError: If the
            TriStateFilter object is not initialized.
        """
        if not self.tri_state_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.tri_state_filter.code
    @code.setter
    def code(self, value: uuid.UUID):  # type: ignore
        """
        Set the code for the TriStateFilter object.
        :param value: The code value.
        :raises AttributeError: If the
            TriStateFilter object is not initialized.
        :raises ValueError: If the code is not a UUID.
        """
        if not self.tri_state_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if not isinstance(value, uuid.UUID):
            raise ValueError("code must be a UUID.")
        self.tri_state_filter.code = value
    # last_change_code
    @property
    def last_change_code(self):
        """
        Get the last change code from the
        TriStateFilter object.
        :return: The last change code.
        :raises AttributeError: If the
            TriStateFilter object is not initialized.
        """
        if not self.tri_state_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.tri_state_filter.last_change_code
    @last_change_code.setter
    def last_change_code(self, value: int):
        """
        Set the last change code for the
        TriStateFilter object.
        :param value: The last change code value.
        :raises AttributeError: If the
            TriStateFilter object is not initialized.
        :raises ValueError: If the last change code is not an integer.
        """
        if not self.tri_state_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if not isinstance(value, int):
            raise ValueError("last_change_code must be an integer.")
        self.tri_state_filter.last_change_code = value
    # insert_user_id
    @property
    def insert_user_id(self):
        """
        Get the insert user ID from the
        TriStateFilter object.
        :return: The insert user ID.
        :raises AttributeError: If the
            TriStateFilter object is not initialized.
        """
        if not self.tri_state_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.tri_state_filter.insert_user_id
    @insert_user_id.setter
    def insert_user_id(self, value: uuid.UUID):
        """
        Set the insert user ID for the
        TriStateFilter object.
        :param value: The insert user ID value.
        :raises AttributeError: If the
            TriStateFilter object is not initialized.
        :raises ValueError: If the insert user ID is not a UUID.
        """
        if not self.tri_state_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if not isinstance(value, uuid.UUID):
            raise ValueError("insert_user_id must be a UUID.")
        self.tri_state_filter.insert_user_id = value
    # last_update_user_id
    @property
    def last_update_user_id(self):
        """
        Get the last update user ID from the
        TriStateFilter object.
        :return: The last update user ID.
        :raises AttributeError: If the
            TriStateFilter object is not initialized.
        """
        if not self.tri_state_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.tri_state_filter.last_update_user_id
    @last_update_user_id.setter
    def last_update_user_id(self, value: uuid.UUID):
        """
        Set the last update user ID for the
        TriStateFilter object.
        :param value: The last update user ID value.
        :raises AttributeError: If the
            TriStateFilter object is not initialized.
        :raises ValueError: If the last update user ID is not a UUID.
        """
        if not self.tri_state_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if not isinstance(value, uuid.UUID):
            raise ValueError("last_update_user_id must be a UUID.")
        self.tri_state_filter.last_update_user_id = value
# endset
    # description
    @property
    def description(self):
        """
        Get the Description from the
        TriStateFilter object.
        :return: The Description.
        :raises AttributeError: If the
            TriStateFilter object is not initialized.
        """
        if not self.tri_state_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if self.tri_state_filter.description is None:
            return ""
        return self.tri_state_filter.description
    @description.setter
    def description(self, value):
        """
        Set the Description for the
        TriStateFilter object.
        :param value: The Description value.
        :raises AttributeError: If the
            TriStateFilter object is not initialized.
        :raises AssertionError: If the Description is not a string.
        """
        if not self.tri_state_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, str), "description must be a string"
        self.tri_state_filter.description = value
    # displayOrder
    @property
    def display_order(self):
        """
        Returns the value of
        display_order attribute of the
        tri_state_filter.
        Raises:
            AttributeError: If the
                tri_state_filter is not initialized.
        Returns:
            int: The value of
                display_order attribute.
        """
        if not self.tri_state_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.tri_state_filter.display_order
    @display_order.setter
    def display_order(self, value):
        """
        Sets the value of
        display_order for the
        tri_state_filter.
        Args:
            value (int): The integer value to set for
                display_order.
        Raises:
            AttributeError: If the
                tri_state_filter is not initialized.
        """
        if not self.tri_state_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, int), (
            "display_order must be an integer")
        self.tri_state_filter.display_order = value
    # isActive
    @property
    def is_active(self):
        """
        Get the Is Active flag from the
        TriStateFilter object.
        :return: The Is Active flag.
        :raises AttributeError: If the
            TriStateFilter object is not initialized.
        """
        if not self.tri_state_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.tri_state_filter.is_active
    @is_active.setter
    def is_active(self, value: bool):
        """
        Set the Is Active flag for the
        TriStateFilter object.
        :param value: The Is Active flag value.
        :raises AttributeError: If the
            TriStateFilter object is not initialized.
        :raises ValueError: If the Is Active flag is not a boolean.
        """
        if not self.tri_state_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if not isinstance(value, bool):
            raise ValueError("is_active must be a boolean.")
        self.tri_state_filter.is_active = value
    # lookupEnumName
    @property
    def lookup_enum_name(self):
        """
        Get the Lookup Enum Name from the
        TriStateFilter object.
        :return: The Lookup Enum Name.
        :raises AttributeError: If the
            TriStateFilter object is not initialized.
        """
        if not self.tri_state_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if self.tri_state_filter.lookup_enum_name is None:
            return ""
        return self.tri_state_filter.lookup_enum_name
    @lookup_enum_name.setter
    def lookup_enum_name(self, value):
        """
        Set the Lookup Enum Name for the
        TriStateFilter object.
        :param value: The Lookup Enum Name value.
        :raises AttributeError: If the
            TriStateFilter object is not initialized.
        :raises AssertionError: If the Lookup Enum Name is not a string.
        """
        if not self.tri_state_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, str), "lookup_enum_name must be a string"
        self.tri_state_filter.lookup_enum_name = value
    # name
    @property
    def name(self):
        """
        Get the Name from the
        TriStateFilter object.
        :return: The Name.
        :raises AttributeError: If the
            TriStateFilter object is not initialized.
        """
        if not self.tri_state_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if self.tri_state_filter.name is None:
            return ""
        return self.tri_state_filter.name
    @name.setter
    def name(self, value):
        """
        Set the Name for the
        TriStateFilter object.
        :param value: The Name value.
        :raises AttributeError: If the
            TriStateFilter object is not initialized.
        :raises AssertionError: If the Name is not a string.
        """
        if not self.tri_state_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, str), "name must be a string"
        self.tri_state_filter.name = value
    # PacID
    # stateIntValue
    @property
    def state_int_value(self):
        """
        Returns the value of
        state_int_value attribute of the
        tri_state_filter.
        Raises:
            AttributeError: If the
                tri_state_filter is not initialized.
        Returns:
            int: The value of
                state_int_value attribute.
        """
        if not self.tri_state_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.tri_state_filter.state_int_value
    @state_int_value.setter
    def state_int_value(self, value):
        """
        Sets the value of
        state_int_value for the
        tri_state_filter.
        Args:
            value (int): The integer value to set for
                state_int_value.
        Raises:
            AttributeError: If the
                tri_state_filter is not initialized.
        """
        if not self.tri_state_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, int), (
            "state_int_value must be an integer")
        self.tri_state_filter.state_int_value = value
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
        Returns the pac ID
        associated with the
        tri_state_filter.
        Raises:
            AttributeError: If the
                tri_state_filter is not initialized.
        Returns:
            int: The pac ID of the tri_state_filter.
        """
        if not self.tri_state_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.tri_state_filter.pac_id
    @pac_id.setter
    def pac_id(self, value):
        """
        Sets the pac ID
        for the tri_state_filter.
        Args:
            value (int or None): The
                pac ID to be set.
                Must be an integer or None.
        Raises:
            AttributeError: If the
                tri_state_filter is not initialized.
        """
        if not self.tri_state_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, int) or value is None, (
            "pac_id must be an integer or None")
        self.tri_state_filter.pac_id = value
    @property
    def pac_code_peek(self) -> uuid.UUID:
        """
        Returns the pac id code peek
        of the tri_state_filter.
        Raises:
            AttributeError: If the
            tri_state_filter is not initialized.
        Returns:
            uuid.UUID: The pac id code peek
            of the tri_state_filter.
        """
        if not self.tri_state_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
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
        Inserts the UTC date and time into
        the tri_state_filter object.
        Raises:
            AttributeError: If the
                tri_state_filter object is not initialized.
        Returns:
            The UTC date and time inserted into the
            tri_state_filter object.
        """
        if not self.tri_state_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.tri_state_filter.insert_utc_date_time
    @insert_utc_date_time.setter
    def insert_utc_date_time(self, value):
        """
        Inserts the UTC date and time for the
        tri_state_filter.
        Args:
            value (datetime): The UTC date and time to be inserted.
                It should be a datetime object or None.
        Raises:
            AttributeError: If the
                tri_state_filter is not initialized.
        """
        if not self.tri_state_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, datetime) or value is None, (
            "insert_utc_date_time must be a datetime object or None")
        self.tri_state_filter.insert_utc_date_time = value
    # update_utc_date_time
    @property
    def last_update_utc_date_time(self):
        """
        Returns the last update UTC date and time
        of the tri_state_filter.
        Raises:
            AttributeError: If the
                tri_state_filter is not initialized.
        Returns:
            datetime: The last update UTC date and time
                of the tri_state_filter.
        """
        if not self.tri_state_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.tri_state_filter.last_update_utc_date_time
    @last_update_utc_date_time.setter
    def last_update_utc_date_time(self, value):
        """
        Sets the last update UTC date and time
        for the tri_state_filter.
        Args:
            value (datetime): The datetime object
                representing the last update UTC date and time.
                Pass None to unset the value.
        Raises:
            AttributeError: If the
                tri_state_filter is not initialized.
        """
        if not self.tri_state_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, datetime) or value is None, (
            "last_update_utc_date_time must be a datetime object or None")
        self.tri_state_filter.last_update_utc_date_time = value
    async def load_from_json(
        self,
        json_data: str
    ):
        """
        Load tri_state_filter data
        from JSON string.
        :param json_data: JSON string containing
            tri_state_filter data.
        :raises ValueError: If json_data is not a string
            or if no tri_state_filter
            data is found.
        """
        if not isinstance(json_data, str):
            raise ValueError("json_data must be a string")
        tri_state_filter_manager = TriStateFilterManager(
            self._session_context)
        self.tri_state_filter = tri_state_filter_manager.from_json(json_data)
        return self
    async def load_from_code(
        self,
        code: uuid.UUID
    ):
        """
        Load tri_state_filter
        data from UUID code.
        :param code: UUID code for loading a specific
            tri_state_filter.
        :raises ValueError: If code is not a UUID or if no
            tri_state_filter data is found.
        """
        if not isinstance(code, uuid.UUID):
            raise ValueError("code must be a UUID")
        tri_state_filter_manager = TriStateFilterManager(
            self._session_context)
        tri_state_filter_obj = await tri_state_filter_manager.get_by_code(
            code)
        self.tri_state_filter = tri_state_filter_obj
        return self
    async def load_from_id(
        self,
        tri_state_filter_id: int
    ):
        """
        Load tri_state_filter data from
        tri_state_filter ID.
        :param tri_state_filter_id: Integer ID for loading a specific
            tri_state_filter.
        :raises ValueError: If tri_state_filter_id
            is not an integer or
            if no tri_state_filter
            data is found.
        """
        if not isinstance(tri_state_filter_id, int):
            raise ValueError("tri_state_filter_id must be an integer")
        tri_state_filter_manager = TriStateFilterManager(
            self._session_context)
        tri_state_filter_obj = await tri_state_filter_manager.get_by_id(
            tri_state_filter_id)
        self.tri_state_filter = tri_state_filter_obj
        return self
    async def load_from_obj_instance(
        self,
        tri_state_filter_obj_instance: TriStateFilter
    ):
        """
        Use the provided
        TriStateFilter instance.
        :param tri_state_filter_obj_instance: Instance of the
            TriStateFilter class.
        :raises ValueError: If tri_state_filter_obj_instance
            is not an instance of
            TriStateFilter.
        """
        if not isinstance(tri_state_filter_obj_instance,
                          TriStateFilter):
            raise ValueError("tri_state_filter_obj_instance must be an instance of TriStateFilter")
        tri_state_filter_manager = TriStateFilterManager(
            self._session_context)
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
        Load tri_state_filter data
        from dictionary.
        :param tri_state_filter_dict: Dictionary containing
            tri_state_filter data.
        :raises ValueError: If tri_state_filter_dict
            is not a
            dictionary or if no
            tri_state_filter data is found.
        """
        if not isinstance(tri_state_filter_dict, dict):
            raise ValueError("tri_state_filter_dict must be a dictionary")
        tri_state_filter_manager = TriStateFilterManager(
            self._session_context)
        self.tri_state_filter = tri_state_filter_manager.from_dict(
            tri_state_filter_dict)
        return self

    def get_session_context(self):
        """
        Returns the session context.
        :return: The session context.
        :rtype: SessionContext
        """
        return self._session_context
    async def refresh(self):
        """
        Refreshes the tri_state_filter
        object by fetching
        the latest data from the database.
        Returns:
            The updated
            tri_state_filter object.
        """
        tri_state_filter_manager = TriStateFilterManager(
            self._session_context)
        self.tri_state_filter = await tri_state_filter_manager.refresh(
            self.tri_state_filter)
        return self
    def is_valid(self):
        """
        Check if the tri_state_filter
        is valid.
        Returns:
            bool: True if the tri_state_filter
                is valid, False otherwise.
        """
        return self.tri_state_filter is not None
    def to_dict(self):
        """
        Converts the TriStateFilter
        object to a dictionary representation.
        Returns:
            dict: A dictionary representation of the
                TriStateFilter object.
        """
        tri_state_filter_manager = TriStateFilterManager(
            self._session_context)
        return tri_state_filter_manager.to_dict(
            self.tri_state_filter)
    def to_json(self):
        """
        Converts the tri_state_filter
        object to a JSON representation.
        Returns:
            str: The JSON representation of the
                tri_state_filter object.
        """
        tri_state_filter_manager = TriStateFilterManager(
            self._session_context)
        return tri_state_filter_manager.to_json(
            self.tri_state_filter)
    async def save(self):
        """
        Saves the tri_state_filter object
        to the database.
        If the tri_state_filter object
        is not initialized, an AttributeError is raised.
        If the tri_state_filter_id
        is greater than 0, the
        tri_state_filter is
        updated in the database.
        If the tri_state_filter_id is 0,
        the tri_state_filter is
        added to the database.
        Returns:
            The updated or added
            tri_state_filter object.
        Raises:
            AttributeError: If the tri_state_filter
            object is not initialized.
        """
        if not self.tri_state_filter:
            raise AttributeError(NOT_INITIALIZED_ERROR_MESSAGE)
        tri_state_filter_id = self.tri_state_filter.tri_state_filter_id
        if tri_state_filter_id > 0:
            tri_state_filter_manager = TriStateFilterManager(
                self._session_context)
            self.tri_state_filter = await tri_state_filter_manager.update(
                self.tri_state_filter)
        if tri_state_filter_id == 0:
            tri_state_filter_manager = TriStateFilterManager(
                self._session_context)
            self.tri_state_filter = await tri_state_filter_manager.add(
                self.tri_state_filter)
        return self
    async def delete(self):
        """
        Deletes the tri_state_filter
        from the database.
        Raises:
            AttributeError: If the tri_state_filter
                is not initialized.
        """
        if not self.tri_state_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if self.tri_state_filter.tri_state_filter_id > 0:
            tri_state_filter_manager = TriStateFilterManager(
                self._session_context)
            await tri_state_filter_manager.delete(
                self.tri_state_filter.tri_state_filter_id)
            self.tri_state_filter = None
    async def randomize_properties(self):
        """
        Randomizes the properties of the
        tri_state_filter object.
        This method generates random values for various
        properties of the tri_state_filter
        object
        Returns:
            self: The current instance of the
                TriStateFilter class.
        Raises:
            AttributeError: If the tri_state_filter
                object is not initialized.
        """
        if not self.tri_state_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        self.tri_state_filter.description = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        self.tri_state_filter.display_order = (
            random.randint(0, 100))
        self.tri_state_filter.is_active = (
            random.choice([True, False]))
        self.tri_state_filter.lookup_enum_name = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        self.tri_state_filter.name = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        # self.tri_state_filter.pac_id = random.randint(0, 100)
        self.tri_state_filter.state_int_value = (
            random.randint(0, 100))
# endset
        return self
    def get_tri_state_filter_obj(self) -> TriStateFilter:
        """
        Returns the tri_state_filter
        object.
        Raises:
            AttributeError: If the tri_state_filter
                object is not initialized.
        Returns:
            TriStateFilter: The tri_state_filter
                object.
        """
        if not self.tri_state_filter:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.tri_state_filter
    def is_equal(
        self,
        tri_state_filter: TriStateFilter
    ) -> bool:
        """
        Checks if the current tri_state_filter
        is equal to the given tri_state_filter.
        Args:
            tri_state_filter (TriStateFilter): The
                tri_state_filter to compare with.
        Returns:
            bool: True if the tri_state_filters
                are equal, False otherwise.
        """
        tri_state_filter_manager = TriStateFilterManager(
            self._session_context)
        my_tri_state_filter = self.get_tri_state_filter_obj()
        return tri_state_filter_manager.is_equal(
            tri_state_filter, my_tri_state_filter)
# endset
    # description,
    # displayOrder,
    # isActive,
    # lookupEnumName,
    # name,
    # PacID
    async def get_pac_id_rel_obj(self) -> models.Pac:
        """
        Retrieves the related Pac object based
        on the pac_id.
        Returns:
            An instance of the Pac model
            representing the related pac.
        """
        pac_manager = managers_and_enums.PacManager(self._session_context)
        pac_obj = await pac_manager.get_by_id(self.pac_id)
        return pac_obj
    # stateIntValue,
# endset
    def get_obj(self) -> TriStateFilter:
        """
        Returns the TriStateFilter object.
        :return: The TriStateFilter object.
        :rtype: TriStateFilter
        """
        return self.tri_state_filter
    def get_object_name(self) -> str:
        """
        Returns the name of the object.
        :return: The name of the object.
        :rtype: str
        """
        return "tri_state_filter"
    def get_id(self) -> int:
        """
        Returns the ID of the tri_state_filter.
        :return: The ID of the tri_state_filter.
        :rtype: int
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
        Get the name of the parent tri_state_filter.
        Returns:
            str: The name of the parent tri_state_filter.
        """
        return 'Pac'
    async def get_parent_code(self) -> uuid.UUID:
        """
        Get the parent code of the tri_state_filter.
        Returns:
            The parent code of the tri_state_filter
            as a UUID.
        """
        return self.pac_code_peek
    async def get_parent_obj(self) -> models.Pac:
        """
        Get the parent object of the current
        tri_state_filter.
        Returns:
            The parent object of the current
            tri_state_filter,
            which is an instance of the
            Pac model.
        """
        pac = await self.get_pac_id_rel_obj()
        return pac
    # stateIntValue,
# endset
