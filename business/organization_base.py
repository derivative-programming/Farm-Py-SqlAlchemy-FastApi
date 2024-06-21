# business/organization_base.py
"""
This module contains the OrganizationBusObj class,
which represents the business object for a Organization.
"""
from decimal import Decimal
import random
import uuid
from typing import List
from datetime import datetime, date
from helpers.session_context import SessionContext
from managers import OrganizationManager
from models import Organization
import models
import managers as managers_and_enums
from .base_bus_obj import BaseBusObj
NOT_INITIALIZED_ERROR_MESSAGE = (
    "Organization object is not initialized")
class OrganizationInvalidInitError(Exception):
    """
    Exception raised when the
    Organization object
    is not initialized properly.
    """
class OrganizationBaseBusObj(BaseBusObj):
    """
    This class represents the base business object
    for a Organization.
    It requires a valid session context for initialization.
    """
    def __init__(self, session_context: SessionContext):
        """
        Initializes a new instance of the
        OrganizationBusObj class.
        :param session_context: The session context.
        :raises ValueError: If the session is not provided.
        """
        if not session_context.session:
            raise ValueError("session required")
        self._session_context = session_context
        self.organization = Organization()
    @property
    def organization_id(self) -> int:
        """
        Get the organization ID from the
        Organization object.
        :return: The organization ID.
        :raises AttributeError: If the
            Organization object is not initialized.
        """
        if not self.organization:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.organization.organization_id
    # code
    @property
    def code(self):
        """
        Get the code from the
        Organization object.
        :return: The code.
        :raises AttributeError: If the
            Organization object is not initialized.
        """
        if not self.organization:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.organization.code
    @code.setter
    def code(self, value: uuid.UUID):  # type: ignore
        """
        Set the code for the Organization object.
        :param value: The code value.
        :raises AttributeError: If the
            Organization object is not initialized.
        :raises ValueError: If the code is not a UUID.
        """
        if not self.organization:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if not isinstance(value, uuid.UUID):
            raise ValueError("code must be a UUID.")
        self.organization.code = value
    # last_change_code
    @property
    def last_change_code(self):
        """
        Get the last change code from the
        Organization object.
        :return: The last change code.
        :raises AttributeError: If the
            Organization object is not initialized.
        """
        if not self.organization:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.organization.last_change_code
    @last_change_code.setter
    def last_change_code(self, value: int):
        """
        Set the last change code for the
        Organization object.
        :param value: The last change code value.
        :raises AttributeError: If the
            Organization object is not initialized.
        :raises ValueError: If the last change code is not an integer.
        """
        if not self.organization:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if not isinstance(value, int):
            raise ValueError("last_change_code must be an integer.")
        self.organization.last_change_code = value
    # insert_user_id
    @property
    def insert_user_id(self):
        """
        Get the insert user ID from the
        Organization object.
        :return: The insert user ID.
        :raises AttributeError: If the
            Organization object is not initialized.
        """
        if not self.organization:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.organization.insert_user_id
    @insert_user_id.setter
    def insert_user_id(self, value: uuid.UUID):
        """
        Set the insert user ID for the
        Organization object.
        :param value: The insert user ID value.
        :raises AttributeError: If the
            Organization object is not initialized.
        :raises ValueError: If the insert user ID is not a UUID.
        """
        if not self.organization:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if not isinstance(value, uuid.UUID):
            raise ValueError("insert_user_id must be a UUID.")
        self.organization.insert_user_id = value
    # last_update_user_id
    @property
    def last_update_user_id(self):
        """
        Get the last update user ID from the
        Organization object.
        :return: The last update user ID.
        :raises AttributeError: If the
            Organization object is not initialized.
        """
        if not self.organization:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.organization.last_update_user_id
    @last_update_user_id.setter
    def last_update_user_id(self, value: uuid.UUID):
        """
        Set the last update user ID for the
        Organization object.
        :param value: The last update user ID value.
        :raises AttributeError: If the
            Organization object is not initialized.
        :raises ValueError: If the last update user ID is not a UUID.
        """
        if not self.organization:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if not isinstance(value, uuid.UUID):
            raise ValueError("last_update_user_id must be a UUID.")
        self.organization.last_update_user_id = value
# endset
    # name
    @property
    def name(self):
        """
        Get the Name from the
        Organization object.
        :return: The Name.
        :raises AttributeError: If the
            Organization object is not initialized.
        """
        if not self.organization:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if self.organization.name is None:
            return ""
        return self.organization.name
    @name.setter
    def name(self, value):
        """
        Set the Name for the
        Organization object.
        :param value: The Name value.
        :raises AttributeError: If the
            Organization object is not initialized.
        :raises AssertionError: If the Name is not a string.
        """
        if not self.organization:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, str), "name must be a string"
        self.organization.name = value
    # TacID
