import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.pac import Pac
class PacManager:
    def __init__(self, session: AsyncSession):
        self.session = session
    async def add(self, **kwargs):
        pac = Pac(**kwargs)
        self.session.add(pac)
        await self.session.commit()
        return pac
    async def get_by_id(self, pac_id: int):
        result = await self.session.execute(select(Pac).filter(Pac.pac_id == pac_id))
        return result.scalars().first()
    async def get_by_code(self, code: uuid.UUID):
        result = await self.session.execute(select(Pac).filter_by(code=code))
        return result.scalars().one_or_none()
    async def update(self, pac_id: int, **kwargs):
        pac = await self.get_by_id(pac_id)
        if pac:
            for key, value in kwargs.items():
                setattr(pac, key, value)
            await self.session.commit()
        return pac
    async def delete(self, pac_id: int):
        pac = await self.get_by_id(pac_id)
        if pac:
            self.session.delete(pac)
            await self.session.commit()
        return pac
    async def get_list(self):
        result = await self.session.execute(select(Pac))
        return result.scalars().all()

