import json
import uuid
from enum import Enum
from typing import List, Optional, Dict
from sqlalchemy import and_, outerjoin
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select#, join, outerjoin, and_
from models.tac import Tac # TacID
from models.organization import Organization
from models.serialization_schema.organization import OrganizationSchema
from services.logging_config import get_logger
import logging
logger = get_logger(__name__)
class OrganizationNotFoundError(Exception):
    pass

class OrganizationManager:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def initialize(self):
        logging.info("OrganizationManager.Initialize")

    async def build(self, **kwargs) -> Organization:
        logging.info("OrganizationManager.build")
        return Organization(**kwargs)
    async def add(self, organization: Organization) -> Organization:
        logging.info("OrganizationManager.add")
        self.session.add(organization)
        await self.session.flush()
        return organization
    def _build_query(self):
        logging.info("OrganizationManager._build_query")
#         join_condition = None
#
#         join_condition = outerjoin(join_condition, Tac, and_(Organization.tac_id == Tac.tac_id, Organization.tac_id != 0))
#
#         if join_condition is not None:
#             query = select(Organization
#                         ,Tac #tac_id
#                         ).select_from(join_condition)
#         else:
#             query = select(Organization)
        query = select(Organization
                    ,Tac #tac_id
                    )

        query = query.outerjoin(Tac, and_(Organization.tac_id == Tac.tac_id, Organization.tac_id != 0))

        return query
    async def _run_query(self, query_filter) -> List[Organization]:
        logging.info("OrganizationManager._run_query")
        organization_query_all = self._build_query()
        if query_filter is not None:
            query = organization_query_all.filter(query_filter)
        else:
            query = organization_query_all
        result_proxy = await self.session.execute(query)
        query_results = result_proxy.all()
        result = list()
        for query_result_row in query_results:
            i = 0
            organization = query_result_row[i]
            i = i + 1

            tac = query_result_row[i] #tac_id
            i = i + 1

            organization.tac_code_peek = tac.code if tac else uuid.UUID(int=0) #tac_id

            result.append(organization)
        return result
    def _first_or_none(self,organization_list:List) -> Organization:
        return organization_list[0] if organization_list else None
    async def get_by_id(self, organization_id: int) -> Optional[Organization]:
        logging.info("OrganizationManager.get_by_id start organization_id:" + str(organization_id))
        if not isinstance(organization_id, int):
            raise TypeError(f"The organization_id must be an integer, got {type(organization_id)} instead.")
        # result = await self.session.execute(select(Organization).filter(Organization.organization_id == organization_id))
        # result = await self.session.execute(select(Organization).filter(Organization.organization_id == organization_id))
        # return result.scalars().first()
        query_filter = Organization.organization_id == organization_id
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)
    async def get_by_code(self, code: uuid.UUID) -> Optional[Organization]:
        logging.info(f"OrganizationManager.get_by_code {code}")
        # result = await self.session.execute(select(Organization).filter_by(code=code))
        # return result.scalars().one_or_none()
        query_filter = Organization.code==code
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)
    async def update(self, organization: Organization, **kwargs) -> Optional[Organization]:
        logging.info("OrganizationManager.update")
        if organization:
            for key, value in kwargs.items():
                setattr(organization, key, value)
            await self.session.flush()
        return organization
    async def delete(self, organization_id: int):
        logging.info(f"OrganizationManager.delete {organization_id}")
        if not isinstance(organization_id, int):
            raise TypeError(f"The organization_id must be an integer, got {type(organization_id)} instead.")
        organization = await self.get_by_id(organization_id)
        if not organization:
            raise OrganizationNotFoundError(f"Organization with ID {organization_id} not found!")
        await self.session.delete(organization)
        await self.session.flush()
    async def get_list(self) -> List[Organization]:
        logging.info("OrganizationManager.get_list")
        # result = await self.session.execute(select(Organization))
        # return result.scalars().all()
        query_results = await self._run_query(None)
        return query_results
    def to_json(self, organization:Organization) -> str:
        logging.info("OrganizationManager.to_json")
        """
        Serialize the Organization object to a JSON string using the OrganizationSchema.
        """
        schema = OrganizationSchema()
        organization_data = schema.dump(organization)
        return json.dumps(organization_data)
    def to_dict(self, organization:Organization) -> dict:
        logging.info("OrganizationManager.to_dict")
        """
        Serialize the Organization object to a JSON string using the OrganizationSchema.
        """
        schema = OrganizationSchema()
        organization_data = schema.dump(organization)
        return organization_data
    def from_json(self, json_str: str) -> Organization:
        logging.info("OrganizationManager.from_json")
        """
        Deserialize a JSON string into a Organization object using the OrganizationSchema.
        """
        schema = OrganizationSchema()
        data = json.loads(json_str)
        organization_dict = schema.load(data)
        new_organization = Organization(**organization_dict)
        return new_organization
    def from_dict(self, organization_dict: str) -> Organization:
        logging.info("OrganizationManager.from_dict")
        schema = OrganizationSchema()
        organization_dict_converted = schema.load(organization_dict)
        new_organization = Organization(**organization_dict_converted)
        return new_organization
    async def add_bulk(self, organizations: List[Organization]) -> List[Organization]:
        logging.info("OrganizationManager.add_bulk")
        """Add multiple organizations at once."""
        self.session.add_all(organizations)
        await self.session.flush()
        return organizations
    async def update_bulk(self, organization_updates: List[Dict[int, Dict]]) -> List[Organization]:
        logging.info("OrganizationManager.update_bulk start")
        updated_organizations = []
        for update in organization_updates:
            organization_id = update.get("organization_id")
            if not isinstance(organization_id, int):
                raise TypeError(f"The organization_id must be an integer, got {type(organization_id)} instead.")
            if not organization_id:
                continue
            logging.info(f"OrganizationManager.update_bulk organization_id:{organization_id}")
            organization = await self.get_by_id(organization_id)
            if not organization:
                raise OrganizationNotFoundError(f"Organization with ID {organization_id} not found!")
            for key, value in update.items():
                if key != "organization_id":
                    setattr(organization, key, value)
            updated_organizations.append(organization)
        await self.session.flush()
        logging.info("OrganizationManager.update_bulk end")
        return updated_organizations
    async def delete_bulk(self, organization_ids: List[int]) -> bool:
        logging.info("OrganizationManager.delete_bulk")
        """Delete multiple organizations by their IDs."""
        for organization_id in organization_ids:
            if not isinstance(organization_id, int):
                raise TypeError(f"The organization_id must be an integer, got {type(organization_id)} instead.")
            organization = await self.get_by_id(organization_id)
            if not organization:
                raise OrganizationNotFoundError(f"Organization with ID {organization_id} not found!")
            if organization:
                await self.session.delete(organization)
        await self.session.flush()
        return True
    async def count(self) -> int:
        logging.info("OrganizationManager.count")
        """Return the total number of organizations."""
        result = await self.session.execute(select(Organization))
        return len(result.scalars().all())
    #TODO fix. needs to populate peek props. use getall and sort List
    async def get_sorted_list(self, sort_by: str, order: Optional[str] = "asc") -> List[Organization]:
        """Retrieve organizations sorted by a particular attribute."""
        if order == "asc":
            result = await self.session.execute(select(Organization).order_by(getattr(Organization, sort_by).asc()))
        else:
            result = await self.session.execute(select(Organization).order_by(getattr(Organization, sort_by).desc()))
        return result.scalars().all()
    async def refresh(self, organization: Organization) -> Organization:
        logging.info("OrganizationManager.refresh")
        """Refresh the state of a given organization instance from the database."""
        await self.session.refresh(organization)
        return organization
    async def exists(self, organization_id: int) -> bool:
        logging.info(f"OrganizationManager.exists {organization_id}")
        """Check if a organization with the given ID exists."""
        if not isinstance(organization_id, int):
            raise TypeError(f"The organization_id must be an integer, got {type(organization_id)} instead.")
        organization = await self.get_by_id(organization_id)
        return bool(organization)
    def is_equal(self, organization1:Organization, organization2:Organization) -> bool:
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

    async def get_by_tac_id(self, tac_id: int) -> List[Organization]: # TacID
        logging.info("OrganizationManager.get_by_tac_id")
        if not isinstance(tac_id, int):
            raise TypeError(f"The organization_id must be an integer, got {type(tac_id)} instead.")
        # result = await self.session.execute(select(Organization).filter(Organization.tac_id == tac_id))
        # return result.scalars().all()
        query_filter = Organization.tac_id == tac_id
        query_results = await self._run_query(query_filter)
        return query_results

