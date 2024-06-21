# models/managers/customer_role.py
# pylint: disable=unused-import
"""
This module contains the
CustomerRoleManager class, which is
responsible for managing
customer_roles in the system.
"""
import json
import logging
import uuid
from enum import Enum  # noqa: F401
from typing import Any, List, Optional, Dict
from sqlalchemy import and_
from sqlalchemy.future import select
from helpers.session_context import SessionContext
from models.customer import Customer  # CustomerID
from models.role import Role  # RoleID
from models.customer_role import CustomerRole
from models.serialization_schema.customer_role import CustomerRoleSchema
from services.logging_config import get_logger
logger = get_logger(__name__)
class CustomerRoleNotFoundError(Exception):
    """
    Exception raised when a specified
    customer_role is not found.
    Attributes:
        message (str): Explanation of the error.
    """
    def __init__(self, message="CustomerRole not found"):
        self.message = message
        super().__init__(self.message)

class CustomerRoleManager:
    """
    The CustomerRoleManager class
    is responsible for managing
    customer_roles in the system.
    It provides methods for adding, updating, deleting,
    and retrieving customer_roles.
    """
    def __init__(self, session_context: SessionContext):
        """
        Initializes a new instance of the
        CustomerRoleManager class.
        Args:
            session_context (SessionContext): The session context object.
                Must contain a valid session.
        Raises:
            ValueError: If the session is not provided.
        """
        if not session_context.session:
            raise ValueError("session required")
        self._session_context = session_context

    async def initialize(self):
        """
        Initializes the CustomerRoleManager.
        """
        logging.info("CustomerRoleManager.Initialize")

    async def build(self, **kwargs) -> CustomerRole:
        """
        Builds a new CustomerRole
        object with the specified attributes.
        Args:
            **kwargs: The attributes of the
                customer_role.
        Returns:
            CustomerRole: The newly created
                CustomerRole object.
        """
        logging.info("CustomerRoleManager.build")
        return CustomerRole(**kwargs)
    async def add(
        self,
        customer_role: CustomerRole
    ) -> CustomerRole:
        """
        Adds a new customer_role to the system.
        Args:
            customer_role (CustomerRole): The
                customer_role to add.
        Returns:
            CustomerRole: The added
                customer_role.
        """
        logging.info("CustomerRoleManager.add")
        customer_role.insert_user_id = self._session_context.customer_code
        customer_role.last_update_user_id = self._session_context.customer_code
        self._session_context.session.add(
            customer_role)
        await self._session_context.session.flush()
        return customer_role
    def _build_query(self):
        """
        Builds the base query for retrieving
        customer_roles.
        Returns:
            The base query for retrieving
            customer_roles.
        """
        logging.info("CustomerRoleManager._build_query")
        query = select(
            CustomerRole,
            Customer,  # customer_id
            Role,  # role_id
        )
# endset
        query = query.outerjoin(  # customer_id
            Customer,
            and_(CustomerRole._customer_id == Customer._customer_id,  # pylint: disable=protected-access  # noqa: E501 # type: ignore
                 CustomerRole._customer_id != 0)  # pylint: disable=protected-access  # noqa: E501 # type: ignore
        )
        query = query.outerjoin(  # role_id
            Role,
            and_(CustomerRole._role_id == Role._role_id,  # pylint: disable=protected-access  # noqa: E501 # type: ignore
                 CustomerRole._role_id != 0)  # pylint: disable=protected-access  # noqa: E501 # type: ignore
        )
# endset
        return query
    async def _run_query(
        self,
        query_filter
    ) -> List[CustomerRole]:
        """
        Runs the query to retrieve
        customer_roles from the database.
        Args:
            query_filter: The filter to apply to the query.
        Returns:
            List[CustomerRole]: The list of
                customer_roles that match the query.
        """
        logging.info("CustomerRoleManager._run_query")
        customer_role_query_all = self._build_query()
        if query_filter is not None:
            query = customer_role_query_all.filter(query_filter)
        else:
            query = customer_role_query_all
        result_proxy = await self._session_context.session.execute(query)
        query_results = result_proxy.all()
        result = list()
        for query_result_row in query_results:
            i = 0
            customer_role = query_result_row[i]
            i = i + 1
# endset
            customer = query_result_row[i]  # customer_id
            i = i + 1
            role = query_result_row[i]  # role_id
            i = i + 1
# endset
            customer_role.customer_code_peek = (  # customer_id
                customer.code if customer else uuid.UUID(int=0))
            customer_role.role_code_peek = (  # role_id
                role.code if role else uuid.UUID(int=0))
