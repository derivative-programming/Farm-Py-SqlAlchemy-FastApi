# business/role_base.py  # pylint: disable=duplicate-code
# pylint: disable=unused-import

"""
This module contains the
RoleBaseBusObj class,
which represents the base
business object for a
Role.
"""

from decimal import Decimal  # noqa: F401
import random
from typing import Optional
import uuid  # noqa: F401
from datetime import datetime, date  # noqa: F401
from helpers.session_context import SessionContext
from managers import RoleManager
from models import Role
import models
import managers as managers_and_enums
from .base_bus_obj import BaseBusObj

NOT_INITIALIZED_ERROR_MESSAGE = (
    "Role object is not initialized")


class RoleInvalidInitError(Exception):
    """
    Exception raised when the
    Role object
    is not initialized properly.
    """


class RoleBaseBusObj(BaseBusObj):
    """
    This class represents the base business object
    for a Role.
    It requires a valid session context for initialization.
    """

    def __init__(
        self,
        session_context: SessionContext,
        role: Optional[Role] = None
    ):
        """
        Initializes a new instance of the
        RoleBusObj class.

        :param session_context: The session context.
        :raises ValueError: If the session is not provided.
        """

        if not session_context.session:
            raise ValueError("session required")

        if role is None:
            role = Role()

        self._session_context = session_context

        self.role = role

    @property
    def role_id(self) -> int:
        """
        Get the role ID from the
        Role object.

        :return: The role ID.
        :raises AttributeError: If the
            Role object is not initialized.
        """

        if not self.role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.role.role_id
    # code

    @property
    def code(self):
        """
        Get the code from the
        Role object.

        :return: The code.
        :raises AttributeError: If the
            Role object is not initialized.
        """

        if not self.role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.role.code

    @code.setter
    def code(self, value: uuid.UUID):  # type: ignore
        """
        Set the code for the Role object.

        :param value: The code value.
        :raises AttributeError: If the
            Role object is not initialized.
        :raises ValueError: If the code is not a UUID.
        """

        if not self.role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, uuid.UUID):
            raise ValueError("code must be a UUID.")

        self.role.code = value
    # last_change_code

    @property
    def last_change_code(self):
        """
        Get the last change code from the
        Role object.

        :return: The last change code.
        :raises AttributeError: If the
            Role object is not initialized.
        """

        if not self.role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.role.last_change_code

    @last_change_code.setter
    def last_change_code(self, value: int):
        """
        Set the last change code for the
        Role object.

        :param value: The last change code value.
        :raises AttributeError: If the
            Role object is not initialized.
        :raises ValueError: If the last change code is not an integer.
        """

        if not self.role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, int):
            raise ValueError("last_change_code must be an integer.")

        self.role.last_change_code = value
    # insert_user_id

    @property
    def insert_user_id(self):
        """
        Get the insert user ID from the
        Role object.

        :return: The insert user ID.
        :raises AttributeError: If the
            Role object is not initialized.
        """

        if not self.role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.role.insert_user_id

    @insert_user_id.setter
    def insert_user_id(self, value: uuid.UUID):
        """
        Set the insert user ID for the
        Role object.

        :param value: The insert user ID value.
        :raises AttributeError: If the
            Role object is not initialized.
        :raises ValueError: If the insert user ID is not a UUID.
        """

        if not self.role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, uuid.UUID):
            raise ValueError(
                "insert_user_id must be a UUID.")

        self.role.insert_user_id = value
    # last_update_user_id

    @property
    def last_update_user_id(self):
        """
        Get the last update user ID from the
        Role object.

        :return: The last update user ID.
        :raises AttributeError: If the
            Role object is not initialized.
        """

        if not self.role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.role.last_update_user_id

    @last_update_user_id.setter
    def last_update_user_id(self, value: uuid.UUID):
        """
        Set the last update user ID for the
        Role object.

        :param value: The last update user ID value.
        :raises AttributeError: If the
            Role object is not initialized.
        :raises ValueError: If the last update user ID is not a UUID.
        """

        if not self.role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, uuid.UUID):
            raise ValueError(
                "last_update_user_id must be a UUID.")

        self.role.last_update_user_id = value

    # description

    @property
    def description(self):
        """
        Get the Description from the
        Role object.

        :return: The Description.
        :raises AttributeError: If the
            Role object is not initialized.
        """

        if not self.role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if self.role.description is None:
            return ""

        return self.role.description

    @description.setter
    def description(self, value):
        """
        Set the Description for the
        Role object.

        :param value: The Description value.
        :raises AttributeError: If the
            Role object is not initialized.
        :raises AssertionError: If the Description is not a string.
        """

        if not self.role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, str), "description must be a string"
        self.role.description = value
    # displayOrder

    @property
    def display_order(self):
        """
        Returns the value of
        display_order attribute of the
        role.

        Raises:
            AttributeError: If the
                role is not initialized.

        Returns:
            int: The value of
                display_order attribute.
        """
        if not self.role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.role.display_order

    @display_order.setter
    def display_order(self, value):
        """
        Sets the value of
        display_order for the
        role.

        Args:
            value (int): The integer value to set for
                display_order.

        Raises:
            AttributeError: If the
                role is not initialized.

        """
        if not self.role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, int), (
            "display_order must be an integer")
        self.role.display_order = value
    # isActive

    @property
    def is_active(self):
        """
        Get the Is Active flag from the
        Role object.

        :return: The Is Active flag.
        :raises AttributeError: If the
            Role object is not initialized.
        """

        if not self.role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.role.is_active

    @is_active.setter
    def is_active(self, value: bool):
        """
        Set the Is Active flag for the
        Role object.

        :param value: The Is Active flag value.
        :raises AttributeError: If the
            Role object is not initialized.
        :raises ValueError: If the Is Active flag is not a boolean.
        """

        if not self.role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, bool):
            raise ValueError(
                "is_active must be a boolean.")

        self.role.is_active = value
    # lookupEnumName

    @property
    def lookup_enum_name(self):
        """
        Get the Lookup Enum Name from the
        Role object.

        :return: The Lookup Enum Name.
        :raises AttributeError: If the
            Role object is not initialized.
        """

        if not self.role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if self.role.lookup_enum_name is None:
            return ""

        return self.role.lookup_enum_name

    @lookup_enum_name.setter
    def lookup_enum_name(self, value):
        """
        Set the Lookup Enum Name for the
        Role object.

        :param value: The Lookup Enum Name value.
        :raises AttributeError: If the
            Role object is not initialized.
        :raises AssertionError: If the Lookup Enum Name is not a string.
        """

        if not self.role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, str), "lookup_enum_name must be a string"
        self.role.lookup_enum_name = value
    # name

    @property
    def name(self):
        """
        Get the Name from the
        Role object.

        :return: The Name.
        :raises AttributeError: If the
            Role object is not initialized.
        """

        if not self.role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if self.role.name is None:
            return ""

        return self.role.name

    @name.setter
    def name(self, value):
        """
        Set the Name for the
        Role object.

        :param value: The Name value.
        :raises AttributeError: If the
            Role object is not initialized.
        :raises AssertionError: If the Name is not a string.
        """

        if not self.role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, str), "name must be a string"
        self.role.name = value
    # PacID
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
        role.

        Raises:
            AttributeError: If the
                role is not initialized.

        Returns:
            int: The pac ID of the role.
        """
        if not self.role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.role.pac_id

    @pac_id.setter
    def pac_id(self, value):
        """
        Sets the pac ID
        for the role.

        Args:
            value (int or None): The
                pac ID to be set.
                Must be an integer or None.

        Raises:
            AttributeError: If the
                role is not initialized.

        """
        if not self.role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, int) or value is None, (
            "pac_id must be an integer or None")

        self.role.pac_id = value

    @property
    def pac_code_peek(self) -> uuid.UUID:
        """
        Returns the pac id code peek
        of the role.

        Raises:
            AttributeError: If the
            role is not initialized.

        Returns:
            uuid.UUID: The pac id code peek
            of the role.
        """
        if not self.role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.role.pac_code_peek
    # insert_utc_date_time

    @property
    def insert_utc_date_time(self):
        """
        Inserts the UTC date and time into
        the role object.

        Raises:
            AttributeError: If the
                role object is not initialized.

        Returns:
            The UTC date and time inserted into the
            role object.
        """
        if not self.role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.role.insert_utc_date_time

    @insert_utc_date_time.setter
    def insert_utc_date_time(self, value):
        """
        Inserts the UTC date and time for the
        role.

        Args:
            value (datetime): The UTC date and time to be inserted.
                It should be a datetime object or None.

        Raises:
            AttributeError: If the
                role is not initialized.

        """
        if not self.role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, datetime) or value is None, (
            "insert_utc_date_time must be "
            "a datetime object or None")

        self.role.insert_utc_date_time = value

    # update_utc_date_time
    @property
    def last_update_utc_date_time(self):
        """
        Returns the last update UTC date and time
        of the role.

        Raises:
            AttributeError: If the
                role is not initialized.

        Returns:
            datetime: The last update UTC date and time
                of the role.
        """
        if not self.role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.role.last_update_utc_date_time

    @last_update_utc_date_time.setter
    def last_update_utc_date_time(self, value):
        """
        Sets the last update UTC date and time
        for the role.

        Args:
            value (datetime): The datetime object
                representing the last update UTC date and time.
                Pass None to unset the value.

        Raises:
            AttributeError: If the
                role is not initialized.

        """
        if not self.role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, datetime) or value is None, (
            "last_update_utc_date_time "
            "must be a datetime object or None")

        self.role.last_update_utc_date_time = value

    async def load_from_json(
        self,
        json_data: str
    ):
        """
        Load role data
        from JSON string.

        :param json_data: JSON string containing
            role data.
        :raises ValueError: If json_data is not a string
            or if no role
            data is found.
        """

        if not isinstance(json_data, str):
            raise ValueError(
                "json_data must be a string")

        role_manager = RoleManager(
            self._session_context)
        self.role = await \
            role_manager.from_json(json_data)

        return self

    async def load_from_code(
        self,
        code: uuid.UUID
    ):
        """
        Load role
        data from UUID code.

        :param code: UUID code for loading a specific
            role.
        :raises ValueError: If code is not a UUID or if no
            role data is found.
        """
        if not isinstance(code, uuid.UUID):
            raise ValueError(
                "code must be a UUID")

        role_manager = RoleManager(
            self._session_context)
        role_obj = await role_manager.get_by_code(
            code)
        self.role = role_obj

        return self

    async def load_from_id(
        self,
        role_id: int
    ):
        """
        Load role data from
        role ID.

        :param role_id: Integer ID for loading a specific
            role.
        :raises ValueError: If role_id
            is not an integer or
            if no role
            data is found.
        """

        if not isinstance(role_id, int):
            raise ValueError(
                "role_id must be an integer")

        role_manager = RoleManager(
            self._session_context)
        role_obj = await role_manager.get_by_id(
            role_id)
        self.role = role_obj

        return self

    def load_from_obj_instance(
        self,
        role_obj_instance: Role
    ):
        """
        Use the provided
        Role instance.

        :param role_obj_instance: Instance of the
            Role class.
        :raises ValueError: If role_obj_instance
            is not an instance of
            Role.
        """

        if not isinstance(role_obj_instance,
                          Role):
            raise ValueError(
                "role_obj_instance must be an "
                "instance of Role")

        self.role = role_obj_instance

        return self

    async def load_from_dict(
        self,
        role_dict: dict
    ):
        """
        Load role data
        from dictionary.

        :param role_dict: Dictionary containing
            role data.
        :raises ValueError: If role_dict
            is not a
            dictionary or if no
            role data is found.
        """
        if not isinstance(role_dict, dict):
            raise ValueError(
                "role_dict must be a dictionary")

        role_manager = RoleManager(
            self._session_context)

        self.role = await \
            role_manager.from_dict(
                role_dict)

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
        Refreshes the role
        object by fetching
        the latest data from the database.

        Returns:
            The updated
            role object.
        """
        role_manager = RoleManager(
            self._session_context)
        self.role = await \
            role_manager.refresh(
                self.role)

        return self

    def is_valid(self):
        """
        Check if the role
        is valid.

        Returns:
            bool: True if the role
                is valid, False otherwise.
        """
        return self.role is not None

    def to_dict(self):
        """
        Converts the Role
        object to a dictionary representation.

        Returns:
            dict: A dictionary representation of the
                Role object.
        """
        role_manager = RoleManager(
            self._session_context)
        return role_manager.to_dict(
            self.role)

    def to_json(self):
        """
        Converts the role
        object to a JSON representation.

        Returns:
            str: The JSON representation of the
                role object.
        """
        role_manager = RoleManager(
            self._session_context)
        return role_manager.to_json(
            self.role)

    async def save(self):
        """
        Saves the role object
        to the database.

        If the role object
        is not initialized, an AttributeError is raised.
        If the role_id
        is greater than 0, the
        role is
        updated in the database.
        If the role_id is 0,
        the role is
        added to the database.

        Returns:
            The updated or added
            role object.

        Raises:
            AttributeError: If the role
            object is not initialized.
        """
        if not self.role:
            raise AttributeError(NOT_INITIALIZED_ERROR_MESSAGE)

        role_id = self.role.role_id

        if role_id > 0:
            role_manager = RoleManager(
                self._session_context)
            self.role = await \
                role_manager.update(
                    self.role)

        if role_id == 0:
            role_manager = RoleManager(
                self._session_context)
            self.role = await \
                role_manager.add(
                    self.role)

        return self

    async def delete(self):
        """
        Deletes the role
        from the database.

        Raises:
            AttributeError: If the role
                is not initialized.
        """
        if not self.role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if self.role.role_id > 0:
            role_manager = RoleManager(
                self._session_context)
            await role_manager.delete(
                self.role.role_id)
            self.role = None

    async def randomize_properties(self):
        """
        Randomizes the properties of the
        role object.

        This method generates random values for various
        properties of the role
        object

        Returns:
            self: The current instance of the
                Role class.

        Raises:
            AttributeError: If the role
                object is not initialized.
        """
        if not self.role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        self.role.description = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        self.role.display_order = (
            random.randint(0, 100))
        self.role.is_active = (
            random.choice([True, False]))
        self.role.lookup_enum_name = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        self.role.name = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        # self.role.pac_id = random.randint(0, 100)

        return self

    def get_role_obj(self) -> Role:
        """
        Returns the role
        object.

        Raises:
            AttributeError: If the role
                object is not initialized.

        Returns:
            Role: The role
                object.
        """
        if not self.role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.role

    def is_equal(
        self,
        role: Role
    ) -> bool:
        """
        Checks if the current role
        is equal to the given role.

        Args:
            role (Role): The
                role to compare with.

        Returns:
            bool: True if the roles
                are equal, False otherwise.
        """
        role_manager = RoleManager(
            self._session_context)
        my_role = self.get_role_obj()
        return role_manager.is_equal(
            role, my_role)

    def get_obj(self) -> Role:
        """
        Returns the Role object.

        :return: The Role object.
        :rtype: Role
        """

        return self.role

    def get_object_name(self) -> str:
        """
        Returns the name of the object.

        :return: The name of the object.
        :rtype: str
        """
        return "role"

    def get_id(self) -> int:
        """
        Returns the ID of the role.

        :return: The ID of the role.
        :rtype: int
        """
        return self.role_id
    # description,
    # displayOrder,
    # isActive,
    # lookupEnumName,
    # name,
    # PacID

    async def get_parent_name(self) -> str:
        """
        Get the name of the parent role.

        Returns:
            str: The name of the parent role.
        """
        return 'Pac'

    async def get_parent_code(self) -> uuid.UUID:
        """
        Get the parent code of the role.

        Returns:
            The parent code of the role
            as a UUID.
        """
        return self.pac_code_peek

    async def get_parent_obj(self) -> models.Pac:
        """
        Get the parent object of the current
        role.

        Returns:
            The parent object of the current
            role,
            which is an instance of the
            Pac model.
        """
        pac_manager = managers_and_enums.PacManager(
            self._session_context)
        pac_obj = await pac_manager.get_by_id(
            self.pac_id)
        return pac_obj
