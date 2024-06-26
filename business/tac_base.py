# business/tac_base.py
# pylint: disable=unused-import

"""
This module contains the
TacBaseBusObj class,
which represents the base
business object for a
Tac.
"""

from decimal import Decimal  # noqa: F401
import random
from typing import Optional
import uuid  # noqa: F401
from datetime import datetime, date  # noqa: F401
from helpers.session_context import SessionContext
from managers import TacManager
from models import Tac
import models
import managers as managers_and_enums
from .base_bus_obj import BaseBusObj

NOT_INITIALIZED_ERROR_MESSAGE = (
    "Tac object is not initialized")


class TacInvalidInitError(Exception):
    """
    Exception raised when the
    Tac object
    is not initialized properly.
    """


class TacBaseBusObj(BaseBusObj):
    """
    This class represents the base business object
    for a Tac.
    It requires a valid session context for initialization.
    """

    def __init__(
        self,
        session_context: SessionContext,
        tac: Optional[Tac] = None
    ):
        """
        Initializes a new instance of the
        TacBusObj class.

        :param session_context: The session context.
        :raises ValueError: If the session is not provided.
        """

        if not session_context.session:
            raise ValueError("session required")

        if tac is None:
            tac = Tac()

        self._session_context = session_context

        self.tac = tac

    @property
    def tac_id(self) -> int:
        """
        Get the tac ID from the
        Tac object.

        :return: The tac ID.
        :raises AttributeError: If the
            Tac object is not initialized.
        """

        if not self.tac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.tac.tac_id
    # code

    @property
    def code(self):
        """
        Get the code from the
        Tac object.

        :return: The code.
        :raises AttributeError: If the
            Tac object is not initialized.
        """

        if not self.tac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.tac.code

    @code.setter
    def code(self, value: uuid.UUID):  # type: ignore
        """
        Set the code for the Tac object.

        :param value: The code value.
        :raises AttributeError: If the
            Tac object is not initialized.
        :raises ValueError: If the code is not a UUID.
        """

        if not self.tac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, uuid.UUID):
            raise ValueError("code must be a UUID.")

        self.tac.code = value
    # last_change_code

    @property
    def last_change_code(self):
        """
        Get the last change code from the
        Tac object.

        :return: The last change code.
        :raises AttributeError: If the
            Tac object is not initialized.
        """

        if not self.tac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.tac.last_change_code

    @last_change_code.setter
    def last_change_code(self, value: int):
        """
        Set the last change code for the
        Tac object.

        :param value: The last change code value.
        :raises AttributeError: If the
            Tac object is not initialized.
        :raises ValueError: If the last change code is not an integer.
        """

        if not self.tac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, int):
            raise ValueError("last_change_code must be an integer.")

        self.tac.last_change_code = value
    # insert_user_id

    @property
    def insert_user_id(self):
        """
        Get the insert user ID from the
        Tac object.

        :return: The insert user ID.
        :raises AttributeError: If the
            Tac object is not initialized.
        """

        if not self.tac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.tac.insert_user_id

    @insert_user_id.setter
    def insert_user_id(self, value: uuid.UUID):
        """
        Set the insert user ID for the
        Tac object.

        :param value: The insert user ID value.
        :raises AttributeError: If the
            Tac object is not initialized.
        :raises ValueError: If the insert user ID is not a UUID.
        """

        if not self.tac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, uuid.UUID):
            raise ValueError(
                "insert_user_id must be a UUID.")

        self.tac.insert_user_id = value
    # last_update_user_id

    @property
    def last_update_user_id(self):
        """
        Get the last update user ID from the
        Tac object.

        :return: The last update user ID.
        :raises AttributeError: If the
            Tac object is not initialized.
        """

        if not self.tac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.tac.last_update_user_id

    @last_update_user_id.setter
    def last_update_user_id(self, value: uuid.UUID):
        """
        Set the last update user ID for the
        Tac object.

        :param value: The last update user ID value.
        :raises AttributeError: If the
            Tac object is not initialized.
        :raises ValueError: If the last update user ID is not a UUID.
        """

        if not self.tac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, uuid.UUID):
            raise ValueError(
                "last_update_user_id must be a UUID.")

        self.tac.last_update_user_id = value

    # description

    @property
    def description(self):
        """
        Get the Description from the
        Tac object.

        :return: The Description.
        :raises AttributeError: If the
            Tac object is not initialized.
        """

        if not self.tac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if self.tac.description is None:
            return ""

        return self.tac.description

    @description.setter
    def description(self, value):
        """
        Set the Description for the
        Tac object.

        :param value: The Description value.
        :raises AttributeError: If the
            Tac object is not initialized.
        :raises AssertionError: If the Description is not a string.
        """

        if not self.tac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, str), "description must be a string"
        self.tac.description = value
    # displayOrder

    @property
    def display_order(self):
        """
        Returns the value of
        display_order attribute of the
        tac.

        Raises:
            AttributeError: If the
                tac is not initialized.

        Returns:
            int: The value of
                display_order attribute.
        """
        if not self.tac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.tac.display_order

    @display_order.setter
    def display_order(self, value):
        """
        Sets the value of
        display_order for the
        tac.

        Args:
            value (int): The integer value to set for
                display_order.

        Raises:
            AttributeError: If the
                tac is not initialized.

        """
        if not self.tac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, int), (
            "display_order must be an integer")
        self.tac.display_order = value
    # isActive

    @property
    def is_active(self):
        """
        Get the Is Active flag from the
        Tac object.

        :return: The Is Active flag.
        :raises AttributeError: If the
            Tac object is not initialized.
        """

        if not self.tac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.tac.is_active

    @is_active.setter
    def is_active(self, value: bool):
        """
        Set the Is Active flag for the
        Tac object.

        :param value: The Is Active flag value.
        :raises AttributeError: If the
            Tac object is not initialized.
        :raises ValueError: If the Is Active flag is not a boolean.
        """

        if not self.tac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, bool):
            raise ValueError(
                "is_active must be a boolean.")

        self.tac.is_active = value
    # lookupEnumName

    @property
    def lookup_enum_name(self):
        """
        Get the Lookup Enum Name from the
        Tac object.

        :return: The Lookup Enum Name.
        :raises AttributeError: If the
            Tac object is not initialized.
        """

        if not self.tac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if self.tac.lookup_enum_name is None:
            return ""

        return self.tac.lookup_enum_name

    @lookup_enum_name.setter
    def lookup_enum_name(self, value):
        """
        Set the Lookup Enum Name for the
        Tac object.

        :param value: The Lookup Enum Name value.
        :raises AttributeError: If the
            Tac object is not initialized.
        :raises AssertionError: If the Lookup Enum Name is not a string.
        """

        if not self.tac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, str), "lookup_enum_name must be a string"
        self.tac.lookup_enum_name = value
    # name

    @property
    def name(self):
        """
        Get the Name from the
        Tac object.

        :return: The Name.
        :raises AttributeError: If the
            Tac object is not initialized.
        """

        if not self.tac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if self.tac.name is None:
            return ""

        return self.tac.name

    @name.setter
    def name(self, value):
        """
        Set the Name for the
        Tac object.

        :param value: The Name value.
        :raises AttributeError: If the
            Tac object is not initialized.
        :raises AssertionError: If the Name is not a string.
        """

        if not self.tac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, str), "name must be a string"
        self.tac.name = value
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
        tac.

        Raises:
            AttributeError: If the
                tac is not initialized.

        Returns:
            int: The pac ID of the tac.
        """
        if not self.tac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.tac.pac_id

    @pac_id.setter
    def pac_id(self, value):
        """
        Sets the pac ID
        for the tac.

        Args:
            value (int or None): The
                pac ID to be set.
                Must be an integer or None.

        Raises:
            AttributeError: If the
                tac is not initialized.

        """
        if not self.tac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, int) or value is None, (
            "pac_id must be an integer or None")

        self.tac.pac_id = value

    @property
    def pac_code_peek(self) -> uuid.UUID:
        """
        Returns the pac id code peek
        of the tac.

        Raises:
            AttributeError: If the
            tac is not initialized.

        Returns:
            uuid.UUID: The pac id code peek
            of the tac.
        """
        if not self.tac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.tac.pac_code_peek
    # insert_utc_date_time

    @property
    def insert_utc_date_time(self):
        """
        Inserts the UTC date and time into
        the tac object.

        Raises:
            AttributeError: If the
                tac object is not initialized.

        Returns:
            The UTC date and time inserted into the
            tac object.
        """
        if not self.tac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.tac.insert_utc_date_time

    @insert_utc_date_time.setter
    def insert_utc_date_time(self, value):
        """
        Inserts the UTC date and time for the
        tac.

        Args:
            value (datetime): The UTC date and time to be inserted.
                It should be a datetime object or None.

        Raises:
            AttributeError: If the
                tac is not initialized.

        """
        if not self.tac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, datetime) or value is None, (
            "insert_utc_date_time must be "
            "a datetime object or None")

        self.tac.insert_utc_date_time = value

    # update_utc_date_time
    @property
    def last_update_utc_date_time(self):
        """
        Returns the last update UTC date and time
        of the tac.

        Raises:
            AttributeError: If the
                tac is not initialized.

        Returns:
            datetime: The last update UTC date and time
                of the tac.
        """
        if not self.tac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.tac.last_update_utc_date_time

    @last_update_utc_date_time.setter
    def last_update_utc_date_time(self, value):
        """
        Sets the last update UTC date and time
        for the tac.

        Args:
            value (datetime): The datetime object
                representing the last update UTC date and time.
                Pass None to unset the value.

        Raises:
            AttributeError: If the
                tac is not initialized.

        """
        if not self.tac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, datetime) or value is None, (
            "last_update_utc_date_time "
            "must be a datetime object or None")

        self.tac.last_update_utc_date_time = value

    async def load_from_json(
        self,
        json_data: str
    ):
        """
        Load tac data
        from JSON string.

        :param json_data: JSON string containing
            tac data.
        :raises ValueError: If json_data is not a string
            or if no tac
            data is found.
        """

        if not isinstance(json_data, str):
            raise ValueError(
                "json_data must be a string")

        tac_manager = TacManager(
            self._session_context)
        self.tac = await \
            tac_manager.from_json(json_data)

        return self

    async def load_from_code(
        self,
        code: uuid.UUID
    ):
        """
        Load tac
        data from UUID code.

        :param code: UUID code for loading a specific
            tac.
        :raises ValueError: If code is not a UUID or if no
            tac data is found.
        """
        if not isinstance(code, uuid.UUID):
            raise ValueError(
                "code must be a UUID")

        tac_manager = TacManager(
            self._session_context)
        tac_obj = await tac_manager.get_by_code(
            code)
        self.tac = tac_obj

        return self

    async def load_from_id(
        self,
        tac_id: int
    ):
        """
        Load tac data from
        tac ID.

        :param tac_id: Integer ID for loading a specific
            tac.
        :raises ValueError: If tac_id
            is not an integer or
            if no tac
            data is found.
        """

        if not isinstance(tac_id, int):
            raise ValueError(
                "tac_id must be an integer")

        tac_manager = TacManager(
            self._session_context)
        tac_obj = await tac_manager.get_by_id(
            tac_id)
        self.tac = tac_obj

        return self

    def load_from_obj_instance(
        self,
        tac_obj_instance: Tac
    ):
        """
        Use the provided
        Tac instance.

        :param tac_obj_instance: Instance of the
            Tac class.
        :raises ValueError: If tac_obj_instance
            is not an instance of
            Tac.
        """

        if not isinstance(tac_obj_instance,
                          Tac):
            raise ValueError(
                "tac_obj_instance must be an "
                "instance of Tac")

        self.tac = tac_obj_instance

        return self

    async def load_from_dict(
        self,
        tac_dict: dict
    ):
        """
        Load tac data
        from dictionary.

        :param tac_dict: Dictionary containing
            tac data.
        :raises ValueError: If tac_dict
            is not a
            dictionary or if no
            tac data is found.
        """
        if not isinstance(tac_dict, dict):
            raise ValueError(
                "tac_dict must be a dictionary")

        tac_manager = TacManager(
            self._session_context)

        self.tac = await \
            tac_manager.from_dict(
                tac_dict)

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
        Refreshes the tac
        object by fetching
        the latest data from the database.

        Returns:
            The updated
            tac object.
        """
        tac_manager = TacManager(
            self._session_context)
        self.tac = await \
            tac_manager.refresh(
                self.tac)

        return self

    def is_valid(self):
        """
        Check if the tac
        is valid.

        Returns:
            bool: True if the tac
                is valid, False otherwise.
        """
        return self.tac is not None

    def to_dict(self):
        """
        Converts the Tac
        object to a dictionary representation.

        Returns:
            dict: A dictionary representation of the
                Tac object.
        """
        tac_manager = TacManager(
            self._session_context)
        return tac_manager.to_dict(
            self.tac)

    def to_json(self):
        """
        Converts the tac
        object to a JSON representation.

        Returns:
            str: The JSON representation of the
                tac object.
        """
        tac_manager = TacManager(
            self._session_context)
        return tac_manager.to_json(
            self.tac)

    async def save(self):
        """
        Saves the tac object
        to the database.

        If the tac object
        is not initialized, an AttributeError is raised.
        If the tac_id
        is greater than 0, the
        tac is
        updated in the database.
        If the tac_id is 0,
        the tac is
        added to the database.

        Returns:
            The updated or added
            tac object.

        Raises:
            AttributeError: If the tac
            object is not initialized.
        """
        if not self.tac:
            raise AttributeError(NOT_INITIALIZED_ERROR_MESSAGE)

        tac_id = self.tac.tac_id

        if tac_id > 0:
            tac_manager = TacManager(
                self._session_context)
            self.tac = await \
                tac_manager.update(
                    self.tac)

        if tac_id == 0:
            tac_manager = TacManager(
                self._session_context)
            self.tac = await \
                tac_manager.add(
                    self.tac)

        return self

    async def delete(self):
        """
        Deletes the tac
        from the database.

        Raises:
            AttributeError: If the tac
                is not initialized.
        """
        if not self.tac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if self.tac.tac_id > 0:
            tac_manager = TacManager(
                self._session_context)
            await tac_manager.delete(
                self.tac.tac_id)
            self.tac = None

    async def randomize_properties(self):
        """
        Randomizes the properties of the
        tac object.

        This method generates random values for various
        properties of the tac
        object

        Returns:
            self: The current instance of the
                Tac class.

        Raises:
            AttributeError: If the tac
                object is not initialized.
        """
        if not self.tac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        self.tac.description = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        self.tac.display_order = (
            random.randint(0, 100))
        self.tac.is_active = (
            random.choice([True, False]))
        self.tac.lookup_enum_name = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        self.tac.name = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        # self.tac.pac_id = random.randint(0, 100)

        return self

    def get_tac_obj(self) -> Tac:
        """
        Returns the tac
        object.

        Raises:
            AttributeError: If the tac
                object is not initialized.

        Returns:
            Tac: The tac
                object.
        """
        if not self.tac:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.tac

    def is_equal(
        self,
        tac: Tac
    ) -> bool:
        """
        Checks if the current tac
        is equal to the given tac.

        Args:
            tac (Tac): The
                tac to compare with.

        Returns:
            bool: True if the tacs
                are equal, False otherwise.
        """
        tac_manager = TacManager(
            self._session_context)
        my_tac = self.get_tac_obj()
        return tac_manager.is_equal(
            tac, my_tac)
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

    def get_obj(self) -> Tac:
        """
        Returns the Tac object.

        :return: The Tac object.
        :rtype: Tac
        """

        return self.tac

    def get_object_name(self) -> str:
        """
        Returns the name of the object.

        :return: The name of the object.
        :rtype: str
        """
        return "tac"

    def get_id(self) -> int:
        """
        Returns the ID of the tac.

        :return: The ID of the tac.
        :rtype: int
        """
        return self.tac_id
    # description,
    # displayOrder,
    # isActive,
    # lookupEnumName,
    # name,
    # PacID

    async def get_parent_name(self) -> str:
        """
        Get the name of the parent tac.

        Returns:
            str: The name of the parent tac.
        """
        return 'Pac'

    async def get_parent_code(self) -> uuid.UUID:
        """
        Get the parent code of the tac.

        Returns:
            The parent code of the tac
            as a UUID.
        """
        return self.pac_code_peek

    async def get_parent_obj(self) -> models.Pac:
        """
        Get the parent object of the current
        tac.

        Returns:
            The parent object of the current
            tac,
            which is an instance of the
            Pac model.
        """
        pac = await self.get_pac_id_rel_obj()

        return pac
