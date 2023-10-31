import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.flavor import Flavor
class FlavorManager:
    def __init__(self, session: AsyncSession):
        self.session = session
    async def add(self, **kwargs):
        flavor = Flavor(**kwargs)
        self.session.add(flavor)
        await self.session.commit()
        return flavor
    async def get_by_id(self, flavor_id: int):
        result = await self.session.execute(select(Flavor).filter(Flavor.flavor_id == flavor_id))
        return result.scalars().first()
    async def get_by_code(self, code: uuid.UUID):
        result = await self.session.execute(select(Flavor).filter_by(code=code))
        return result.scalars().one_or_none()
    async def update(self, flavor_id: int, **kwargs):
        flavor = await self.get_by_id(flavor_id)
        if flavor:
            for key, value in kwargs.items():
                setattr(flavor, key, value)
            await self.session.commit()
        return flavor
    async def delete(self, flavor_id: int):
        flavor = await self.get_by_id(flavor_id)
        if flavor:
            self.session.delete(flavor)
            await self.session.commit()
        return flavor
    async def get_list(self):
        result = await self.session.execute(select(Flavor))
        return result.scalars().all()
    async def get_by_pac_id(self, pac_id: int):
        result = await self.session.execute(select(Flavor).filter(Flavor.pac_id == pac_id))
        return result.scalars().all()
