import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from managers.organization_manager import OrganizationManager as OrganizationIDManager #OrganizationID
from managers.org_customer_manager import OrgCustomerManager as OrgCustomerIDManager #OrgCustomerID
from managers.org_api_key_manager import OrgApiKeyManager
from models.org_api_key import OrgApiKey
class OrgApiKeyBusObj:
    def __init__(self, code:uuid.UUID=None, org_api_key_id:int=None, org_api_key:OrgApiKey=None, session:AsyncSession=None):
        self.org_api_key = org_api_key
        self.session = session
        self.manager = OrgApiKeyManager(session)
        # If initialized with a org_api_key_id and not a org_api_key object, load the org_api_key
        if org_api_key_id and not org_api_key and not code:
            org_api_key_obj = self.manager.get_by_id(org_api_key_id)
            self.org_api_key = org_api_key_obj
        if code and not org_api_key and not org_api_key_id:
            org_api_key_obj = self.manager.get_by_code(code)
            self.org_api_key = org_api_key_obj
    async def save(self):
        if self.org_api_key.id > 0:
            self.org_api_key = await self.manager.update(self.org_api_key)
        if self.org_api_key.id == 0:
            self.org_api_key = await self.manager.add(self.org_api_key)
    async def delete(self):
        if self.org_api_key.id > 0:
            self.org_api_key = await self.manager.delete(self.org_api_key.id)
    async def get_organization_id_rel_obj(self, organization_id: int): #OrganizationID
        organization_manager = OrganizationIDManager(self.session)
        return organization_manager.get_by_id(self.org_api_key.organization_id)
    async def get_org_customer_id_rel_obj(self, org_customer_id: int): #OrgCustomerID
        org_customer_manager = OrgCustomerIDManager(self.session)
        return org_customer_manager.get_by_id(self.org_api_key.org_customer_id)
