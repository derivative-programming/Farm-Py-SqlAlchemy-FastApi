# business/customer_role_base.py
"""
This module contains the CustomerRoleBaseBusObj class,
which represents the base business object for a CustomerRole.
"""
from decimal import Decimal
import random
import uuid
from datetime import datetime, date
from helpers.session_context import SessionContext
from managers import CustomerRoleManager
from models import CustomerRole
import models
import managers as managers_and_enums
from .base_bus_obj import BaseBusObj
NOT_INITIALIZED_ERROR_MESSAGE = (
    "CustomerRole object is not initialized")
class CustomerRoleInvalidInitError(Exception):
    """
    Exception raised when the
    CustomerRole object
    is not initialized properly.
    """
class CustomerRoleBaseBusObj(BaseBusObj):
    """
    This class represents the base business object
    for a CustomerRole.
    It requires a valid session context for initialization.
    """
    def __init__(self, session_context: SessionContext):
        """
        Initializes a new instance of the
        CustomerRoleBusObj class.
        :param session_context: The session context.
        :raises ValueError: If the session is not provided.
        """
        if not session_context.session:
            raise ValueError("session required")
        self._session_context = session_context
        self.customer_role = CustomerRole()
    @property
    def customer_role_id(self) -> int:
        """
        Get the customer_role ID from the
        CustomerRole object.
        :return: The customer_role ID.
        :raises AttributeError: If the
            CustomerRole object is not initialized.
        """
        if not self.customer_role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.customer_role.customer_role_id
    # code
    @property
    def code(self):
        """
        Get the code from the
        CustomerRole object.
        :return: The code.
        :raises AttributeError: If the
            CustomerRole object is not initialized.
        """
        if not self.customer_role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.customer_role.code
    @code.setter
    def code(self, value: uuid.UUID):  # type: ignore
        """
        Set the code for the CustomerRole object.
        :param value: The code value.
        :raises AttributeError: If the
            CustomerRole object is not initialized.
        :raises ValueError: If the code is not a UUID.
        """
        if not self.customer_role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if not isinstance(value, uuid.UUID):
            raise ValueError("code must be a UUID.")
        self.customer_role.code = value
    # last_change_code
    @property
    def last_change_code(self):
        """
        Get the last change code from the
        CustomerRole object.
        :return: The last change code.
        :raises AttributeError: If the
            CustomerRole object is not initialized.
        """
        if not self.customer_role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.customer_role.last_change_code
    @last_change_code.setter
    def last_change_code(self, value: int):
        """
        Set the last change code for the
        CustomerRole object.
        :param value: The last change code value.
        :raises AttributeError: If the
            CustomerRole object is not initialized.
        :raises ValueError: If the last change code is not an integer.
        """
        if not self.customer_role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if not isinstance(value, int):
            raise ValueError("last_change_code must be an integer.")
        self.customer_role.last_change_code = value
    # insert_user_id
    @property
    def insert_user_id(self):
        """
        Get the insert user ID from the
        CustomerRole object.
        :return: The insert user ID.
        :raises AttributeError: If the
            CustomerRole object is not initialized.
        """
        if not self.customer_role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.customer_role.insert_user_id
    @insert_user_id.setter
    def insert_user_id(self, value: uuid.UUID):
        """
        Set the insert user ID for the
        CustomerRole object.
        :param value: The insert user ID value.
        :raises AttributeError: If the
            CustomerRole object is not initialized.
        :raises ValueError: If the insert user ID is not a UUID.
        """
        if not self.customer_role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if not isinstance(value, uuid.UUID):
            raise ValueError("insert_user_id must be a UUID.")
        self.customer_role.insert_user_id = value
    # last_update_user_id
    @property
    def last_update_user_id(self):
        """
        Get the last update user ID from the
        CustomerRole object.
        :return: The last update user ID.
        :raises AttributeError: If the
            CustomerRole object is not initialized.
        """
        if not self.customer_role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.customer_role.last_update_user_id
    @last_update_user_id.setter
    def last_update_user_id(self, value: uuid.UUID):
        """
        Set the last update user ID for the
        CustomerRole object.
        :param value: The last update user ID value.
        :raises AttributeError: If the
            CustomerRole object is not initialized.
        :raises ValueError: If the last update user ID is not a UUID.
        """
        if not self.customer_role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if not isinstance(value, uuid.UUID):
            raise ValueError("last_update_user_id must be a UUID.")
        self.customer_role.last_update_user_id = value
