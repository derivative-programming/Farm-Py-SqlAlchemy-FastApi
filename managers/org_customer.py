import json
import random
import uuid
from datetime import date, datetime
from enum import Enum
from typing import List, Optional, Dict
from sqlalchemy import and_, outerjoin
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select#, join, outerjoin, and_
from models.customer import Customer # CustomerID
from models.organization import Organization # OrganizationID
from models.org_customer import OrgCustomer
from models.serialization_schema.org_customer import OrgCustomerSchema
from services.db_config import generate_uuid
from services.logging_config import get_logger
import logging
logger = get_logger(__name__)
class OrgCustomerNotFoundError(Exception):
    pass

class OrgCustomerManager:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def initialize(self):
        logging.info("OrgCustomerManager.Initialize")

    async def build(self, **kwargs) -> OrgCustomer:
        logging.info("OrgCustomerManager.build")
        return OrgCustomer(**kwargs)
    async def add(self, org_customer: OrgCustomer) -> OrgCustomer:
        logging.info("OrgCustomerManager.add")
        self.session.add(org_customer)
        await self.session.flush()
        return org_customer
    def _build_query(self):
        logging.info("OrgCustomerManager._build_query")
#         join_condition = None
#
#         join_condition = outerjoin(OrgCustomer, Customer, and_(OrgCustomer.customer_id == Customer.customer_id, OrgCustomer.customer_id != 0))
#         join_condition = outerjoin(join_condition, Organization, and_(OrgCustomer.organization_id == Organization.organization_id, OrgCustomer.organization_id != 0))
#
#         if join_condition is not None:
#             query = select(OrgCustomer
#                         ,Customer #customer_id
#                         ,Organization #organization_id
#                         ).select_from(join_condition)
#         else:
#             query = select(OrgCustomer)
        query = select(OrgCustomer
                    ,Customer #customer_id
                    ,Organization #organization_id
                    )

        query = query.outerjoin(Customer, and_(OrgCustomer.customer_id == Customer.customer_id, OrgCustomer.customer_id != 0))
        query = query.outerjoin(Organization, and_(OrgCustomer.organization_id == Organization.organization_id, OrgCustomer.organization_id != 0))

        return query
    async def _run_query(self, query_filter) -> List[OrgCustomer]:
        logging.info("OrgCustomerManager._run_query")
        org_customer_query_all = self._build_query()
        if query_filter is not None:
            query = org_customer_query_all.filter(query_filter)
        else:
            query = org_customer_query_all
        result_proxy = await self.session.execute(query)
        query_results = result_proxy.all()
        result = list()
        for query_result_row in query_results:
            i = 0
            org_customer = query_result_row[i]
            i = i + 1

            customer = query_result_row[i] #customer_id
            i = i + 1
            organization = query_result_row[i] #organization_id
            i = i + 1

            org_customer.customer_code_peek = customer.code if customer else uuid.UUID(int=0) #customer_id
            org_customer.organization_code_peek = organization.code if organization else uuid.UUID(int=0) #organization_id

            result.append(org_customer)
        return result
    def _first_or_none(self,org_customer_list:List) -> OrgCustomer:
        return org_customer_list[0] if org_customer_list else None
    async def get_by_id(self, org_customer_id: int) -> Optional[OrgCustomer]:
        logging.info("OrgCustomerManager.get_by_id start org_customer_id:" + str(org_customer_id))
        if not isinstance(org_customer_id, int):
            raise TypeError(f"The org_customer_id must be an integer, got {type(org_customer_id)} instead.")
        # result = await self.session.execute(select(OrgCustomer).filter(OrgCustomer.org_customer_id == org_customer_id))
        # result = await self.session.execute(select(OrgCustomer).filter(OrgCustomer.org_customer_id == org_customer_id))
        # return result.scalars().first()
        query_filter = OrgCustomer.org_customer_id == org_customer_id
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)
    async def get_by_code(self, code: uuid.UUID) -> Optional[OrgCustomer]:
        logging.info(f"OrgCustomerManager.get_by_code {code}")
        # result = await self.session.execute(select(OrgCustomer).filter_by(code=code))
        # return result.scalars().one_or_none()
        query_filter = OrgCustomer.code==code
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)
    async def update(self, org_customer: OrgCustomer, **kwargs) -> Optional[OrgCustomer]:
        logging.info("OrgCustomerManager.update")
        if org_customer:
            for key, value in kwargs.items():
                setattr(org_customer, key, value)
            await self.session.flush()
        return org_customer
    async def delete(self, org_customer_id: int):
        logging.info(f"OrgCustomerManager.delete {org_customer_id}")
        if not isinstance(org_customer_id, int):
            raise TypeError(f"The org_customer_id must be an integer, got {type(org_customer_id)} instead.")
        org_customer = await self.get_by_id(org_customer_id)
        if not org_customer:
            raise OrgCustomerNotFoundError(f"OrgCustomer with ID {org_customer_id} not found!")
        await self.session.delete(org_customer)
        await self.session.flush()
    async def get_list(self) -> List[OrgCustomer]:
        logging.info("OrgCustomerManager.get_list")
        # result = await self.session.execute(select(OrgCustomer))
        # return result.scalars().all()
        query_results = await self._run_query(None)
        return query_results
    def to_json(self, org_customer:OrgCustomer) -> str:
        logging.info("OrgCustomerManager.to_json")
        """
        Serialize the OrgCustomer object to a JSON string using the OrgCustomerSchema.
        """
        schema = OrgCustomerSchema()
        org_customer_data = schema.dump(org_customer)
        return json.dumps(org_customer_data)
    def to_dict(self, org_customer:OrgCustomer) -> dict:
        logging.info("OrgCustomerManager.to_dict")
        """
        Serialize the OrgCustomer object to a JSON string using the OrgCustomerSchema.
        """
        schema = OrgCustomerSchema()
        org_customer_data = schema.dump(org_customer)
        return org_customer_data
    def from_json(self, json_str: str) -> OrgCustomer:
        logging.info("OrgCustomerManager.from_json")
        """
        Deserialize a JSON string into a OrgCustomer object using the OrgCustomerSchema.
        """
        schema = OrgCustomerSchema()
        data = json.loads(json_str)
        org_customer_dict = schema.load(data)
        new_org_customer = OrgCustomer(**org_customer_dict)
        return new_org_customer
    def from_dict(self, org_customer_dict: str) -> OrgCustomer:
        logging.info("OrgCustomerManager.from_dict")
        schema = OrgCustomerSchema()
        org_customer_dict_converted = schema.load(org_customer_dict)
        new_org_customer = OrgCustomer(**org_customer_dict_converted)
        return new_org_customer
    async def add_bulk(self, org_customers: List[OrgCustomer]) -> List[OrgCustomer]:
        logging.info("OrgCustomerManager.add_bulk")
        """Add multiple org_customers at once."""
        self.session.add_all(org_customers)
        await self.session.flush()
        return org_customers
    async def update_bulk(self, org_customer_updates: List[Dict[int, Dict]]) -> List[OrgCustomer]:
        logging.info("OrgCustomerManager.update_bulk start")
        updated_org_customers = []
        for update in org_customer_updates:
            org_customer_id = update.get("org_customer_id")
            if not isinstance(org_customer_id, int):
                raise TypeError(f"The org_customer_id must be an integer, got {type(org_customer_id)} instead.")
            if not org_customer_id:
                continue
            logging.info(f"OrgCustomerManager.update_bulk org_customer_id:{org_customer_id}")
            org_customer = await self.get_by_id(org_customer_id)
            if not org_customer:
                raise OrgCustomerNotFoundError(f"OrgCustomer with ID {org_customer_id} not found!")
            for key, value in update.items():
                if key != "org_customer_id":
                    setattr(org_customer, key, value)
            updated_org_customers.append(org_customer)
        await self.session.flush()
        logging.info("OrgCustomerManager.update_bulk end")
        return updated_org_customers
    async def delete_bulk(self, org_customer_ids: List[int]) -> bool:
        logging.info("OrgCustomerManager.delete_bulk")
        """Delete multiple org_customers by their IDs."""
        for org_customer_id in org_customer_ids:
            if not isinstance(org_customer_id, int):
                raise TypeError(f"The org_customer_id must be an integer, got {type(org_customer_id)} instead.")
            org_customer = await self.get_by_id(org_customer_id)
            if not org_customer:
                raise OrgCustomerNotFoundError(f"OrgCustomer with ID {org_customer_id} not found!")
            if org_customer:
                await self.session.delete(org_customer)
        await self.session.flush()
        return True
    async def count(self) -> int:
        logging.info("OrgCustomerManager.count")
        """Return the total number of org_customers."""
        result = await self.session.execute(select(OrgCustomer))
        return len(result.scalars().all())
    #TODO fix. needs to populate peek props. use getall and sort List
    async def get_sorted_list(self, sort_by: str, order: Optional[str] = "asc") -> List[OrgCustomer]:
        """Retrieve org_customers sorted by a particular attribute."""
        if order == "asc":
            result = await self.session.execute(select(OrgCustomer).order_by(getattr(OrgCustomer, sort_by).asc()))
        else:
            result = await self.session.execute(select(OrgCustomer).order_by(getattr(OrgCustomer, sort_by).desc()))
        return result.scalars().all()
    async def refresh(self, org_customer: OrgCustomer) -> OrgCustomer:
        logging.info("OrgCustomerManager.refresh")
        """Refresh the state of a given org_customer instance from the database."""
        await self.session.refresh(org_customer)
        return org_customer
    async def exists(self, org_customer_id: int) -> bool:
        logging.info(f"OrgCustomerManager.exists {org_customer_id}")
        """Check if a org_customer with the given ID exists."""
        if not isinstance(org_customer_id, int):
            raise TypeError(f"The org_customer_id must be an integer, got {type(org_customer_id)} instead.")
        org_customer = await self.get_by_id(org_customer_id)
        return bool(org_customer)
    def is_equal(self, org_customer1:OrgCustomer, org_customer2:OrgCustomer) -> bool:
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

    async def get_by_customer_id(self, customer_id: int) -> List[OrgCustomer]: # CustomerID
        logging.info("OrgCustomerManager.get_by_customer_id")
        if not isinstance(customer_id, int):
            raise TypeError(f"The org_customer_id must be an integer, got {type(customer_id)} instead.")
        # result = await self.session.execute(select(OrgCustomer).filter(OrgCustomer.customer_id == customer_id))
        # return result.scalars().all()
        query_filter = OrgCustomer.customer_id == customer_id
        query_results = await self._run_query(query_filter)
        return query_results
    async def get_by_organization_id(self, organization_id: int) -> List[OrgCustomer]: # OrganizationID
        logging.info("OrgCustomerManager.get_by_organization_id")
        if not isinstance(organization_id, int):
            raise TypeError(f"The org_customer_id must be an integer, got {type(organization_id)} instead.")
        # result = await self.session.execute(select(OrgCustomer).filter(OrgCustomer.organization_id == organization_id))
        # return result.scalars().all()
        query_filter = OrgCustomer.organization_id == organization_id
        query_results = await self._run_query(query_filter)
        return query_results

