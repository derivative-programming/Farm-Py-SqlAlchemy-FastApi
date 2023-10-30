import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from managers import PacManager
from models import Pac
class PacBusObj:
    def __init__(self, code:uuid.UUID=None, pac_id:int=None, pac:Pac=None, session:AsyncSession=None):
        self.pac = pac
        self.session = session
        self.manager = PacManager(session)
        # If initialized with a pac_id and not a pac object, load the pac
        if pac_id and not pac and not code:
            pac_obj = self.manager.get_by_id(pac_id)
            self.pac = pac_obj
        if code and not pac and not pac_id:
            pac_obj = self.manager.get_by_code(code)
            self.pac = pac_obj
    async def save(self):
        if self.pac.id > 0:
            self.pac = await self.manager.update(self.pac)
        if self.pac.id == 0:
            self.pac = await self.manager.add(self.pac)
    async def delete(self):
        if self.pac.id > 0:
            self.pac = await self.manager.delete(self.pac.id)
