import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.org_customer import OrgCustomer
class OrgCustomerManager:
    def __init__(self, session: AsyncSession):
        self.session = session
    async def add(self, **kwargs):
        org_customer = OrgCustomer(**kwargs)
        self.session.add(org_customer)
        await self.session.commit()
        return org_customer
    async def get_by_id(self, org_customer_id: int):
        result = await self.session.execute(select(OrgCustomer).filter(OrgCustomer.org_customer_id == org_customer_id))
        return result.scalars().first()
    async def get_by_code(self, code: uuid.UUID):
        result = await self.session.execute(select(OrgCustomer).filter_by(code=code))
        return result.scalars().one_or_none()
    async def update(self, org_customer_id: int, **kwargs):
        org_customer = await self.get_by_id(org_customer_id)
        if org_customer:
            for key, value in kwargs.items():
                setattr(org_customer, key, value)
            await self.session.commit()
        return org_customer
    async def delete(self, org_customer_id: int):
        org_customer = await self.get_by_id(org_customer_id)
        if org_customer:
            self.session.delete(org_customer)
            await self.session.commit()
        return org_customer
    async def get_list(self):
        result = await self.session.execute(select(OrgCustomer))
        return result.scalars().all()
    async def get_by_customer_id(self, customer_id: int):
        result = await self.session.execute(select(OrgCustomer).filter(OrgCustomer.customer_id == customer_id))
        return result.scalars().all()
    async def get_by_organization_id(self, organization_id: int):
        result = await self.session.execute(select(OrgCustomer).filter(OrgCustomer.organization_id == organization_id))
        return result.scalars().all()
