import json
import uuid
from typing import List, Optional, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.org_api_key import OrgApiKey
from models.serialization_schema.org_api_key import OrgApiKeySchema
class OrgApiKeyManager:
    def __init__(self, session: AsyncSession):
        self.session = session
    def build(self, **kwargs) -> OrgApiKey:
        return OrgApiKey(**kwargs)
    async def add(self, org_api_key: OrgApiKey) -> OrgApiKey:
        self.session.add(org_api_key)
        await self.session.commit()
        return org_api_key
    async def get_by_id(self, org_api_key_id: int) -> Optional[OrgApiKey]:
        result = await self.session.execute(select(OrgApiKey).filter(OrgApiKey.org_api_key_id == org_api_key_id))
        return result.scalars().first()
    async def get_by_code(self, code: uuid.UUID) -> Optional[OrgApiKey]:
        result = await self.session.execute(select(OrgApiKey).filter_by(code=code))
        return result.scalars().one_or_none()
    async def update(self, org_api_key: OrgApiKey, **kwargs) -> Optional[OrgApiKey]:
        if org_api_key:
            for key, value in kwargs.items():
                setattr(org_api_key, key, value)
            await self.session.commit()
        return org_api_key
    async def delete(self, org_api_key_id: int) -> Optional[OrgApiKey]:
        org_api_key = await self.get_by_id(org_api_key_id)
        if org_api_key:
            self.session.delete(org_api_key)
            await self.session.commit()
        return org_api_key
    async def get_list(self) -> List[OrgApiKey]:
        result = await self.session.execute(select(OrgApiKey))
        return result.scalars().all()
    def to_json(self, org_api_key:OrgApiKey) -> str:
        """
        Serialize the OrgApiKey object to a JSON string using the OrgApiKeySchema.
        """
        schema = OrgApiKeySchema()
        org_api_key_data = schema.dump(org_api_key)
        return json.dumps(org_api_key_data)
    def from_json(self, json_str: str) -> OrgApiKey:
        """
        Deserialize a JSON string into a OrgApiKey object using the OrgApiKeySchema.
        """
        schema = OrgApiKeySchema()
        data = json.loads(json_str)
        org_api_key_dict = schema.load(data)
        new_org_api_key = OrgApiKey(**org_api_key_dict)
        return new_org_api_key
    async def add_bulk(self, org_api_keys_data: List[Dict]) -> List[OrgApiKey]:
        """Add multiple org_api_keys at once."""
        org_api_keys = [OrgApiKey(**data) for data in org_api_keys_data]
        self.session.add_all(org_api_keys)
        await self.session.commit()
        return org_api_keys
    async def update_bulk(self, org_api_key_updates: List[Dict[int, Dict]]) -> List[OrgApiKey]:
        """Update multiple org_api_keys at once."""
        updated_org_api_keys = []
        for update in org_api_key_updates:
            org_api_key_id = update.get("org_api_key_id")
            if not org_api_key_id:
                continue
            org_api_key = await self.get_by_id(org_api_key_id)
            if not org_api_key:
                continue
            for key, value in update.items():
                if key != "org_api_key_id":
                    setattr(org_api_key, key, value)
            updated_org_api_keys.append(org_api_key)
        await self.session.commit()
        return updated_org_api_keys
    async def delete_bulk(self, org_api_key_ids: List[int]) -> bool:
        """Delete multiple org_api_keys by their IDs."""
        for org_api_key_id in org_api_key_ids:
            org_api_key = await self.get_by_id(org_api_key_id)
            if org_api_key:
                self.session.delete(org_api_key)
        await self.session.commit()
        return True
    async def count(self) -> int:
        """Return the total number of org_api_keys."""
        result = await self.session.execute(select(OrgApiKey))
        return len(result.scalars().all())
    async def get_sorted_list(self, sort_by: str, order: Optional[str] = "asc") -> List[OrgApiKey]:
        """Retrieve org_api_keys sorted by a particular attribute."""
        if order == "asc":
            result = await self.session.execute(select(OrgApiKey).order_by(getattr(OrgApiKey, sort_by).asc()))
        else:
            result = await self.session.execute(select(OrgApiKey).order_by(getattr(OrgApiKey, sort_by).desc()))
        return result.scalars().all()
    async def refresh(self, org_api_key: OrgApiKey) -> OrgApiKey:
        """Refresh the state of a given org_api_key instance from the database."""
        self.session.refresh(org_api_key)
        return org_api_key
    async def exists(self, org_api_key_id: int) -> bool:
        """Check if a org_api_key with the given ID exists."""
        org_api_key = await self.get_by_id(org_api_key_id)
        return bool(org_api_key)

    async def get_by_organization_id(self, organization_id: int): # OrganizationID
        result = await self.session.execute(select(OrgApiKey).filter(OrgApiKey.organization_id == organization_id))
        return result.scalars().all()
    async def get_by_org_customer_id(self, org_customer_id: int): # OrgCustomerID
        result = await self.session.execute(select(OrgApiKey).filter(OrgApiKey.org_customer_id == org_customer_id))
        return result.scalars().all()

