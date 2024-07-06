# business/dyna_flow_task_type_base.py  # pylint: disable=duplicate-code
# pylint: disable=unused-import

"""
This module contains the
DynaFlowTaskTypeBaseBusObj class,
which represents the base
business object for a
DynaFlowTaskType.
"""

from decimal import Decimal  # noqa: F401
import random
from typing import Optional
import uuid  # noqa: F401
from datetime import datetime, date  # noqa: F401
from helpers.session_context import SessionContext
from managers import DynaFlowTaskTypeManager
from models import DynaFlowTaskType
import models
import managers as managers_and_enums
from .base_bus_obj import BaseBusObj

NOT_INITIALIZED_ERROR_MESSAGE = (
    "DynaFlowTaskType object is not initialized")


class DynaFlowTaskTypeInvalidInitError(Exception):
    """
    Exception raised when the
    DynaFlowTaskType object
    is not initialized properly.
    """


class DynaFlowTaskTypeBaseBusObj(BaseBusObj):
    """
    This class represents the base business object
    for a DynaFlowTaskType.
    It requires a valid session context for initialization.
    """

    def __init__(
        self,
        session_context: SessionContext,
        dyna_flow_task_type: Optional[DynaFlowTaskType] = None
    ):
        """
        Initializes a new instance of the
        DynaFlowTaskTypeBusObj class.

        :param session_context: The session context.
        :raises ValueError: If the session is not provided.
        """

        if not session_context.session:
            raise ValueError("session required")

        if dyna_flow_task_type is None:
            dyna_flow_task_type = DynaFlowTaskType()

        self._session_context = session_context

        self.dyna_flow_task_type = dyna_flow_task_type

    @property
    def dyna_flow_task_type_id(self) -> int:
        """
        Get the dyna_flow_task_type ID from the
        DynaFlowTaskType object.

        :return: The dyna_flow_task_type ID.
        :raises AttributeError: If the
            DynaFlowTaskType object is not initialized.
        """

        if not self.dyna_flow_task_type:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow_task_type.dyna_flow_task_type_id
    # code

    @property
    def code(self):
        """
        Get the code from the
        DynaFlowTaskType object.

        :return: The code.
        :raises AttributeError: If the
            DynaFlowTaskType object is not initialized.
        """

        if not self.dyna_flow_task_type:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow_task_type.code

    @code.setter
    def code(self, value: uuid.UUID):  # type: ignore
        """
        Set the code for the DynaFlowTaskType object.

        :param value: The code value.
        :raises AttributeError: If the
            DynaFlowTaskType object is not initialized.
        :raises ValueError: If the code is not a UUID.
        """

        if not self.dyna_flow_task_type:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, uuid.UUID):
            raise ValueError("code must be a UUID.")

        self.dyna_flow_task_type.code = value
    # last_change_code

    @property
    def last_change_code(self):
        """
        Get the last change code from the
        DynaFlowTaskType object.

        :return: The last change code.
        :raises AttributeError: If the
            DynaFlowTaskType object is not initialized.
        """

        if not self.dyna_flow_task_type:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow_task_type.last_change_code

    @last_change_code.setter
    def last_change_code(self, value: int):
        """
        Set the last change code for the
        DynaFlowTaskType object.

        :param value: The last change code value.
        :raises AttributeError: If the
            DynaFlowTaskType object is not initialized.
        :raises ValueError: If the last change code is not an integer.
        """

        if not self.dyna_flow_task_type:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, int):
            raise ValueError("last_change_code must be an integer.")

        self.dyna_flow_task_type.last_change_code = value
    # insert_user_id

    @property
    def insert_user_id(self):
        """
        Get the insert user ID from the
        DynaFlowTaskType object.

        :return: The insert user ID.
        :raises AttributeError: If the
            DynaFlowTaskType object is not initialized.
        """

        if not self.dyna_flow_task_type:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow_task_type.insert_user_id

    @insert_user_id.setter
    def insert_user_id(self, value: uuid.UUID):
        """
        Set the insert user ID for the
        DynaFlowTaskType object.

        :param value: The insert user ID value.
        :raises AttributeError: If the
            DynaFlowTaskType object is not initialized.
        :raises ValueError: If the insert user ID is not a UUID.
        """

        if not self.dyna_flow_task_type:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, uuid.UUID):
            raise ValueError(
                "insert_user_id must be a UUID.")

        self.dyna_flow_task_type.insert_user_id = value
    # last_update_user_id

    @property
    def last_update_user_id(self):
        """
        Get the last update user ID from the
        DynaFlowTaskType object.

        :return: The last update user ID.
        :raises AttributeError: If the
            DynaFlowTaskType object is not initialized.
        """

        if not self.dyna_flow_task_type:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow_task_type.last_update_user_id

    @last_update_user_id.setter
    def last_update_user_id(self, value: uuid.UUID):
        """
        Set the last update user ID for the
        DynaFlowTaskType object.

        :param value: The last update user ID value.
        :raises AttributeError: If the
            DynaFlowTaskType object is not initialized.
        :raises ValueError: If the last update user ID is not a UUID.
        """

        if not self.dyna_flow_task_type:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, uuid.UUID):
            raise ValueError(
                "last_update_user_id must be a UUID.")

        self.dyna_flow_task_type.last_update_user_id = value

    # description

    @property
    def description(self):
        """
        Get the Description from the
        DynaFlowTaskType object.

        :return: The Description.
        :raises AttributeError: If the
            DynaFlowTaskType object is not initialized.
        """

        if not self.dyna_flow_task_type:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if self.dyna_flow_task_type.description is None:
            return ""

        return self.dyna_flow_task_type.description

    @description.setter
    def description(self, value):
        """
        Set the Description for the
        DynaFlowTaskType object.

        :param value: The Description value.
        :raises AttributeError: If the
            DynaFlowTaskType object is not initialized.
        :raises AssertionError: If the Description is not a string.
        """

        if not self.dyna_flow_task_type:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, str), "description must be a string"
        self.dyna_flow_task_type.description = value
    # displayOrder

    @property
    def display_order(self):
        """
        Returns the value of
        display_order attribute of the
        dyna_flow_task_type.

        Raises:
            AttributeError: If the
                dyna_flow_task_type is not initialized.

        Returns:
            int: The value of
                display_order attribute.
        """
        if not self.dyna_flow_task_type:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow_task_type.display_order

    @display_order.setter
    def display_order(self, value):
        """
        Sets the value of
        display_order for the
        dyna_flow_task_type.

        Args:
            value (int): The integer value to set for
                display_order.

        Raises:
            AttributeError: If the
                dyna_flow_task_type is not initialized.

        """
        if not self.dyna_flow_task_type:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, int), (
            "display_order must be an integer")
        self.dyna_flow_task_type.display_order = value
    # isActive

    @property
    def is_active(self):
        """
        Get the Is Active flag from the
        DynaFlowTaskType object.

        :return: The Is Active flag.
        :raises AttributeError: If the
            DynaFlowTaskType object is not initialized.
        """

        if not self.dyna_flow_task_type:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow_task_type.is_active

    @is_active.setter
    def is_active(self, value: bool):
        """
        Set the Is Active flag for the
        DynaFlowTaskType object.

        :param value: The Is Active flag value.
        :raises AttributeError: If the
            DynaFlowTaskType object is not initialized.
        :raises ValueError: If the Is Active flag is not a boolean.
        """

        if not self.dyna_flow_task_type:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, bool):
            raise ValueError(
                "is_active must be a boolean.")

        self.dyna_flow_task_type.is_active = value
    # lookupEnumName

    @property
    def lookup_enum_name(self):
        """
        Get the Lookup Enum Name from the
        DynaFlowTaskType object.

        :return: The Lookup Enum Name.
        :raises AttributeError: If the
            DynaFlowTaskType object is not initialized.
        """

        if not self.dyna_flow_task_type:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if self.dyna_flow_task_type.lookup_enum_name is None:
            return ""

        return self.dyna_flow_task_type.lookup_enum_name

    @lookup_enum_name.setter
    def lookup_enum_name(self, value):
        """
        Set the Lookup Enum Name for the
        DynaFlowTaskType object.

        :param value: The Lookup Enum Name value.
        :raises AttributeError: If the
            DynaFlowTaskType object is not initialized.
        :raises AssertionError: If the Lookup Enum Name is not a string.
        """

        if not self.dyna_flow_task_type:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, str), "lookup_enum_name must be a string"
        self.dyna_flow_task_type.lookup_enum_name = value
    # maxRetryCount

    @property
    def max_retry_count(self):
        """
        Returns the value of
        max_retry_count attribute of the
        dyna_flow_task_type.

        Raises:
            AttributeError: If the
                dyna_flow_task_type is not initialized.

        Returns:
            int: The value of
                max_retry_count attribute.
        """
        if not self.dyna_flow_task_type:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow_task_type.max_retry_count

    @max_retry_count.setter
    def max_retry_count(self, value):
        """
        Sets the value of
        max_retry_count for the
        dyna_flow_task_type.

        Args:
            value (int): The integer value to set for
                max_retry_count.

        Raises:
            AttributeError: If the
                dyna_flow_task_type is not initialized.

        """
        if not self.dyna_flow_task_type:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, int), (
            "max_retry_count must be an integer")
        self.dyna_flow_task_type.max_retry_count = value
    # name

    @property
    def name(self):
        """
        Get the Name from the
        DynaFlowTaskType object.

        :return: The Name.
        :raises AttributeError: If the
            DynaFlowTaskType object is not initialized.
        """

        if not self.dyna_flow_task_type:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if self.dyna_flow_task_type.name is None:
            return ""

        return self.dyna_flow_task_type.name

    @name.setter
    def name(self, value):
        """
        Set the Name for the
        DynaFlowTaskType object.

        :param value: The Name value.
        :raises AttributeError: If the
            DynaFlowTaskType object is not initialized.
        :raises AssertionError: If the Name is not a string.
        """

        if not self.dyna_flow_task_type:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, str), "name must be a string"
        self.dyna_flow_task_type.name = value
    # PacID
    # description,
    # displayOrder,
    # isActive,
    # lookupEnumName,
    # maxRetryCount,
    # name,
    # PacID

    @property
    def pac_id(self):
        """
        Returns the pac ID
        associated with the
        dyna_flow_task_type.

        Raises:
            AttributeError: If the
                dyna_flow_task_type is not initialized.

        Returns:
            int: The pac ID of the dyna_flow_task_type.
        """
        if not self.dyna_flow_task_type:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow_task_type.pac_id

    @pac_id.setter
    def pac_id(self, value):
        """
        Sets the pac ID
        for the dyna_flow_task_type.

        Args:
            value (int or None): The
                pac ID to be set.
                Must be an integer or None.

        Raises:
            AttributeError: If the
                dyna_flow_task_type is not initialized.

        """
        if not self.dyna_flow_task_type:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, int) or value is None, (
            "pac_id must be an integer or None")

        self.dyna_flow_task_type.pac_id = value

    @property
    def pac_code_peek(self) -> uuid.UUID:
        """
        Returns the pac id code peek
        of the dyna_flow_task_type.

        Raises:
            AttributeError: If the
            dyna_flow_task_type is not initialized.

        Returns:
            uuid.UUID: The pac id code peek
            of the dyna_flow_task_type.
        """
        if not self.dyna_flow_task_type:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow_task_type.pac_code_peek
    # insert_utc_date_time

    @property
    def insert_utc_date_time(self):
        """
        Inserts the UTC date and time into
        the dyna_flow_task_type object.

        Raises:
            AttributeError: If the
                dyna_flow_task_type object is not initialized.

        Returns:
            The UTC date and time inserted into the
            dyna_flow_task_type object.
        """
        if not self.dyna_flow_task_type:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow_task_type.insert_utc_date_time

    @insert_utc_date_time.setter
    def insert_utc_date_time(self, value):
        """
        Inserts the UTC date and time for the
        dyna_flow_task_type.

        Args:
            value (datetime): The UTC date and time to be inserted.
                It should be a datetime object or None.

        Raises:
            AttributeError: If the
                dyna_flow_task_type is not initialized.

        """
        if not self.dyna_flow_task_type:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, datetime) or value is None, (
            "insert_utc_date_time must be "
            "a datetime object or None")

        self.dyna_flow_task_type.insert_utc_date_time = value

    # update_utc_date_time
    @property
    def last_update_utc_date_time(self):
        """
        Returns the last update UTC date and time
        of the dyna_flow_task_type.

        Raises:
            AttributeError: If the
                dyna_flow_task_type is not initialized.

        Returns:
            datetime: The last update UTC date and time
                of the dyna_flow_task_type.
        """
        if not self.dyna_flow_task_type:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow_task_type.last_update_utc_date_time

    @last_update_utc_date_time.setter
    def last_update_utc_date_time(self, value):
        """
        Sets the last update UTC date and time
        for the dyna_flow_task_type.

        Args:
            value (datetime): The datetime object
                representing the last update UTC date and time.
                Pass None to unset the value.

        Raises:
            AttributeError: If the
                dyna_flow_task_type is not initialized.

        """
        if not self.dyna_flow_task_type:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, datetime) or value is None, (
            "last_update_utc_date_time "
            "must be a datetime object or None")

        self.dyna_flow_task_type.last_update_utc_date_time = value

    async def load_from_json(
        self,
        json_data: str
    ):
        """
        Load dyna_flow_task_type data
        from JSON string.

        :param json_data: JSON string containing
            dyna_flow_task_type data.
        :raises ValueError: If json_data is not a string
            or if no dyna_flow_task_type
            data is found.
        """

        if not isinstance(json_data, str):
            raise ValueError(
                "json_data must be a string")

        dyna_flow_task_type_manager = DynaFlowTaskTypeManager(
            self._session_context)
        self.dyna_flow_task_type = await \
            dyna_flow_task_type_manager.from_json(json_data)

        return self

    async def load_from_code(
        self,
        code: uuid.UUID
    ):
        """
        Load dyna_flow_task_type
        data from UUID code.

        :param code: UUID code for loading a specific
            dyna_flow_task_type.
        :raises ValueError: If code is not a UUID or if no
            dyna_flow_task_type data is found.
        """
        if not isinstance(code, uuid.UUID):
            raise ValueError(
                "code must be a UUID")

        dyna_flow_task_type_manager = DynaFlowTaskTypeManager(
            self._session_context)
        dyna_flow_task_type_obj = await dyna_flow_task_type_manager.get_by_code(
            code)
        self.dyna_flow_task_type = dyna_flow_task_type_obj

        return self

    async def load_from_id(
        self,
        dyna_flow_task_type_id: int
    ):
        """
        Load dyna_flow_task_type data from
        dyna_flow_task_type ID.

        :param dyna_flow_task_type_id: Integer ID for loading a specific
            dyna_flow_task_type.
        :raises ValueError: If dyna_flow_task_type_id
            is not an integer or
            if no dyna_flow_task_type
            data is found.
        """

        if not isinstance(dyna_flow_task_type_id, int):
            raise ValueError(
                "dyna_flow_task_type_id must be an integer")

        dyna_flow_task_type_manager = DynaFlowTaskTypeManager(
            self._session_context)
        dyna_flow_task_type_obj = await dyna_flow_task_type_manager.get_by_id(
            dyna_flow_task_type_id)
        self.dyna_flow_task_type = dyna_flow_task_type_obj

        return self

    def load_from_obj_instance(
        self,
        dyna_flow_task_type_obj_instance: DynaFlowTaskType
    ):
        """
        Use the provided
        DynaFlowTaskType instance.

        :param dyna_flow_task_type_obj_instance: Instance of the
            DynaFlowTaskType class.
        :raises ValueError: If dyna_flow_task_type_obj_instance
            is not an instance of
            DynaFlowTaskType.
        """

        if not isinstance(dyna_flow_task_type_obj_instance,
                          DynaFlowTaskType):
            raise ValueError(
                "dyna_flow_task_type_obj_instance must be an "
                "instance of DynaFlowTaskType")

        self.dyna_flow_task_type = dyna_flow_task_type_obj_instance

        return self

    async def load_from_dict(
        self,
        dyna_flow_task_type_dict: dict
    ):
        """
        Load dyna_flow_task_type data
        from dictionary.

        :param dyna_flow_task_type_dict: Dictionary containing
            dyna_flow_task_type data.
        :raises ValueError: If dyna_flow_task_type_dict
            is not a
            dictionary or if no
            dyna_flow_task_type data is found.
        """
        if not isinstance(dyna_flow_task_type_dict, dict):
            raise ValueError(
                "dyna_flow_task_type_dict must be a dictionary")

        dyna_flow_task_type_manager = DynaFlowTaskTypeManager(
            self._session_context)

        self.dyna_flow_task_type = await \
            dyna_flow_task_type_manager.from_dict(
                dyna_flow_task_type_dict)

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
        Refreshes the dyna_flow_task_type
        object by fetching
        the latest data from the database.

        Returns:
            The updated
            dyna_flow_task_type object.
        """
        dyna_flow_task_type_manager = DynaFlowTaskTypeManager(
            self._session_context)
        self.dyna_flow_task_type = await \
            dyna_flow_task_type_manager.refresh(
                self.dyna_flow_task_type)

        return self

    def is_valid(self):
        """
        Check if the dyna_flow_task_type
        is valid.

        Returns:
            bool: True if the dyna_flow_task_type
                is valid, False otherwise.
        """
        return self.dyna_flow_task_type is not None

    def to_dict(self):
        """
        Converts the DynaFlowTaskType
        object to a dictionary representation.

        Returns:
            dict: A dictionary representation of the
                DynaFlowTaskType object.
        """
        dyna_flow_task_type_manager = DynaFlowTaskTypeManager(
            self._session_context)
        return dyna_flow_task_type_manager.to_dict(
            self.dyna_flow_task_type)

    def to_json(self):
        """
        Converts the dyna_flow_task_type
        object to a JSON representation.

        Returns:
            str: The JSON representation of the
                dyna_flow_task_type object.
        """
        dyna_flow_task_type_manager = DynaFlowTaskTypeManager(
            self._session_context)
        return dyna_flow_task_type_manager.to_json(
            self.dyna_flow_task_type)

    async def save(self):
        """
        Saves the dyna_flow_task_type object
        to the database.

        If the dyna_flow_task_type object
        is not initialized, an AttributeError is raised.
        If the dyna_flow_task_type_id
        is greater than 0, the
        dyna_flow_task_type is
        updated in the database.
        If the dyna_flow_task_type_id is 0,
        the dyna_flow_task_type is
        added to the database.

        Returns:
            The updated or added
            dyna_flow_task_type object.

        Raises:
            AttributeError: If the dyna_flow_task_type
            object is not initialized.
        """
        if not self.dyna_flow_task_type:
            raise AttributeError(NOT_INITIALIZED_ERROR_MESSAGE)

        dyna_flow_task_type_id = self.dyna_flow_task_type.dyna_flow_task_type_id

        if dyna_flow_task_type_id > 0:
            dyna_flow_task_type_manager = DynaFlowTaskTypeManager(
                self._session_context)
            self.dyna_flow_task_type = await \
                dyna_flow_task_type_manager.update(
                    self.dyna_flow_task_type)

        if dyna_flow_task_type_id == 0:
            dyna_flow_task_type_manager = DynaFlowTaskTypeManager(
                self._session_context)
            self.dyna_flow_task_type = await \
                dyna_flow_task_type_manager.add(
                    self.dyna_flow_task_type)

        return self

    async def delete(self):
        """
        Deletes the dyna_flow_task_type
        from the database.

        Raises:
            AttributeError: If the dyna_flow_task_type
                is not initialized.
        """
        if not self.dyna_flow_task_type:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if self.dyna_flow_task_type.dyna_flow_task_type_id > 0:
            dyna_flow_task_type_manager = DynaFlowTaskTypeManager(
                self._session_context)
            await dyna_flow_task_type_manager.delete(
                self.dyna_flow_task_type.dyna_flow_task_type_id)
            self.dyna_flow_task_type = None

    async def randomize_properties(self):
        """
        Randomizes the properties of the
        dyna_flow_task_type object.

        This method generates random values for various
        properties of the dyna_flow_task_type
        object

        Returns:
            self: The current instance of the
                DynaFlowTaskType class.

        Raises:
            AttributeError: If the dyna_flow_task_type
                object is not initialized.
        """
        if not self.dyna_flow_task_type:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        self.dyna_flow_task_type.description = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        self.dyna_flow_task_type.display_order = (
            random.randint(0, 100))
        self.dyna_flow_task_type.is_active = (
            random.choice([True, False]))
        self.dyna_flow_task_type.lookup_enum_name = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        self.dyna_flow_task_type.max_retry_count = (
            random.randint(0, 100))
        self.dyna_flow_task_type.name = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        # self.dyna_flow_task_type.pac_id = random.randint(0, 100)

        return self

    def get_dyna_flow_task_type_obj(self) -> DynaFlowTaskType:
        """
        Returns the dyna_flow_task_type
        object.

        Raises:
            AttributeError: If the dyna_flow_task_type
                object is not initialized.

        Returns:
            DynaFlowTaskType: The dyna_flow_task_type
                object.
        """
        if not self.dyna_flow_task_type:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dyna_flow_task_type

    def is_equal(
        self,
        dyna_flow_task_type: DynaFlowTaskType
    ) -> bool:
        """
        Checks if the current dyna_flow_task_type
        is equal to the given dyna_flow_task_type.

        Args:
            dyna_flow_task_type (DynaFlowTaskType): The
                dyna_flow_task_type to compare with.

        Returns:
            bool: True if the dyna_flow_task_types
                are equal, False otherwise.
        """
        dyna_flow_task_type_manager = DynaFlowTaskTypeManager(
            self._session_context)
        my_dyna_flow_task_type = self.get_dyna_flow_task_type_obj()
        return dyna_flow_task_type_manager.is_equal(
            dyna_flow_task_type, my_dyna_flow_task_type)

    def get_obj(self) -> DynaFlowTaskType:
        """
        Returns the DynaFlowTaskType object.

        :return: The DynaFlowTaskType object.
        :rtype: DynaFlowTaskType
        """

        return self.dyna_flow_task_type

    def get_object_name(self) -> str:
        """
        Returns the name of the object.

        :return: The name of the object.
        :rtype: str
        """
        return "dyna_flow_task_type"

    def get_id(self) -> int:
        """
        Returns the ID of the dyna_flow_task_type.

        :return: The ID of the dyna_flow_task_type.
        :rtype: int
        """
        return self.dyna_flow_task_type_id
    # description,
    # displayOrder,
    # isActive,
    # lookupEnumName,
    # maxRetryCount,
    # name,
    # PacID

    async def get_parent_name(self) -> str:
        """
        Get the name of the parent dyna_flow_task_type.

        Returns:
            str: The name of the parent dyna_flow_task_type.
        """
        return 'Pac'

    async def get_parent_code(self) -> uuid.UUID:
        """
        Get the parent code of the dyna_flow_task_type.

        Returns:
            The parent code of the dyna_flow_task_type
            as a UUID.
        """
        return self.pac_code_peek

    async def get_parent_obj(self) -> models.Pac:
        """
        Get the parent object of the current
        dyna_flow_task_type.

        Returns:
            The parent object of the current
            dyna_flow_task_type,
            which is an instance of the
            Pac model.
        """
        pac_manager = managers_and_enums.PacManager(
            self._session_context)
        pac_obj = await pac_manager.get_by_id(
            self.pac_id)
        return pac_obj
