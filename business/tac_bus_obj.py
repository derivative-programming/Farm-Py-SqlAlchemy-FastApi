import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from managers.pac_manager import PacManager as PacIDManager #PacID
from managers.tac_manager import TacManager
from models.tac import Tac
class TacBusObj:
    def __init__(self, code:uuid.UUID=None, tac_id:int=None, tac:Tac=None, session:AsyncSession=None):
        self.tac = tac
        self.session = session
        self.manager = TacManager(session)
        # If initialized with a tac_id and not a tac object, load the tac
        if tac_id and not tac and not code:
            tac_obj = self.manager.get_by_id(tac_id)
            self.tac = tac_obj
        if code and not tac and not tac_id:
            tac_obj = self.manager.get_by_code(code)
            self.tac = tac_obj
    async def save(self):
        if self.tac.id > 0:
            self.tac = await self.manager.update(self.tac)
        if self.tac.id == 0:
            self.tac = await self.manager.add(self.tac)
    async def delete(self):
        if self.tac.id > 0:
            self.tac = await self.manager.delete(self.tac.id)
    async def get_pac_id_rel_obj(self, pac_id: int): #PacID
        pac_manager = PacIDManager(self.session)
        return pac_manager.get_by_id(self.tac.pac_id)
