# business/land_base.py
# pylint: disable=unused-import

"""
This module contains the
LandBaseBusObj class,
which represents the base
business object for a
Land.
"""

from decimal import Decimal  # noqa: F401
import random
from typing import Optional
import uuid  # noqa: F401
from datetime import datetime, date  # noqa: F401
from helpers.session_context import SessionContext
from managers import LandManager
from models import Land
import models
import managers as managers_and_enums
from .base_bus_obj import BaseBusObj

NOT_INITIALIZED_ERROR_MESSAGE = (
    "Land object is not initialized")


class LandInvalidInitError(Exception):
    """
    Exception raised when the
    Land object
    is not initialized properly.
    """


class LandBaseBusObj(BaseBusObj):
    """
    This class represents the base business object
    for a Land.
    It requires a valid session context for initialization.
    """

    def __init__(
        self,
        session_context: SessionContext,
        land: Optional[Land] = None
    ):
        """
        Initializes a new instance of the
        LandBusObj class.

        :param session_context: The session context.
        :raises ValueError: If the session is not provided.
        """

        if not session_context.session:
            raise ValueError("session required")

        if land is None:
            land = Land()

        self._session_context = session_context

        self.land = land

    @property
    def land_id(self) -> int:
        """
        Get the land ID from the
        Land object.

        :return: The land ID.
        :raises AttributeError: If the
            Land object is not initialized.
        """

        if not self.land:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.land.land_id
    # code

    @property
    def code(self):
        """
        Get the code from the
        Land object.

        :return: The code.
        :raises AttributeError: If the
            Land object is not initialized.
        """

        if not self.land:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.land.code

    @code.setter
    def code(self, value: uuid.UUID):  # type: ignore
        """
        Set the code for the Land object.

        :param value: The code value.
        :raises AttributeError: If the
            Land object is not initialized.
        :raises ValueError: If the code is not a UUID.
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
        Get the last change code from the
        Land object.

        :return: The last change code.
        :raises AttributeError: If the
            Land object is not initialized.
        """

        if not self.land:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.land.last_change_code

    @last_change_code.setter
    def last_change_code(self, value: int):
        """
        Set the last change code for the
        Land object.

        :param value: The last change code value.
        :raises AttributeError: If the
            Land object is not initialized.
        :raises ValueError: If the last change code is not an integer.
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
        Get the insert user ID from the
        Land object.

        :return: The insert user ID.
        :raises AttributeError: If the
            Land object is not initialized.
        """

        if not self.land:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.land.insert_user_id

    @insert_user_id.setter
    def insert_user_id(self, value: uuid.UUID):
        """
        Set the insert user ID for the
        Land object.

        :param value: The insert user ID value.
        :raises AttributeError: If the
            Land object is not initialized.
        :raises ValueError: If the insert user ID is not a UUID.
        """

        if not self.land:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, uuid.UUID):
            raise ValueError(
                "insert_user_id must be a UUID.")

        self.land.insert_user_id = value
    # last_update_user_id

    @property
    def last_update_user_id(self):
        """
        Get the last update user ID from the
        Land object.

        :return: The last update user ID.
        :raises AttributeError: If the
            Land object is not initialized.
        """

        if not self.land:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.land.last_update_user_id

    @last_update_user_id.setter
    def last_update_user_id(self, value: uuid.UUID):
        """
        Set the last update user ID for the
        Land object.

        :param value: The last update user ID value.
        :raises AttributeError: If the
            Land object is not initialized.
        :raises ValueError: If the last update user ID is not a UUID.
        """

        if not self.land:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, uuid.UUID):
            raise ValueError(
                "last_update_user_id must be a UUID.")

        self.land.last_update_user_id = value

    # description

    @property
    def description(self):
        """
        Get the Description from the
        Land object.

        :return: The Description.
        :raises AttributeError: If the
            Land object is not initialized.
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
        Set the Description for the
        Land object.

        :param value: The Description value.
        :raises AttributeError: If the
            Land object is not initialized.
        :raises AssertionError: If the Description is not a string.
        """

        if not self.land:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, str), "description must be a string"
        self.land.description = value
    # displayOrder

    @property
    def display_order(self):
        """
        Returns the value of
        display_order attribute of the
        land.

        Raises:
            AttributeError: If the
                land is not initialized.

        Returns:
            int: The value of
                display_order attribute.
        """
        if not self.land:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.land.display_order

    @display_order.setter
    def display_order(self, value):
        """
        Sets the value of
        display_order for the
        land.

        Args:
            value (int): The integer value to set for
                display_order.

        Raises:
            AttributeError: If the
                land is not initialized.

        """
        if not self.land:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, int), (
            "display_order must be an integer")
        self.land.display_order = value
    # isActive

    @property
    def is_active(self):
        """
        Get the Is Active flag from the
        Land object.

        :return: The Is Active flag.
        :raises AttributeError: If the
            Land object is not initialized.
        """

        if not self.land:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.land.is_active

    @is_active.setter
    def is_active(self, value: bool):
        """
        Set the Is Active flag for the
        Land object.

        :param value: The Is Active flag value.
        :raises AttributeError: If the
            Land object is not initialized.
        :raises ValueError: If the Is Active flag is not a boolean.
        """

        if not self.land:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, bool):
            raise ValueError(
                "is_active must be a boolean.")

        self.land.is_active = value
    # lookupEnumName

    @property
    def lookup_enum_name(self):
        """
        Get the Lookup Enum Name from the
        Land object.

        :return: The Lookup Enum Name.
        :raises AttributeError: If the
            Land object is not initialized.
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
        Set the Lookup Enum Name for the
        Land object.

        :param value: The Lookup Enum Name value.
        :raises AttributeError: If the
            Land object is not initialized.
        :raises AssertionError: If the Lookup Enum Name is not a string.
        """

        if not self.land:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, str), "lookup_enum_name must be a string"
        self.land.lookup_enum_name = value
    # name

    @property
    def name(self):
        """
        Get the Name from the
        Land object.

        :return: The Name.
        :raises AttributeError: If the
            Land object is not initialized.
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
        Set the Name for the
        Land object.

        :param value: The Name value.
        :raises AttributeError: If the
            Land object is not initialized.
        :raises AssertionError: If the Name is not a string.
        """

        if not self.land:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, str), "name must be a string"
        self.land.name = value
    # PacID
    # isDeleteAllowed,
    # isEditAllowed,
    # otherFlavor,
    # someBigIntVal,
    # someBitVal,
    # someDecimalVal,
    # someEmailAddress,
    # someFloatVal,
    # someIntVal,
    # someMoneyVal,
    # someNVarCharVal,
    # someDateVal
    # someUTCDateTimeVal
    # PacID
    @property
    def pac_id(self):
        """
        Returns the pac ID
        associated with the
        land.

        Raises:
            AttributeError: If the
                land is not initialized.

        Returns:
            int: The pac ID of the land.
        """
        if not self.land:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.land.pac_id

    @pac_id.setter
    def pac_id(self, value):
        """
        Sets the pac ID
        for the land.

        Args:
            value (int or None): The
                pac ID to be set.
                Must be an integer or None.

        Raises:
            AttributeError: If the
                land is not initialized.

        """
        if not self.land:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, int) or value is None, (
            "pac_id must be an integer or None")

        self.land.pac_id = value

    @property
    def pac_code_peek(self) -> uuid.UUID:
        """
        Returns the pac id code peek
        of the land.

        Raises:
            AttributeError: If the
            land is not initialized.

        Returns:
            uuid.UUID: The pac id code peek
            of the land.
        """
        if not self.land:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.land.pac_code_peek
    # insert_utc_date_time

    @property
    def insert_utc_date_time(self):
        """
        Inserts the UTC date and time into
        the land object.

        Raises:
            AttributeError: If the
                land object is not initialized.

        Returns:
            The UTC date and time inserted into the
            land object.
        """
        if not self.land:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.land.insert_utc_date_time

    @insert_utc_date_time.setter
    def insert_utc_date_time(self, value):
        """
        Inserts the UTC date and time for the
        land.

        Args:
            value (datetime): The UTC date and time to be inserted.
                It should be a datetime object or None.

        Raises:
            AttributeError: If the
                land is not initialized.

        """
        if not self.land:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, datetime) or value is None, (
            "insert_utc_date_time must be "
            "a datetime object or None")

        self.land.insert_utc_date_time = value

    # update_utc_date_time
    @property
    def last_update_utc_date_time(self):
        """
        Returns the last update UTC date and time
        of the land.

        Raises:
            AttributeError: If the
                land is not initialized.

        Returns:
            datetime: The last update UTC date and time
                of the land.
        """
        if not self.land:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.land.last_update_utc_date_time

    @last_update_utc_date_time.setter
    def last_update_utc_date_time(self, value):
        """
        Sets the last update UTC date and time
        for the land.

        Args:
            value (datetime): The datetime object
                representing the last update UTC date and time.
                Pass None to unset the value.

        Raises:
            AttributeError: If the
                land is not initialized.

        """
        if not self.land:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, datetime) or value is None, (
            "last_update_utc_date_time "
            "must be a datetime object or None")

        self.land.last_update_utc_date_time = value

    async def load_from_json(
        self,
        json_data: str
    ):
        """
        Load land data
        from JSON string.

        :param json_data: JSON string containing
            land data.
        :raises ValueError: If json_data is not a string
            or if no land
            data is found.
        """

        if not isinstance(json_data, str):
            raise ValueError(
                "json_data must be a string")

        land_manager = LandManager(
            self._session_context)
        self.land = await \
            land_manager.from_json(json_data)

        return self

    async def load_from_code(
        self,
        code: uuid.UUID
    ):
        """
        Load land
        data from UUID code.

        :param code: UUID code for loading a specific
            land.
        :raises ValueError: If code is not a UUID or if no
            land data is found.
        """
        if not isinstance(code, uuid.UUID):
            raise ValueError(
                "code must be a UUID")

        land_manager = LandManager(
            self._session_context)
        land_obj = await land_manager.get_by_code(
            code)
        self.land = land_obj

        return self

    async def load_from_id(
        self,
        land_id: int
    ):
        """
        Load land data from
        land ID.

        :param land_id: Integer ID for loading a specific
            land.
        :raises ValueError: If land_id
            is not an integer or
            if no land
            data is found.
        """

        if not isinstance(land_id, int):
            raise ValueError(
                "land_id must be an integer")

        land_manager = LandManager(
            self._session_context)
        land_obj = await land_manager.get_by_id(
            land_id)
        self.land = land_obj

        return self

    def load_from_obj_instance(
        self,
        land_obj_instance: Land
    ):
        """
        Use the provided
        Land instance.

        :param land_obj_instance: Instance of the
            Land class.
        :raises ValueError: If land_obj_instance
            is not an instance of
            Land.
        """

        if not isinstance(land_obj_instance,
                          Land):
            raise ValueError(
                "land_obj_instance must be an "
                "instance of Land")

        self.land = land_obj_instance

        return self

    async def load_from_dict(
        self,
        land_dict: dict
    ):
        """
        Load land data
        from dictionary.

        :param land_dict: Dictionary containing
            land data.
        :raises ValueError: If land_dict
            is not a
            dictionary or if no
            land data is found.
        """
        if not isinstance(land_dict, dict):
            raise ValueError(
                "land_dict must be a dictionary")

        land_manager = LandManager(
            self._session_context)

        self.land = await \
            land_manager.from_dict(
                land_dict)

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
        Refreshes the land
        object by fetching
        the latest data from the database.

        Returns:
            The updated
            land object.
        """
        land_manager = LandManager(
            self._session_context)
        self.land = await \
            land_manager.refresh(
                self.land)

        return self

    def is_valid(self):
        """
        Check if the land
        is valid.

        Returns:
            bool: True if the land
                is valid, False otherwise.
        """
        return self.land is not None

    def to_dict(self):
        """
        Converts the Land
        object to a dictionary representation.

        Returns:
            dict: A dictionary representation of the
                Land object.
        """
        land_manager = LandManager(
            self._session_context)
        return land_manager.to_dict(
            self.land)

    def to_json(self):
        """
        Converts the land
        object to a JSON representation.

        Returns:
            str: The JSON representation of the
                land object.
        """
        land_manager = LandManager(
            self._session_context)
        return land_manager.to_json(
            self.land)

    async def save(self):
        """
        Saves the land object
        to the database.

        If the land object
        is not initialized, an AttributeError is raised.
        If the land_id
        is greater than 0, the
        land is
        updated in the database.
        If the land_id is 0,
        the land is
        added to the database.

        Returns:
            The updated or added
            land object.

        Raises:
            AttributeError: If the land
            object is not initialized.
        """
        if not self.land:
            raise AttributeError(NOT_INITIALIZED_ERROR_MESSAGE)

        land_id = self.land.land_id

        if land_id > 0:
            land_manager = LandManager(
                self._session_context)
            self.land = await \
                land_manager.update(
                    self.land)

        if land_id == 0:
            land_manager = LandManager(
                self._session_context)
            self.land = await \
                land_manager.add(
                    self.land)

        return self

    async def delete(self):
        """
        Deletes the land
        from the database.

        Raises:
            AttributeError: If the land
                is not initialized.
        """
        if not self.land:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if self.land.land_id > 0:
            land_manager = LandManager(
                self._session_context)
            await land_manager.delete(
                self.land.land_id)
            self.land = None

    async def randomize_properties(self):
        """
        Randomizes the properties of the
        land object.

        This method generates random values for various
        properties of the land
        object

        Returns:
            self: The current instance of the
                Land class.

        Raises:
            AttributeError: If the land
                object is not initialized.
        """
        if not self.land:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        self.land.description = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        self.land.display_order = (
            random.randint(0, 100))
        self.land.is_active = (
            random.choice([True, False]))
        self.land.lookup_enum_name = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        self.land.name = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        # self.land.pac_id = random.randint(0, 100)

        return self

    def get_land_obj(self) -> Land:
        """
        Returns the land
        object.

        Raises:
            AttributeError: If the land
                object is not initialized.

        Returns:
            Land: The land
                object.
        """
        if not self.land:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.land

    def is_equal(
        self,
        land: Land
    ) -> bool:
        """
        Checks if the current land
        is equal to the given land.

        Args:
            land (Land): The
                land to compare with.

        Returns:
            bool: True if the lands
                are equal, False otherwise.
        """
        land_manager = LandManager(
            self._session_context)
        my_land = self.get_land_obj()
        return land_manager.is_equal(
            land, my_land)

    def get_obj(self) -> Land:
        """
        Returns the Land object.

        :return: The Land object.
        :rtype: Land
        """

        return self.land

    def get_object_name(self) -> str:
        """
        Returns the name of the object.

        :return: The name of the object.
        :rtype: str
        """
        return "land"

    def get_id(self) -> int:
        """
        Returns the ID of the land.

        :return: The ID of the land.
        :rtype: int
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
        Get the name of the parent land.

        Returns:
            str: The name of the parent land.
        """
        return 'Pac'

    async def get_parent_code(self) -> uuid.UUID:
        """
        Get the parent code of the land.

        Returns:
            The parent code of the land
            as a UUID.
        """
        return self.pac_code_peek

    async def get_parent_obj(self) -> models.Pac:
        """
        Get the parent object of the current
        land.

        Returns:
            The parent object of the current
            land,
            which is an instance of the
            Pac model.
        """
        pac_manager = managers_and_enums.PacManager(
            self._session_context)
        pac_obj = await pac_manager.get_by_id(
            self.pac_id)
        return pac_obj
