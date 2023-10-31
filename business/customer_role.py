import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from managers import CustomerManager as CustomerIDManager #CustomerID
from managers import RoleManager as RoleIDManager #RoleID
from managers import CustomerRoleManager
from models import CustomerRole
class CustomerRoleBusObj:
    def __init__(self, code:uuid.UUID=None, customer_role_id:int=None, customer_role:CustomerRole=None, session:AsyncSession=None):
        self.customer_role = customer_role
        self.session = session
        self.manager = CustomerRoleManager(session)
        # If initialized with a customer_role_id and not a customer_role object, load the customer_role
        if customer_role_id and not customer_role and not code:
            customer_role_obj = self.manager.get_by_id(customer_role_id)
            self.customer_role = customer_role_obj
        if code and not customer_role and not customer_role_id:
            customer_role_obj = self.manager.get_by_code(code)
            self.customer_role = customer_role_obj
    async def save(self):
        if self.customer_role.customer_role_id > 0:
            self.customer_role = await self.manager.update(self.customer_role)
        if self.customer_role.customer_role_id == 0:
            self.customer_role = await self.manager.add(self.customer_role)
    async def delete(self):
        if self.customer_role.customer_role_id > 0:
            self.customer_role = await self.manager.delete(self.customer_role.customer_role_id)
    async def get_customer_id_rel_obj(self, customer_id: int): #CustomerID
        customer_manager = CustomerIDManager(self.session)
        return customer_manager.get_by_id(self.customer_role.customer_id)
    async def get_role_id_rel_obj(self, role_id: int): #RoleID
        role_manager = RoleIDManager(self.session)
        return role_manager.get_by_id(self.customer_role.role_id)
