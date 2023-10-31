import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.land import Land
class LandManager:
    def __init__(self, session: AsyncSession):
        self.session = session
    async def add(self, **kwargs):
        land = Land(**kwargs)
        self.session.add(land)
        await self.session.commit()
        return land
    async def get_by_id(self, land_id: int):
        result = await self.session.execute(select(Land).filter(Land.land_id == land_id))
        return result.scalars().first()
    async def get_by_code(self, code: uuid.UUID):
        result = await self.session.execute(select(Land).filter_by(code=code))
        return result.scalars().one_or_none()
    async def update(self, land_id: int, **kwargs):
        land = await self.get_by_id(land_id)
        if land:
            for key, value in kwargs.items():
                setattr(land, key, value)
            await self.session.commit()
        return land
    async def delete(self, land_id: int):
        land = await self.get_by_id(land_id)
        if land:
            self.session.delete(land)
            await self.session.commit()
        return land
    async def get_list(self):
        result = await self.session.execute(select(Land))
        return result.scalars().all()
    async def get_by_pac_id(self, pac_id: int):
        result = await self.session.execute(select(Land).filter(Land.pac_id == pac_id))
        return result.scalars().all()
