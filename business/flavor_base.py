# business/flavor_base.py
# pylint: disable=unused-import

"""
This module contains the
FlavorBaseBusObj class,
which represents the base
business object for a
Flavor.
"""

from decimal import Decimal  # noqa: F401
import random
from typing import Optional
import uuid  # noqa: F401
from datetime import datetime, date  # noqa: F401
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
    Exception raised when the
    Flavor object
    is not initialized properly.
    """


class FlavorBaseBusObj(BaseBusObj):
    """
    This class represents the base business object
    for a Flavor.
    It requires a valid session context for initialization.
    """

    def __init__(
        self,
        session_context: SessionContext,
        flavor: Optional[Flavor] = None
    ):
        """
        Initializes a new instance of the
        FlavorBusObj class.

        :param session_context: The session context.
        :raises ValueError: If the session is not provided.
        """

        if not session_context.session:
            raise ValueError("session required")

        if flavor is None:
            flavor = Flavor()

        self._session_context = session_context

        self.flavor = flavor

    @property
    def flavor_id(self) -> int:
        """
        Get the flavor ID from the
        Flavor object.

        :return: The flavor ID.
        :raises AttributeError: If the
            Flavor object is not initialized.
        """

        if not self.flavor:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.flavor.flavor_id
    # code

    @property
    def code(self):
        """
        Get the code from the
        Flavor object.

        :return: The code.
        :raises AttributeError: If the
            Flavor object is not initialized.
        """

        if not self.flavor:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.flavor.code

    @code.setter
    def code(self, value: uuid.UUID):  # type: ignore
        """
        Set the code for the Flavor object.

        :param value: The code value.
        :raises AttributeError: If the
            Flavor object is not initialized.
        :raises ValueError: If the code is not a UUID.
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
        Get the last change code from the
        Flavor object.

        :return: The last change code.
        :raises AttributeError: If the
            Flavor object is not initialized.
        """

        if not self.flavor:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.flavor.last_change_code

    @last_change_code.setter
    def last_change_code(self, value: int):
        """
        Set the last change code for the
        Flavor object.

        :param value: The last change code value.
        :raises AttributeError: If the
            Flavor object is not initialized.
        :raises ValueError: If the last change code is not an integer.
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
        Get the insert user ID from the
        Flavor object.

        :return: The insert user ID.
        :raises AttributeError: If the
            Flavor object is not initialized.
        """

        if not self.flavor:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.flavor.insert_user_id

    @insert_user_id.setter
    def insert_user_id(self, value: uuid.UUID):
        """
        Set the insert user ID for the
        Flavor object.

        :param value: The insert user ID value.
        :raises AttributeError: If the
            Flavor object is not initialized.
        :raises ValueError: If the insert user ID is not a UUID.
        """

        if not self.flavor:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, uuid.UUID):
            raise ValueError(
                "insert_user_id must be a UUID.")

        self.flavor.insert_user_id = value
    # last_update_user_id

    @property
    def last_update_user_id(self):
        """
        Get the last update user ID from the
        Flavor object.

        :return: The last update user ID.
        :raises AttributeError: If the
            Flavor object is not initialized.
        """

        if not self.flavor:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.flavor.last_update_user_id

    @last_update_user_id.setter
    def last_update_user_id(self, value: uuid.UUID):
        """
        Set the last update user ID for the
        Flavor object.

        :param value: The last update user ID value.
        :raises AttributeError: If the
            Flavor object is not initialized.
        :raises ValueError: If the last update user ID is not a UUID.
        """

        if not self.flavor:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, uuid.UUID):
            raise ValueError(
                "last_update_user_id must be a UUID.")

        self.flavor.last_update_user_id = value

    # description

    @property
    def description(self):
        """
        Get the Description from the
        Flavor object.

        :return: The Description.
        :raises AttributeError: If the
            Flavor object is not initialized.
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
        Set the Description for the
        Flavor object.

        :param value: The Description value.
        :raises AttributeError: If the
            Flavor object is not initialized.
        :raises AssertionError: If the Description is not a string.
        """

        if not self.flavor:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, str), "description must be a string"
        self.flavor.description = value
    # displayOrder

    @property
    def display_order(self):
        """
        Returns the value of
        display_order attribute of the
        flavor.

        Raises:
            AttributeError: If the
                flavor is not initialized.

        Returns:
            int: The value of
                display_order attribute.
        """
        if not self.flavor:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.flavor.display_order

    @display_order.setter
    def display_order(self, value):
        """
        Sets the value of
        display_order for the
        flavor.

        Args:
            value (int): The integer value to set for
                display_order.

        Raises:
            AttributeError: If the
                flavor is not initialized.

        """
        if not self.flavor:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, int), (
            "display_order must be an integer")
        self.flavor.display_order = value
    # isActive

    @property
    def is_active(self):
        """
        Get the Is Active flag from the
        Flavor object.

        :return: The Is Active flag.
        :raises AttributeError: If the
            Flavor object is not initialized.
        """

        if not self.flavor:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.flavor.is_active

    @is_active.setter
    def is_active(self, value: bool):
        """
        Set the Is Active flag for the
        Flavor object.

        :param value: The Is Active flag value.
        :raises AttributeError: If the
            Flavor object is not initialized.
        :raises ValueError: If the Is Active flag is not a boolean.
        """

        if not self.flavor:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, bool):
            raise ValueError(
                "is_active must be a boolean.")

        self.flavor.is_active = value
    # lookupEnumName

    @property
    def lookup_enum_name(self):
        """
        Get the Lookup Enum Name from the
        Flavor object.

        :return: The Lookup Enum Name.
        :raises AttributeError: If the
            Flavor object is not initialized.
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
        Set the Lookup Enum Name for the
        Flavor object.

        :param value: The Lookup Enum Name value.
        :raises AttributeError: If the
            Flavor object is not initialized.
        :raises AssertionError: If the Lookup Enum Name is not a string.
        """

        if not self.flavor:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, str), "lookup_enum_name must be a string"
        self.flavor.lookup_enum_name = value
    # name

    @property
    def name(self):
        """
        Get the Name from the
        Flavor object.

        :return: The Name.
        :raises AttributeError: If the
            Flavor object is not initialized.
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
        Set the Name for the
        Flavor object.

        :param value: The Name value.
        :raises AttributeError: If the
            Flavor object is not initialized.
        :raises AssertionError: If the Name is not a string.
        """

        if not self.flavor:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, str), "name must be a string"
        self.flavor.name = value
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
        flavor.

        Raises:
            AttributeError: If the
                flavor is not initialized.

        Returns:
            int: The pac ID of the flavor.
        """
        if not self.flavor:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.flavor.pac_id

    @pac_id.setter
    def pac_id(self, value):
        """
        Sets the pac ID
        for the flavor.

        Args:
            value (int or None): The
                pac ID to be set.
                Must be an integer or None.

        Raises:
            AttributeError: If the
                flavor is not initialized.

        """
        if not self.flavor:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, int) or value is None, (
            "pac_id must be an integer or None")

        self.flavor.pac_id = value

    @property
    def pac_code_peek(self) -> uuid.UUID:
        """
        Returns the pac id code peek
        of the flavor.

        Raises:
            AttributeError: If the
            flavor is not initialized.

        Returns:
            uuid.UUID: The pac id code peek
            of the flavor.
        """
        if not self.flavor:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.flavor.pac_code_peek
    # insert_utc_date_time

    @property
    def insert_utc_date_time(self):
        """
        Inserts the UTC date and time into
        the flavor object.

        Raises:
            AttributeError: If the
                flavor object is not initialized.

        Returns:
            The UTC date and time inserted into the
            flavor object.
        """
        if not self.flavor:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.flavor.insert_utc_date_time

    @insert_utc_date_time.setter
    def insert_utc_date_time(self, value):
        """
        Inserts the UTC date and time for the
        flavor.

        Args:
            value (datetime): The UTC date and time to be inserted.
                It should be a datetime object or None.

        Raises:
            AttributeError: If the
                flavor is not initialized.

        """
        if not self.flavor:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, datetime) or value is None, (
            "insert_utc_date_time must be "
            "a datetime object or None")

        self.flavor.insert_utc_date_time = value

    # update_utc_date_time
    @property
    def last_update_utc_date_time(self):
        """
        Returns the last update UTC date and time
        of the flavor.

        Raises:
            AttributeError: If the
                flavor is not initialized.

        Returns:
            datetime: The last update UTC date and time
                of the flavor.
        """
        if not self.flavor:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.flavor.last_update_utc_date_time

    @last_update_utc_date_time.setter
    def last_update_utc_date_time(self, value):
        """
        Sets the last update UTC date and time
        for the flavor.

        Args:
            value (datetime): The datetime object
                representing the last update UTC date and time.
                Pass None to unset the value.

        Raises:
            AttributeError: If the
                flavor is not initialized.

        """
        if not self.flavor:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, datetime) or value is None, (
            "last_update_utc_date_time "
            "must be a datetime object or None")

        self.flavor.last_update_utc_date_time = value

    async def load_from_json(
        self,
        json_data: str
    ):
        """
        Load flavor data
        from JSON string.

        :param json_data: JSON string containing
            flavor data.
        :raises ValueError: If json_data is not a string
            or if no flavor
            data is found.
        """

        if not isinstance(json_data, str):
            raise ValueError(
                "json_data must be a string")

        flavor_manager = FlavorManager(
            self._session_context)
        self.flavor = await \
            flavor_manager.from_json(json_data)

        return self

    async def load_from_code(
        self,
        code: uuid.UUID
    ):
        """
        Load flavor
        data from UUID code.

        :param code: UUID code for loading a specific
            flavor.
        :raises ValueError: If code is not a UUID or if no
            flavor data is found.
        """
        if not isinstance(code, uuid.UUID):
            raise ValueError(
                "code must be a UUID")

        flavor_manager = FlavorManager(
            self._session_context)
        flavor_obj = await flavor_manager.get_by_code(
            code)
        self.flavor = flavor_obj

        return self

    async def load_from_id(
        self,
        flavor_id: int
    ):
        """
        Load flavor data from
        flavor ID.

        :param flavor_id: Integer ID for loading a specific
            flavor.
        :raises ValueError: If flavor_id
            is not an integer or
            if no flavor
            data is found.
        """

        if not isinstance(flavor_id, int):
            raise ValueError(
                "flavor_id must be an integer")

        flavor_manager = FlavorManager(
            self._session_context)
        flavor_obj = await flavor_manager.get_by_id(
            flavor_id)
        self.flavor = flavor_obj

        return self

    def load_from_obj_instance(
        self,
        flavor_obj_instance: Flavor
    ):
        """
        Use the provided
        Flavor instance.

        :param flavor_obj_instance: Instance of the
            Flavor class.
        :raises ValueError: If flavor_obj_instance
            is not an instance of
            Flavor.
        """

        if not isinstance(flavor_obj_instance,
                          Flavor):
            raise ValueError(
                "flavor_obj_instance must be an "
                "instance of Flavor")

        self.flavor = flavor_obj_instance

        return self

    async def load_from_dict(
        self,
        flavor_dict: dict
    ):
        """
        Load flavor data
        from dictionary.

        :param flavor_dict: Dictionary containing
            flavor data.
        :raises ValueError: If flavor_dict
            is not a
            dictionary or if no
            flavor data is found.
        """
        if not isinstance(flavor_dict, dict):
            raise ValueError(
                "flavor_dict must be a dictionary")

        flavor_manager = FlavorManager(
            self._session_context)

        self.flavor = await \
            flavor_manager.from_dict(
                flavor_dict)

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
        Refreshes the flavor
        object by fetching
        the latest data from the database.

        Returns:
            The updated
            flavor object.
        """
        flavor_manager = FlavorManager(
            self._session_context)
        self.flavor = await \
            flavor_manager.refresh(
                self.flavor)

        return self

    def is_valid(self):
        """
        Check if the flavor
        is valid.

        Returns:
            bool: True if the flavor
                is valid, False otherwise.
        """
        return self.flavor is not None

    def to_dict(self):
        """
        Converts the Flavor
        object to a dictionary representation.

        Returns:
            dict: A dictionary representation of the
                Flavor object.
        """
        flavor_manager = FlavorManager(
            self._session_context)
        return flavor_manager.to_dict(
            self.flavor)

    def to_json(self):
        """
        Converts the flavor
        object to a JSON representation.

        Returns:
            str: The JSON representation of the
                flavor object.
        """
        flavor_manager = FlavorManager(
            self._session_context)
        return flavor_manager.to_json(
            self.flavor)

    async def save(self):
        """
        Saves the flavor object
        to the database.

        If the flavor object
        is not initialized, an AttributeError is raised.
        If the flavor_id
        is greater than 0, the
        flavor is
        updated in the database.
        If the flavor_id is 0,
        the flavor is
        added to the database.

        Returns:
            The updated or added
            flavor object.

        Raises:
            AttributeError: If the flavor
            object is not initialized.
        """
        if not self.flavor:
            raise AttributeError(NOT_INITIALIZED_ERROR_MESSAGE)

        flavor_id = self.flavor.flavor_id

        if flavor_id > 0:
            flavor_manager = FlavorManager(
                self._session_context)
            self.flavor = await \
                flavor_manager.update(
                    self.flavor)

        if flavor_id == 0:
            flavor_manager = FlavorManager(
                self._session_context)
            self.flavor = await \
                flavor_manager.add(
                    self.flavor)

        return self

    async def delete(self):
        """
        Deletes the flavor
        from the database.

        Raises:
            AttributeError: If the flavor
                is not initialized.
        """
        if not self.flavor:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if self.flavor.flavor_id > 0:
            flavor_manager = FlavorManager(
                self._session_context)
            await flavor_manager.delete(
                self.flavor.flavor_id)
            self.flavor = None

    async def randomize_properties(self):
        """
        Randomizes the properties of the
        flavor object.

        This method generates random values for various
        properties of the flavor
        object

        Returns:
            self: The current instance of the
                Flavor class.

        Raises:
            AttributeError: If the flavor
                object is not initialized.
        """
        if not self.flavor:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        self.flavor.description = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        self.flavor.display_order = (
            random.randint(0, 100))
        self.flavor.is_active = (
            random.choice([True, False]))
        self.flavor.lookup_enum_name = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        self.flavor.name = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        # self.flavor.pac_id = random.randint(0, 100)

        return self

    def get_flavor_obj(self) -> Flavor:
        """
        Returns the flavor
        object.

        Raises:
            AttributeError: If the flavor
                object is not initialized.

        Returns:
            Flavor: The flavor
                object.
        """
        if not self.flavor:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.flavor

    def is_equal(
        self,
        flavor: Flavor
    ) -> bool:
        """
        Checks if the current flavor
        is equal to the given flavor.

        Args:
            flavor (Flavor): The
                flavor to compare with.

        Returns:
            bool: True if the flavors
                are equal, False otherwise.
        """
        flavor_manager = FlavorManager(
            self._session_context)
        my_flavor = self.get_flavor_obj()
        return flavor_manager.is_equal(
            flavor, my_flavor)
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
        pac_manager = managers_and_enums.PacManager(
            self._session_context)
        pac_obj = await pac_manager.get_by_id(
            self.pac_id)
        return pac_obj

    def get_obj(self) -> Flavor:
        """
        Returns the Flavor object.

        :return: The Flavor object.
        :rtype: Flavor
        """

        return self.flavor

    def get_object_name(self) -> str:
        """
        Returns the name of the object.

        :return: The name of the object.
        :rtype: str
        """
        return "flavor"

    def get_id(self) -> int:
        """
        Returns the ID of the flavor.

        :return: The ID of the flavor.
        :rtype: int
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
        Get the name of the parent flavor.

        Returns:
            str: The name of the parent flavor.
        """
        return 'Pac'

    async def get_parent_code(self) -> uuid.UUID:
        """
        Get the parent code of the flavor.

        Returns:
            The parent code of the flavor
            as a UUID.
        """
        return self.pac_code_peek

    async def get_parent_obj(self) -> models.Pac:
        """
        Get the parent object of the current
        flavor.

        Returns:
            The parent object of the current
            flavor,
            which is an instance of the
            Pac model.
        """
        pac = await self.get_pac_id_rel_obj()

        return pac

