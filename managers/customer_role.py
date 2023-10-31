import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.customer_role import CustomerRole
class CustomerRoleManager:
    def __init__(self, session: AsyncSession):
        self.session = session
    async def add(self, **kwargs):
        customer_role = CustomerRole(**kwargs)
        self.session.add(customer_role)
        await self.session.commit()
        return customer_role
    async def get_by_id(self, customer_role_id: int):
        result = await self.session.execute(select(CustomerRole).filter(CustomerRole.customer_role_id == customer_role_id))
        return result.scalars().first()
    async def get_by_code(self, code: uuid.UUID):
        result = await self.session.execute(select(CustomerRole).filter_by(code=code))
        return result.scalars().one_or_none()
    async def update(self, customer_role_id: int, **kwargs):
        customer_role = await self.get_by_id(customer_role_id)
        if customer_role:
            for key, value in kwargs.items():
                setattr(customer_role, key, value)
            await self.session.commit()
        return customer_role
    async def delete(self, customer_role_id: int):
        customer_role = await self.get_by_id(customer_role_id)
        if customer_role:
            self.session.delete(customer_role)
            await self.session.commit()
        return customer_role
    async def get_list(self):
        result = await self.session.execute(select(CustomerRole))
        return result.scalars().all()
    async def get_by_customer_id(self, customer_id: int):
        result = await self.session.execute(select(CustomerRole).filter(CustomerRole.customer_id == customer_id))
        return result.scalars().all()
    async def get_by_role_id(self, role_id: int):
        result = await self.session.execute(select(CustomerRole).filter(CustomerRole.role_id == role_id))
        return result.scalars().all()
