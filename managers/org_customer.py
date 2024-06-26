# models/managers/org_customer.py
# pylint: disable=unused-import

"""
This module contains the
OrgCustomerManager class, which is
responsible for managing
org_customers in the system.
"""

import json
import logging
import uuid  # noqa: F401
from enum import Enum  # noqa: F401
from typing import Any, List, Optional, Dict
from sqlalchemy import and_
from sqlalchemy.future import select
from helpers.session_context import SessionContext
from models.customer import Customer  # CustomerID
from models.organization import Organization  # OrganizationID
from models.org_customer import OrgCustomer
from models.serialization_schema.org_customer import OrgCustomerSchema
from services.logging_config import get_logger

logger = get_logger(__name__)


class OrgCustomerNotFoundError(Exception):
    """
    Exception raised when a specified
    org_customer is not found.

    Attributes:
        message (str): Explanation of the error.
    """
    def __init__(self, message="OrgCustomer not found"):
        self.message = message
        super().__init__(self.message)


class OrgCustomerManager:
    """
    The OrgCustomerManager class
    is responsible for managing
    org_customers in the system.
    It provides methods for adding, updating, deleting,
    and retrieving org_customers.
    """

    def __init__(self, session_context: SessionContext):
        """
        Initializes a new instance of the
        OrgCustomerManager class.

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
        Initializes the OrgCustomerManager.
        """
        logging.info(
            "OrgCustomerManager.Initialize")


    async def build(self, **kwargs) -> OrgCustomer:
        """
        Builds a new OrgCustomer
        object with the specified attributes.

        Args:
            **kwargs: The attributes of the
                org_customer.

        Returns:
            OrgCustomer: The newly created
                OrgCustomer object.
        """
        logging.info(
            "OrgCustomerManager.build")
        return OrgCustomer(**kwargs)

    async def add(
        self,
        org_customer: OrgCustomer
    ) -> OrgCustomer:
        """
        Adds a new org_customer to the system.

        Args:
            org_customer (OrgCustomer): The
                org_customer to add.

        Returns:
            OrgCustomer: The added
                org_customer.
        """
        logging.info(
            "OrgCustomerManager.add")
        org_customer.insert_user_id = (
            self._session_context.customer_code)
        org_customer.last_update_user_id = (
            self._session_context.customer_code)
        self._session_context.session.add(
            org_customer)
        await self._session_context.session.flush()
        return org_customer

    def _build_query(self):
        """
        Builds the base query for retrieving
        org_customers.

        Returns:
            The base query for retrieving
            org_customers.
        """
        logging.info(
            "OrgCustomerManager._build_query")

        query = select(
            OrgCustomer,
            Customer,  # customer_id
            Organization,  # organization_id
        )
        query = query.outerjoin(  # customer_id
            Customer,
            and_(OrgCustomer._customer_id == Customer._customer_id,  # pylint: disable=protected-access  # noqa: E501 # type: ignore
                 OrgCustomer._customer_id != 0)  # pylint: disable=protected-access  # noqa: E501 # type: ignore
        )
        query = query.outerjoin(  # organization_id
            Organization,
            and_(OrgCustomer._organization_id == Organization._organization_id,  # pylint: disable=protected-access  # noqa: E501 # type: ignore
                 OrgCustomer._organization_id != 0)  # pylint: disable=protected-access  # noqa: E501 # type: ignore
        )

        return query

    async def _run_query(
        self,
        query_filter
    ) -> List[OrgCustomer]:
        """
        Runs the query to retrieve
        org_customers from the database.

        Args:
            query_filter: The filter to apply to the query.

        Returns:
            List[OrgCustomer]: The list of
                org_customers that match the query.
        """
        logging.info(
            "OrgCustomerManager._run_query")
        org_customer_query_all = self._build_query()

        if query_filter is not None:
            query = org_customer_query_all.filter(query_filter)
        else:
            query = org_customer_query_all

        result_proxy = await self._session_context.session.execute(query)

        query_results = result_proxy.all()

        result = list()

        for query_result_row in query_results:
            i = 0
            org_customer = query_result_row[i]
            i = i + 1
            customer = query_result_row[i]  # customer_id
            i = i + 1
            organization = query_result_row[i]  # organization_id
            i = i + 1
            org_customer.customer_code_peek = (  # customer_id
                customer.code if customer else uuid.UUID(int=0))
            org_customer.organization_code_peek = (  # organization_id
                organization.code if organization else uuid.UUID(int=0))
            result.append(org_customer)

        return result

    def _first_or_none(
        self,
        org_customer_list: List['OrgCustomer']
    ) -> Optional['OrgCustomer']:
        """
        Returns the first element of the list if it exists,
        otherwise returns None.

        Args:
            org_customer_list (List[OrgCustomer]):
                The list to retrieve
                the first element from.

        Returns:
            Optional[OrgCustomer]: The
                first element of the list
                if it exists, otherwise None.
        """
        return (
            org_customer_list[0]
            if org_customer_list
            else None
        )

    async def get_by_id(
        self, org_customer_id: int
    ) -> Optional[OrgCustomer]:
        """
        Retrieves a org_customer by its ID.

        Args:
            org_customer_id (int): The ID of the
                org_customer to retrieve.

        Returns:
            Optional[OrgCustomer]: The retrieved
                org_customer, or None if not found.
        """
        logging.info(
            "OrgCustomerManager.get_by_id start org_customer_id: %s",
            str(org_customer_id))
        if not isinstance(org_customer_id, int):
            raise TypeError(
                "The org_customer_id must be an integer, "
                f"got {type(org_customer_id)} instead.")

        query_filter = (
            OrgCustomer._org_customer_id == org_customer_id)  # pylint: disable=protected-access

        query_results = await self._run_query(query_filter)

        return self._first_or_none(query_results)

    async def get_by_code(
        self, code: uuid.UUID
    ) -> Optional[OrgCustomer]:
        """
        Retrieves a org_customer
        by its code.

        Args:
            code (uuid.UUID): The code of the
                org_customer to retrieve.

        Returns:
            Optional[OrgCustomer]: The retrieved
                org_customer, or None if not found.
        """
        logging.info("OrgCustomerManager.get_by_code %s",
                     code)

        query_filter = OrgCustomer._code == str(code)  # pylint: disable=protected-access  # noqa: E501

        query_results = await self._run_query(query_filter)

        return self._first_or_none(query_results)

    async def update(
        self,
        org_customer: OrgCustomer, **kwargs
    ) -> Optional[OrgCustomer]:
        """
        Updates a org_customer with
        the specified attributes.

        Args:
            org_customer (OrgCustomer): The
                org_customer to update.
            **kwargs: The attributes to update.

        Returns:
            Optional[OrgCustomer]: The updated
                org_customer, or None if not found.

        Raises:
            ValueError: If an invalid property is provided.
        """
        logging.info("OrgCustomerManager.update")
        property_list = OrgCustomer.property_list()
        if org_customer:
            org_customer.last_update_user_id = \
                self._session_context.customer_code
            for key, value in kwargs.items():
                if key not in property_list:
                    raise ValueError(f"Invalid property: {key}")
                setattr(org_customer, key, value)
            await self._session_context.session.flush()
        return org_customer

    async def delete(self, org_customer_id: int):
        """
        Deletes a org_customer by its ID.

        Args:
            org_customer_id (int): The ID of the
                org_customer to delete.

        Raises:
            TypeError: If the org_customer_id
                is not an integer.
            OrgCustomerNotFoundError: If the
                org_customer with the
                specified ID is not found.
        """
        logging.info(
            "OrgCustomerManager.delete %s",
            org_customer_id)
        if not isinstance(org_customer_id, int):
            raise TypeError(
                f"The org_customer_id must be an integer, "
                f"got {type(org_customer_id)} instead."
            )
        org_customer = await self.get_by_id(
            org_customer_id)
        if not org_customer:
            raise OrgCustomerNotFoundError(
                f"OrgCustomer with ID {org_customer_id} not found!")

        await self._session_context.session.delete(
            org_customer)

        await self._session_context.session.flush()

    async def get_list(
        self
    ) -> List[OrgCustomer]:
        """
        Retrieves a list of all org_customers.

        Returns:
            List[OrgCustomer]: The list of
                org_customers.
        """
        logging.info(
            "OrgCustomerManager.get_list")

        query_results = await self._run_query(None)

        return query_results

    def to_json(
            self,
            org_customer: OrgCustomer) -> str:
        """
        Serializes a OrgCustomer object
        to a JSON string.

        Args:
            org_customer (OrgCustomer): The
                org_customer to serialize.

        Returns:
            str: The JSON string representation of the
                org_customer.
        """
        logging.info(
            "OrgCustomerManager.to_json")
        schema = OrgCustomerSchema()
        org_customer_data = schema.dump(org_customer)
        return json.dumps(org_customer_data)

    def to_dict(
        self,
        org_customer: OrgCustomer
    ) -> Dict[str, Any]:
        """
        Serializes a OrgCustomer
        object to a dictionary.

        Args:
            org_customer (OrgCustomer): The
                org_customer to serialize.

        Returns:
            Dict[str, Any]: The dictionary representation of the
                org_customer.
        """
        logging.info(
            "OrgCustomerManager.to_dict")
        schema = OrgCustomerSchema()
        org_customer_data = schema.dump(org_customer)

        assert isinstance(org_customer_data, dict)

        return org_customer_data

    async def from_json(self, json_str: str) -> OrgCustomer:
        """
        Deserializes a JSON string into a
        OrgCustomer object.

        Args:
            json_str (str): The JSON string to deserialize.

        Returns:
            OrgCustomer: The deserialized
                OrgCustomer object.
        """
        logging.info(
            "OrgCustomerManager.from_json")
        schema = OrgCustomerSchema()
        data = json.loads(json_str)
        org_customer_dict = schema.load(data)

        #we need to load the obj form db and into session first.
        # If not found, then no chagnes can be saved

        # new_org_customer = OrgCustomer(**org_customer_dict)

        # load or create
        new_org_customer = await self.get_by_id(
            org_customer_dict["org_customer_id"])
        if new_org_customer is None:
            new_org_customer = OrgCustomer(**org_customer_dict)
            self._session_context.session.add(new_org_customer)
        else:
            for key, value in org_customer_dict.items():
                setattr(new_org_customer, key, value)

        return new_org_customer

    async def from_dict(
        self, org_customer_dict: Dict[str, Any]
    ) -> OrgCustomer:
        """
        Creates a OrgCustomer
        instance from a dictionary of attributes.

        Args:
            org_customer_dict (Dict[str, Any]): A dictionary
                containing org_customer
                attributes.

        Returns:
            OrgCustomer: A new
                OrgCustomer instance
                created from the given
                dictionary.
        """
        logging.info(
            "OrgCustomerManager.from_dict")

        # Deserialize the dictionary into a validated schema object
        schema = OrgCustomerSchema()
        org_customer_dict_converted = schema.load(
            org_customer_dict)

        #we need to load the obj form db and into session first.
        # If not found, then no chagnes can be saved

        # Create a new OrgCustomer instance
        # using the validated data
        # new_org_customer = OrgCustomer(**org_customer_dict_converted)

        # load or create
        new_org_customer = await self.get_by_id(
            org_customer_dict_converted["org_customer_id"])
        if new_org_customer is None:
            new_org_customer = OrgCustomer(**org_customer_dict_converted)
            self._session_context.session.add(new_org_customer)
        else:
            for key, value in org_customer_dict_converted.items():
                setattr(new_org_customer, key, value)

        return new_org_customer

    async def add_bulk(
        self,
        org_customers: List[OrgCustomer]
    ) -> List[OrgCustomer]:
        """
        Adds multiple org_customers
        to the system.

        Args:
            org_customers (List[OrgCustomer]): The list of
                org_customers to add.

        Returns:
            List[OrgCustomer]: The added
                org_customers.
        """
        logging.info(
            "OrgCustomerManager.add_bulk")
        for list_item in org_customers:
            org_customer_id = \
                list_item.org_customer_id
            code = list_item.code
            if list_item.org_customer_id is not None and \
                    list_item.org_customer_id > 0:
                raise ValueError(
                    "OrgCustomer is already added"
                    f": {str(code)} {str(org_customer_id)}"
                )
            list_item.insert_user_id = (
                self._session_context.customer_code)
            list_item.last_update_user_id = (
                self._session_context.customer_code)
        self._session_context.session.add_all(org_customers)
        await self._session_context.session.flush()
        return org_customers

    async def update_bulk(
        self,
        org_customer_updates: List[Dict[str, Any]]
    ) -> List[OrgCustomer]:
        """
        Update multiple org_customers
        with the provided updates.

        Args:
            org_customer_updates (List[Dict[str, Any]]): A list of
            dictionaries containing the updates for each
            org_customer.

        Returns:
            List[OrgCustomer]: A list of updated
                OrgCustomer objects.

        Raises:
            TypeError: If the org_customer_id is not an integer.
            OrgCustomerNotFoundError: If a
                org_customer with the
                provided org_customer_id is not found.
        """

        logging.info(
            "OrgCustomerManager.update_bulk start")
        updated_org_customers = []
        for update in org_customer_updates:
            org_customer_id = update.get("org_customer_id")
            if not isinstance(org_customer_id, int):
                raise TypeError(
                    f"The org_customer_id must be an integer, "
                    f"got {type(org_customer_id)} instead."
                )
            if not org_customer_id:
                continue

            logging.info(
                "OrgCustomerManager.update_bulk org_customer_id:%s",
                org_customer_id)

            org_customer = await self.get_by_id(
                org_customer_id)

            if not org_customer:
                raise OrgCustomerNotFoundError(
                    f"OrgCustomer with ID {org_customer_id} not found!")

            for key, value in update.items():
                if key != "org_customer_id":
                    setattr(org_customer, key, value)

            org_customer.last_update_user_id =\
                self._session_context.customer_code

            updated_org_customers.append(org_customer)

        await self._session_context.session.flush()

        logging.info(
            "OrgCustomerManager.update_bulk end")

        return updated_org_customers

    async def delete_bulk(self, org_customer_ids: List[int]) -> bool:
        """
        Delete multiple org_customers
        by their IDs.
        """
        logging.info(
            "OrgCustomerManager.delete_bulk")

        for org_customer_id in org_customer_ids:
            if not isinstance(org_customer_id, int):
                raise TypeError(
                    f"The org_customer_id must be an integer, "
                    f"got {type(org_customer_id)} instead."
                )

            org_customer = await self.get_by_id(
                org_customer_id)
            if not org_customer:
                raise OrgCustomerNotFoundError(
                    f"OrgCustomer with ID {org_customer_id} not found!"
                )

            if org_customer:
                await self._session_context.session.delete(
                    org_customer)

        await self._session_context.session.flush()

        return True

    async def count(self) -> int:
        """
        return the total number of
        org_customers.
        """
        logging.info(
            "OrgCustomerManager.count")
        result = await self._session_context.session.execute(
            select(OrgCustomer))
        return len(list(result.scalars().all()))

    async def refresh(
        self,
        org_customer: OrgCustomer
    ) -> OrgCustomer:
        """
        Refresh the state of a given
        org_customer instance
        from the database.
        """

        logging.info(
            "OrgCustomerManager.refresh")

        await self._session_context.session.refresh(org_customer)

        return org_customer

    async def exists(self, org_customer_id: int) -> bool:
        """
        Check if a org_customer
        with the given ID exists.
        """
        logging.info(
            "OrgCustomerManager.exists %s",
            org_customer_id)
        if not isinstance(org_customer_id, int):
            raise TypeError(
                f"The org_customer_id must be an integer, "
                f"got {type(org_customer_id)} instead."
            )
        org_customer = await self.get_by_id(
            org_customer_id)
        return bool(org_customer)

    def is_equal(
        self,
        org_customer1: OrgCustomer,
        org_customer2: OrgCustomer
    ) -> bool:
        """
        Check if two OrgCustomer
        objects are equal.

        Args:
            org_customer1 (OrgCustomer): The first
                OrgCustomer object.
            org_customer2 (OrgCustomer): The second
                OrgCustomer object.

        Returns:
            bool: True if the two OrgCustomer
                objects are equal, False otherwise.

        Raises:
            TypeError: If either org_customer1
                or org_customer2
                is not provided or is not an instance of
                OrgCustomer.
        """
        if not org_customer1:
            raise TypeError("OrgCustomer1 required.")

        if not org_customer2:
            raise TypeError("OrgCustomer2 required.")

        if not isinstance(org_customer1,
                          OrgCustomer):
            raise TypeError("The org_customer1 must be an "
                            "OrgCustomer instance.")

        if not isinstance(org_customer2,
                          OrgCustomer):
            raise TypeError("The org_customer2 must be an "
                            "OrgCustomer instance.")

        dict1 = self.to_dict(org_customer1)
        dict2 = self.to_dict(org_customer2)

        return dict1 == dict2
    # CustomerID

    async def get_by_customer_id(
            self,
            customer_id: int) -> List[OrgCustomer]:
        """
        Retrieve a list of org_customers
            based on the
            given customer_id.

        Args:
            customer_id (int): The
                customer_id
                to filter the
                org_customers.

        Returns:
            List[OrgCustomer]: A list of OrgCustomer
                objects
                matching the given
                customer_id.
        """

        logging.info(
            "OrgCustomerManager.get_by_customer_id")
        if not isinstance(customer_id, int):
            raise TypeError(
                f"The org_customer_id must be an integer, "
                f"got {type(customer_id)} instead."
            )

        query_filter = OrgCustomer._customer_id == customer_id  # pylint: disable=protected-access  # noqa: E501

        query_results = await self._run_query(query_filter)

        return query_results
    # OrganizationID
    async def get_by_organization_id(
            self,
            organization_id: int) -> List[OrgCustomer]:
        """
        Retrieve a list of org_customers by
        organization ID.

        Args:
            organization_id (int): The ID of the organization.

        Returns:
            List[OrgCustomer]: A list of
                org_customers associated
                with the specified organization ID.
        """

        logging.info(
            "OrgCustomerManager.get_by_organization_id")
        if not isinstance(organization_id, int):
            raise TypeError(
                f"The org_customer_id must be an integer, "
                f"got {type(organization_id)} instead."
            )

        query_filter = OrgCustomer._organization_id == organization_id  # pylint: disable=protected-access  # noqa: E501

        query_results = await self._run_query(query_filter)

        return query_results
