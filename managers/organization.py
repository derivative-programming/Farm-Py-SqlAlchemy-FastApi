import json
import uuid
from typing import List, Optional, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.organization import Organization
from models.serialization_schema.organization import OrganizationSchema
from services.logging_config import get_logger
logger = get_logger(__name__)
class OrganizationNotFoundError(Exception):
    pass
class OrganizationManager:
    def __init__(self, session: AsyncSession):
        self.session = session
    async def build(self, **kwargs) -> Organization:
        return Organization(**kwargs)
    async def add(self, organization: Organization) -> Organization:
        self.session.add(organization)
        await self.session.commit()
        return organization
    async def get_by_id(self, organization_id: int) -> Optional[Organization]:
        if not isinstance(organization_id, int):
            raise TypeError(f"The organization_id must be an integer, got {type(organization_id)} instead.")
        result = await self.session.execute(select(Organization).filter(Organization.organization_id == organization_id))
        return result.scalars().first()
    async def get_by_code(self, code: uuid.UUID) -> Optional[Organization]:
        result = await self.session.execute(select(Organization).filter_by(code=code))
        return result.scalars().one_or_none()
    async def update(self, organization: Organization, **kwargs) -> Optional[Organization]:
        if organization:
            for key, value in kwargs.items():
                setattr(organization, key, value)
            await self.session.commit()
        return organization
    async def delete(self, organization_id: int):
        if not isinstance(organization_id, int):
            raise TypeError(f"The organization_id must be an integer, got {type(organization_id)} instead.")
        organization = await self.get_by_id(organization_id)
        if not organization:
            raise OrganizationNotFoundError(f"Organization with ID {organization_id} not found!")
        await self.session.delete(organization)
        await self.session.commit()
    async def get_list(self) -> List[Organization]:
        result = await self.session.execute(select(Organization))
        return result.scalars().all()
    def to_json(self, organization:Organization) -> str:
        """
        Serialize the Organization object to a JSON string using the OrganizationSchema.
        """
        schema = OrganizationSchema()
        organization_data = schema.dump(organization)
        return json.dumps(organization_data)
    def to_dict(self, organization:Organization) -> dict:
        """
        Serialize the Organization object to a JSON string using the OrganizationSchema.
        """
        schema = OrganizationSchema()
        organization_data = schema.dump(organization)
        return organization_data
    def from_json(self, json_str: str) -> Organization:
        """
        Deserialize a JSON string into a Organization object using the OrganizationSchema.
        """
        schema = OrganizationSchema()
        data = json.loads(json_str)
        organization_dict = schema.load(data)
        new_organization = Organization(**organization_dict)
        return new_organization
    def from_dict(self, organization_dict: str) -> Organization:
        schema = OrganizationSchema()
        organization_dict_converted = schema.load(organization_dict)
        new_organization = Organization(**organization_dict_converted)
        return new_organization
    async def add_bulk(self, organizations: List[Organization]) -> List[Organization]:
        """Add multiple organizations at once."""
        self.session.add_all(organizations)
        await self.session.commit()
        return organizations
    async def update_bulk(self, organization_updates: List[Dict[int, Dict]]) -> List[Organization]:
        """Update multiple organizations at once."""
        updated_organizations = []
        for update in organization_updates:
            organization_id = update.get("organization_id")
            if not isinstance(organization_id, int):
                raise TypeError(f"The organization_id must be an integer, got {type(organization_id)} instead.")
            if not organization_id:
                continue
            organization = await self.get_by_id(organization_id)
            if not organization:
                raise OrganizationNotFoundError(f"Organization with ID {organization_id} not found!")
            for key, value in update.items():
                if key != "organization_id":
                    setattr(organization, key, value)
            updated_organizations.append(organization)
        await self.session.commit()
        return updated_organizations
    async def delete_bulk(self, organization_ids: List[int]) -> bool:
        """Delete multiple organizations by their IDs."""
        for organization_id in organization_ids:
            if not isinstance(organization_id, int):
                raise TypeError(f"The organization_id must be an integer, got {type(organization_id)} instead.")
            organization = await self.get_by_id(organization_id)
            if not organization:
                raise OrganizationNotFoundError(f"Organization with ID {organization_id} not found!")
            if organization:
                await self.session.delete(organization)
        await self.session.commit()
        return True
    async def count(self) -> int:
        """Return the total number of organizations."""
        result = await self.session.execute(select(Organization))
        return len(result.scalars().all())
    async def get_sorted_list(self, sort_by: str, order: Optional[str] = "asc") -> List[Organization]:
        """Retrieve organizations sorted by a particular attribute."""
        if order == "asc":
            result = await self.session.execute(select(Organization).order_by(getattr(Organization, sort_by).asc()))
        else:
            result = await self.session.execute(select(Organization).order_by(getattr(Organization, sort_by).desc()))
        return result.scalars().all()
    async def refresh(self, organization: Organization) -> Organization:
        """Refresh the state of a given organization instance from the database."""
        await self.session.refresh(organization)
        return organization
    async def exists(self, organization_id: int) -> bool:
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
        logger.info("vrtest")
        logger.info(dict1)
        logger.info(dict2)
        return dict1 == dict2

    async def get_by_tac_id(self, tac_id: int): # TacID
        if not isinstance(tac_id, int):
            raise TypeError(f"The organization_id must be an integer, got {type(tac_id)} instead.")
        result = await self.session.execute(select(Organization).filter(Organization.tac_id == tac_id))
        return result.scalars().all()