# endset
    # CustomerID
    # isPlaceholder
    @property
    def is_placeholder(self):
        """
        Get the Is Placeholder flag from the
        CustomerRole object.
        :return: The Is Placeholder flag.
        :raises AttributeError: If the
            CustomerRole object is not initialized.
        """
        if not self.customer_role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.customer_role.is_placeholder
    @is_placeholder.setter
    def is_placeholder(self, value: bool):
        """
        Set the Is Placeholder flag for the
        CustomerRole object.
        :param value: The Is Placeholder flag value.
        :raises AttributeError: If the
            CustomerRole object is not initialized.
        :raises ValueError: If the Is Placeholder flag is not a boolean.
        """
        if not self.customer_role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if not isinstance(value, bool):
            raise ValueError("is_placeholder must be a boolean.")
        self.customer_role.is_placeholder = value
    # placeholder
    @property
    def placeholder(self):
        """
        Get the Placeholder flag from the
        CustomerRole object.
        :return: The Placeholder flag.
        :raises AttributeError: If the
            CustomerRole object is not initialized.
        """
        if not self.customer_role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.customer_role.placeholder
    @placeholder.setter
    def placeholder(self, value: bool):
        """
        Set the Placeholder flag for the
        CustomerRole object.
        :param value: The Placeholder flag value.
        :raises AttributeError: If the
            CustomerRole object is not initialized.
        :raises ValueError: If the Placeholder flag is not a boolean.
        """
        if not self.customer_role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if not isinstance(value, bool):
            raise ValueError("placeholder must be a boolean.")
        self.customer_role.placeholder = value
    # RoleID
# endset
    # CustomerID
    @property
    def customer_id(self):
        """
        Returns the customer ID
        associated with the
        customer_role.
        Raises:
            AttributeError: If the
                customer_role is not initialized.
        Returns:
            int: The customer ID of the customer_role.
        """
        if not self.customer_role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.customer_role.customer_id
    @customer_id.setter
    def customer_id(self, value):
        """
        Sets the customer ID
        for the customer_role.
        Args:
            value (int or None): The
                customer ID to be set.
                Must be an integer or None.
        Raises:
            AttributeError: If the
                customer_role is not initialized.
        """
        if not self.customer_role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, int) or value is None, (
            "customer_id must be an integer or None")
        self.customer_role.customer_id = value
    @property
    def customer_code_peek(self) -> uuid.UUID:
        """
        Returns the customer id code peek
        of the customer_role.
        Raises:
            AttributeError: If the
            customer_role is not initialized.
        Returns:
            uuid.UUID: The customer id code peek
            of the customer_role.
        """
        if not self.customer_role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.customer_role.customer_code_peek
    # @customer_code_peek.setter
    # def customer_code_peek(self, value):
    #     assert isinstance(value, uuid.UUID),
    #           "customer_code_peek must be a UUID"
    #     self.customer_role.customer_code_peek = value
    # isPlaceholder,
    # placeholder,
    # RoleID
    @property
    def role_id(self):
        """
        Returns the role_id
        of the role
        associated with the
        customer_role.
        Raises:
            AttributeError: If the
            customer_role is not initialized.
        Returns:
            int: The foreign key ID of the role.
        """
        if not self.customer_role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.customer_role.role_id
    @role_id.setter
    def role_id(self, value: int):
        """
        Sets the foreign key ID for the
        role of the
        customer_role.
        Args:
            value (int): The foreign key ID to set.
        Raises:
            AttributeError: If the
                customer_role is not initialized.
            ValueError: If the value is not an integer.
        """
        if not self.customer_role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if not isinstance(value, int):
            raise ValueError("role_id must be an integer.")
        self.customer_role.role_id = value
    @property
    def role_code_peek(self) -> uuid.UUID:
        """
        Returns the role_id code peek
        of the customer_role.
        Raises:
            AttributeError: If the customer_role
                is not initialized.
        Returns:
            uuid.UUID: The flvr foreign key code peek
            of the customer_role.
        """
        if not self.customer_role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.customer_role.role_code_peek
    # @role_code_peek.setter
    # def role_code_peek(self, value):
    #     assert isinstance(
    #       value, uuid.UUID),
    #       "role_code_peek must be a UUID"
    #     self.customer_role.role_code_peek = value
