import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from managers import TacManager as TacIDManager #TacID
from managers import OrganizationManager
from models import Organization
class OrganizationBusObj:
    def __init__(self, code:uuid.UUID=None, organization_id:int=None, organization:Organization=None, session:AsyncSession=None):
        self.organization = organization
        self.session = session
        self.manager = OrganizationManager(session)
        # If initialized with a organization_id and not a organization object, load the organization
        if organization_id and not organization and not code:
            organization_obj = self.manager.get_by_id(organization_id)
            self.organization = organization_obj
        if code and not organization and not organization_id:
            organization_obj = self.manager.get_by_code(code)
            self.organization = organization_obj
    async def save(self):
        if self.organization.id > 0:
            self.organization = await self.manager.update(self.organization)
        if self.organization.id == 0:
            self.organization = await self.manager.add(self.organization)
    async def delete(self):
        if self.organization.id > 0:
            self.organization = await self.manager.delete(self.organization.id)
    async def get_tac_id_rel_obj(self, tac_id: int): #TacID
        tac_manager = TacIDManager(self.session)
        return tac_manager.get_by_id(self.organization.tac_id)
