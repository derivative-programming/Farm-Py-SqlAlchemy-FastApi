# models/managers/organization.py
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
from models.tac import Tac  # TacID
from models.organization import Organization
from models.serialization_schema.organization import OrganizationSchema
from services.logging_config import get_logger
logger = get_logger(__name__)
class OrganizationNotFoundError(Exception):
    """
    Exception raised when a specified organization is not found.
    Attributes:
        message (str):Explanation of the error.
    """
    def __init__(self, message="Organization not found"):
        self.message = message
        super().__init__(self.message)

class OrganizationManager:
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
        logging.info("OrganizationManager.Initialize")

    async def build(self, **kwargs) -> Organization:
        """
            #TODO add comment
        """
        logging.info("OrganizationManager.build")
        return Organization(**kwargs)
    async def add(self, organization: Organization) -> Organization:
        """
            #TODO add comment
        """
        logging.info("OrganizationManager.add")
        organization.insert_user_id = self.convert_uuid_to_model_uuid(
            self._session_context.customer_code)
        organization.last_update_user_id = self.convert_uuid_to_model_uuid(
            self._session_context.customer_code)
        self._session_context.session.add(organization)
        await self._session_context.session.flush()
        return organization
    def _build_query(self):
        """
            #TODO add comment
        """
        logging.info("OrganizationManager._build_query")
#         join_condition = None
# # endset
#         join_condition = outerjoin(join_condition, Tac, and_(Organization.tac_id == Tac.tac_id, Organization.tac_id != 0))
# # endset
#         if join_condition is not None:
#             query = select(Organization
#                         , Tac  # tac_id
#                         ).select_from(join_condition)
#         else:
#             query = select(Organization)
        query = select(
            Organization,
            Tac,  # tac_id
        )
# endset
        query = query.outerjoin(  # tac_id
            Tac,
            and_(Organization.tac_id == Tac._tac_id,  # pylint: disable=protected-access
                 Organization.tac_id != 0)
        )
# endset
        return query
    async def _run_query(self, query_filter) -> List[Organization]:
        """
            #TODO add comment
        """
        logging.info("OrganizationManager._run_query")
        organization_query_all = self._build_query()
        if query_filter is not None:
            query = organization_query_all.filter(query_filter)
        else:
            query = organization_query_all
        result_proxy = await self._session_context.session.execute(query)
        query_results = result_proxy.all()
        result = list()
        for query_result_row in query_results:
            i = 0
            organization = query_result_row[i]
            i = i + 1
# endset
            tac = query_result_row[i]  # tac_id
            i = i + 1
# endset
            organization.tac_code_peek = (  # tac_id
                tac.code if tac else uuid.UUID(int=0))
