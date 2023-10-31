import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from managers import PacManager as PacIDManager #PacID
from managers import FlavorManager
from models import Flavor
class FlavorBusObj:
    def __init__(self, code:uuid.UUID=None, flavor_id:int=None, flavor:Flavor=None, session:AsyncSession=None):
        self.flavor = flavor
        self.session = session
        self.manager = FlavorManager(session)
        # If initialized with a flavor_id and not a flavor object, load the flavor
        if flavor_id and not flavor and not code:
            flavor_obj = self.manager.get_by_id(flavor_id)
            self.flavor = flavor_obj
        if code and not flavor and not flavor_id:
            flavor_obj = self.manager.get_by_code(code)
            self.flavor = flavor_obj
    async def save(self):
        if self.flavor.flavor_id > 0:
            self.flavor = await self.manager.update(self.flavor)
        if self.flavor.flavor_id == 0:
            self.flavor = await self.manager.add(self.flavor)
    async def delete(self):
        if self.flavor.flavor_id > 0:
            self.flavor = await self.manager.delete(self.flavor.flavor_id)
    async def get_pac_id_rel_obj(self, pac_id: int): #PacID
        pac_manager = PacIDManager(self.session)
        return pac_manager.get_by_id(self.flavor.pac_id)
