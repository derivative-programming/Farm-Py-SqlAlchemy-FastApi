# models/managers/org_api_key.py
# pylint: disable=unused-import
"""
    #TODO add comment
"""
import json
import logging
import uuid
from enum import Enum  # noqa: F401
from typing import List, Optional, Dict
from sqlalchemy import and_
from sqlalchemy.future import select
from helpers.session_context import SessionContext
from models.organization import Organization  # OrganizationID
from models.org_customer import OrgCustomer  # OrgCustomerID
from models.org_api_key import OrgApiKey
from models.serialization_schema.org_api_key import OrgApiKeySchema
from services.logging_config import get_logger
logger = get_logger(__name__)
class OrgApiKeyNotFoundError(Exception):
    """
    Exception raised when a specified org_api_key is not found.
    Attributes:
        message (str):Explanation of the error.
    """
    def __init__(self, message="OrgApiKey not found"):
        self.message = message
        super().__init__(self.message)

class OrgApiKeyManager:
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
        logging.info("OrgApiKeyManager.Initialize")

    async def build(self, **kwargs) -> OrgApiKey:
        """
            #TODO add comment
        """
        logging.info("OrgApiKeyManager.build")
        return OrgApiKey(**kwargs)
    async def add(self, org_api_key: OrgApiKey) -> OrgApiKey:
        """
            #TODO add comment
        """
        logging.info("OrgApiKeyManager.add")
        org_api_key.insert_user_id = self.convert_uuid_to_model_uuid(
            self._session_context.customer_code)
        org_api_key.last_update_user_id = self.convert_uuid_to_model_uuid(
            self._session_context.customer_code)
        self._session_context.session.add(org_api_key)
        await self._session_context.session.flush()
        return org_api_key
    def _build_query(self):
        """
            #TODO add comment
        """
        logging.info("OrgApiKeyManager._build_query")
#         join_condition = None
# # endset
#         join_condition = outerjoin(join_condition, Organization, and_(OrgApiKey.organization_id == Organization.organization_id, OrgApiKey.organization_id != 0))
#         join_condition = outerjoin(OrgApiKey, OrgCustomer, and_(OrgApiKey.org_customer_id == OrgCustomer.org_customer_id, OrgApiKey.org_customer_id != 0))
# # endset
#         if join_condition is not None:
#             query = select(OrgApiKey
#                         , Organization  # organization_id
#                         , OrgCustomer  # org_customer_id
#                         ).select_from(join_condition)
#         else:
#             query = select(OrgApiKey)
        query = select(
            OrgApiKey,
            Organization,  # organization_id
            OrgCustomer,  # org_customer_id
        )
# endset
        query = query.outerjoin(  # organization_id
            Organization,
            and_(OrgApiKey.organization_id == Organization.organization_id,
                 OrgApiKey.organization_id != 0)
        )
        query = query.outerjoin(  # org_customer_id
            OrgCustomer,
            and_(OrgApiKey.org_customer_id == OrgCustomer.org_customer_id,
                 OrgApiKey.org_customer_id != 0)
        )
# endset
        return query
    async def _run_query(self, query_filter) -> List[OrgApiKey]:
        """
            #TODO add comment
        """
        logging.info("OrgApiKeyManager._run_query")
        org_api_key_query_all = self._build_query()
        if query_filter is not None:
            query = org_api_key_query_all.filter(query_filter)
        else:
            query = org_api_key_query_all
        result_proxy = await self._session_context.session.execute(query)
        query_results = result_proxy.all()
        result = list()
        for query_result_row in query_results:
            i = 0
            org_api_key = query_result_row[i]
            i = i + 1
# endset
            organization = query_result_row[i]  # organization_id
            i = i + 1
            org_customer = query_result_row[i]  # org_customer_id
            i = i + 1
# endset
            org_api_key.organization_code_peek = organization.code if organization else uuid.UUID(int=0)  # organization_id
            org_api_key.org_customer_code_peek = org_customer.code if org_customer else uuid.UUID(int=0)  # org_customer_id
