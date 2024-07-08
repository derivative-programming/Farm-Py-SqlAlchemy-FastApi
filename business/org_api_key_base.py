# business/org_api_key_base.py  # pylint: disable=duplicate-code
# pylint: disable=unused-import

"""
This module contains the
OrgApiKeyBaseBusObj class,
which represents the base
business object for a
OrgApiKey.
"""

from decimal import Decimal  # noqa: F401
import random
from typing import Optional
import uuid  # noqa: F401
from datetime import datetime, date  # noqa: F401
from helpers.session_context import SessionContext
from managers import OrgApiKeyManager
from models import OrgApiKey
import models
import managers as managers_and_enums
from .base_bus_obj import BaseBusObj

NOT_INITIALIZED_ERROR_MESSAGE = (
    "OrgApiKey object is not initialized")


class OrgApiKeyInvalidInitError(Exception):
    """
    Exception raised when the
    OrgApiKey object
    is not initialized properly.
    """


class OrgApiKeyBaseBusObj(BaseBusObj):
    """
    This class represents the base business object
    for a OrgApiKey.
    It requires a valid session context for initialization.
    """

    def __init__(
        self,
        session_context: SessionContext,
        org_api_key: Optional[OrgApiKey] = None
    ):
        """
        Initializes a new instance of the
        OrgApiKeyBusObj class.

        :param session_context: The session context.
        :raises ValueError: If the session is not provided.
        """

        if not session_context.session:
            raise ValueError("session required")

        if org_api_key is None:
            org_api_key = OrgApiKey()

        self._session_context = session_context

        self.org_api_key = org_api_key

    @property
    def org_api_key_id(self) -> int:
        """
        Get the org_api_key ID from the
        OrgApiKey object.

        :return: The org_api_key ID.
        :raises AttributeError: If the
            OrgApiKey object is not initialized.
        """

        if not self.org_api_key:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.org_api_key.org_api_key_id
    # code

    @property
    def code(self):
        """
        Get the code from the
        OrgApiKey object.

        :return: The code.
        :raises AttributeError: If the
            OrgApiKey object is not initialized.
        """

        if not self.org_api_key:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.org_api_key.code

    @code.setter
    def code(self, value: uuid.UUID):  # type: ignore
        """
        Set the code for the OrgApiKey object.

        :param value: The code value.
        :raises AttributeError: If the
            OrgApiKey object is not initialized.
        :raises ValueError: If the code is not a UUID.
        """

        if not self.org_api_key:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, uuid.UUID):
            raise ValueError("code must be a UUID.")

        self.org_api_key.code = value
    # last_change_code

    @property
    def last_change_code(self):
        """
        Get the last change code from the
        OrgApiKey object.

        :return: The last change code.
        :raises AttributeError: If the
            OrgApiKey object is not initialized.
        """

        if not self.org_api_key:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.org_api_key.last_change_code

    @last_change_code.setter
    def last_change_code(self, value: int):
        """
        Set the last change code for the
        OrgApiKey object.

        :param value: The last change code value.
        :raises AttributeError: If the
            OrgApiKey object is not initialized.
        :raises ValueError: If the last change code is not an integer.
        """

        if not self.org_api_key:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, int):
            raise ValueError("last_change_code must be an integer.")

        self.org_api_key.last_change_code = value
    # insert_user_id

    @property
    def insert_user_id(self):
        """
        Get the insert user ID from the
        OrgApiKey object.

        :return: The insert user ID.
        :raises AttributeError: If the
            OrgApiKey object is not initialized.
        """

        if not self.org_api_key:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.org_api_key.insert_user_id

    @insert_user_id.setter
    def insert_user_id(self, value: uuid.UUID):
        """
        Set the insert user ID for the
        OrgApiKey object.

        :param value: The insert user ID value.
        :raises AttributeError: If the
            OrgApiKey object is not initialized.
        :raises ValueError: If the insert user ID is not a UUID.
        """

        if not self.org_api_key:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, uuid.UUID):
            raise ValueError(
                "insert_user_id must be a UUID.")

        self.org_api_key.insert_user_id = value
    # last_update_user_id

    @property
    def last_update_user_id(self):
        """
        Get the last update user ID from the
        OrgApiKey object.

        :return: The last update user ID.
        :raises AttributeError: If the
            OrgApiKey object is not initialized.
        """

        if not self.org_api_key:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.org_api_key.last_update_user_id

    @last_update_user_id.setter
    def last_update_user_id(self, value: uuid.UUID):
        """
        Set the last update user ID for the
        OrgApiKey object.

        :param value: The last update user ID value.
        :raises AttributeError: If the
            OrgApiKey object is not initialized.
        :raises ValueError: If the last update user ID is not a UUID.
        """

        if not self.org_api_key:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, uuid.UUID):
            raise ValueError(
                "last_update_user_id must be a UUID.")

        self.org_api_key.last_update_user_id = value

    # apiKeyValue

    @property
    def api_key_value(self):
        """
        Get the Api Key Value from the
        OrgApiKey object.

        :return: The Api Key Value.
        :raises AttributeError: If the
            OrgApiKey object is not initialized.
        """

        if not self.org_api_key:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if self.org_api_key.api_key_value is None:
            return ""

        return self.org_api_key.api_key_value

    @api_key_value.setter
    def api_key_value(self, value):
        """
        Set the Api Key Value for the
        OrgApiKey object.

        :param value: The Api Key Value value.
        :raises AttributeError: If the
            OrgApiKey object is not initialized.
        :raises AssertionError: If the
            Api Key Value
            is not a string.
        """

        if not self.org_api_key:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, str), \
            "api_key_value must be a string"
        self.org_api_key.api_key_value = value
    # createdBy

    @property
    def created_by(self):
        """
        Get the Created By from the
        OrgApiKey object.

        :return: The Created By.
        :raises AttributeError: If the
            OrgApiKey object is not initialized.
        """

        if not self.org_api_key:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if self.org_api_key.created_by is None:
            return ""

        return self.org_api_key.created_by

    @created_by.setter
    def created_by(self, value):
        """
        Set the Created By for the
        OrgApiKey object.

        :param value: The Created By value.
        :raises AttributeError: If the
            OrgApiKey object is not initialized.
        :raises AssertionError: If the
            Created By
            is not a string.
        """

        if not self.org_api_key:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, str), \
            "created_by must be a string"
        self.org_api_key.created_by = value
    # createdUTCDateTime

    @property
    def created_utc_date_time(self):
        """
        Returns the value of
        created_utc_date_time attribute of the
        org_api_key.

        Raises:
            AttributeError: If the
                org_api_key is not initialized.

        Returns:
            The value of
            created_utc_date_time
            attribute.
        """
        if not self.org_api_key:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.org_api_key.created_utc_date_time

    @created_utc_date_time.setter
    def created_utc_date_time(self, value):
        """
        Sets the value of
        created_utc_date_time attribute
        for the org_api_key.

        Args:
            value (datetime): The datetime value to be set.

        Raises:
            AttributeError: If the
                org_api_key is not initialized.

        """
        if not self.org_api_key:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, datetime), (
            "created_utc_date_time "
            "must be a datetime object")
        self.org_api_key.created_utc_date_time = value
    # expirationUTCDateTime

    @property
    def expiration_utc_date_time(self):
        """
        Returns the value of
        expiration_utc_date_time attribute of the
        org_api_key.

        Raises:
            AttributeError: If the
                org_api_key is not initialized.

        Returns:
            The value of
            expiration_utc_date_time
            attribute.
        """
        if not self.org_api_key:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.org_api_key.expiration_utc_date_time

    @expiration_utc_date_time.setter
    def expiration_utc_date_time(self, value):
        """
        Sets the value of
        expiration_utc_date_time attribute
        for the org_api_key.

        Args:
            value (datetime): The datetime value to be set.

        Raises:
            AttributeError: If the
                org_api_key is not initialized.

        """
        if not self.org_api_key:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, datetime), (
            "expiration_utc_date_time "
            "must be a datetime object")
        self.org_api_key.expiration_utc_date_time = value
    # isActive

    @property
    def is_active(self):
        """
        Get the Is Active flag from the
        OrgApiKey object.

        :return: The Is Active flag.
        :raises AttributeError: If the
            OrgApiKey object is not initialized.
        """

        if not self.org_api_key:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.org_api_key.is_active

    @is_active.setter
    def is_active(self, value: bool):
        """
        Set the Is Active flag for the
        OrgApiKey object.

        :param value: The Is Active flag value.
        :raises AttributeError: If the
            OrgApiKey object is not initialized.
        :raises ValueError: If the Is Active flag is not a boolean.
        """

        if not self.org_api_key:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, bool):
            raise ValueError(
                "is_active must be a boolean.")

        self.org_api_key.is_active = value
    # isTempUserKey

    @property
    def is_temp_user_key(self):
        """
        Get the Is Temp User Key flag from the
        OrgApiKey object.

        :return: The Is Temp User Key flag.
        :raises AttributeError: If the
            OrgApiKey object is not initialized.
        """

        if not self.org_api_key:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.org_api_key.is_temp_user_key

    @is_temp_user_key.setter
    def is_temp_user_key(self, value: bool):
        """
        Set the Is Temp User Key flag for the
        OrgApiKey object.

        :param value: The Is Temp User Key flag value.
        :raises AttributeError: If the
            OrgApiKey object is not initialized.
        :raises ValueError: If the Is Temp User Key flag is not a boolean.
        """

        if not self.org_api_key:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, bool):
            raise ValueError(
                "is_temp_user_key must be a boolean.")

        self.org_api_key.is_temp_user_key = value
    # name

    @property
    def name(self):
        """
        Get the Name from the
        OrgApiKey object.

        :return: The Name.
        :raises AttributeError: If the
            OrgApiKey object is not initialized.
        """

        if not self.org_api_key:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if self.org_api_key.name is None:
            return ""

        return self.org_api_key.name

    @name.setter
    def name(self, value):
        """
        Set the Name for the
        OrgApiKey object.

        :param value: The Name value.
        :raises AttributeError: If the
            OrgApiKey object is not initialized.
        :raises AssertionError: If the
            Name
            is not a string.
        """

        if not self.org_api_key:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, str), \
            "name must be a string"
        self.org_api_key.name = value
    # OrganizationID
    # OrgCustomerID
    # apiKeyValue
    # createdBy
    # createdUTCDateTime
    # expirationUTCDateTime
    # isActive
    # isTempUserKey
    # name
    # OrganizationID

    @property
    def organization_id(self):
        """
        Returns the organization ID
        associated with the
        org_api_key.

        Raises:
            AttributeError: If the
                org_api_key is not initialized.

        Returns:
            int: The organization ID of the org_api_key.
        """
        if not self.org_api_key:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.org_api_key.organization_id

    @organization_id.setter
    def organization_id(self, value):
        """
        Sets the organization ID
        for the org_api_key.

        Args:
            value (int or None): The
                organization ID to be set.
                Must be an integer or None.

        Raises:
            AttributeError: If the
                org_api_key is not initialized.

        """
        if not self.org_api_key:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, int) or value is None, (
            "organization_id must be an integer or None")

        self.org_api_key.organization_id = value

    @property
    def organization_code_peek(self) -> uuid.UUID:
        """
        Returns the organization id code peek
        of the org_api_key.

        Raises:
            AttributeError: If the
            org_api_key is not initialized.

        Returns:
            uuid.UUID: The organization id code peek
            of the org_api_key.
        """
        if not self.org_api_key:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.org_api_key.organization_code_peek
    # OrgCustomerID

    @property
    def org_customer_id(self):
        """
        Returns the org_customer_id
        of the org_customer
        associated with the
        org_api_key.

        Raises:
            AttributeError: If the
            org_api_key is not initialized.

        Returns:
            int: The foreign key ID of the org_customer.
        """
        if not self.org_api_key:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.org_api_key.org_customer_id

    @org_customer_id.setter
    def org_customer_id(self, value: int):
        """
        Sets the foreign key ID for the
        org_customer of the
        org_api_key.

        Args:
            value (int): The foreign key ID to set.

        Raises:
            AttributeError: If the
                org_api_key is not initialized.
            ValueError: If the value is not an integer.
        """

        if not self.org_api_key:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, int):
            raise ValueError("org_customer_id must be an integer.")

        self.org_api_key.org_customer_id = value

    @property
    def org_customer_code_peek(self) -> uuid.UUID:
        """
        Returns the org_customer_id code peek
        of the org_api_key.

        Raises:
            AttributeError: If the org_api_key
                is not initialized.

        Returns:
            uuid.UUID: The flvr foreign key code peek
            of the org_api_key.
        """
        if not self.org_api_key:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.org_api_key.org_customer_code_peek
    # insert_utc_date_time

    @property
    def insert_utc_date_time(self):
        """
        Inserts the UTC date and time into
        the org_api_key object.

        Raises:
            AttributeError: If the
                org_api_key object is not initialized.

        Returns:
            The UTC date and time inserted into the
            org_api_key object.
        """
        if not self.org_api_key:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.org_api_key.insert_utc_date_time

    @insert_utc_date_time.setter
    def insert_utc_date_time(self, value):
        """
        Inserts the UTC date and time for the
        org_api_key.

        Args:
            value (datetime): The UTC date and time to be inserted.
                It should be a datetime object or None.

        Raises:
            AttributeError: If the
                org_api_key is not initialized.

        """
        if not self.org_api_key:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, datetime) or value is None, (
            "insert_utc_date_time must be "
            "a datetime object or None")

        self.org_api_key.insert_utc_date_time = value

    # update_utc_date_time
    @property
    def last_update_utc_date_time(self):
        """
        Returns the last update UTC date and time
        of the org_api_key.

        Raises:
            AttributeError: If the
                org_api_key is not initialized.

        Returns:
            datetime: The last update UTC date and time
                of the org_api_key.
        """
        if not self.org_api_key:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.org_api_key.last_update_utc_date_time

    @last_update_utc_date_time.setter
    def last_update_utc_date_time(self, value):
        """
        Sets the last update UTC date and time
        for the org_api_key.

        Args:
            value (datetime): The datetime object
                representing the last update UTC date and time.
                Pass None to unset the value.

        Raises:
            AttributeError: If the
                org_api_key is not initialized.

        """
        if not self.org_api_key:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, datetime) or value is None, (
            "last_update_utc_date_time "
            "must be a datetime object or None")

        self.org_api_key.last_update_utc_date_time = value

    async def load_from_json(
        self,
        json_data: str
    ):
        """
        Load org_api_key data
        from JSON string.

        :param json_data: JSON string containing
            org_api_key data.
        :raises ValueError: If json_data is not a string
            or if no org_api_key
            data is found.
        """

        if not isinstance(json_data, str):
            raise ValueError(
                "json_data must be a string")

        org_api_key_manager = OrgApiKeyManager(
            self._session_context)
        self.org_api_key = await \
            org_api_key_manager.from_json(json_data)

        return self

    async def load_from_code(
        self,
        code: uuid.UUID
    ):
        """
        Load org_api_key
        data from UUID code.

        :param code: UUID code for loading a specific
            org_api_key.
        :raises ValueError: If code is not a UUID or if no
            org_api_key data is found.
        """
        if not isinstance(code, uuid.UUID):
            raise ValueError(
                "code must be a UUID")

        org_api_key_manager = OrgApiKeyManager(
            self._session_context)
        org_api_key_obj = await org_api_key_manager.get_by_code(
            code)
        self.org_api_key = org_api_key_obj

        return self

    async def load_from_id(
        self,
        org_api_key_id: int
    ):
        """
        Load org_api_key data from
        org_api_key ID.

        :param org_api_key_id: Integer ID for loading a specific
            org_api_key.
        :raises ValueError: If org_api_key_id
            is not an integer or
            if no org_api_key
            data is found.
        """

        if not isinstance(org_api_key_id, int):
            raise ValueError(
                "org_api_key_id must be an integer")

        org_api_key_manager = OrgApiKeyManager(
            self._session_context)
        org_api_key_obj = await org_api_key_manager.get_by_id(
            org_api_key_id)
        self.org_api_key = org_api_key_obj

        return self

    def load_from_obj_instance(
        self,
        org_api_key_obj_instance: OrgApiKey
    ):
        """
        Use the provided
        OrgApiKey instance.

        :param org_api_key_obj_instance: Instance of the
            OrgApiKey class.
        :raises ValueError: If org_api_key_obj_instance
            is not an instance of
            OrgApiKey.
        """

        if not isinstance(org_api_key_obj_instance,
                          OrgApiKey):
            raise ValueError(
                "org_api_key_obj_instance must be an "
                "instance of OrgApiKey")

        self.org_api_key = org_api_key_obj_instance

        return self

    async def load_from_dict(
        self,
        org_api_key_dict: dict
    ):
        """
        Load org_api_key data
        from dictionary.

        :param org_api_key_dict: Dictionary containing
            org_api_key data.
        :raises ValueError: If org_api_key_dict
            is not a
            dictionary or if no
            org_api_key data is found.
        """
        if not isinstance(org_api_key_dict, dict):
            raise ValueError(
                "org_api_key_dict must be a dictionary")

        org_api_key_manager = OrgApiKeyManager(
            self._session_context)

        self.org_api_key = await \
            org_api_key_manager.from_dict(
                org_api_key_dict)

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
        Refreshes the org_api_key
        object by fetching
        the latest data from the database.

        Returns:
            The updated
            org_api_key object.
        """
        org_api_key_manager = OrgApiKeyManager(
            self._session_context)
        self.org_api_key = await \
            org_api_key_manager.refresh(
                self.org_api_key)

        return self

    def is_valid(self):
        """
        Check if the org_api_key
        is valid.

        Returns:
            bool: True if the org_api_key
                is valid, False otherwise.
        """
        return self.org_api_key is not None

    def to_dict(self):
        """
        Converts the OrgApiKey
        object to a dictionary representation.

        Returns:
            dict: A dictionary representation of the
                OrgApiKey object.
        """
        org_api_key_manager = OrgApiKeyManager(
            self._session_context)
        return org_api_key_manager.to_dict(
            self.org_api_key)

    def to_json(self):
        """
        Converts the org_api_key
        object to a JSON representation.

        Returns:
            str: The JSON representation of the
                org_api_key object.
        """
        org_api_key_manager = OrgApiKeyManager(
            self._session_context)
        return org_api_key_manager.to_json(
            self.org_api_key)

    async def save(self):
        """
        Saves the org_api_key object
        to the database.

        If the org_api_key object
        is not initialized, an AttributeError is raised.
        If the org_api_key_id
        is greater than 0, the
        org_api_key is
        updated in the database.
        If the org_api_key_id is 0,
        the org_api_key is
        added to the database.

        Returns:
            The updated or added
            org_api_key object.

        Raises:
            AttributeError: If the org_api_key
            object is not initialized.
        """
        if not self.org_api_key:
            raise AttributeError(NOT_INITIALIZED_ERROR_MESSAGE)

        org_api_key_id = self.org_api_key.org_api_key_id

        if org_api_key_id > 0:
            org_api_key_manager = OrgApiKeyManager(
                self._session_context)
            self.org_api_key = await \
                org_api_key_manager.update(
                    self.org_api_key)

        if org_api_key_id == 0:
            org_api_key_manager = OrgApiKeyManager(
                self._session_context)
            self.org_api_key = await \
                org_api_key_manager.add(
                    self.org_api_key)

        return self

    async def delete(self):
        """
        Deletes the org_api_key
        from the database.

        Raises:
            AttributeError: If the org_api_key
                is not initialized.
        """
        if not self.org_api_key:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if self.org_api_key.org_api_key_id > 0:
            org_api_key_manager = OrgApiKeyManager(
                self._session_context)
            await org_api_key_manager.delete(
                self.org_api_key.org_api_key_id)
            self.org_api_key = None

    async def randomize_properties(self):
        """
        Randomizes the properties of the
        org_api_key object.

        This method generates random values for various
        properties of the org_api_key
        object

        Returns:
            self: The current instance of the
                OrgApiKey class.

        Raises:
            AttributeError: If the org_api_key
                object is not initialized.
        """
        if not self.org_api_key:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        self.org_api_key.api_key_value = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        self.org_api_key.created_by = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        self.org_api_key.created_utc_date_time = datetime(
            random.randint(2000, 2023),
            random.randint(1, 12),
            random.randint(1, 28))
        self.org_api_key.expiration_utc_date_time = datetime(
            random.randint(2000, 2023),
            random.randint(1, 12),
            random.randint(1, 28))
        self.org_api_key.is_active = (
            random.choice([True, False]))
        self.org_api_key.is_temp_user_key = (
            random.choice([True, False]))
        self.org_api_key.name = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        # organization_id
        self.org_api_key.org_customer_id = random.choice(
            await managers_and_enums.OrgCustomerManager(
                self._session_context).get_list()).org_customer_id

        return self

    def get_org_api_key_obj(self) -> OrgApiKey:
        """
        Returns the org_api_key
        object.

        Raises:
            AttributeError: If the org_api_key
                object is not initialized.

        Returns:
            OrgApiKey: The org_api_key
                object.
        """
        if not self.org_api_key:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.org_api_key

    def is_equal(
        self,
        org_api_key: OrgApiKey
    ) -> bool:
        """
        Checks if the current org_api_key
        is equal to the given org_api_key.

        Args:
            org_api_key (OrgApiKey): The
                org_api_key to compare with.

        Returns:
            bool: True if the org_api_keys
                are equal, False otherwise.
        """
        org_api_key_manager = OrgApiKeyManager(
            self._session_context)
        my_org_api_key = self.get_org_api_key_obj()
        return org_api_key_manager.is_equal(
            org_api_key, my_org_api_key)

    def get_obj(self) -> OrgApiKey:
        """
        Returns the OrgApiKey object.

        :return: The OrgApiKey object.
        :rtype: OrgApiKey
        """

        return self.org_api_key

    def get_object_name(self) -> str:
        """
        Returns the name of the object.

        :return: The name of the object.
        :rtype: str
        """
        return "org_api_key"

    def get_id(self) -> int:
        """
        Returns the ID of the org_api_key.

        :return: The ID of the org_api_key.
        :rtype: int
        """
        return self.org_api_key_id
    # apiKeyValue
    # createdBy
    # createdUTCDateTime
    # expirationUTCDateTime
    # isActive
    # isTempUserKey
    # name
    # OrganizationID

    async def get_parent_name(self) -> str:
        """
        Get the name of the parent org_api_key.

        Returns:
            str: The name of the parent org_api_key.
        """
        return 'Organization'

    async def get_parent_code(self) -> uuid.UUID:
        """
        Get the parent code of the org_api_key.

        Returns:
            The parent code of the org_api_key
            as a UUID.
        """
        return self.organization_code_peek

    async def get_parent_obj(self) -> models.Organization:
        """
        Get the parent object of the current
        org_api_key.

        Returns:
            The parent object of the current
            org_api_key,
            which is an instance of the
            Organization model.
        """
        organization_manager = managers_and_enums.OrganizationManager(
            self._session_context)
        organization_obj = await organization_manager.get_by_id(
            self.organization_id)
        return organization_obj
    # OrgCustomerID
