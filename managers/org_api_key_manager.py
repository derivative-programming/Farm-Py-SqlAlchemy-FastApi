import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.org_api_key import OrgApiKey
class OrgApiKeyManager:
    def __init__(self, session: AsyncSession):
        self.session = session
    async def add(self, **kwargs):
        org_api_key = OrgApiKey(**kwargs)
        self.session.add(org_api_key)
        await self.session.commit()
        return org_api_key
    async def get_by_id(self, org_api_key_id: int):
        result = await self.session.execute(select(OrgApiKey).filter(OrgApiKey.id == org_api_key_id))
        return result.scalars().first()
    async def get_by_code(self, code: uuid.UUID):
        result = await self.session.execute(select(OrgApiKey).filter_by(code=code))
        return result.scalars().one_or_none()
    async def update(self, org_api_key_id: int, **kwargs):
        org_api_key = await self.get_by_id(org_api_key_id)
        if org_api_key:
            for key, value in kwargs.items():
                setattr(org_api_key, key, value)
            await self.session.commit()
        return org_api_key
    async def delete(self, org_api_key_id: int):
        org_api_key = await self.get_by_id(org_api_key_id)
        if org_api_key:
            self.session.delete(org_api_key)
            await self.session.commit()
        return org_api_key
    async def get_list(self):
        result = await self.session.execute(select(OrgApiKey))
        return result.scalars().all()
    async def get_by_organization_id(self, organization_id: int):
        result = await self.session.execute(select(OrgApiKey).filter(OrgApiKey.organization_id == organization_id))
        return result.scalars().all()
    async def get_by_org_customer_id(self, org_customer_id: int):
        result = await self.session.execute(select(OrgApiKey).filter(OrgApiKey.org_customer_id == org_customer_id))
        return result.scalars().all()