# endset
            result.append(organization)
        return result
    def _first_or_none(self, organization_list: List) -> Organization:
        """
            #TODO add comment
        """
        return organization_list[0] if organization_list else None
    async def get_by_id(self, organization_id: int) -> Optional[Organization]:
        """
            #TODO add comment
        """
        logging.info(
            "OrganizationManager.get_by_id start organization_id: %s",
            str(organization_id))
        if not isinstance(organization_id, int):
            raise TypeError(
                "The organization_id must be an integer, "
                f"got {type(organization_id)} instead.")
        query_filter = (
            Organization._organization_id == organization_id)  # pylint: disable=protected-access
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)
    async def get_by_code(self, code: uuid.UUID) -> Optional[Organization]:
        """
            #TODO add comment
        """
        logging.info("OrganizationManager.get_by_code %s", code)
        query_filter = Organization._code == str(code)  # pylint: disable=protected-access
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)
    async def update(self, organization: Organization, **kwargs) -> Optional[Organization]:
        """
            #TODO add comment
        """
        logging.info("OrganizationManager.update")
        property_list = Organization.property_list()
        if organization:
            organization.last_update_user_id = self.convert_uuid_to_model_uuid(
                self._session_context.customer_code)
            for key, value in kwargs.items():
                if key not in property_list:
                    raise ValueError(f"Invalid property: {key}")
                setattr(organization, key, value)
            await self._session_context.session.flush()
        return organization
    async def delete(self, organization_id: int):
        """
            #TODO add comment
        """
        logging.info("OrganizationManager.delete %s", organization_id)
        if not isinstance(organization_id, int):
            raise TypeError(
                f"The organization_id must be an integer, "
                f"got {type(organization_id)} instead."
            )
        organization = await self.get_by_id(organization_id)
        if not organization:
            raise OrganizationNotFoundError(f"Organization with ID {organization_id} not found!")
        await self._session_context.session.delete(organization)
        await self._session_context.session.flush()
    async def get_list(self) -> List[Organization]:
        """
            #TODO add comment
        """
        logging.info("OrganizationManager.get_list")
        query_results = await self._run_query(None)
        return query_results
    def to_json(self, organization: Organization) -> str:
        """
        Serialize the Organization object to a JSON string using the OrganizationSchema.
        """
        logging.info("OrganizationManager.to_json")
        schema = OrganizationSchema()
        organization_data = schema.dump(organization)
        return json.dumps(organization_data)
    def to_dict(self, organization: Organization) -> dict:
        """
        Serialize the Organization object to a JSON string using the OrganizationSchema.
        """
        logging.info("OrganizationManager.to_dict")
        schema = OrganizationSchema()
        organization_data = schema.dump(organization)
        return organization_data
    def from_json(self, json_str: str) -> Organization:
        """
        Deserialize a JSON string into a Organization object using the OrganizationSchema.
        """
        logging.info("OrganizationManager.from_json")
        schema = OrganizationSchema()
        data = json.loads(json_str)
        organization_dict = schema.load(data)
        new_organization = Organization(**organization_dict)
        return new_organization
    def from_dict(self, organization_dict: str) -> Organization:
        """
        #TODO add comment
        """
        logging.info("OrganizationManager.from_dict")
        schema = OrganizationSchema()
        organization_dict_converted = schema.load(organization_dict)
        new_organization = Organization(**organization_dict_converted)
        return new_organization
    async def add_bulk(self, organizations: List[Organization]) -> List[Organization]:
        """
        Add multiple organizations at once.
        """
        logging.info("OrganizationManager.add_bulk")
        for organization in organizations:
            organization_id = organization.organization_id
            code = organization.code
            if organization.organization_id is not None and organization.organization_id > 0:
                raise ValueError(
                    f"Organization is already added: {str(code)} {str(organization_id)}"
                )
            organization.insert_user_id = self.convert_uuid_to_model_uuid(
                self._session_context.customer_code)
            organization.last_update_user_id = self.convert_uuid_to_model_uuid(
                self._session_context.customer_code)
        self._session_context.session.add_all(organizations)
        await self._session_context.session.flush()
        return organizations
    async def update_bulk(
        self,
        organization_updates: List[Dict[int, Dict]]
    ) -> List[Organization]:
        """
        #TODO add comment
        """
        logging.info("OrganizationManager.update_bulk start")
        updated_organizations = []
        for update in organization_updates:
            organization_id = update.get("organization_id")
            if not isinstance(organization_id, int):
                raise TypeError(
                    f"The organization_id must be an integer, "
                    f"got {type(organization_id)} instead."
                )
            if not organization_id:
                continue
            logging.info("OrganizationManager.update_bulk organization_id:%s", organization_id)
            organization = await self.get_by_id(organization_id)
            if not organization:
                raise OrganizationNotFoundError(
                    f"Organization with ID {organization_id} not found!")
            for key, value in update.items():
                if key != "organization_id":
                    setattr(organization, key, value)
            organization.last_update_user_id = self.convert_uuid_to_model_uuid(
                self._session_context.customer_code)
            updated_organizations.append(organization)
        await self._session_context.session.flush()
        logging.info("OrganizationManager.update_bulk end")
        return updated_organizations
    async def delete_bulk(self, organization_ids: List[int]) -> bool:
        """
        Delete multiple organizations by their IDs.
        """
        logging.info("OrganizationManager.delete_bulk")
        for organization_id in organization_ids:
            if not isinstance(organization_id, int):
                raise TypeError(
                    f"The organization_id must be an integer, "
                    f"got {type(organization_id)} instead."
                )
            organization = await self.get_by_id(organization_id)
            if not organization:
                raise OrganizationNotFoundError(
                    f"Organization with ID {organization_id} not found!"
                )
            if organization:
                await self._session_context.session.delete(organization)
        await self._session_context.session.flush()
        return True
    async def count(self) -> int:
        """
        return the total number of organizations.
        """
        logging.info("OrganizationManager.count")
        result = await self._session_context.session.execute(select(Organization))
        return len(result.scalars().all())
    #TODO fix. needs to populate peek props. use getall and sort List
    async def get_sorted_list(
            self,
            sort_by: str,
            order: Optional[str] = "asc") -> List[Organization]:
        """
        Retrieve organizations sorted by a particular attribute.
        """
        if sort_by == "organization_id":
            sort_by = "_organization_id"
        if order == "asc":
            result = await self._session_context.session.execute(
                select(Organization).order_by(getattr(Organization, sort_by).asc()))
        else:
            result = await self._session_context.session.execute(
                select(Organization).order_by(getattr(Organization, sort_by).desc()))
        return result.scalars().all()
    async def refresh(self, organization: Organization) -> Organization:
        """
        Refresh the state of a given organization instance from the database.
        """
        logging.info("OrganizationManager.refresh")
        await self._session_context.session.refresh(organization)
        return organization
    async def exists(self, organization_id: int) -> bool:
        """
        Check if a organization with the given ID exists.
        """
        logging.info("OrganizationManager.exists %s", organization_id)
        if not isinstance(organization_id, int):
            raise TypeError(
                f"The organization_id must be an integer, "
                f"got {type(organization_id)} instead."
            )
        organization = await self.get_by_id(organization_id)
        return bool(organization)
    def is_equal(self, organization1: Organization, organization2: Organization) -> bool:
        """
        #TODO add comment
        """
        if not organization1:
            raise TypeError("Organization1 required.")
        if not organization2:
            raise TypeError("Organization2 required.")
        if not isinstance(organization1, Organization):
            raise TypeError("The organization1 must be an Organization instance.")
        if not isinstance(organization2, Organization):
            raise TypeError("The organization2 must be an Organization instance.")
        dict1 = self.to_dict(organization1)
        dict2 = self.to_dict(organization2)
        return dict1 == dict2
# endset
    async def get_by_tac_id(self, tac_id: int) -> List[Organization]:  # TacID
        """
        #TODO add comment
        """
        logging.info("OrganizationManager.get_by_tac_id")
        if not isinstance(tac_id, int):
            raise TypeError(
                f"The organization_id must be an integer, "
                f"got {type(tac_id)} instead."
            )
        query_filter = Organization.tac_id == tac_id
        query_results = await self._run_query(query_filter)
        return query_results
# endset

