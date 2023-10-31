import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.customer import Customer
class CustomerManager:
    def __init__(self, session: AsyncSession):
        self.session = session
    async def add(self, **kwargs):
        customer = Customer(**kwargs)
        self.session.add(customer)
        await self.session.commit()
        return customer
    async def get_by_id(self, customer_id: int):
        result = await self.session.execute(select(Customer).filter(Customer.customer_id == customer_id))
        return result.scalars().first()
    async def get_by_code(self, code: uuid.UUID):
        result = await self.session.execute(select(Customer).filter_by(code=code))
        return result.scalars().one_or_none()
    async def update(self, customer_id: int, **kwargs):
        customer = await self.get_by_id(customer_id)
        if customer:
            for key, value in kwargs.items():
                setattr(customer, key, value)
            await self.session.commit()
        return customer
    async def delete(self, customer_id: int):
        customer = await self.get_by_id(customer_id)
        if customer:
            self.session.delete(customer)
            await self.session.commit()
        return customer
    async def get_list(self):
        result = await self.session.execute(select(Customer))
        return result.scalars().all()
    async def get_by_tac_id(self, tac_id: int):
        result = await self.session.execute(select(Customer).filter(Customer.tac_id == tac_id))
        return result.scalars().all()