# endset
            result.append(org_api_key)
        return result
    def _first_or_none(self, org_api_key_list: List) -> OrgApiKey:
        """
            #TODO add comment
        """
        return org_api_key_list[0] if org_api_key_list else None
    async def get_by_id(self, org_api_key_id: int) -> Optional[OrgApiKey]:
        """
            #TODO add comment
        """
        logging.info(
            "OrgApiKeyManager.get_by_id start org_api_key_id: %s",
            str(org_api_key_id))
        if not isinstance(org_api_key_id, int):
            raise TypeError(
                "The org_api_key_id must be an integer, got %s instead.",
                type(org_api_key_id))
        query_filter = OrgApiKey.org_api_key_id == org_api_key_id
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)
    async def get_by_code(self, code: uuid.UUID) -> Optional[OrgApiKey]:
        """
            #TODO add comment
        """
        logging.info("OrgApiKeyManager.get_by_code %s", code)
        query_filter = OrgApiKey._code == str(code)
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)
    async def update(self, org_api_key: OrgApiKey, **kwargs) -> Optional[OrgApiKey]:
        """
            #TODO add comment
        """
        logging.info("OrgApiKeyManager.update")
        property_list = OrgApiKey.property_list()
        if org_api_key:
            org_api_key.last_update_user_id = self.convert_uuid_to_model_uuid(
                self._session_context.customer_code)
            for key, value in kwargs.items():
                if key not in property_list:
                    raise ValueError(f"Invalid property: {key}")
                setattr(org_api_key, key, value)
            await self._session_context.session.flush()
        return org_api_key
    async def delete(self, org_api_key_id: int):
        """
            #TODO add comment
        """
        logging.info("OrgApiKeyManager.delete %s", org_api_key_id)
        if not isinstance(org_api_key_id, int):
            raise TypeError(
                f"The org_api_key_id must be an integer, got {type(org_api_key_id)} instead."
            )
        org_api_key = await self.get_by_id(org_api_key_id)
        if not org_api_key:
            raise OrgApiKeyNotFoundError(f"OrgApiKey with ID {org_api_key_id} not found!")
        await self._session_context.session.delete(org_api_key)
        await self._session_context.session.flush()
    async def get_list(self) -> List[OrgApiKey]:
        """
            #TODO add comment
        """
        logging.info("OrgApiKeyManager.get_list")
        query_results = await self._run_query(None)
        return query_results
    def to_json(self, org_api_key: OrgApiKey) -> str:
        """
        Serialize the OrgApiKey object to a JSON string using the OrgApiKeySchema.
        """
        logging.info("OrgApiKeyManager.to_json")
        schema = OrgApiKeySchema()
        org_api_key_data = schema.dump(org_api_key)
        return json.dumps(org_api_key_data)
    def to_dict(self, org_api_key: OrgApiKey) -> dict:
        """
        Serialize the OrgApiKey object to a JSON string using the OrgApiKeySchema.
        """
        logging.info("OrgApiKeyManager.to_dict")
        schema = OrgApiKeySchema()
        org_api_key_data = schema.dump(org_api_key)
        return org_api_key_data
    def from_json(self, json_str: str) -> OrgApiKey:
        """
        Deserialize a JSON string into a OrgApiKey object using the OrgApiKeySchema.
        """
        logging.info("OrgApiKeyManager.from_json")
        schema = OrgApiKeySchema()
        data = json.loads(json_str)
        org_api_key_dict = schema.load(data)
        new_org_api_key = OrgApiKey(**org_api_key_dict)
        return new_org_api_key
    def from_dict(self, org_api_key_dict: str) -> OrgApiKey:
        """
        #TODO add comment
        """
        logging.info("OrgApiKeyManager.from_dict")
        schema = OrgApiKeySchema()
        org_api_key_dict_converted = schema.load(org_api_key_dict)
        new_org_api_key = OrgApiKey(**org_api_key_dict_converted)
        return new_org_api_key
    async def add_bulk(self, org_api_keys: List[OrgApiKey]) -> List[OrgApiKey]:
        """
        Add multiple org_api_keys at once.
        """
        logging.info("OrgApiKeyManager.add_bulk")
        for org_api_key in org_api_keys:
            if org_api_key.org_api_key_id is not None and org_api_key.org_api_key_id > 0:
                raise ValueError("OrgApiKey is already added: " +
                                 str(org_api_key.code) +
                                 " " + str(org_api_key.org_api_key_id))
            org_api_key.insert_user_id = self.convert_uuid_to_model_uuid(
                self._session_context.customer_code)
            org_api_key.last_update_user_id = self.convert_uuid_to_model_uuid(
                self._session_context.customer_code)
        self._session_context.session.add_all(org_api_keys)
        await self._session_context.session.flush()
        return org_api_keys
    async def update_bulk(
        self,
        org_api_key_updates: List[Dict[int, Dict]]
    ) -> List[OrgApiKey]:
        """
        #TODO add comment
        """
        logging.info("OrgApiKeyManager.update_bulk start")
        updated_org_api_keys = []
        for update in org_api_key_updates:
            org_api_key_id = update.get("org_api_key_id")
            if not isinstance(org_api_key_id, int):
                raise TypeError(
                    f"The org_api_key_id must be an integer, got {type(org_api_key_id)} instead."
                )
            if not org_api_key_id:
                continue
            logging.info("OrgApiKeyManager.update_bulk org_api_key_id:%s", org_api_key_id)
            org_api_key = await self.get_by_id(org_api_key_id)
            if not org_api_key:
                raise OrgApiKeyNotFoundError(
                    f"OrgApiKey with ID {org_api_key_id} not found!")
            for key, value in update.items():
                if key != "org_api_key_id":
                    setattr(org_api_key, key, value)
            org_api_key.last_update_user_id = self.convert_uuid_to_model_uuid(
                self._session_context.customer_code)
            updated_org_api_keys.append(org_api_key)
        await self._session_context.session.flush()
        logging.info("OrgApiKeyManager.update_bulk end")
        return updated_org_api_keys
    async def delete_bulk(self, org_api_key_ids: List[int]) -> bool:
        """
        Delete multiple org_api_keys by their IDs.
        """
        logging.info("OrgApiKeyManager.delete_bulk")
        for org_api_key_id in org_api_key_ids:
            if not isinstance(org_api_key_id, int):
                raise TypeError(
                    f"The org_api_key_id must be an integer, got {type(org_api_key_id)} instead."
                )
            org_api_key = await self.get_by_id(org_api_key_id)
            if not org_api_key:
                raise OrgApiKeyNotFoundError(
                    f"OrgApiKey with ID {org_api_key_id} not found!"
                )
            if org_api_key:
                await self._session_context.session.delete(org_api_key)
        await self._session_context.session.flush()
        return True
    async def count(self) -> int:
        """
        return the total number of org_api_keys.
        """
        logging.info("OrgApiKeyManager.count")
        result = await self._session_context.session.execute(select(OrgApiKey))
        return len(result.scalars().all())
    #TODO fix. needs to populate peek props. use getall and sort List
    async def get_sorted_list(
            self,
            sort_by: str,
            order: Optional[str] = "asc") -> List[OrgApiKey]:
        """
        Retrieve org_api_keys sorted by a particular attribute.
        """
        if order == "asc":
            result = await self._session_context.session.execute(
                select(OrgApiKey).order_by(getattr(OrgApiKey, sort_by).asc()))
        else:
            result = await self._session_context.session.execute(
                select(OrgApiKey).order_by(getattr(OrgApiKey, sort_by).desc()))
        return result.scalars().all()
    async def refresh(self, org_api_key: OrgApiKey) -> OrgApiKey:
        """
        Refresh the state of a given org_api_key instance from the database.
        """
        logging.info("OrgApiKeyManager.refresh")
        await self._session_context.session.refresh(org_api_key)
        return org_api_key
    async def exists(self, org_api_key_id: int) -> bool:
        """
        Check if a org_api_key with the given ID exists.
        """
        logging.info("OrgApiKeyManager.exists %s", org_api_key_id)
        if not isinstance(org_api_key_id, int):
            raise TypeError(
                f"The org_api_key_id must be an integer, got {type(org_api_key_id)} instead."
            )
        org_api_key = await self.get_by_id(org_api_key_id)
        return bool(org_api_key)
    def is_equal(self, org_api_key1: OrgApiKey, org_api_key2: OrgApiKey) -> bool:
        """
        #TODO add comment
        """
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
# endset
    async def get_by_organization_id(self, organization_id: int) -> List[OrgApiKey]:  # OrganizationID
        """
        #TODO add comment
        """
        logging.info("OrgApiKeyManager.get_by_organization_id")
        if not isinstance(organization_id, int):
            raise TypeError(
                f"The org_api_key_id must be an integer, got {type(organization_id)} instead."
            )
        query_filter = OrgApiKey.organization_id == organization_id
        query_results = await self._run_query(query_filter)
        return query_results
    async def get_by_org_customer_id(
        self,
        org_customer_id: int
    ) -> List[OrgApiKey]:  # OrgCustomerID
        """
        #TODO add comment
        """
        logging.info("OrgApiKeyManager.get_by_org_customer_id")
        if not isinstance(org_customer_id, int):
            raise TypeError(
                f"The org_api_key_id must be an integer, got {type(org_customer_id)} instead."
            )
        query_filter = OrgApiKey.org_customer_id == org_customer_id
        query_results = await self._run_query(query_filter)
        return query_results
# endset

