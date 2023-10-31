import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.date_greater_than_filter import DateGreaterThanFilter
class DateGreaterThanFilterManager:
    def __init__(self, session: AsyncSession):
        self.session = session
    async def add(self, **kwargs):
        date_greater_than_filter = DateGreaterThanFilter(**kwargs)
        self.session.add(date_greater_than_filter)
        await self.session.commit()
        return date_greater_than_filter
    async def get_by_id(self, date_greater_than_filter_id: int):
        result = await self.session.execute(select(DateGreaterThanFilter).filter(DateGreaterThanFilter.date_greater_than_filter_id == date_greater_than_filter_id))
        return result.scalars().first()
    async def get_by_code(self, code: uuid.UUID):
        result = await self.session.execute(select(DateGreaterThanFilter).filter_by(code=code))
        return result.scalars().one_or_none()
    async def update(self, date_greater_than_filter_id: int, **kwargs):
        date_greater_than_filter = await self.get_by_id(date_greater_than_filter_id)
        if date_greater_than_filter:
            for key, value in kwargs.items():
                setattr(date_greater_than_filter, key, value)
            await self.session.commit()
        return date_greater_than_filter
    async def delete(self, date_greater_than_filter_id: int):
        date_greater_than_filter = await self.get_by_id(date_greater_than_filter_id)
        if date_greater_than_filter:
            self.session.delete(date_greater_than_filter)
            await self.session.commit()
        return date_greater_than_filter
    async def get_list(self):
        result = await self.session.execute(select(DateGreaterThanFilter))
        return result.scalars().all()
    async def get_by_pac_id(self, pac_id: int):
        result = await self.session.execute(select(DateGreaterThanFilter).filter(DateGreaterThanFilter.pac_id == pac_id))
        return result.scalars().all()
