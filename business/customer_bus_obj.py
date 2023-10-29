import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from managers.tac_manager import TacManager as TacIDManager #TacID
from managers.customer_manager import CustomerManager
from models.customer import Customer
class CustomerBusObj:
    def __init__(self, code:uuid.UUID=None, customer_id:int=None, customer:Customer=None, session:AsyncSession=None):
        self.customer = customer
        self.session = session
        self.manager = CustomerManager(session)
        # If initialized with a customer_id and not a customer object, load the customer
        if customer_id and not customer and not code:
            customer_obj = self.manager.get_by_id(customer_id)
            self.customer = customer_obj
        if code and not customer and not customer_id:
            customer_obj = self.manager.get_by_code(code)
            self.customer = customer_obj
    async def save(self):
        if self.customer.id > 0:
            self.customer = await self.manager.update(self.customer)
        if self.customer.id == 0:
            self.customer = await self.manager.add(self.customer)
    async def delete(self):
        if self.customer.id > 0:
            self.customer = await self.manager.delete(self.customer.id)
    async def get_tac_id_rel_obj(self, tac_id: int): #TacID
        tac_manager = TacIDManager(self.session)
        return tac_manager.get_by_id(self.customer.tac_id)