# endset
    # name,
    # TacID
    @property
    def tac_id(self):
        """
        Returns the tac ID
        associated with the
        organization.
        Raises:
            AttributeError: If the
                organization is not initialized.
        Returns:
            int: The tac ID of the organization.
        """
        if not self.organization:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.organization.tac_id
    @tac_id.setter
    def tac_id(self, value):
        """
        Sets the tac ID
        for the organization.
        Args:
            value (int or None): The
                tac ID to be set.
                Must be an integer or None.
        Raises:
            AttributeError: If the
                organization is not initialized.
        """
        if not self.organization:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, int) or value is None, (
            "tac_id must be an integer or None")
        self.organization.tac_id = value
    @property
    def tac_code_peek(self) -> uuid.UUID:
        """
        Returns the tac id code peek
        of the organization.
        Raises:
            AttributeError: If the
            organization is not initialized.
        Returns:
            uuid.UUID: The tac id code peek
            of the organization.
        """
        if not self.organization:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.organization.tac_code_peek
    # @tac_code_peek.setter
    # def tac_code_peek(self, value):
    #     assert isinstance(value, uuid.UUID),
    #           "tac_code_peek must be a UUID"
    #     self.organization.tac_code_peek = value
# endset
    # insert_utc_date_time
    @property
    def insert_utc_date_time(self):
        """
        Inserts the UTC date and time into
        the organization object.
        Raises:
            AttributeError: If the
                organization object is not initialized.
        Returns:
            The UTC date and time inserted into the
            organization object.
        """
        if not self.organization:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.organization.insert_utc_date_time
    @insert_utc_date_time.setter
    def insert_utc_date_time(self, value):
        """
        Inserts the UTC date and time for the
        organization.
        Args:
            value (datetime): The UTC date and time to be inserted.
                It should be a datetime object or None.
        Raises:
            AttributeError: If the
                organization is not initialized.
        """
        if not self.organization:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, datetime) or value is None, (
            "insert_utc_date_time must be a datetime object or None")
        self.organization.insert_utc_date_time = value
    # update_utc_date_time
    @property
    def last_update_utc_date_time(self):
        """
        Returns the last update UTC date and time
        of the organization.
        Raises:
            AttributeError: If the
                organization is not initialized.
        Returns:
            datetime: The last update UTC date and time
                of the organization.
        """
        if not self.organization:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.organization.last_update_utc_date_time
    @last_update_utc_date_time.setter
    def last_update_utc_date_time(self, value):
        """
        Sets the last update UTC date and time
        for the organization.
        Args:
            value (datetime): The datetime object
                representing the last update UTC date and time.
                Pass None to unset the value.
        Raises:
            AttributeError: If the
                organization is not initialized.
        """
        if not self.organization:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, datetime) or value is None, (
            "last_update_utc_date_time must be a datetime object or None")
        self.organization.last_update_utc_date_time = value
    async def load_from_json(
        self,
        json_data: str
    ):
        """
        Load organization data
        from JSON string.
        :param json_data: JSON string containing
            organization data.
        :raises ValueError: If json_data is not a string
            or if no organization
            data is found.
        """
        if not isinstance(json_data, str):
            raise ValueError("json_data must be a string")
        organization_manager = OrganizationManager(
            self._session_context)
        self.organization = organization_manager.from_json(json_data)
        return self
    async def load_from_code(
        self,
        code: uuid.UUID
    ):
        """
        Load organization
        data from UUID code.
        :param code: UUID code for loading a specific
            organization.
        :raises ValueError: If code is not a UUID or if no
            organization data is found.
        """
        if not isinstance(code, uuid.UUID):
            raise ValueError("code must be a UUID")
        organization_manager = OrganizationManager(
            self._session_context)
        organization_obj = await organization_manager.get_by_code(
            code)
        self.organization = organization_obj
        return self
    async def load_from_id(
        self,
        organization_id: int
    ):
        """
        Load organization data from
        organization ID.
        :param organization_id: Integer ID for loading a specific
            organization.
        :raises ValueError: If organization_id
            is not an integer or
            if no organization
            data is found.
        """
        if not isinstance(organization_id, int):
            raise ValueError("organization_id must be an integer")
        organization_manager = OrganizationManager(
            self._session_context)
        organization_obj = await organization_manager.get_by_id(
            organization_id)
        self.organization = organization_obj
        return self
    async def load_from_obj_instance(
        self,
        organization_obj_instance: Organization
    ):
        """
        Use the provided
        Organization instance.
        :param organization_obj_instance: Instance of the
            Organization class.
        :raises ValueError: If organization_obj_instance
            is not an instance of
            Organization.
        """
        if not isinstance(organization_obj_instance,
                          Organization):
            raise ValueError("organization_obj_instance must be an instance of Organization")
        organization_manager = OrganizationManager(
            self._session_context)
        organization_obj_instance_organization_id = organization_obj_instance.organization_id
        organization_obj = await organization_manager.get_by_id(
            organization_obj_instance_organization_id
        )
        self.organization = organization_obj
        return self
    async def load_from_dict(
        self,
        organization_dict: dict
    ):
        """
        Load organization data
        from dictionary.
        :param organization_dict: Dictionary containing
            organization data.
        :raises ValueError: If organization_dict
            is not a
            dictionary or if no
            organization data is found.
        """
        if not isinstance(organization_dict, dict):
            raise ValueError("organization_dict must be a dictionary")
        organization_manager = OrganizationManager(
            self._session_context)
        self.organization = organization_manager.from_dict(
            organization_dict)
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
        Refreshes the organization
        object by fetching
        the latest data from the database.
        Returns:
            The updated
            organization object.
        """
        organization_manager = OrganizationManager(
            self._session_context)
        self.organization = await organization_manager.refresh(
            self.organization)
        return self
    def is_valid(self):
        """
        Check if the organization
        is valid.
        Returns:
            bool: True if the organization
                is valid, False otherwise.
        """
        return self.organization is not None
    def to_dict(self):
        """
        Converts the Organization
        object to a dictionary representation.
        Returns:
            dict: A dictionary representation of the
                Organization object.
        """
        organization_manager = OrganizationManager(
            self._session_context)
        return organization_manager.to_dict(
            self.organization)
    def to_json(self):
        """
        Converts the organization
        object to a JSON representation.
        Returns:
            str: The JSON representation of the
                organization object.
        """
        organization_manager = OrganizationManager(
            self._session_context)
        return organization_manager.to_json(
            self.organization)
    async def save(self):
        """
        Saves the organization object
        to the database.
        If the organization object
        is not initialized, an AttributeError is raised.
        If the organization_id
        is greater than 0, the
        organization is
        updated in the database.
        If the organization_id is 0,
        the organization is
        added to the database.
        Returns:
            The updated or added
            organization object.
        Raises:
            AttributeError: If the organization
            object is not initialized.
        """
        if not self.organization:
            raise AttributeError(NOT_INITIALIZED_ERROR_MESSAGE)
        organization_id = self.organization.organization_id
        if organization_id > 0:
            organization_manager = OrganizationManager(
                self._session_context)
            self.organization = await organization_manager.update(
                self.organization)
        if organization_id == 0:
            organization_manager = OrganizationManager(
                self._session_context)
            self.organization = await organization_manager.add(
                self.organization)
        return self
    async def delete(self):
        """
        Deletes the organization
        from the database.
        Raises:
            AttributeError: If the organization
                is not initialized.
        """
        if not self.organization:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if self.organization.organization_id > 0:
            organization_manager = OrganizationManager(
                self._session_context)
            await organization_manager.delete(
                self.organization.organization_id)
            self.organization = None
    async def randomize_properties(self):
        """
        Randomizes the properties of the
        organization object.
        This method generates random values for various
        properties of the organization
        object
        Returns:
            self: The current instance of the
                Organization class.
        Raises:
            AttributeError: If the organization
                object is not initialized.
        """
        if not self.organization:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        self.organization.name = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        # self.organization.tac_id = random.randint(0, 100)
# endset
        return self
    def get_organization_obj(self) -> Organization:
        """
        Returns the organization
        object.
        Raises:
            AttributeError: If the organization
                object is not initialized.
        Returns:
            Organization: The organization
                object.
        """
        if not self.organization:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.organization
    def is_equal(
        self,
        organization: Organization
    ) -> bool:
        """
        Checks if the current organization
        is equal to the given organization.
        Args:
            organization (Organization): The
                organization to compare with.
        Returns:
            bool: True if the organizations
                are equal, False otherwise.
        """
        organization_manager = OrganizationManager(
            self._session_context)
        my_organization = self.get_organization_obj()
        return organization_manager.is_equal(
            organization, my_organization)
# endset
    # name,
    # TacID
    async def get_tac_id_rel_obj(self) -> models.Tac:
        """
        Retrieves the related Tac object based
        on the tac_id.
        Returns:
            An instance of the Tac model
            representing the related tac.
        """
        tac_manager = managers_and_enums.TacManager(self._session_context)
        tac_obj = await tac_manager.get_by_id(self.tac_id)
        return tac_obj
# endset
    def get_obj(self) -> Organization:
        """
        Returns the Organization object.
        :return: The Organization object.
        :rtype: Organization
        """
        return self.organization
    def get_object_name(self) -> str:
        """
        Returns the name of the object.
        :return: The name of the object.
        :rtype: str
        """
        return "organization"
    def get_id(self) -> int:
        """
        Returns the ID of the organization.
        :return: The ID of the organization.
        :rtype: int
        """
        return self.organization_id
    # name,
    # TacID
    async def get_parent_name(self) -> str:
        """
        Get the name of the parent organization.
        Returns:
            str: The name of the parent organization.
        """
        return 'Tac'
    async def get_parent_code(self) -> uuid.UUID:
        """
        Get the parent code of the organization.
        Returns:
            The parent code of the organization
            as a UUID.
        """
        return self.tac_code_peek
    async def get_parent_obj(self) -> models.Tac:
        """
        Get the parent object of the current
        organization.
        Returns:
            The parent object of the current
            organization,
            which is an instance of the
            Tac model.
        """
        tac = await self.get_tac_id_rel_obj()
        return tac
# endset
