import json
import uuid
from typing import List, Optional, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.org_api_key import OrgApiKey
from models.serialization_schema.org_api_key import OrgApiKeySchema
class OrgApiKeyNotFoundError(Exception):
    pass
class OrgApiKeyManager:
    def __init__(self, session: AsyncSession):
        self.session = session
    async def build(self, **kwargs) -> OrgApiKey:
        return OrgApiKey(**kwargs)
    async def add(self, org_api_key: OrgApiKey) -> OrgApiKey:
        self.session.add(org_api_key)
        await self.session.commit()
        return org_api_key
    async def get_by_id(self, org_api_key_id: int) -> Optional[OrgApiKey]:
        if not isinstance(org_api_key_id, int):
            raise TypeError(f"The org_api_key_id must be an integer, got {type(org_api_key_id)} instead.")
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
    async def delete(self, org_api_key_id: int):
        if not isinstance(org_api_key_id, int):
            raise TypeError(f"The org_api_key_id must be an integer, got {type(org_api_key_id)} instead.")
        org_api_key = await self.get_by_id(org_api_key_id)
        if not org_api_key:
            raise OrgApiKeyNotFoundError(f"OrgApiKey with ID {org_api_key_id} not found!")
        await self.session.delete(org_api_key)
        await self.session.commit()
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
    def to_dict(self, org_api_key:OrgApiKey) -> dict:
        """
        Serialize the OrgApiKey object to a JSON string using the OrgApiKeySchema.
        """
        schema = OrgApiKeySchema()
        org_api_key_data = schema.dump(org_api_key)
        return org_api_key_data
    def from_json(self, json_str: str) -> OrgApiKey:
        """
        Deserialize a JSON string into a OrgApiKey object using the OrgApiKeySchema.
        """
        schema = OrgApiKeySchema()
        data = json.loads(json_str)
        org_api_key_dict = schema.load(data)
        new_org_api_key = OrgApiKey(**org_api_key_dict)
        return new_org_api_key
    def from_dict(self, org_api_key_dict: str) -> OrgApiKey:
        new_org_api_key = OrgApiKey(**org_api_key_dict)
        return new_org_api_key
    async def add_bulk(self, org_api_keys: List[OrgApiKey]) -> List[OrgApiKey]:
        """Add multiple org_api_keys at once."""
        self.session.add_all(org_api_keys)
        await self.session.commit()
        return org_api_keys
    async def update_bulk(self, org_api_key_updates: List[Dict[int, Dict]]) -> List[OrgApiKey]:
        """Update multiple org_api_keys at once."""
        updated_org_api_keys = []
        for update in org_api_key_updates:
            org_api_key_id = update.get("org_api_key_id")
            if not isinstance(org_api_key_id, int):
                raise TypeError(f"The org_api_key_id must be an integer, got {type(org_api_key_id)} instead.")
            if not org_api_key_id:
                continue
            org_api_key = await self.get_by_id(org_api_key_id)
            if not org_api_key:
                raise OrgApiKeyNotFoundError(f"OrgApiKey with ID {org_api_key_id} not found!")
            for key, value in update.items():
                if key != "org_api_key_id":
                    setattr(org_api_key, key, value)
            updated_org_api_keys.append(org_api_key)
        await self.session.commit()
        return updated_org_api_keys
    async def delete_bulk(self, org_api_key_ids: List[int]) -> bool:
        """Delete multiple org_api_keys by their IDs."""
        for org_api_key_id in org_api_key_ids:
            if not isinstance(org_api_key_id, int):
                raise TypeError(f"The org_api_key_id must be an integer, got {type(org_api_key_id)} instead.")
            org_api_key = await self.get_by_id(org_api_key_id)
            if not org_api_key:
                raise OrgApiKeyNotFoundError(f"OrgApiKey with ID {org_api_key_id} not found!")
            if org_api_key:
                await self.session.delete(org_api_key)
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
        await self.session.refresh(org_api_key)
        return org_api_key
    async def exists(self, org_api_key_id: int) -> bool:
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

    async def get_by_organization_id(self, organization_id: int): # OrganizationID
        if not isinstance(organization_id, int):
            raise TypeError(f"The org_api_key_id must be an integer, got {type(organization_id)} instead.")
        result = await self.session.execute(select(OrgApiKey).filter(OrgApiKey.organization_id == organization_id))
        return result.scalars().all()
    async def get_by_org_customer_id(self, org_customer_id: int): # OrgCustomerID
        if not isinstance(org_customer_id, int):
            raise TypeError(f"The org_api_key_id must be an integer, got {type(org_customer_id)} instead.")
        result = await self.session.execute(select(OrgApiKey).filter(OrgApiKey.org_customer_id == org_customer_id))
        return result.scalars().all()

