import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from managers.pac_manager import PacManager as PacIDManager #PacID
from managers.date_greater_than_filter_manager import DateGreaterThanFilterManager
from models.date_greater_than_filter import DateGreaterThanFilter
class DateGreaterThanFilterBusObj:
    def __init__(self, code:uuid.UUID=None, date_greater_than_filter_id:int=None, date_greater_than_filter:DateGreaterThanFilter=None, session:AsyncSession=None):
        self.date_greater_than_filter = date_greater_than_filter
        self.session = session
        self.manager = DateGreaterThanFilterManager(session)
        # If initialized with a date_greater_than_filter_id and not a date_greater_than_filter object, load the date_greater_than_filter
        if date_greater_than_filter_id and not date_greater_than_filter and not code:
            date_greater_than_filter_obj = self.manager.get_by_id(date_greater_than_filter_id)
            self.date_greater_than_filter = date_greater_than_filter_obj
        if code and not date_greater_than_filter and not date_greater_than_filter_id:
            date_greater_than_filter_obj = self.manager.get_by_code(code)
            self.date_greater_than_filter = date_greater_than_filter_obj
    async def save(self):
        if self.date_greater_than_filter.id > 0:
            self.date_greater_than_filter = await self.manager.update(self.date_greater_than_filter)
        if self.date_greater_than_filter.id == 0:
            self.date_greater_than_filter = await self.manager.add(self.date_greater_than_filter)
    async def delete(self):
        if self.date_greater_than_filter.id > 0:
            self.date_greater_than_filter = await self.manager.delete(self.date_greater_than_filter.id)
    async def get_pac_id_rel_obj(self, pac_id: int): #PacID
        pac_manager = PacIDManager(self.session)
        return pac_manager.get_by_id(self.date_greater_than_filter.pac_id)
