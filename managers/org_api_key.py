import json
import uuid
from enum import Enum
from typing import List, Optional, Dict
from sqlalchemy import and_, outerjoin
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select#, join, outerjoin, and_
from models.organization import Organization # OrganizationID
from models.org_customer import OrgCustomer # OrgCustomerID
from models.org_api_key import OrgApiKey
from models.serialization_schema.org_api_key import OrgApiKeySchema
from services.logging_config import get_logger
import logging
logger = get_logger(__name__)
class OrgApiKeyNotFoundError(Exception):
    pass

class OrgApiKeyManager:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def initialize(self):
        logging.info("OrgApiKeyManager.Initialize")

    async def build(self, **kwargs) -> OrgApiKey:
        logging.info("OrgApiKeyManager.build")
        return OrgApiKey(**kwargs)
    async def add(self, org_api_key: OrgApiKey) -> OrgApiKey:
        logging.info("OrgApiKeyManager.add")
        self.session.add(org_api_key)
        await self.session.flush()
        return org_api_key
    def _build_query(self):
        logging.info("OrgApiKeyManager._build_query")
#         join_condition = None
#
#         join_condition = outerjoin(join_condition, Organization, and_(OrgApiKey.organization_id == Organization.organization_id, OrgApiKey.organization_id != 0))
#         join_condition = outerjoin(OrgApiKey, OrgCustomer, and_(OrgApiKey.org_customer_id == OrgCustomer.org_customer_id, OrgApiKey.org_customer_id != 0))
#
#         if join_condition is not None:
#             query = select(OrgApiKey
#                         ,Organization #organization_id
#                         ,OrgCustomer #org_customer_id
#                         ).select_from(join_condition)
#         else:
#             query = select(OrgApiKey)
        query = select(OrgApiKey
                    ,Organization #organization_id
                    ,OrgCustomer #org_customer_id
                    )

        query = query.outerjoin(Organization, and_(OrgApiKey.organization_id == Organization.organization_id, OrgApiKey.organization_id != 0))
        query = query.outerjoin(OrgCustomer, and_(OrgApiKey.org_customer_id == OrgCustomer.org_customer_id, OrgApiKey.org_customer_id != 0))

        return query
    async def _run_query(self, query_filter) -> List[OrgApiKey]:
        logging.info("OrgApiKeyManager._run_query")
        org_api_key_query_all = self._build_query()
        if query_filter is not None:
            query = org_api_key_query_all.filter(query_filter)
        else:
            query = org_api_key_query_all
        result_proxy = await self.session.execute(query)
        query_results = result_proxy.all()
        result = list()
        for query_result_row in query_results:
            i = 0
            org_api_key = query_result_row[i]
            i = i + 1

            organization = query_result_row[i] #organization_id
            i = i + 1
            org_customer = query_result_row[i] #org_customer_id
            i = i + 1

            org_api_key.organization_code_peek = organization.code if organization else uuid.UUID(int=0) #organization_id
            org_api_key.org_customer_code_peek = org_customer.code if org_customer else uuid.UUID(int=0) #org_customer_id

            result.append(org_api_key)
        return result
    def _first_or_none(self,org_api_key_list:List) -> OrgApiKey:
        return org_api_key_list[0] if org_api_key_list else None
    async def get_by_id(self, org_api_key_id: int) -> Optional[OrgApiKey]:
        logging.info("OrgApiKeyManager.get_by_id start org_api_key_id:" + str(org_api_key_id))
        if not isinstance(org_api_key_id, int):
            raise TypeError(f"The org_api_key_id must be an integer, got {type(org_api_key_id)} instead.")
        # result = await self.session.execute(select(OrgApiKey).filter(OrgApiKey.org_api_key_id == org_api_key_id))
        # result = await self.session.execute(select(OrgApiKey).filter(OrgApiKey.org_api_key_id == org_api_key_id))
        # return result.scalars().first()
        query_filter = OrgApiKey.org_api_key_id == org_api_key_id
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)
    async def get_by_code(self, code: uuid.UUID) -> Optional[OrgApiKey]:
        logging.info(f"OrgApiKeyManager.get_by_code {code}")
        # result = await self.session.execute(select(OrgApiKey).filter_by(code=code))
        # return result.scalars().one_or_none()
        query_filter = OrgApiKey.code==code
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)
    async def update(self, org_api_key: OrgApiKey, **kwargs) -> Optional[OrgApiKey]:
        logging.info("OrgApiKeyManager.update")
        if org_api_key:
            for key, value in kwargs.items():
                setattr(org_api_key, key, value)
            await self.session.flush()
        return org_api_key
    async def delete(self, org_api_key_id: int):
        logging.info(f"OrgApiKeyManager.delete {org_api_key_id}")
        if not isinstance(org_api_key_id, int):
            raise TypeError(f"The org_api_key_id must be an integer, got {type(org_api_key_id)} instead.")
        org_api_key = await self.get_by_id(org_api_key_id)
        if not org_api_key:
            raise OrgApiKeyNotFoundError(f"OrgApiKey with ID {org_api_key_id} not found!")
        await self.session.delete(org_api_key)
        await self.session.flush()
    async def get_list(self) -> List[OrgApiKey]:
        logging.info("OrgApiKeyManager.get_list")
        # result = await self.session.execute(select(OrgApiKey))
        # return result.scalars().all()
        query_results = await self._run_query(None)
        return query_results
    def to_json(self, org_api_key:OrgApiKey) -> str:
        logging.info("OrgApiKeyManager.to_json")
        """
        Serialize the OrgApiKey object to a JSON string using the OrgApiKeySchema.
        """
        schema = OrgApiKeySchema()
        org_api_key_data = schema.dump(org_api_key)
        return json.dumps(org_api_key_data)
    def to_dict(self, org_api_key:OrgApiKey) -> dict:
        logging.info("OrgApiKeyManager.to_dict")
        """
        Serialize the OrgApiKey object to a JSON string using the OrgApiKeySchema.
        """
        schema = OrgApiKeySchema()
        org_api_key_data = schema.dump(org_api_key)
        return org_api_key_data
    def from_json(self, json_str: str) -> OrgApiKey:
        logging.info("OrgApiKeyManager.from_json")
        """
        Deserialize a JSON string into a OrgApiKey object using the OrgApiKeySchema.
        """
        schema = OrgApiKeySchema()
        data = json.loads(json_str)
        org_api_key_dict = schema.load(data)
        new_org_api_key = OrgApiKey(**org_api_key_dict)
        return new_org_api_key
    def from_dict(self, org_api_key_dict: str) -> OrgApiKey:
        logging.info("OrgApiKeyManager.from_dict")
        schema = OrgApiKeySchema()
        org_api_key_dict_converted = schema.load(org_api_key_dict)
        new_org_api_key = OrgApiKey(**org_api_key_dict_converted)
        return new_org_api_key
    async def add_bulk(self, org_api_keys: List[OrgApiKey]) -> List[OrgApiKey]:
        logging.info("OrgApiKeyManager.add_bulk")
        """Add multiple org_api_keys at once."""
        self.session.add_all(org_api_keys)
        await self.session.flush()
        return org_api_keys
    async def update_bulk(self, org_api_key_updates: List[Dict[int, Dict]]) -> List[OrgApiKey]:
        logging.info("OrgApiKeyManager.update_bulk start")
        updated_org_api_keys = []
        for update in org_api_key_updates:
            org_api_key_id = update.get("org_api_key_id")
            if not isinstance(org_api_key_id, int):
                raise TypeError(f"The org_api_key_id must be an integer, got {type(org_api_key_id)} instead.")
            if not org_api_key_id:
                continue
            logging.info(f"OrgApiKeyManager.update_bulk org_api_key_id:{org_api_key_id}")
            org_api_key = await self.get_by_id(org_api_key_id)
            if not org_api_key:
                raise OrgApiKeyNotFoundError(f"OrgApiKey with ID {org_api_key_id} not found!")
            for key, value in update.items():
                if key != "org_api_key_id":
                    setattr(org_api_key, key, value)
            updated_org_api_keys.append(org_api_key)
        await self.session.flush()
        logging.info("OrgApiKeyManager.update_bulk end")
        return updated_org_api_keys
    async def delete_bulk(self, org_api_key_ids: List[int]) -> bool:
        logging.info("OrgApiKeyManager.delete_bulk")
        """Delete multiple org_api_keys by their IDs."""
        for org_api_key_id in org_api_key_ids:
            if not isinstance(org_api_key_id, int):
                raise TypeError(f"The org_api_key_id must be an integer, got {type(org_api_key_id)} instead.")
            org_api_key = await self.get_by_id(org_api_key_id)
            if not org_api_key:
                raise OrgApiKeyNotFoundError(f"OrgApiKey with ID {org_api_key_id} not found!")
            if org_api_key:
                await self.session.delete(org_api_key)
        await self.session.flush()
        return True
    async def count(self) -> int:
        logging.info("OrgApiKeyManager.count")
        """Return the total number of org_api_keys."""
        result = await self.session.execute(select(OrgApiKey))
        return len(result.scalars().all())
    #TODO fix. needs to populate peek props. use getall and sort List
    async def get_sorted_list(self, sort_by: str, order: Optional[str] = "asc") -> List[OrgApiKey]:
        """Retrieve org_api_keys sorted by a particular attribute."""
        if order == "asc":
            result = await self.session.execute(select(OrgApiKey).order_by(getattr(OrgApiKey, sort_by).asc()))
        else:
            result = await self.session.execute(select(OrgApiKey).order_by(getattr(OrgApiKey, sort_by).desc()))
        return result.scalars().all()
    async def refresh(self, org_api_key: OrgApiKey) -> OrgApiKey:
        logging.info("OrgApiKeyManager.refresh")
        """Refresh the state of a given org_api_key instance from the database."""
        await self.session.refresh(org_api_key)
        return org_api_key
    async def exists(self, org_api_key_id: int) -> bool:
        logging.info(f"OrgApiKeyManager.exists {org_api_key_id}")
        """Check if a org_api_key with the given ID exists."""
        if not isinstance(org_api_key_id, int):
            raise TypeError(f"The org_api_key_id must be an integer, got {type(org_api_key_id)} instead.")
        org_api_key = await self.get_by_id(org_api_key_id)
        return bool(org_api_key)
    def is_equal(self, org_api_key1:OrgApiKey, org_api_key2:OrgApiKey) -> bool:
        if not org_api_key1:
            raise TypeError("OrgApiKey1 required.")
        if not org_api_key2:
            raise TypeError("OrgApiKey2 required.")
        if not isinstance(org_api_key1, OrgApiKey):
            raise TypeError("The org_api_key1 must be an OrgApiKey instance.")
        if not isinstance(org_api_key2, OrgApiKey):
            raise TypeError("The org_api_key2 must be an OrgApiKey instance.")
        dict1 = self.to_dict(org_api_key1)
        dict2 = self.to_dict(org_api_key2)
        return dict1 == dict2

    async def get_by_organization_id(self, organization_id: int) -> List[OrgApiKey]: # OrganizationID
        logging.info("OrgApiKeyManager.get_by_organization_id")
        if not isinstance(organization_id, int):
            raise TypeError(f"The org_api_key_id must be an integer, got {type(organization_id)} instead.")
        # result = await self.session.execute(select(OrgApiKey).filter(OrgApiKey.organization_id == organization_id))
        # return result.scalars().all()
        query_filter = OrgApiKey.organization_id == organization_id
        query_results = await self._run_query(query_filter)
        return query_results
    async def get_by_org_customer_id(self, org_customer_id: int) -> List[OrgApiKey]: # OrgCustomerID
        logging.info("OrgApiKeyManager.get_by_org_customer_id")
        if not isinstance(org_customer_id, int):
            raise TypeError(f"The org_api_key_id must be an integer, got {type(org_customer_id)} instead.")
        # result = await self.session.execute(select(OrgApiKey).filter(OrgApiKey.org_customer_id == org_customer_id))
        # return result.scalars().all()
        query_filter = OrgApiKey.org_customer_id == org_customer_id
        query_results = await self._run_query(query_filter)
        return query_results

