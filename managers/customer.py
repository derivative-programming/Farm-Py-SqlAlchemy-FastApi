# models/managers/customer.py
# pylint: disable=unused-import
"""
This module contains the CustomerManager class, which is
responsible for managing customers in the system.
"""
import json
import logging
import uuid
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
    Exception raised when a specified customer is not found.
    Attributes:
        message (str):Explanation of the error.
    """
    def __init__(self, message="Customer not found"):
        self.message = message
        super().__init__(self.message)

class CustomerManager:
    """
    #TODO add comment
    """
    def __init__(self, session_context: SessionContext):
        """
            #TODO add comment
        """
        if not session_context.session:
            raise ValueError("session required")
        self._session_context = session_context
    def convert_uuid_to_model_uuid(self, value: uuid.UUID):
        """
            #TODO add comment
        """
        # Conditionally set the UUID column type
        return value

    async def initialize(self):
        """
            #TODO add comment
        """
        logging.info("CustomerManager.Initialize")

    async def build(self, **kwargs) -> Customer:
        """
            #TODO add comment
        """
        logging.info("CustomerManager.build")
        return Customer(**kwargs)
    async def add(self, customer: Customer) -> Customer:
        """
            #TODO add comment
        """
        logging.info("CustomerManager.add")
        customer.insert_user_id = self.convert_uuid_to_model_uuid(
            self._session_context.customer_code)
        customer.last_update_user_id = self.convert_uuid_to_model_uuid(
            self._session_context.customer_code)
        self._session_context.session.add(customer)
        await self._session_context.session.flush()
        return customer
    def _build_query(self):
        """
            #TODO add comment
        """
        logging.info("CustomerManager._build_query")
        query = select(
            Customer,
            Tac,  # tac_id
        )
# endset
        query = query.outerjoin(  # tac_id
            Tac,
            and_(Customer._tac_id == Tac._tac_id,  # pylint: disable=protected-access  # noqa: E501 # type: ignore
                 Customer._tac_id != 0)  # pylint: disable=protected-access  # noqa: E501 # type: ignore
        )
# endset
        return query
    async def _run_query(self, query_filter) -> List[Customer]:
        """
            #TODO add comment
        """
        logging.info("CustomerManager._run_query")
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
# endset
            tac = query_result_row[i]  # tac_id
            i = i + 1
# endset
            customer.tac_code_peek = (  # tac_id
                tac.code if tac else uuid.UUID(int=0))
# endset
            result.append(customer)
        return result
    def _first_or_none(
        self,
        customer_list: List['Customer']
    ) -> Optional['Customer']:
        """
        Return the first element of the list if it exists,
        otherwise return None.
        Args:
            customer_list (List[Customer]):
                The list to retrieve the first element from.
        Returns:
            Optional[Customer]: The first element
                of the list if it exists, otherwise None.
        """
        return (
            customer_list[0]
            if customer_list
            else None
        )
    async def get_by_id(self, customer_id: int) -> Optional[Customer]:
        """
            #TODO add comment
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
    async def get_by_code(self, code: uuid.UUID) -> Optional[Customer]:
        """
            #TODO add comment
        """
        logging.info("CustomerManager.get_by_code %s", code)
        query_filter = Customer._code == str(code)  # pylint: disable=protected-access  # noqa: E501
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)
    async def update(self, customer: Customer, **kwargs) -> Optional[Customer]:
        """
            #TODO add comment
        """
        logging.info("CustomerManager.update")
        property_list = Customer.property_list()
        if customer:
            customer.last_update_user_id = self.convert_uuid_to_model_uuid(
                self._session_context.customer_code)
            for key, value in kwargs.items():
                if key not in property_list:
                    raise ValueError(f"Invalid property: {key}")
                setattr(customer, key, value)
            await self._session_context.session.flush()
        return customer
    async def delete(self, customer_id: int):
        """
            #TODO add comment
        """
        logging.info("CustomerManager.delete %s", customer_id)
        if not isinstance(customer_id, int):
            raise TypeError(
                f"The customer_id must be an integer, "
                f"got {type(customer_id)} instead."
            )
        customer = await self.get_by_id(customer_id)
        if not customer:
            raise CustomerNotFoundError(f"Customer with ID {customer_id} not found!")
        await self._session_context.session.delete(customer)
        await self._session_context.session.flush()
    async def get_list(self) -> List[Customer]:
        """
            #TODO add comment
        """
        logging.info("CustomerManager.get_list")
        query_results = await self._run_query(None)
        return query_results
    def to_json(self, customer: Customer) -> str:
        """
        Serialize the Customer object to a JSON string using the CustomerSchema.
        """
        logging.info("CustomerManager.to_json")
        schema = CustomerSchema()
        customer_data = schema.dump(customer)
        return json.dumps(customer_data)
    def to_dict(self, customer: Customer) -> Dict[str, Any]:
        """
        Serialize the Customer object to a JSON string using the CustomerSchema.
        """
        logging.info("CustomerManager.to_dict")
        schema = CustomerSchema()
        customer_data = schema.dump(customer)
        assert isinstance(customer_data, dict)
        return customer_data
    def from_json(self, json_str: str) -> Customer:
        """
        Deserializes a JSON string into a Customer object using the CustomerSchema.
        Args:
            json_str (str): The JSON string to deserialize.
        Returns:
            Customer: The deserialized Customer object.
        """
        logging.info("CustomerManager.from_json")
        schema = CustomerSchema()
        data = json.loads(json_str)
        customer_dict = schema.load(data)
        new_customer = Customer(**customer_dict)
        return new_customer
    def from_dict(self, customer_dict: Dict[str, Any]) -> Customer:
        """
        Creates a Customer instance from a dictionary of attributes.
        Args:
            customer_dict (Dict[str, Any]): A dictionary containing
                customer attributes.
        Returns:
            Customer: A new Customer instance created from the given dictionary.
        """
        logging.info("CustomerManager.from_dict")
        # Deserialize the dictionary into a validated schema object
        schema = CustomerSchema()
        customer_dict_converted = schema.load(customer_dict)
        # Create a new Customer instance using the validated data
        new_customer = Customer(**customer_dict_converted)
        return new_customer
    async def add_bulk(self, customers: List[Customer]) -> List[Customer]:
        """
        Adds multiple customers at once.
        Args:
            customers (List[Customer]): The list of customers to add.
        Returns:
            List[Customer]: The list of added customers.
        """
        logging.info("CustomerManager.add_bulk")
        for customer in customers:
            customer_id = customer.customer_id
            code = customer.code
            if customer.customer_id is not None and customer.customer_id > 0:
                raise ValueError(
                    f"Customer is already added: {str(code)} {str(customer_id)}"
                )
            customer.insert_user_id = self.convert_uuid_to_model_uuid(
                self._session_context.customer_code)
            customer.last_update_user_id = self.convert_uuid_to_model_uuid(
                self._session_context.customer_code)
        self._session_context.session.add_all(customers)
        await self._session_context.session.flush()
        return customers
    async def update_bulk(
        self,
        customer_updates: List[Dict[str, Any]]
    ) -> List[Customer]:
        """
        #TODO add comment
        """
        logging.info("CustomerManager.update_bulk start")
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
            logging.info("CustomerManager.update_bulk customer_id:%s", customer_id)
            customer = await self.get_by_id(customer_id)
            if not customer:
                raise CustomerNotFoundError(
                    f"Customer with ID {customer_id} not found!")
            for key, value in update.items():
                if key != "customer_id":
                    setattr(customer, key, value)
            customer.last_update_user_id = self.convert_uuid_to_model_uuid(
                self._session_context.customer_code)
            updated_customers.append(customer)
        await self._session_context.session.flush()
        logging.info("CustomerManager.update_bulk end")
        return updated_customers
    async def delete_bulk(self, customer_ids: List[int]) -> bool:
        """
        Delete multiple customers by their IDs.
        """
        logging.info("CustomerManager.delete_bulk")
        for customer_id in customer_ids:
            if not isinstance(customer_id, int):
                raise TypeError(
                    f"The customer_id must be an integer, "
                    f"got {type(customer_id)} instead."
                )
            customer = await self.get_by_id(customer_id)
            if not customer:
                raise CustomerNotFoundError(
                    f"Customer with ID {customer_id} not found!"
                )
            if customer:
                await self._session_context.session.delete(customer)
        await self._session_context.session.flush()
        return True
    async def count(self) -> int:
        """
        return the total number of customers.
        """
        logging.info("CustomerManager.count")
        result = await self._session_context.session.execute(select(Customer))
        return len(result.scalars().all())
    #TODO fix. needs to populate peek props. use getall and sort List
    async def get_sorted_list(
            self,
            sort_by: str,
            order: Optional[str] = "asc") -> List[Customer]:
        """
        Retrieve customers sorted by a particular attribute.
        """
        if sort_by == "customer_id":
            sort_by = "_customer_id"
        if order == "asc":
            result = await self._session_context.session.execute(
                select(Customer).order_by(getattr(Customer, sort_by).asc()))
        else:
            result = await self._session_context.session.execute(
                select(Customer).order_by(getattr(Customer, sort_by).desc()))
        return result.scalars().all()
    async def refresh(self, customer: Customer) -> Customer:
        """
        Refresh the state of a given customer instance from the database.
        """
        logging.info("CustomerManager.refresh")
        await self._session_context.session.refresh(customer)
        return customer
    async def exists(self, customer_id: int) -> bool:
        """
        Check if a customer with the given ID exists.
        """
        logging.info("CustomerManager.exists %s", customer_id)
        if not isinstance(customer_id, int):
            raise TypeError(
                f"The customer_id must be an integer, "
                f"got {type(customer_id)} instead."
            )
        customer = await self.get_by_id(customer_id)
        return bool(customer)
    def is_equal(self, customer1: Customer, customer2: Customer) -> bool:
        """
        #TODO add comment
        """
        if not customer1:
            raise TypeError("Customer1 required.")
        if not customer2:
            raise TypeError("Customer2 required.")
        if not isinstance(customer1, Customer):
            raise TypeError("The customer1 must be an Customer instance.")
        if not isinstance(customer2, Customer):
            raise TypeError("The customer2 must be an Customer instance.")
        dict1 = self.to_dict(customer1)
        dict2 = self.to_dict(customer2)
        return dict1 == dict2
# endset
    async def get_by_tac_id(self, tac_id: int) -> List[Customer]:  # TacID
        """
        #TODO add comment
        """
        logging.info("CustomerManager.get_by_tac_id")
        if not isinstance(tac_id, int):
            raise TypeError(
                f"The customer_id must be an integer, "
                f"got {type(tac_id)} instead."
            )
        query_filter = Customer._tac_id == tac_id  # pylint: disable=protected-access  # noqa: E501
        query_results = await self._run_query(query_filter)
        return query_results
# endset
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
