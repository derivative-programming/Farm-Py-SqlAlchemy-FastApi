# business/org_customer_base.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import

"""
This module contains the
OrgCustomerBaseBusObj class,
which represents the base
business object for a
OrgCustomer.
"""

from decimal import Decimal  # noqa: F401
import random
from typing import Optional
import uuid  # noqa: F401
from datetime import datetime, date  # noqa: F401
from helpers.session_context import SessionContext
from managers import OrgCustomerManager
from models import OrgCustomer
import models
import managers as managers_and_enums
from .base_bus_obj import BaseBusObj

NOT_INITIALIZED_ERROR_MESSAGE = (
    "OrgCustomer object is not initialized")


class OrgCustomerInvalidInitError(Exception):
    """
    Exception raised when the
    OrgCustomer object
    is not initialized properly.
    """


class OrgCustomerBaseBusObj(BaseBusObj):
    """
    This class represents the base business object
    for a OrgCustomer.
    It requires a valid session context for initialization.
    """

    def __init__(
        self,
        session_context: SessionContext,
        org_customer: Optional[OrgCustomer] = None
    ):
        """
        Initializes a new instance of the
        OrgCustomerBusObj class.

        :param session_context: The session context.
        :raises ValueError: If the session is not provided.
        """

        if not session_context.session:
            raise ValueError("session required")

        if org_customer is None:
            org_customer = OrgCustomer()

        self._session_context = session_context

        self.org_customer = org_customer

    @property
    def org_customer_id(self) -> int:
        """
        Get the org_customer ID from the
        OrgCustomer object.

        :return: The org_customer ID.
        :raises AttributeError: If the
            OrgCustomer object is not initialized.
        """

        if not self.org_customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.org_customer.org_customer_id
    # code

    @property
    def code(self):
        """
        Get the code from the
        OrgCustomer object.

        :return: The code.
        :raises AttributeError: If the
            OrgCustomer object is not initialized.
        """

        if not self.org_customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.org_customer.code

    @code.setter
    def code(self, value: uuid.UUID):  # type: ignore
        """
        Set the code for the OrgCustomer object.

        :param value: The code value.
        :raises AttributeError: If the
            OrgCustomer object is not initialized.
        :raises ValueError: If the code is not a UUID.
        """

        if not self.org_customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, uuid.UUID):
            raise ValueError("code must be a UUID.")

        self.org_customer.code = value
    # last_change_code

    @property
    def last_change_code(self):
        """
        Get the last change code from the
        OrgCustomer object.

        :return: The last change code.
        :raises AttributeError: If the
            OrgCustomer object is not initialized.
        """

        if not self.org_customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.org_customer.last_change_code

    @last_change_code.setter
    def last_change_code(self, value: int):
        """
        Set the last change code for the
        OrgCustomer object.

        :param value: The last change code value.
        :raises AttributeError: If the
            OrgCustomer object is not initialized.
        :raises ValueError: If the last change code is not an integer.
        """

        if not self.org_customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, int):
            raise ValueError("last_change_code must be an integer.")

        self.org_customer.last_change_code = value
    # insert_user_id

    @property
    def insert_user_id(self):
        """
        Get the insert user ID from the
        OrgCustomer object.

        :return: The insert user ID.
        :raises AttributeError: If the
            OrgCustomer object is not initialized.
        """

        if not self.org_customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.org_customer.insert_user_id

    @insert_user_id.setter
    def insert_user_id(self, value: uuid.UUID):
        """
        Set the insert user ID for the
        OrgCustomer object.

        :param value: The insert user ID value.
        :raises AttributeError: If the
            OrgCustomer object is not initialized.
        :raises ValueError: If the insert user ID is not a UUID.
        """

        if not self.org_customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, uuid.UUID):
            raise ValueError(
                "insert_user_id must be a UUID.")

        self.org_customer.insert_user_id = value
    # last_update_user_id

    @property
    def last_update_user_id(self):
        """
        Get the last update user ID from the
        OrgCustomer object.

        :return: The last update user ID.
        :raises AttributeError: If the
            OrgCustomer object is not initialized.
        """

        if not self.org_customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.org_customer.last_update_user_id

    @last_update_user_id.setter
    def last_update_user_id(self, value: uuid.UUID):
        """
        Set the last update user ID for the
        OrgCustomer object.

        :param value: The last update user ID value.
        :raises AttributeError: If the
            OrgCustomer object is not initialized.
        :raises ValueError: If the last update user ID is not a UUID.
        """

        if not self.org_customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, uuid.UUID):
            raise ValueError(
                "last_update_user_id must be a UUID.")

        self.org_customer.last_update_user_id = value

    # CustomerID
    # email

    @property
    def email(self):
        """
        Returns the Email
        associated with the org_customer.

        :return: The Email
            of the org_customer.
        :rtype: str
        :raises AttributeError: If the
            org_customer is not initialized.
        """

        if not self.org_customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if self.org_customer.email is None:
            return ""

        return self.org_customer.email

    @email.setter
    def email(self, value):
        """
        Sets the Email
        for the org_customer.

        Args:
            value (str): The Email
                to be set.

        Raises:
            AttributeError: If the
                org_customer is not initialized.

        """
        if not self.org_customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, str), (
            "email must be a string")
        self.org_customer.email = value
    # OrganizationID
    # CustomerID

    @property
    def customer_id(self):
        """
        Returns the customer_id
        of the customer
        associated with the
        org_customer.

        Raises:
            AttributeError: If the
            org_customer is not initialized.

        Returns:
            int: The foreign key ID of the customer.
        """
        if not self.org_customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.org_customer.customer_id

    @customer_id.setter
    def customer_id(self, value: int):
        """
        Sets the foreign key ID for the
        customer of the
        org_customer.

        Args:
            value (int): The foreign key ID to set.

        Raises:
            AttributeError: If the
                org_customer is not initialized.
            ValueError: If the value is not an integer.
        """

        if not self.org_customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, int):
            raise ValueError("customer_id must be an integer.")

        self.org_customer.customer_id = value

    @property
    def customer_code_peek(self) -> uuid.UUID:
        """
        Returns the customer_id code peek
        of the org_customer.

        Raises:
            AttributeError: If the org_customer
                is not initialized.

        Returns:
            uuid.UUID: The flvr foreign key code peek
            of the org_customer.
        """
        if not self.org_customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.org_customer.customer_code_peek
    # email
    # OrganizationID

    @property
    def organization_id(self):
        """
        Returns the organization ID
        associated with the
        org_customer.

        Raises:
            AttributeError: If the
                org_customer is not initialized.

        Returns:
            int: The organization ID of the org_customer.
        """
        if not self.org_customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.org_customer.organization_id

    @organization_id.setter
    def organization_id(self, value):
        """
        Sets the organization ID
        for the org_customer.

        Args:
            value (int or None): The
                organization ID to be set.
                Must be an integer or None.

        Raises:
            AttributeError: If the
                org_customer is not initialized.

        """
        if not self.org_customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, int) or value is None, (
            "organization_id must be an integer or None")

        self.org_customer.organization_id = value

    @property
    def organization_code_peek(self) -> uuid.UUID:
        """
        Returns the organization id code peek
        of the org_customer.

        Raises:
            AttributeError: If the
            org_customer is not initialized.

        Returns:
            uuid.UUID: The organization id code peek
            of the org_customer.
        """
        if not self.org_customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.org_customer.organization_code_peek
    # insert_utc_date_time

    @property
    def insert_utc_date_time(self):
        """
        Inserts the UTC date and time into
        the org_customer object.

        Raises:
            AttributeError: If the
                org_customer object is not initialized.

        Returns:
            The UTC date and time inserted into the
            org_customer object.
        """
        if not self.org_customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.org_customer.insert_utc_date_time

    @insert_utc_date_time.setter
    def insert_utc_date_time(self, value):
        """
        Inserts the UTC date and time for the
        org_customer.

        Args:
            value (datetime): The UTC date and time to be inserted.
                It should be a datetime object or None.

        Raises:
            AttributeError: If the
                org_customer is not initialized.

        """
        if not self.org_customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, datetime) or value is None, (
            "insert_utc_date_time must be "
            "a datetime object or None")

        self.org_customer.insert_utc_date_time = value

    # update_utc_date_time
    @property
    def last_update_utc_date_time(self):
        """
        Returns the last update UTC date and time
        of the org_customer.

        Raises:
            AttributeError: If the
                org_customer is not initialized.

        Returns:
            datetime: The last update UTC date and time
                of the org_customer.
        """
        if not self.org_customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.org_customer.last_update_utc_date_time

    @last_update_utc_date_time.setter
    def last_update_utc_date_time(self, value):
        """
        Sets the last update UTC date and time
        for the org_customer.

        Args:
            value (datetime): The datetime object
                representing the last update UTC date and time.
                Pass None to unset the value.

        Raises:
            AttributeError: If the
                org_customer is not initialized.

        """
        if not self.org_customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, datetime) or value is None, (
            "last_update_utc_date_time "
            "must be a datetime object or None")

        self.org_customer.last_update_utc_date_time = value

    async def load_from_json(
        self,
        json_data: str
    ):
        """
        Load org_customer data
        from JSON string.

        :param json_data: JSON string containing
            org_customer data.
        :raises ValueError: If json_data is not a string
            or if no org_customer
            data is found.
        """

        if not isinstance(json_data, str):
            raise ValueError(
                "json_data must be a string")

        org_customer_manager = OrgCustomerManager(
            self._session_context)
        self.org_customer = await \
            org_customer_manager.from_json(json_data)

        return self

    async def load_from_code(
        self,
        code: uuid.UUID
    ):
        """
        Load org_customer
        data from UUID code.

        :param code: UUID code for loading a specific
            org_customer.
        :raises ValueError: If code is not a UUID or if no
            org_customer data is found.
        """
        if not isinstance(code, uuid.UUID):
            raise ValueError(
                "code must be a UUID")

        org_customer_manager = OrgCustomerManager(
            self._session_context)
        org_customer_obj = await org_customer_manager.get_by_code(
            code)
        self.org_customer = org_customer_obj

        return self

    async def load_from_id(
        self,
        org_customer_id: int
    ):
        """
        Load org_customer data from
        org_customer ID.

        :param org_customer_id: Integer ID for loading a specific
            org_customer.
        :raises ValueError: If org_customer_id
            is not an integer or
            if no org_customer
            data is found.
        """

        if not isinstance(org_customer_id, int):
            raise ValueError(
                "org_customer_id must be an integer")

        org_customer_manager = OrgCustomerManager(
            self._session_context)
        org_customer_obj = await org_customer_manager.get_by_id(
            org_customer_id)
        self.org_customer = org_customer_obj

        return self

    def load_from_obj_instance(
        self,
        org_customer_obj_instance: OrgCustomer
    ):
        """
        Use the provided
        OrgCustomer instance.

        :param org_customer_obj_instance: Instance of the
            OrgCustomer class.
        :raises ValueError: If org_customer_obj_instance
            is not an instance of
            OrgCustomer.
        """

        if not isinstance(org_customer_obj_instance,
                          OrgCustomer):
            raise ValueError(
                "org_customer_obj_instance must be an "
                "instance of OrgCustomer")

        self.org_customer = org_customer_obj_instance

        return self

    async def load_from_dict(
        self,
        org_customer_dict: dict
    ):
        """
        Load org_customer data
        from dictionary.

        :param org_customer_dict: Dictionary containing
            org_customer data.
        :raises ValueError: If org_customer_dict
            is not a
            dictionary or if no
            org_customer data is found.
        """
        if not isinstance(org_customer_dict, dict):
            raise ValueError(
                "org_customer_dict must be a dictionary")

        org_customer_manager = OrgCustomerManager(
            self._session_context)

        self.org_customer = await \
            org_customer_manager.from_dict(
                org_customer_dict)

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
        Refreshes the org_customer
        object by fetching
        the latest data from the database.

        Returns:
            The updated
            org_customer object.
        """
        org_customer_manager = OrgCustomerManager(
            self._session_context)
        self.org_customer = await \
            org_customer_manager.refresh(
                self.org_customer)

        return self

    def is_valid(self):
        """
        Check if the org_customer
        is valid.

        Returns:
            bool: True if the org_customer
                is valid, False otherwise.
        """
        return self.org_customer is not None

    def to_dict(self):
        """
        Converts the OrgCustomer
        object to a dictionary representation.

        Returns:
            dict: A dictionary representation of the
                OrgCustomer object.
        """
        org_customer_manager = OrgCustomerManager(
            self._session_context)
        return org_customer_manager.to_dict(
            self.org_customer)

    def to_json(self):
        """
        Converts the org_customer
        object to a JSON representation.

        Returns:
            str: The JSON representation of the
                org_customer object.
        """
        org_customer_manager = OrgCustomerManager(
            self._session_context)
        return org_customer_manager.to_json(
            self.org_customer)

    async def save(self):
        """
        Saves the org_customer object
        to the database.

        If the org_customer object
        is not initialized, an AttributeError is raised.
        If the org_customer_id
        is greater than 0, the
        org_customer is
        updated in the database.
        If the org_customer_id is 0,
        the org_customer is
        added to the database.

        Returns:
            The updated or added
            org_customer object.

        Raises:
            AttributeError: If the org_customer
            object is not initialized.
        """
        if not self.org_customer:
            raise AttributeError(NOT_INITIALIZED_ERROR_MESSAGE)

        org_customer_id = self.org_customer.org_customer_id

        if org_customer_id > 0:
            org_customer_manager = OrgCustomerManager(
                self._session_context)
            self.org_customer = await \
                org_customer_manager.update(
                    self.org_customer)

        if org_customer_id == 0:
            org_customer_manager = OrgCustomerManager(
                self._session_context)
            self.org_customer = await \
                org_customer_manager.add(
                    self.org_customer)

        return self

    async def delete(self):
        """
        Deletes the org_customer
        from the database.

        Raises:
            AttributeError: If the org_customer
                is not initialized.
        """
        if not self.org_customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if self.org_customer.org_customer_id > 0:
            org_customer_manager = OrgCustomerManager(
                self._session_context)
            await org_customer_manager.delete(
                self.org_customer.org_customer_id)
            self.org_customer = None

    async def randomize_properties(self):
        """
        Randomizes the properties of the
        org_customer object.

        This method generates random values for various
        properties of the org_customer
        object

        Returns:
            self: The current instance of the
                OrgCustomer class.

        Raises:
            AttributeError: If the org_customer
                object is not initialized.
        """
        if not self.org_customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        self.org_customer.customer_id = random.choice(
            await managers_and_enums.CustomerManager(
                self._session_context).get_list()).customer_id
        self.org_customer.email = (
            f"user{random.randint(1, 100)}@abc.com")
        # organization_id

        return self

    def get_org_customer_obj(self) -> OrgCustomer:
        """
        Returns the org_customer
        object.

        Raises:
            AttributeError: If the org_customer
                object is not initialized.

        Returns:
            OrgCustomer: The org_customer
                object.
        """
        if not self.org_customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.org_customer

    def is_equal(
        self,
        org_customer: OrgCustomer
    ) -> bool:
        """
        Checks if the current org_customer
        is equal to the given org_customer.

        Args:
            org_customer (OrgCustomer): The
                org_customer to compare with.

        Returns:
            bool: True if the org_customers
                are equal, False otherwise.
        """
        org_customer_manager = OrgCustomerManager(
            self._session_context)
        my_org_customer = self.get_org_customer_obj()
        return org_customer_manager.is_equal(
            org_customer, my_org_customer)

    def get_obj(self) -> OrgCustomer:
        """
        Returns the OrgCustomer object.

        :return: The OrgCustomer object.
        :rtype: OrgCustomer
        """

        return self.org_customer

    def get_object_name(self) -> str:
        """
        Returns the name of the object.

        :return: The name of the object.
        :rtype: str
        """
        return "org_customer"

    def get_id(self) -> int:
        """
        Returns the ID of the org_customer.

        :return: The ID of the org_customer.
        :rtype: int
        """
        return self.org_customer_id
    # CustomerID
    # email
    # OrganizationID

    async def get_parent_name(self) -> str:
        """
        Get the name of the parent org_customer.

        Returns:
            str: The name of the parent org_customer.
        """
        return 'Organization'

    async def get_parent_code(self) -> uuid.UUID:
        """
        Get the parent code of the org_customer.

        Returns:
            The parent code of the org_customer
            as a UUID.
        """
        return self.organization_code_peek

    async def get_parent_obj(self) -> models.Organization:
        """
        Get the parent object of the current
        org_customer.

        Returns:
            The parent object of the current
            org_customer,
            which is an instance of the
            Organization model.
        """
        organization_manager = managers_and_enums.OrganizationManager(
            self._session_context)
        organization_obj = await organization_manager.get_by_id(
            self.organization_id)
        return organization_obj
