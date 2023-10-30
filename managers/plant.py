import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.plant import Plant
class PlantManager:
    def __init__(self, session: AsyncSession):
        self.session = session
    async def add(self, **kwargs):
        plant = Plant(**kwargs)
        self.session.add(plant)
        await self.session.commit()
        return plant
    async def get_by_id(self, plant_id: int):
        result = await self.session.execute(select(Plant).filter(Plant.id == plant_id))
        return result.scalars().first()
    async def get_by_code(self, code: uuid.UUID):
        result = await self.session.execute(select(Plant).filter_by(code=code))
        return result.scalars().one_or_none()
    async def update(self, plant_id: int, **kwargs):
        plant = await self.get_by_id(plant_id)
        if plant:
            for key, value in kwargs.items():
                setattr(plant, key, value)
            await self.session.commit()
        return plant
    async def delete(self, plant_id: int):
        plant = await self.get_by_id(plant_id)
        if plant:
            self.session.delete(plant)
            await self.session.commit()
        return plant
    async def get_list(self):
        result = await self.session.execute(select(Plant))
        return result.scalars().all()
    async def get_by_flvr_foreign_key_id(self, flvr_foreign_key_id: int):
        result = await self.session.execute(select(Plant).filter(Plant.flvr_foreign_key_id == flvr_foreign_key_id))
        return result.scalars().all()
    async def get_by_land_id(self, land_id: int):
        result = await self.session.execute(select(Plant).filter(Plant.land_id == land_id))
        return result.scalars().all()
