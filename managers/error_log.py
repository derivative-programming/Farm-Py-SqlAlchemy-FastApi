import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.error_log import ErrorLog
class ErrorLogManager:
    def __init__(self, session: AsyncSession):
        self.session = session
    async def add(self, **kwargs):
        error_log = ErrorLog(**kwargs)
        self.session.add(error_log)
        await self.session.commit()
        return error_log
    async def get_by_id(self, error_log_id: int):
        result = await self.session.execute(select(ErrorLog).filter(ErrorLog.error_log_id == error_log_id))
        return result.scalars().first()
    async def get_by_code(self, code: uuid.UUID):
        result = await self.session.execute(select(ErrorLog).filter_by(code=code))
        return result.scalars().one_or_none()
    async def update(self, error_log_id: int, **kwargs):
        error_log = await self.get_by_id(error_log_id)
        if error_log:
            for key, value in kwargs.items():
                setattr(error_log, key, value)
            await self.session.commit()
        return error_log
    async def delete(self, error_log_id: int):
        error_log = await self.get_by_id(error_log_id)
        if error_log:
            self.session.delete(error_log)
            await self.session.commit()
        return error_log
    async def get_list(self):
        result = await self.session.execute(select(ErrorLog))
        return result.scalars().all()
    async def get_by_pac_id(self, pac_id: int):
        result = await self.session.execute(select(ErrorLog).filter(ErrorLog.pac_id == pac_id))
        return result.scalars().all()
