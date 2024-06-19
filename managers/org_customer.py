# models/managers/org_customer.py
# pylint: disable=unused-import
"""
This module contains the OrgCustomerManager class, which is
responsible for managing org_customers in the system.
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
from models.organization import Organization  # OrganizationID
from models.org_customer import OrgCustomer
from models.serialization_schema.org_customer import OrgCustomerSchema
from services.logging_config import get_logger
logger = get_logger(__name__)
class OrgCustomerNotFoundError(Exception):
    """
    Exception raised when a specified org_customer is not found.
    Attributes:
        message (str):Explanation of the error.
    """
    def __init__(self, message="OrgCustomer not found"):
        self.message = message
        super().__init__(self.message)

class OrgCustomerManager:
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
        logging.info("OrgCustomerManager.Initialize")

    async def build(self, **kwargs) -> OrgCustomer:
        """
            #TODO add comment
        """
        logging.info("OrgCustomerManager.build")
        return OrgCustomer(**kwargs)
    async def add(self, org_customer: OrgCustomer) -> OrgCustomer:
        """
            #TODO add comment
        """
        logging.info("OrgCustomerManager.add")
        org_customer.insert_user_id = self.convert_uuid_to_model_uuid(
            self._session_context.customer_code)
        org_customer.last_update_user_id = self.convert_uuid_to_model_uuid(
            self._session_context.customer_code)
        self._session_context.session.add(org_customer)
        await self._session_context.session.flush()
        return org_customer
    def _build_query(self):
        """
            #TODO add comment
        """
        logging.info("OrgCustomerManager._build_query")
        query = select(
            OrgCustomer,
            Customer,  # customer_id
            Organization,  # organization_id
        )
# endset
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
# endset
        return query
    async def _run_query(self, query_filter) -> List[OrgCustomer]:
        """
            #TODO add comment
        """
        logging.info("OrgCustomerManager._run_query")
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
# endset
            customer = query_result_row[i]  # customer_id
            i = i + 1
            organization = query_result_row[i]  # organization_id
            i = i + 1
# endset
            org_customer.customer_code_peek = (  # customer_id
                customer.code if customer else uuid.UUID(int=0))
            org_customer.organization_code_peek = (  # organization_id
                organization.code if organization else uuid.UUID(int=0))
# endset
            result.append(org_customer)
        return result
    def _first_or_none(
        self,
        org_customer_list: List['OrgCustomer']
    ) -> Optional['OrgCustomer']:
        """
        Return the first element of the list if it exists,
        otherwise return None.
        Args:
            org_customer_list (List[OrgCustomer]):
                The list to retrieve the first element from.
        Returns:
            Optional[OrgCustomer]: The first element
                of the list if it exists, otherwise None.
        """
        return (
            org_customer_list[0]
            if org_customer_list
            else None
        )
    async def get_by_id(self, org_customer_id: int) -> Optional[OrgCustomer]:
        """
            #TODO add comment
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
    async def get_by_code(self, code: uuid.UUID) -> Optional[OrgCustomer]:
        """
            #TODO add comment
        """
        logging.info("OrgCustomerManager.get_by_code %s", code)
        query_filter = OrgCustomer._code == str(code)  # pylint: disable=protected-access  # noqa: E501
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)
    async def update(self, org_customer: OrgCustomer, **kwargs) -> Optional[OrgCustomer]:
        """
            #TODO add comment
        """
        logging.info("OrgCustomerManager.update")
        property_list = OrgCustomer.property_list()
        if org_customer:
            org_customer.last_update_user_id = self.convert_uuid_to_model_uuid(
                self._session_context.customer_code)
            for key, value in kwargs.items():
                if key not in property_list:
                    raise ValueError(f"Invalid property: {key}")
                setattr(org_customer, key, value)
            await self._session_context.session.flush()
        return org_customer
    async def delete(self, org_customer_id: int):
        """
            #TODO add comment
        """
        logging.info("OrgCustomerManager.delete %s", org_customer_id)
        if not isinstance(org_customer_id, int):
            raise TypeError(
                f"The org_customer_id must be an integer, "
                f"got {type(org_customer_id)} instead."
            )
        org_customer = await self.get_by_id(org_customer_id)
        if not org_customer:
            raise OrgCustomerNotFoundError(f"OrgCustomer with ID {org_customer_id} not found!")
        await self._session_context.session.delete(org_customer)
        await self._session_context.session.flush()
    async def get_list(self) -> List[OrgCustomer]:
        """
            #TODO add comment
        """
        logging.info("OrgCustomerManager.get_list")
        query_results = await self._run_query(None)
        return query_results
    def to_json(self, org_customer: OrgCustomer) -> str:
        """
        Serialize the OrgCustomer object to a JSON string using the OrgCustomerSchema.
        """
        logging.info("OrgCustomerManager.to_json")
        schema = OrgCustomerSchema()
        org_customer_data = schema.dump(org_customer)
        return json.dumps(org_customer_data)
    def to_dict(self, org_customer: OrgCustomer) -> Dict[str, Any]:
        """
        Serialize the OrgCustomer object to a JSON string using the OrgCustomerSchema.
        """
        logging.info("OrgCustomerManager.to_dict")
        schema = OrgCustomerSchema()
        org_customer_data = schema.dump(org_customer)
        assert isinstance(org_customer_data, dict)
        return org_customer_data
    def from_json(self, json_str: str) -> OrgCustomer:
        """
        Deserializes a JSON string into a OrgCustomer object using the OrgCustomerSchema.
        Args:
            json_str (str): The JSON string to deserialize.
        Returns:
            OrgCustomer: The deserialized OrgCustomer object.
        """
        logging.info("OrgCustomerManager.from_json")
        schema = OrgCustomerSchema()
        data = json.loads(json_str)
        org_customer_dict = schema.load(data)
        new_org_customer = OrgCustomer(**org_customer_dict)
        return new_org_customer
    def from_dict(self, org_customer_dict: Dict[str, Any]) -> OrgCustomer:
        """
        Creates a OrgCustomer instance from a dictionary of attributes.
        Args:
            org_customer_dict (Dict[str, Any]): A dictionary containing
                org_customer attributes.
        Returns:
            OrgCustomer: A new OrgCustomer instance created from the given dictionary.
        """
        logging.info("OrgCustomerManager.from_dict")
        # Deserialize the dictionary into a validated schema object
        schema = OrgCustomerSchema()
        org_customer_dict_converted = schema.load(org_customer_dict)
        # Create a new OrgCustomer instance using the validated data
        new_org_customer = OrgCustomer(**org_customer_dict_converted)
        return new_org_customer
    async def add_bulk(self, org_customers: List[OrgCustomer]) -> List[OrgCustomer]:
        """
        Adds multiple org_customers at once.
        Args:
            org_customers (List[OrgCustomer]): The list of org_customers to add.
        Returns:
            List[OrgCustomer]: The list of added org_customers.
        """
        logging.info("OrgCustomerManager.add_bulk")
        for org_customer in org_customers:
            org_customer_id = org_customer.org_customer_id
            code = org_customer.code
            if org_customer.org_customer_id is not None and org_customer.org_customer_id > 0:
                raise ValueError(
                    f"OrgCustomer is already added: {str(code)} {str(org_customer_id)}"
                )
            org_customer.insert_user_id = self.convert_uuid_to_model_uuid(
                self._session_context.customer_code)
            org_customer.last_update_user_id = self.convert_uuid_to_model_uuid(
                self._session_context.customer_code)
        self._session_context.session.add_all(org_customers)
        await self._session_context.session.flush()
        return org_customers
    async def update_bulk(
        self,
        org_customer_updates: List[Dict[str, Any]]
    ) -> List[OrgCustomer]:
        """
        #TODO add comment
        """
        logging.info("OrgCustomerManager.update_bulk start")
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
            logging.info("OrgCustomerManager.update_bulk org_customer_id:%s", org_customer_id)
            org_customer = await self.get_by_id(org_customer_id)
            if not org_customer:
                raise OrgCustomerNotFoundError(
                    f"OrgCustomer with ID {org_customer_id} not found!")
            for key, value in update.items():
                if key != "org_customer_id":
                    setattr(org_customer, key, value)
            org_customer.last_update_user_id = self.convert_uuid_to_model_uuid(
                self._session_context.customer_code)
            updated_org_customers.append(org_customer)
        await self._session_context.session.flush()
        logging.info("OrgCustomerManager.update_bulk end")
        return updated_org_customers
    async def delete_bulk(self, org_customer_ids: List[int]) -> bool:
        """
        Delete multiple org_customers by their IDs.
        """
        logging.info("OrgCustomerManager.delete_bulk")
        for org_customer_id in org_customer_ids:
            if not isinstance(org_customer_id, int):
                raise TypeError(
                    f"The org_customer_id must be an integer, "
                    f"got {type(org_customer_id)} instead."
                )
            org_customer = await self.get_by_id(org_customer_id)
            if not org_customer:
                raise OrgCustomerNotFoundError(
                    f"OrgCustomer with ID {org_customer_id} not found!"
                )
            if org_customer:
                await self._session_context.session.delete(org_customer)
        await self._session_context.session.flush()
        return True
    async def count(self) -> int:
        """
        return the total number of org_customers.
        """
        logging.info("OrgCustomerManager.count")
        result = await self._session_context.session.execute(select(OrgCustomer))
        return len(result.scalars().all())
    #TODO fix. needs to populate peek props. use getall and sort List
    async def get_sorted_list(
            self,
            sort_by: str,
            order: Optional[str] = "asc") -> List[OrgCustomer]:
        """
        Retrieve org_customers sorted by a particular attribute.
        """
        if sort_by == "org_customer_id":
            sort_by = "_org_customer_id"
        if order == "asc":
            result = await self._session_context.session.execute(
                select(OrgCustomer).order_by(getattr(OrgCustomer, sort_by).asc()))
        else:
            result = await self._session_context.session.execute(
                select(OrgCustomer).order_by(getattr(OrgCustomer, sort_by).desc()))
        return result.scalars().all()
    async def refresh(self, org_customer: OrgCustomer) -> OrgCustomer:
        """
        Refresh the state of a given org_customer instance from the database.
        """
        logging.info("OrgCustomerManager.refresh")
        await self._session_context.session.refresh(org_customer)
        return org_customer
    async def exists(self, org_customer_id: int) -> bool:
        """
        Check if a org_customer with the given ID exists.
        """
        logging.info("OrgCustomerManager.exists %s", org_customer_id)
        if not isinstance(org_customer_id, int):
            raise TypeError(
                f"The org_customer_id must be an integer, "
                f"got {type(org_customer_id)} instead."
            )
        org_customer = await self.get_by_id(org_customer_id)
        return bool(org_customer)
    def is_equal(self, org_customer1: OrgCustomer, org_customer2: OrgCustomer) -> bool:
        """
        #TODO add comment
        """
        if not org_customer1:
            raise TypeError("OrgCustomer1 required.")
        if not org_customer2:
            raise TypeError("OrgCustomer2 required.")
        if not isinstance(org_customer1, OrgCustomer):
            raise TypeError("The org_customer1 must be an OrgCustomer instance.")
        if not isinstance(org_customer2, OrgCustomer):
            raise TypeError("The org_customer2 must be an OrgCustomer instance.")
        dict1 = self.to_dict(org_customer1)
        dict2 = self.to_dict(org_customer2)
        return dict1 == dict2
# endset
    async def get_by_customer_id(
        self,
        customer_id: int
    ) -> List[OrgCustomer]:  # CustomerID
        """
        #TODO add comment
        """
        logging.info("OrgCustomerManager.get_by_customer_id")
        if not isinstance(customer_id, int):
            raise TypeError(
                f"The org_customer_id must be an integer, "
                f"got {type(customer_id)} instead."
            )
        query_filter = OrgCustomer._customer_id == customer_id  # pylint: disable=protected-access  # noqa: E501
        query_results = await self._run_query(query_filter)
        return query_results
    async def get_by_organization_id(self, organization_id: int) -> List[OrgCustomer]:  # OrganizationID
        """
        #TODO add comment
        """
        logging.info("OrgCustomerManager.get_by_organization_id")
        if not isinstance(organization_id, int):
            raise TypeError(
                f"The org_customer_id must be an integer, "
                f"got {type(organization_id)} instead."
            )
        query_filter = OrgCustomer._organization_id == organization_id  # pylint: disable=protected-access  # noqa: E501
        query_results = await self._run_query(query_filter)
        return query_results
# endset

