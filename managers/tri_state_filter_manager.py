import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.tri_state_filter import TriStateFilter
class TriStateFilterManager:
    def __init__(self, session: AsyncSession):
        self.session = session
    async def add(self, **kwargs):
        tri_state_filter = TriStateFilter(**kwargs)
        self.session.add(tri_state_filter)
        await self.session.commit()
        return tri_state_filter
    async def get_by_id(self, tri_state_filter_id: int):
        result = await self.session.execute(select(TriStateFilter).filter(TriStateFilter.id == tri_state_filter_id))
        return result.scalars().first()
    async def get_by_code(self, code: uuid.UUID):
        result = await self.session.execute(select(TriStateFilter).filter_by(code=code))
        return result.scalars().one_or_none()
    async def update(self, tri_state_filter_id: int, **kwargs):
        tri_state_filter = await self.get_by_id(tri_state_filter_id)
        if tri_state_filter:
            for key, value in kwargs.items():
                setattr(tri_state_filter, key, value)
            await self.session.commit()
        return tri_state_filter
    async def delete(self, tri_state_filter_id: int):
        tri_state_filter = await self.get_by_id(tri_state_filter_id)
        if tri_state_filter:
            self.session.delete(tri_state_filter)
            await self.session.commit()
        return tri_state_filter
    async def get_list(self):
        result = await self.session.execute(select(TriStateFilter))
        return result.scalars().all()
    async def get_by_pac_id(self, pac_id: int):
        result = await self.session.execute(select(TriStateFilter).filter(TriStateFilter.pac_id == pac_id))
        return result.scalars().all()