# endset
    # insert_utc_date_time
    @property
    def insert_utc_date_time(self):
        """
        Inserts the UTC date and time into
        the customer_role object.
        Raises:
            AttributeError: If the
                customer_role object is not initialized.
        Returns:
            The UTC date and time inserted into the
            customer_role object.
        """
        if not self.customer_role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.customer_role.insert_utc_date_time
    @insert_utc_date_time.setter
    def insert_utc_date_time(self, value):
        """
        Inserts the UTC date and time for the
        customer_role.
        Args:
            value (datetime): The UTC date and time to be inserted.
                It should be a datetime object or None.
        Raises:
            AttributeError: If the
                customer_role is not initialized.
        """
        if not self.customer_role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, datetime) or value is None, (
            "insert_utc_date_time must be a datetime object or None")
        self.customer_role.insert_utc_date_time = value
    # update_utc_date_time
    @property
    def last_update_utc_date_time(self):
        """
        Returns the last update UTC date and time
        of the customer_role.
        Raises:
            AttributeError: If the
                customer_role is not initialized.
        Returns:
            datetime: The last update UTC date and time
                of the customer_role.
        """
        if not self.customer_role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.customer_role.last_update_utc_date_time
    @last_update_utc_date_time.setter
    def last_update_utc_date_time(self, value):
        """
        Sets the last update UTC date and time
        for the customer_role.
        Args:
            value (datetime): The datetime object
                representing the last update UTC date and time.
                Pass None to unset the value.
        Raises:
            AttributeError: If the
                customer_role is not initialized.
        """
        if not self.customer_role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, datetime) or value is None, (
            "last_update_utc_date_time must be a datetime object or None")
        self.customer_role.last_update_utc_date_time = value
    async def load_from_json(
        self,
        json_data: str
    ):
        """
        Load customer_role data
        from JSON string.
        :param json_data: JSON string containing
            customer_role data.
        :raises ValueError: If json_data is not a string
            or if no customer_role
            data is found.
        """
        if not isinstance(json_data, str):
            raise ValueError("json_data must be a string")
        customer_role_manager = CustomerRoleManager(
            self._session_context)
        self.customer_role = customer_role_manager.from_json(json_data)
        return self
    async def load_from_code(
        self,
        code: uuid.UUID
    ):
        """
        Load customer_role
        data from UUID code.
        :param code: UUID code for loading a specific
            customer_role.
        :raises ValueError: If code is not a UUID or if no
            customer_role data is found.
        """
        if not isinstance(code, uuid.UUID):
            raise ValueError("code must be a UUID")
        customer_role_manager = CustomerRoleManager(
            self._session_context)
        customer_role_obj = await customer_role_manager.get_by_code(
            code)
        self.customer_role = customer_role_obj
        return self
    async def load_from_id(
        self,
        customer_role_id: int
    ):
        """
        Load customer_role data from
        customer_role ID.
        :param customer_role_id: Integer ID for loading a specific
            customer_role.
        :raises ValueError: If customer_role_id
            is not an integer or
            if no customer_role
            data is found.
        """
        if not isinstance(customer_role_id, int):
            raise ValueError("customer_role_id must be an integer")
        customer_role_manager = CustomerRoleManager(
            self._session_context)
        customer_role_obj = await customer_role_manager.get_by_id(
            customer_role_id)
        self.customer_role = customer_role_obj
        return self
    async def load_from_obj_instance(
        self,
        customer_role_obj_instance: CustomerRole
    ):
        """
        Use the provided
        CustomerRole instance.
        :param customer_role_obj_instance: Instance of the
            CustomerRole class.
        :raises ValueError: If customer_role_obj_instance
            is not an instance of
            CustomerRole.
        """
        if not isinstance(customer_role_obj_instance,
                          CustomerRole):
            raise ValueError("customer_role_obj_instance must be an instance of CustomerRole")
        customer_role_manager = CustomerRoleManager(
            self._session_context)
        customer_role_obj_instance_customer_role_id = customer_role_obj_instance.customer_role_id
        customer_role_obj = await customer_role_manager.get_by_id(
            customer_role_obj_instance_customer_role_id
        )
        self.customer_role = customer_role_obj
        return self
    async def load_from_dict(
        self,
        customer_role_dict: dict
    ):
        """
        Load customer_role data
        from dictionary.
        :param customer_role_dict: Dictionary containing
            customer_role data.
        :raises ValueError: If customer_role_dict
            is not a
            dictionary or if no
            customer_role data is found.
        """
        if not isinstance(customer_role_dict, dict):
            raise ValueError("customer_role_dict must be a dictionary")
        customer_role_manager = CustomerRoleManager(
            self._session_context)
        self.customer_role = customer_role_manager.from_dict(
            customer_role_dict)
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
        Refreshes the customer_role
        object by fetching
        the latest data from the database.
        Returns:
            The updated
            customer_role object.
        """
        customer_role_manager = CustomerRoleManager(
            self._session_context)
        self.customer_role = await customer_role_manager.refresh(
            self.customer_role)
        return self
    def is_valid(self):
        """
        Check if the customer_role
        is valid.
        Returns:
            bool: True if the customer_role
                is valid, False otherwise.
        """
        return self.customer_role is not None
    def to_dict(self):
        """
        Converts the CustomerRole
        object to a dictionary representation.
        Returns:
            dict: A dictionary representation of the
                CustomerRole object.
        """
        customer_role_manager = CustomerRoleManager(
            self._session_context)
        return customer_role_manager.to_dict(
            self.customer_role)
    def to_json(self):
        """
        Converts the customer_role
        object to a JSON representation.
        Returns:
            str: The JSON representation of the
                customer_role object.
        """
        customer_role_manager = CustomerRoleManager(
            self._session_context)
        return customer_role_manager.to_json(
            self.customer_role)
    async def save(self):
        """
        Saves the customer_role object
        to the database.
        If the customer_role object
        is not initialized, an AttributeError is raised.
        If the customer_role_id
        is greater than 0, the
        customer_role is
        updated in the database.
        If the customer_role_id is 0,
        the customer_role is
        added to the database.
        Returns:
            The updated or added
            customer_role object.
        Raises:
            AttributeError: If the customer_role
            object is not initialized.
        """
        if not self.customer_role:
            raise AttributeError(NOT_INITIALIZED_ERROR_MESSAGE)
        customer_role_id = self.customer_role.customer_role_id
        if customer_role_id > 0:
            customer_role_manager = CustomerRoleManager(
                self._session_context)
            self.customer_role = await customer_role_manager.update(
                self.customer_role)
        if customer_role_id == 0:
            customer_role_manager = CustomerRoleManager(
                self._session_context)
            self.customer_role = await customer_role_manager.add(
                self.customer_role)
        return self
    async def delete(self):
        """
        Deletes the customer_role
        from the database.
        Raises:
            AttributeError: If the customer_role
                is not initialized.
        """
        if not self.customer_role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if self.customer_role.customer_role_id > 0:
            customer_role_manager = CustomerRoleManager(
                self._session_context)
            await customer_role_manager.delete(
                self.customer_role.customer_role_id)
            self.customer_role = None
    async def randomize_properties(self):
        """
        Randomizes the properties of the
        customer_role object.
        This method generates random values for various
        properties of the customer_role
        object
        Returns:
            self: The current instance of the
                CustomerRole class.
        Raises:
            AttributeError: If the customer_role
                object is not initialized.
        """
        if not self.customer_role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        # self.customer_role.customer_id = random.randint(0, 100)
        self.customer_role.is_placeholder = (
            random.choice([True, False]))
        self.customer_role.placeholder = (
            random.choice([True, False]))
        self.customer_role.role_id = random.choice(
            await managers_and_enums.RoleManager(
                self._session_context).get_list()).role_id
# endset
        return self
    def get_customer_role_obj(self) -> CustomerRole:
        """
        Returns the customer_role
        object.
        Raises:
            AttributeError: If the customer_role
                object is not initialized.
        Returns:
            CustomerRole: The customer_role
                object.
        """
        if not self.customer_role:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.customer_role
    def is_equal(
        self,
        customer_role: CustomerRole
    ) -> bool:
        """
        Checks if the current customer_role
        is equal to the given customer_role.
        Args:
            customer_role (CustomerRole): The
                customer_role to compare with.
        Returns:
            bool: True if the customer_roles
                are equal, False otherwise.
        """
        customer_role_manager = CustomerRoleManager(
            self._session_context)
        my_customer_role = self.get_customer_role_obj()
        return customer_role_manager.is_equal(
            customer_role, my_customer_role)
# endset
    # CustomerID
    async def get_customer_id_rel_obj(self) -> models.Customer:
        """
        Retrieves the related Customer object based
        on the customer_id.
        Returns:
            An instance of the Customer model
            representing the related customer.
        """
        customer_manager = managers_and_enums.CustomerManager(self._session_context)
        customer_obj = await customer_manager.get_by_id(self.customer_id)
        return customer_obj
    # isPlaceholder,
    # placeholder,
    # RoleID
    async def get_role_id_rel_obj(self) -> models.Role:
        """
        Retrieves the related Role object based on the
        role_id.
        Returns:
            The related Role object.
        """
        role_manager = managers_and_enums.RoleManager(
            self._session_context)
        role_obj = await role_manager.get_by_id(
            self.role_id
        )
        return role_obj
# endset
    def get_obj(self) -> CustomerRole:
        """
        Returns the CustomerRole object.
        :return: The CustomerRole object.
        :rtype: CustomerRole
        """
        return self.customer_role
    def get_object_name(self) -> str:
        """
        Returns the name of the object.
        :return: The name of the object.
        :rtype: str
        """
        return "customer_role"
    def get_id(self) -> int:
        """
        Returns the ID of the customer_role.
        :return: The ID of the customer_role.
        :rtype: int
        """
        return self.customer_role_id
    # CustomerID
    async def get_parent_name(self) -> str:
        """
        Get the name of the parent customer_role.
        Returns:
            str: The name of the parent customer_role.
        """
        return 'Customer'
    async def get_parent_code(self) -> uuid.UUID:
        """
        Get the parent code of the customer_role.
        Returns:
            The parent code of the customer_role
            as a UUID.
        """
        return self.customer_code_peek
    async def get_parent_obj(self) -> models.Customer:
        """
        Get the parent object of the current
        customer_role.
        Returns:
            The parent object of the current
            customer_role,
            which is an instance of the
            Customer model.
        """
        customer = await self.get_customer_id_rel_obj()
        return customer
    # isPlaceholder,
    # placeholder,
    # RoleID
# endset
