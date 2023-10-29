import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from managers.pac_manager import PacManager as PacIDManager #PacID
from managers.role_manager import RoleManager
from models.role import Role
class RoleBusObj:
    def __init__(self, code:uuid.UUID=None, role_id:int=None, role:Role=None, session:AsyncSession=None):
        self.role = role
        self.session = session
        self.manager = RoleManager(session)
        # If initialized with a role_id and not a role object, load the role
        if role_id and not role and not code:
            role_obj = self.manager.get_by_id(role_id)
            self.role = role_obj
        if code and not role and not role_id:
            role_obj = self.manager.get_by_code(code)
            self.role = role_obj
    async def save(self):
        if self.role.id > 0:
            self.role = await self.manager.update(self.role)
        if self.role.id == 0:
            self.role = await self.manager.add(self.role)
    async def delete(self):
        if self.role.id > 0:
            self.role = await self.manager.delete(self.role.id)
    async def get_pac_id_rel_obj(self, pac_id: int): #PacID
        pac_manager = PacIDManager(self.session)
        return pac_manager.get_by_id(self.role.pac_id)
