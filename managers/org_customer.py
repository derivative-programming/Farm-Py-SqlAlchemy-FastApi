# models/managers/org_customer.py
"""
    #TODO add comment
"""
import json
import logging
import uuid
from enum import Enum  # pylint: disable=unused-import
from typing import List, Optional, Dict
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
#         join_condition = None
# # endset
#         join_condition = outerjoin(OrgCustomer, Customer, and_(OrgCustomer.customer_id == Customer.customer_id, OrgCustomer.customer_id != 0))
#         join_condition = outerjoin(join_condition, Organization, and_(OrgCustomer.organization_id == Organization.organization_id, OrgCustomer.organization_id != 0))
# # endset
#         if join_condition is not None:
#             query = select(OrgCustomer
#                         , Customer  # customer_id
#                         , Organization  # organization_id
#                         ).select_from(join_condition)
#         else:
#             query = select(OrgCustomer)
        query = select(
            OrgCustomer,
            Customer,  # customer_id
            Organization,  # organization_id
        )
# endset
        query = query.outerjoin(  # customer_id
            Customer,
            and_(OrgCustomer.customer_id == Customer.customer_id,
                 OrgCustomer.customer_id != 0)
        )
        query = query.outerjoin(  # organization_id
            Organization,
            and_(OrgCustomer.organization_id == Organization.organization_id,
                 OrgCustomer.organization_id != 0)
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
            org_customer.customer_code_peek = customer.code if customer else uuid.UUID(int=0)  # customer_id
            org_customer.organization_code_peek = organization.code if organization else uuid.UUID(int=0)  # organization_id
# endset
            result.append(org_customer)
        return result
    def _first_or_none(self, org_customer_list: List) -> OrgCustomer:
        """
            #TODO add comment
        """
        return org_customer_list[0] if org_customer_list else None
    async def get_by_id(self, org_customer_id: int) -> Optional[OrgCustomer]:
        """
            #TODO add comment
        """
        logging.info(
            "OrgCustomerManager.get_by_id start org_customer_id: %s",
            str(org_customer_id))
        if not isinstance(org_customer_id, int):
            raise TypeError(
                "The org_customer_id must be an integer, got %s instead.",
                type(org_customer_id))
        query_filter = OrgCustomer.org_customer_id == org_customer_id
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)
    async def get_by_code(self, code: uuid.UUID) -> Optional[OrgCustomer]:
        """
            #TODO add comment
        """
        logging.info("OrgCustomerManager.get_by_code %s", code)
        query_filter = OrgCustomer._code == str(code)
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
                f"The org_customer_id must be an integer, got {type(org_customer_id)} instead."
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
    def to_dict(self, org_customer: OrgCustomer) -> dict:
        """
        Serialize the OrgCustomer object to a JSON string using the OrgCustomerSchema.
        """
        logging.info("OrgCustomerManager.to_dict")
        schema = OrgCustomerSchema()
        org_customer_data = schema.dump(org_customer)
        return org_customer_data
    def from_json(self, json_str: str) -> OrgCustomer:
        """
        Deserialize a JSON string into a OrgCustomer object using the OrgCustomerSchema.
        """
        logging.info("OrgCustomerManager.from_json")
        schema = OrgCustomerSchema()
        data = json.loads(json_str)
        org_customer_dict = schema.load(data)
        new_org_customer = OrgCustomer(**org_customer_dict)
        return new_org_customer
    def from_dict(self, org_customer_dict: str) -> OrgCustomer:
        """
        #TODO add comment
        """
        logging.info("OrgCustomerManager.from_dict")
        schema = OrgCustomerSchema()
        org_customer_dict_converted = schema.load(org_customer_dict)
        new_org_customer = OrgCustomer(**org_customer_dict_converted)
        return new_org_customer
    async def add_bulk(self, org_customers: List[OrgCustomer]) -> List[OrgCustomer]:
        """
        Add multiple org_customers at once.
        """
        logging.info("OrgCustomerManager.add_bulk")
        for org_customer in org_customers:
            if org_customer.org_customer_id is not None and org_customer.org_customer_id > 0:
                raise ValueError("OrgCustomer is already added: " +
                                 str(org_customer.code) +
                                 " " + str(org_customer.org_customer_id))
            org_customer.insert_user_id = self.convert_uuid_to_model_uuid(
                self._session_context.customer_code)
            org_customer.last_update_user_id = self.convert_uuid_to_model_uuid(
                self._session_context.customer_code)
        self._session_context.session.add_all(org_customers)
        await self._session_context.session.flush()
        return org_customers
    async def update_bulk(
        self,
        org_customer_updates: List[Dict[int, Dict]]
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
                    f"The org_customer_id must be an integer, got {type(org_customer_id)} instead."
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
                    f"The org_customer_id must be an integer, got {type(org_customer_id)} instead."
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
                f"The org_customer_id must be an integer, got {type(org_customer_id)} instead."
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
                f"The org_customer_id must be an integer, got {type(customer_id)} instead."
            )
        query_filter = OrgCustomer.customer_id == customer_id
        query_results = await self._run_query(query_filter)
        return query_results
    async def get_by_organization_id(self, organization_id: int) -> List[OrgCustomer]:  # OrganizationID
        """
        #TODO add comment
        """
        logging.info("OrgCustomerManager.get_by_organization_id")
        if not isinstance(organization_id, int):
            raise TypeError(
                f"The org_customer_id must be an integer, got {type(organization_id)} instead."
            )
        query_filter = OrgCustomer.organization_id == organization_id
        query_results = await self._run_query(query_filter)
        return query_results
# endset

