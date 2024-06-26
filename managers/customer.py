# models/managers/customer.py
# pylint: disable=unused-import

"""
This module contains the
CustomerManager class, which is
responsible for managing
customers in the system.
"""

import json
import logging
import uuid  # noqa: F401
from enum import Enum  # noqa: F401
from typing import Any, List, Optional, Dict
from sqlalchemy import and_
from sqlalchemy.future import select
from helpers.session_context import SessionContext
from models.tac import Tac  # TacID
from models.customer import Customer
from models.serialization_schema.customer import CustomerSchema
from services.logging_config import get_logger

logger = get_logger(__name__)


class CustomerNotFoundError(Exception):
    """
    Exception raised when a specified
    customer is not found.

    Attributes:
        message (str): Explanation of the error.
    """
    def __init__(self, message="Customer not found"):
        self.message = message
        super().__init__(self.message)


class CustomerManager:
    """
    The CustomerManager class
    is responsible for managing
    customers in the system.
    It provides methods for adding, updating, deleting,
    and retrieving customers.
    """

    def __init__(self, session_context: SessionContext):
        """
        Initializes a new instance of the
        CustomerManager class.

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
        Initializes the CustomerManager.
        """
        logging.info(
            "CustomerManager.Initialize")


    async def build(self, **kwargs) -> Customer:
        """
        Builds a new Customer
        object with the specified attributes.

        Args:
            **kwargs: The attributes of the
                customer.

        Returns:
            Customer: The newly created
                Customer object.
        """
        logging.info(
            "CustomerManager.build")
        return Customer(**kwargs)

    async def add(
        self,
        customer: Customer
    ) -> Customer:
        """
        Adds a new customer to the system.

        Args:
            customer (Customer): The
                customer to add.

        Returns:
            Customer: The added
                customer.
        """
        logging.info(
            "CustomerManager.add")
        customer.insert_user_id = (
            self._session_context.customer_code)
        customer.last_update_user_id = (
            self._session_context.customer_code)
        self._session_context.session.add(
            customer)
        await self._session_context.session.flush()
        return customer

    def _build_query(self):
        """
        Builds the base query for retrieving
        customers.

        Returns:
            The base query for retrieving
            customers.
        """
        logging.info(
            "CustomerManager._build_query")

        query = select(
            Customer,
            Tac,  # tac_id
        )
        query = query.outerjoin(  # tac_id
            Tac,
            and_(Customer._tac_id == Tac._tac_id,  # pylint: disable=protected-access  # noqa: E501 # type: ignore
                 Customer._tac_id != 0)  # pylint: disable=protected-access  # noqa: E501 # type: ignore
        )

        return query

    async def _run_query(
        self,
        query_filter
    ) -> List[Customer]:
        """
        Runs the query to retrieve
        customers from the database.

        Args:
            query_filter: The filter to apply to the query.

        Returns:
            List[Customer]: The list of
                customers that match the query.
        """
        logging.info(
            "CustomerManager._run_query")
        customer_query_all = self._build_query()

        if query_filter is not None:
            query = customer_query_all.filter(query_filter)
        else:
            query = customer_query_all

        result_proxy = await self._session_context.session.execute(query)

        query_results = result_proxy.all()

        result = list()

        for query_result_row in query_results:
            i = 0
            customer = query_result_row[i]
            i = i + 1
            tac = query_result_row[i]  # tac_id
            i = i + 1
            customer.tac_code_peek = (  # tac_id
                tac.code if tac else uuid.UUID(int=0))
            result.append(customer)

        return result

    def _first_or_none(
        self,
        customer_list: List['Customer']
    ) -> Optional['Customer']:
        """
        Returns the first element of the list if it exists,
        otherwise returns None.

        Args:
            customer_list (List[Customer]):
                The list to retrieve
                the first element from.

        Returns:
            Optional[Customer]: The
                first element of the list
                if it exists, otherwise None.
        """
        return (
            customer_list[0]
            if customer_list
            else None
        )

    async def get_by_id(
        self, customer_id: int
    ) -> Optional[Customer]:
        """
        Retrieves a customer by its ID.

        Args:
            customer_id (int): The ID of the
                customer to retrieve.

        Returns:
            Optional[Customer]: The retrieved
                customer, or None if not found.
        """
        logging.info(
            "CustomerManager.get_by_id start customer_id: %s",
            str(customer_id))
        if not isinstance(customer_id, int):
            raise TypeError(
                "The customer_id must be an integer, "
                f"got {type(customer_id)} instead.")

        query_filter = (
            Customer._customer_id == customer_id)  # pylint: disable=protected-access

        query_results = await self._run_query(query_filter)

        return self._first_or_none(query_results)

    async def get_by_code(
        self, code: uuid.UUID
    ) -> Optional[Customer]:
        """
        Retrieves a customer
        by its code.

        Args:
            code (uuid.UUID): The code of the
                customer to retrieve.

        Returns:
            Optional[Customer]: The retrieved
                customer, or None if not found.
        """
        logging.info("CustomerManager.get_by_code %s",
                     code)

        query_filter = Customer._code == str(code)  # pylint: disable=protected-access  # noqa: E501

        query_results = await self._run_query(query_filter)

        return self._first_or_none(query_results)

    async def update(
        self,
        customer: Customer, **kwargs
    ) -> Optional[Customer]:
        """
        Updates a customer with
        the specified attributes.

        Args:
            customer (Customer): The
                customer to update.
            **kwargs: The attributes to update.

        Returns:
            Optional[Customer]: The updated
                customer, or None if not found.

        Raises:
            ValueError: If an invalid property is provided.
        """
        logging.info("CustomerManager.update")
        property_list = Customer.property_list()
        if customer:
            customer.last_update_user_id = \
                self._session_context.customer_code
            for key, value in kwargs.items():
                if key not in property_list:
                    raise ValueError(f"Invalid property: {key}")
                setattr(customer, key, value)
            await self._session_context.session.flush()
        return customer

    async def delete(self, customer_id: int):
        """
        Deletes a customer by its ID.

        Args:
            customer_id (int): The ID of the
                customer to delete.

        Raises:
            TypeError: If the customer_id
                is not an integer.
            CustomerNotFoundError: If the
                customer with the
                specified ID is not found.
        """
        logging.info(
            "CustomerManager.delete %s",
            customer_id)
        if not isinstance(customer_id, int):
            raise TypeError(
                f"The customer_id must be an integer, "
                f"got {type(customer_id)} instead."
            )
        customer = await self.get_by_id(
            customer_id)
        if not customer:
            raise CustomerNotFoundError(
                f"Customer with ID {customer_id} not found!")

        await self._session_context.session.delete(
            customer)

        await self._session_context.session.flush()

    async def get_list(
        self
    ) -> List[Customer]:
        """
        Retrieves a list of all customers.

        Returns:
            List[Customer]: The list of
                customers.
        """
        logging.info(
            "CustomerManager.get_list")

        query_results = await self._run_query(None)

        return query_results

    def to_json(
            self,
            customer: Customer) -> str:
        """
        Serializes a Customer object
        to a JSON string.

        Args:
            customer (Customer): The
                customer to serialize.

        Returns:
            str: The JSON string representation of the
                customer.
        """
        logging.info(
            "CustomerManager.to_json")
        schema = CustomerSchema()
        customer_data = schema.dump(customer)
        return json.dumps(customer_data)

    def to_dict(
        self,
        customer: Customer
    ) -> Dict[str, Any]:
        """
        Serializes a Customer
        object to a dictionary.

        Args:
            customer (Customer): The
                customer to serialize.

        Returns:
            Dict[str, Any]: The dictionary representation of the
                customer.
        """
        logging.info(
            "CustomerManager.to_dict")
        schema = CustomerSchema()
        customer_data = schema.dump(customer)

        assert isinstance(customer_data, dict)

        return customer_data

    async def from_json(self, json_str: str) -> Customer:
        """
        Deserializes a JSON string into a
        Customer object.

        Args:
            json_str (str): The JSON string to deserialize.

        Returns:
            Customer: The deserialized
                Customer object.
        """
        logging.info(
            "CustomerManager.from_json")
        schema = CustomerSchema()
        data = json.loads(json_str)
        customer_dict = schema.load(data)

        #we need to load the obj form db and into session first.
        # If not found, then no chagnes can be saved

        # new_customer = Customer(**customer_dict)

        # load or create
        new_customer = await self.get_by_id(
            customer_dict["customer_id"])
        if new_customer is None:
            new_customer = Customer(**customer_dict)
            self._session_context.session.add(new_customer)
        else:
            for key, value in customer_dict.items():
                setattr(new_customer, key, value)

        return new_customer

    async def from_dict(
        self, customer_dict: Dict[str, Any]
    ) -> Customer:
        """
        Creates a Customer
        instance from a dictionary of attributes.

        Args:
            customer_dict (Dict[str, Any]): A dictionary
                containing customer
                attributes.

        Returns:
            Customer: A new
                Customer instance
                created from the given
                dictionary.
        """
        logging.info(
            "CustomerManager.from_dict")

        # Deserialize the dictionary into a validated schema object
        schema = CustomerSchema()
        customer_dict_converted = schema.load(
            customer_dict)

        #we need to load the obj form db and into session first.
        # If not found, then no chagnes can be saved

        # Create a new Customer instance
        # using the validated data
        # new_customer = Customer(**customer_dict_converted)

        # load or create
        new_customer = await self.get_by_id(
            customer_dict_converted["customer_id"])
        if new_customer is None:
            new_customer = Customer(**customer_dict_converted)
            self._session_context.session.add(new_customer)
        else:
            for key, value in customer_dict_converted.items():
                setattr(new_customer, key, value)

        return new_customer

    async def add_bulk(
        self,
        customers: List[Customer]
    ) -> List[Customer]:
        """
        Adds multiple customers
        to the system.

        Args:
            customers (List[Customer]): The list of
                customers to add.

        Returns:
            List[Customer]: The added
                customers.
        """
        logging.info(
            "CustomerManager.add_bulk")
        for list_item in customers:
            customer_id = \
                list_item.customer_id
            code = list_item.code
            if list_item.customer_id is not None and \
                    list_item.customer_id > 0:
                raise ValueError(
                    "Customer is already added"
                    f": {str(code)} {str(customer_id)}"
                )
            list_item.insert_user_id = (
                self._session_context.customer_code)
            list_item.last_update_user_id = (
                self._session_context.customer_code)
        self._session_context.session.add_all(customers)
        await self._session_context.session.flush()
        return customers

    async def update_bulk(
        self,
        customer_updates: List[Dict[str, Any]]
    ) -> List[Customer]:
        """
        Update multiple customers
        with the provided updates.

        Args:
            customer_updates (List[Dict[str, Any]]): A list of
            dictionaries containing the updates for each
            customer.

        Returns:
            List[Customer]: A list of updated
                Customer objects.

        Raises:
            TypeError: If the customer_id is not an integer.
            CustomerNotFoundError: If a
                customer with the
                provided customer_id is not found.
        """

        logging.info(
            "CustomerManager.update_bulk start")
        updated_customers = []
        for update in customer_updates:
            customer_id = update.get("customer_id")
            if not isinstance(customer_id, int):
                raise TypeError(
                    f"The customer_id must be an integer, "
                    f"got {type(customer_id)} instead."
                )
            if not customer_id:
                continue

            logging.info(
                "CustomerManager.update_bulk customer_id:%s",
                customer_id)

            customer = await self.get_by_id(
                customer_id)

            if not customer:
                raise CustomerNotFoundError(
                    f"Customer with ID {customer_id} not found!")

            for key, value in update.items():
                if key != "customer_id":
                    setattr(customer, key, value)

            customer.last_update_user_id =\
                self._session_context.customer_code

            updated_customers.append(customer)

        await self._session_context.session.flush()

        logging.info(
            "CustomerManager.update_bulk end")

        return updated_customers

    async def delete_bulk(self, customer_ids: List[int]) -> bool:
        """
        Delete multiple customers
        by their IDs.
        """
        logging.info(
            "CustomerManager.delete_bulk")

        for customer_id in customer_ids:
            if not isinstance(customer_id, int):
                raise TypeError(
                    f"The customer_id must be an integer, "
                    f"got {type(customer_id)} instead."
                )

            customer = await self.get_by_id(
                customer_id)
            if not customer:
                raise CustomerNotFoundError(
                    f"Customer with ID {customer_id} not found!"
                )

            if customer:
                await self._session_context.session.delete(
                    customer)

        await self._session_context.session.flush()

        return True

    async def count(self) -> int:
        """
        return the total number of
        customers.
        """
        logging.info(
            "CustomerManager.count")
        result = await self._session_context.session.execute(
            select(Customer))
        return len(list(result.scalars().all()))

    async def refresh(
        self,
        customer: Customer
    ) -> Customer:
        """
        Refresh the state of a given
        customer instance
        from the database.
        """

        logging.info(
            "CustomerManager.refresh")

        await self._session_context.session.refresh(customer)

        return customer

    async def exists(self, customer_id: int) -> bool:
        """
        Check if a customer
        with the given ID exists.
        """
        logging.info(
            "CustomerManager.exists %s",
            customer_id)
        if not isinstance(customer_id, int):
            raise TypeError(
                f"The customer_id must be an integer, "
                f"got {type(customer_id)} instead."
            )
        customer = await self.get_by_id(
            customer_id)
        return bool(customer)

    def is_equal(
        self,
        customer1: Customer,
        customer2: Customer
    ) -> bool:
        """
        Check if two Customer
        objects are equal.

        Args:
            customer1 (Customer): The first
                Customer object.
            customer2 (Customer): The second
                Customer object.

        Returns:
            bool: True if the two Customer
                objects are equal, False otherwise.

        Raises:
            TypeError: If either customer1
                or customer2
                is not provided or is not an instance of
                Customer.
        """
        if not customer1:
            raise TypeError("Customer1 required.")

        if not customer2:
            raise TypeError("Customer2 required.")

        if not isinstance(customer1,
                          Customer):
            raise TypeError("The customer1 must be an "
                            "Customer instance.")

        if not isinstance(customer2,
                          Customer):
            raise TypeError("The customer2 must be an "
                            "Customer instance.")

        dict1 = self.to_dict(customer1)
        dict2 = self.to_dict(customer2)

        return dict1 == dict2
    # TacID
    async def get_by_tac_id(
            self,
            tac_id: int) -> List[Customer]:
        """
        Retrieve a list of customers by
        tac ID.

        Args:
            tac_id (int): The ID of the tac.

        Returns:
            List[Customer]: A list of
                customers associated
                with the specified tac ID.
        """

        logging.info(
            "CustomerManager.get_by_tac_id")
        if not isinstance(tac_id, int):
            raise TypeError(
                f"The customer_id must be an integer, "
                f"got {type(tac_id)} instead."
            )

        query_filter = Customer._tac_id == tac_id  # pylint: disable=protected-access  # noqa: E501

        query_results = await self._run_query(query_filter)

        return query_results
    async def get_by_email_prop(
        self,
        email
    ) -> List[Customer]:
        logging.info(
            "CustomerManager"
            ".get_by_email_prop")
        query_filter = (
            Customer._email == email)  # pylint: disable=protected-access  # noqa: E501
        query_results = await self._run_query(query_filter)
        return query_results
    async def get_by_fs_user_code_value_prop(
        self,
        fs_user_code_value
    ) -> List[Customer]:
        logging.info(
            "CustomerManager"
            ".get_by_fs_user_code_value_prop")
        query_filter = (
            Customer._fs_user_code_value == fs_user_code_value)  # pylint: disable=protected-access  # noqa: E501
        query_results = await self._run_query(query_filter)
        return query_results