# endset
            result.append(customer_role)
        return result
    def _first_or_none(
        self,
        customer_role_list: List['CustomerRole']
    ) -> Optional['CustomerRole']:
        """
        Returns the first element of the list if it exists,
        otherwise returns None.
        Args:
            customer_role_list (List[CustomerRole]):
                The list to retrieve
                the first element from.
        Returns:
            Optional[CustomerRole]: The
                first element of the list
                if it exists, otherwise None.
        """
        return (
            customer_role_list[0]
            if customer_role_list
            else None
        )
    async def get_by_id(self, customer_role_id: int) -> Optional[CustomerRole]:
        """
        Retrieves a customer_role by its ID.
        Args:
            customer_role_id (int): The ID of the
                customer_role to retrieve.
        Returns:
            Optional[CustomerRole]: The retrieved
                customer_role, or None if not found.
        """
        logging.info(
            "CustomerRoleManager.get_by_id start customer_role_id: %s",
            str(customer_role_id))
        if not isinstance(customer_role_id, int):
            raise TypeError(
                "The customer_role_id must be an integer, "
                f"got {type(customer_role_id)} instead.")
        query_filter = (
            CustomerRole._customer_role_id == customer_role_id)  # pylint: disable=protected-access
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)
    async def get_by_code(self, code: uuid.UUID) -> Optional[CustomerRole]:
        """
        Retrieves a customer_role
        by its code.
        Args:
            code (uuid.UUID): The code of the
                customer_role to retrieve.
        Returns:
            Optional[CustomerRole]: The retrieved
                customer_role, or None if not found.
        """
        logging.info("CustomerRoleManager.get_by_code %s", code)
        query_filter = CustomerRole._code == str(code)  # pylint: disable=protected-access  # noqa: E501
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)
    async def update(
        self,
        customer_role: CustomerRole, **kwargs
    ) -> Optional[CustomerRole]:
        """
        Updates a customer_role with
        the specified attributes.
        Args:
            customer_role (CustomerRole): The
                customer_role to update.
            **kwargs: The attributes to update.
        Returns:
            Optional[CustomerRole]: The updated
                customer_role, or None if not found.
        Raises:
            ValueError: If an invalid property is provided.
        """
        logging.info("CustomerRoleManager.update")
        property_list = CustomerRole.property_list()
        if customer_role:
            customer_role.last_update_user_id = self._session_context.customer_code
            for key, value in kwargs.items():
                if key not in property_list:
                    raise ValueError(f"Invalid property: {key}")
                setattr(customer_role, key, value)
            await self._session_context.session.flush()
        return customer_role
    async def delete(self, customer_role_id: int):
        """
        Deletes a customer_role by its ID.
        Args:
            customer_role_id (int): The ID of the
                customer_role to delete.
        Raises:
            TypeError: If the customer_role_id
                is not an integer.
            CustomerRoleNotFoundError: If the
                customer_role with the
                specified ID is not found.
        """
        logging.info("CustomerRoleManager.delete %s", customer_role_id)
        if not isinstance(customer_role_id, int):
            raise TypeError(
                f"The customer_role_id must be an integer, "
                f"got {type(customer_role_id)} instead."
            )
        customer_role = await self.get_by_id(
            customer_role_id)
        if not customer_role:
            raise CustomerRoleNotFoundError(f"CustomerRole with ID {customer_role_id} not found!")
        await self._session_context.session.delete(
            customer_role)
        await self._session_context.session.flush()
    async def get_list(
        self
    ) -> List[CustomerRole]:
        """
        Retrieves a list of all customer_roles.
        Returns:
            List[CustomerRole]: The list of
                customer_roles.
        """
        logging.info("CustomerRoleManager.get_list")
        query_results = await self._run_query(None)
        return query_results
    def to_json(
            self,
            customer_role: CustomerRole) -> str:
        """
        Serializes a CustomerRole object
        to a JSON string.
        Args:
            customer_role (CustomerRole): The
                customer_role to serialize.
        Returns:
            str: The JSON string representation of the
                customer_role.
        """
        logging.info("CustomerRoleManager.to_json")
        schema = CustomerRoleSchema()
        customer_role_data = schema.dump(customer_role)
        return json.dumps(customer_role_data)
    def to_dict(
        self,
        customer_role: CustomerRole
    ) -> Dict[str, Any]:
        """
        Serializes a CustomerRole
        object to a dictionary.
        Args:
            customer_role (CustomerRole): The
                customer_role to serialize.
        Returns:
            Dict[str, Any]: The dictionary representation of the
                customer_role.
        """
        logging.info("CustomerRoleManager.to_dict")
        schema = CustomerRoleSchema()
        customer_role_data = schema.dump(customer_role)
        assert isinstance(customer_role_data, dict)
        return customer_role_data
    def from_json(self, json_str: str) -> CustomerRole:
        """
        Deserializes a JSON string into a
        CustomerRole object.
        Args:
            json_str (str): The JSON string to deserialize.
        Returns:
            CustomerRole: The deserialized
                CustomerRole object.
        """
        logging.info("CustomerRoleManager.from_json")
        schema = CustomerRoleSchema()
        data = json.loads(json_str)
        customer_role_dict = schema.load(data)
        new_customer_role = CustomerRole(**customer_role_dict)
        return new_customer_role
    def from_dict(self, customer_role_dict: Dict[str, Any]) -> CustomerRole:
        """
        Creates a CustomerRole
        instance from a dictionary of attributes.
        Args:
            customer_role_dict (Dict[str, Any]): A dictionary
                containing customer_role
                attributes.
        Returns:
            CustomerRole: A new
                CustomerRole instance
                created from the given
                dictionary.
        """
        logging.info("CustomerRoleManager.from_dict")
        # Deserialize the dictionary into a validated schema object
        schema = CustomerRoleSchema()
        customer_role_dict_converted = schema.load(
            customer_role_dict)
        # Create a new CustomerRole instance
        # using the validated data
        new_customer_role = CustomerRole(**customer_role_dict_converted)
        return new_customer_role
    async def add_bulk(
        self,
        customer_roles: List[CustomerRole]
    ) -> List[CustomerRole]:
        """
        Adds multiple customer_roles
        to the system.
        Args:
            customer_roles (List[CustomerRole]): The list of
                customer_roles to add.
        Returns:
            List[CustomerRole]: The added
                customer_roles.
        """
        logging.info("CustomerRoleManager.add_bulk")
        for customer_role in customer_roles:
            customer_role_id = customer_role.customer_role_id
            code = customer_role.code
            if customer_role.customer_role_id is not None and customer_role.customer_role_id > 0:
                raise ValueError(
                    "CustomerRole is already added"
                    f": {str(code)} {str(customer_role_id)}"
                )
            customer_role.insert_user_id = self._session_context.customer_code
            customer_role.last_update_user_id = self._session_context.customer_code
        self._session_context.session.add_all(customer_roles)
        await self._session_context.session.flush()
        return customer_roles
    async def update_bulk(
        self,
        customer_role_updates: List[Dict[str, Any]]
    ) -> List[CustomerRole]:
        """
        Update multiple customer_roles
        with the provided updates.
        Args:
            customer_role_updates (List[Dict[str, Any]]): A list of
            dictionaries containing the updates for each
            customer_role.
        Returns:
            List[CustomerRole]: A list of updated
                CustomerRole objects.
        Raises:
            TypeError: If the customer_role_id is not an integer.
            CustomerRoleNotFoundError: If a
                customer_role with the
                provided customer_role_id is not found.
        """
        logging.info("CustomerRoleManager.update_bulk start")
        updated_customer_roles = []
        for update in customer_role_updates:
            customer_role_id = update.get("customer_role_id")
            if not isinstance(customer_role_id, int):
                raise TypeError(
                    f"The customer_role_id must be an integer, "
                    f"got {type(customer_role_id)} instead."
                )
            if not customer_role_id:
                continue
            logging.info("CustomerRoleManager.update_bulk customer_role_id:%s", customer_role_id)
            customer_role = await self.get_by_id(
                customer_role_id)
            if not customer_role:
                raise CustomerRoleNotFoundError(
                    f"CustomerRole with ID {customer_role_id} not found!")
            for key, value in update.items():
                if key != "customer_role_id":
                    setattr(customer_role, key, value)
            customer_role.last_update_user_id = self._session_context.customer_code
            updated_customer_roles.append(customer_role)
        await self._session_context.session.flush()
        logging.info("CustomerRoleManager.update_bulk end")
        return updated_customer_roles
    async def delete_bulk(self, customer_role_ids: List[int]) -> bool:
        """
        Delete multiple customer_roles
        by their IDs.
        """
        logging.info("CustomerRoleManager.delete_bulk")
        for customer_role_id in customer_role_ids:
            if not isinstance(customer_role_id, int):
                raise TypeError(
                    f"The customer_role_id must be an integer, "
                    f"got {type(customer_role_id)} instead."
                )
            customer_role = await self.get_by_id(
                customer_role_id)
            if not customer_role:
                raise CustomerRoleNotFoundError(
                    f"CustomerRole with ID {customer_role_id} not found!"
                )
            if customer_role:
                await self._session_context.session.delete(
                    customer_role)
        await self._session_context.session.flush()
        return True
    async def count(self) -> int:
        """
        return the total number of
        customer_roles.
        """
        logging.info("CustomerRoleManager.count")
        result = await self._session_context.session.execute(
            select(CustomerRole))
        return len(list(result.scalars().all()))
    #TODO fix. needs to populate peek props. use getall and sort List
    async def get_sorted_list(
        self,
        sort_by: str,
        order: Optional[str] = "asc"
    ) -> List[CustomerRole]:
        """
        Retrieve customer_roles
        sorted by a particular attribute.
        """
        if sort_by == "customer_role_id":
            sort_by = "_customer_role_id"
        if order == "asc":
            result = await self._session_context.session.execute(
                select(CustomerRole).order_by(
                    getattr(CustomerRole, sort_by).asc()))
        else:
            result = await self._session_context.session.execute(
                select(CustomerRole).order_by(
                    getattr(CustomerRole, sort_by).desc()))
        return list(result.scalars().all())
    async def refresh(
        self,
        customer_role: CustomerRole
    ) -> CustomerRole:
        """
        Refresh the state of a given
        customer_role instance
        from the database.
        """
        logging.info("CustomerRoleManager.refresh")
        await self._session_context.session.refresh(customer_role)
        return customer_role
    async def exists(self, customer_role_id: int) -> bool:
        """
        Check if a customer_role
        with the given ID exists.
        """
        logging.info("CustomerRoleManager.exists %s", customer_role_id)
        if not isinstance(customer_role_id, int):
            raise TypeError(
                f"The customer_role_id must be an integer, "
                f"got {type(customer_role_id)} instead."
            )
        customer_role = await self.get_by_id(
            customer_role_id)
        return bool(customer_role)
    def is_equal(
        self,
        customer_role1: CustomerRole,
        customer_role2: CustomerRole
    ) -> bool:
        """
        Check if two CustomerRole
        objects are equal.
        Args:
            customer_role1 (CustomerRole): The first
                CustomerRole object.
            customer_role2 (CustomerRole): The second
                CustomerRole object.
        Returns:
            bool: True if the two CustomerRole
                objects are equal, False otherwise.
        Raises:
            TypeError: If either customer_role1
                or customer_role2
                is not provided or is not an instance of
                CustomerRole.
        """
        if not customer_role1:
            raise TypeError("CustomerRole1 required.")
        if not customer_role2:
            raise TypeError("CustomerRole2 required.")
        if not isinstance(customer_role1, CustomerRole):
            raise TypeError("The customer_role1 must be an "
                            "CustomerRole instance.")
        if not isinstance(customer_role2, CustomerRole):
            raise TypeError("The customer_role2 must be an "
                            "CustomerRole instance.")
        dict1 = self.to_dict(customer_role1)
        dict2 = self.to_dict(customer_role2)
        return dict1 == dict2
