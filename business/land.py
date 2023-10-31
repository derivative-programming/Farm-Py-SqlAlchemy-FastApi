import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from managers import PacManager as PacIDManager #PacID
from managers import LandManager
from models import Land
class LandBusObj:
    def __init__(self, code:uuid.UUID=None, land_id:int=None, land:Land=None, session:AsyncSession=None):
        self.land = land
        self.session = session
        self.manager = LandManager(session)
        # If initialized with a land_id and not a land object, load the land
        if land_id and not land and not code:
            land_obj = self.manager.get_by_id(land_id)
            self.land = land_obj
        if code and not land and not land_id:
            land_obj = self.manager.get_by_code(code)
            self.land = land_obj
    async def save(self):
        if self.land.land_id > 0:
            self.land = await self.manager.update(self.land)
        if self.land.land_id == 0:
            self.land = await self.manager.add(self.land)
    async def delete(self):
        if self.land.land_id > 0:
            self.land = await self.manager.delete(self.land.land_id)
    async def get_pac_id_rel_obj(self, pac_id: int): #PacID
        pac_manager = PacIDManager(self.session)
        return pac_manager.get_by_id(self.land.pac_id)
