import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.tac import Tac
class TacManager:
    def __init__(self, session: AsyncSession):
        self.session = session
    async def add(self, **kwargs):
        tac = Tac(**kwargs)
        self.session.add(tac)
        await self.session.commit()
        return tac
    async def get_by_id(self, tac_id: int):
        result = await self.session.execute(select(Tac).filter(Tac.id == tac_id))
        return result.scalars().first()
    async def get_by_code(self, code: uuid.UUID):
        result = await self.session.execute(select(Tac).filter_by(code=code))
        return result.scalars().one_or_none()
    async def update(self, tac_id: int, **kwargs):
        tac = await self.get_by_id(tac_id)
        if tac:
            for key, value in kwargs.items():
                setattr(tac, key, value)
            await self.session.commit()
        return tac
    async def delete(self, tac_id: int):
        tac = await self.get_by_id(tac_id)
        if tac:
            self.session.delete(tac)
            await self.session.commit()
        return tac
    async def get_list(self):
        result = await self.session.execute(select(Tac))
        return result.scalars().all()
    async def get_by_pac_id(self, pac_id: int):
        result = await self.session.execute(select(Tac).filter(Tac.pac_id == pac_id))
        return result.scalars().all()