# endset
    async def get_by_customer_id(self, customer_id: int) -> List[CustomerRole]:  # CustomerID
        """
        Retrieve a list of customer_roles by
        customer ID.
        Args:
            customer_id (int): The ID of the customer.
        Returns:
            List[CustomerRole]: A list of
                customer_roles associated
                with the specified customer ID.
        """
        logging.info("CustomerRoleManager.get_by_customer_id")
        if not isinstance(customer_id, int):
            raise TypeError(
                f"The customer_role_id must be an integer, "
                f"got {type(customer_id)} instead."
            )
        query_filter = CustomerRole._customer_id == customer_id  # pylint: disable=protected-access  # noqa: E501
        query_results = await self._run_query(query_filter)
        return query_results
    async def get_by_role_id(
        self,
        role_id: int
    ) -> List[CustomerRole]:  # RoleID
        """
        Retrieve a list of customer_roles
            based on the
            given role_id.
        Args:
            role_id (int): The
                role_id
                to filter the
                customer_roles.
        Returns:
            List[CustomerRole]: A list of CustomerRole
                objects
                matching the given
                role_id.
        """
        logging.info("CustomerRoleManager.get_by_role_id")
        if not isinstance(role_id, int):
            raise TypeError(
                f"The customer_role_id must be an integer, "
                f"got {type(role_id)} instead."
            )
        query_filter = CustomerRole._role_id == role_id  # pylint: disable=protected-access  # noqa: E501
        query_results = await self._run_query(query_filter)
        return query_results
# endset

