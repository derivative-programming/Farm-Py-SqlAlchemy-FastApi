import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.organization import Organization
class OrganizationManager:
    def __init__(self, session: AsyncSession):
        self.session = session
    async def add(self, **kwargs):
        organization = Organization(**kwargs)
        self.session.add(organization)
        await self.session.commit()
        return organization
    async def get_by_id(self, organization_id: int):
        result = await self.session.execute(select(Organization).filter(Organization.id == organization_id))
        return result.scalars().first()
    async def get_by_code(self, code: uuid.UUID):
        result = await self.session.execute(select(Organization).filter_by(code=code))
        return result.scalars().one_or_none()
    async def update(self, organization_id: int, **kwargs):
        organization = await self.get_by_id(organization_id)
        if organization:
            for key, value in kwargs.items():
                setattr(organization, key, value)
            await self.session.commit()
        return organization
    async def delete(self, organization_id: int):
        organization = await self.get_by_id(organization_id)
        if organization:
            self.session.delete(organization)
            await self.session.commit()
        return organization
    async def get_list(self):
        result = await self.session.execute(select(Organization))
        return result.scalars().all()
    async def get_by_tac_id(self, tac_id: int):
        result = await self.session.execute(select(Organization).filter(Organization.tac_id == tac_id))
        return result.scalars().all()
