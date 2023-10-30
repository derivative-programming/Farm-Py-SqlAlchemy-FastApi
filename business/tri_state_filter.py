import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from managers import PacManager as PacIDManager #PacID
from managers import TriStateFilterManager
from models import TriStateFilter
class TriStateFilterBusObj:
    def __init__(self, code:uuid.UUID=None, tri_state_filter_id:int=None, tri_state_filter:TriStateFilter=None, session:AsyncSession=None):
        self.tri_state_filter = tri_state_filter
        self.session = session
        self.manager = TriStateFilterManager(session)
        # If initialized with a tri_state_filter_id and not a tri_state_filter object, load the tri_state_filter
        if tri_state_filter_id and not tri_state_filter and not code:
            tri_state_filter_obj = self.manager.get_by_id(tri_state_filter_id)
            self.tri_state_filter = tri_state_filter_obj
        if code and not tri_state_filter and not tri_state_filter_id:
            tri_state_filter_obj = self.manager.get_by_code(code)
            self.tri_state_filter = tri_state_filter_obj
    async def save(self):
        if self.tri_state_filter.id > 0:
            self.tri_state_filter = await self.manager.update(self.tri_state_filter)
        if self.tri_state_filter.id == 0:
            self.tri_state_filter = await self.manager.add(self.tri_state_filter)
    async def delete(self):
        if self.tri_state_filter.id > 0:
            self.tri_state_filter = await self.manager.delete(self.tri_state_filter.id)
    async def get_pac_id_rel_obj(self, pac_id: int): #PacID
        pac_manager = PacIDManager(self.session)
        return pac_manager.get_by_id(self.tri_state_filter.pac_id)
