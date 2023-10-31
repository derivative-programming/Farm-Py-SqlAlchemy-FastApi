import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from managers import CustomerManager as CustomerIDManager #CustomerID
from managers import OrganizationManager as OrganizationIDManager #OrganizationID
from managers import OrgCustomerManager
from models import OrgCustomer
class OrgCustomerBusObj:
    def __init__(self, code:uuid.UUID=None, org_customer_id:int=None, org_customer:OrgCustomer=None, session:AsyncSession=None):
        self.org_customer = org_customer
        self.session = session
        self.manager = OrgCustomerManager(session)
        # If initialized with a org_customer_id and not a org_customer object, load the org_customer
        if org_customer_id and not org_customer and not code:
            org_customer_obj = self.manager.get_by_id(org_customer_id)
            self.org_customer = org_customer_obj
        if code and not org_customer and not org_customer_id:
            org_customer_obj = self.manager.get_by_code(code)
            self.org_customer = org_customer_obj
    async def save(self):
        if self.org_customer.org_customer_id > 0:
            self.org_customer = await self.manager.update(self.org_customer)
        if self.org_customer.org_customer_id == 0:
            self.org_customer = await self.manager.add(self.org_customer)
    async def delete(self):
        if self.org_customer.org_customer_id > 0:
            self.org_customer = await self.manager.delete(self.org_customer.org_customer_id)
    async def get_customer_id_rel_obj(self, customer_id: int): #CustomerID
        customer_manager = CustomerIDManager(self.session)
        return customer_manager.get_by_id(self.org_customer.customer_id)
    async def get_organization_id_rel_obj(self, organization_id: int): #OrganizationID
        organization_manager = OrganizationIDManager(self.session)
        return organization_manager.get_by_id(self.org_customer.organization_id)
