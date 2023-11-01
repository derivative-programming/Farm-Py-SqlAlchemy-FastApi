import json
import uuid
from typing import List, Optional, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.org_customer import OrgCustomer
from models.serialization_schema.org_customer import OrgCustomerSchema
class OrgCustomerManager:
    def __init__(self, session: AsyncSession):
        self.session = session
    def build(self, **kwargs) -> OrgCustomer:
        return OrgCustomer(**kwargs)
    async def add(self, org_customer: OrgCustomer) -> OrgCustomer:
        self.session.add(org_customer)
        await self.session.commit()
        return org_customer
    async def get_by_id(self, org_customer_id: int) -> Optional[OrgCustomer]:
        result = await self.session.execute(select(OrgCustomer).filter(OrgCustomer.org_customer_id == org_customer_id))
        return result.scalars().first()
    async def get_by_code(self, code: uuid.UUID) -> Optional[OrgCustomer]:
        result = await self.session.execute(select(OrgCustomer).filter_by(code=code))
        return result.scalars().one_or_none()
    async def update(self, org_customer: OrgCustomer, **kwargs) -> Optional[OrgCustomer]:
        if org_customer:
            for key, value in kwargs.items():
                setattr(org_customer, key, value)
            await self.session.commit()
        return org_customer
    async def delete(self, org_customer_id: int) -> Optional[OrgCustomer]:
        org_customer = await self.get_by_id(org_customer_id)
        if org_customer:
            self.session.delete(org_customer)
            await self.session.commit()
        return org_customer
    async def get_list(self) -> List[OrgCustomer]:
        result = await self.session.execute(select(OrgCustomer))
        return result.scalars().all()
    def to_json(self, org_customer:OrgCustomer) -> str:
        """
        Serialize the OrgCustomer object to a JSON string using the OrgCustomerSchema.
        """
        schema = OrgCustomerSchema()
        org_customer_data = schema.dump(org_customer)
        return json.dumps(org_customer_data)
    def from_json(self, json_str: str) -> OrgCustomer:
        """
        Deserialize a JSON string into a OrgCustomer object using the OrgCustomerSchema.
        """
        schema = OrgCustomerSchema()
        data = json.loads(json_str)
        org_customer_dict = schema.load(data)
        new_org_customer = OrgCustomer(**org_customer_dict)
        return new_org_customer
    async def add_bulk(self, org_customers_data: List[Dict]) -> List[OrgCustomer]:
        """Add multiple org_customers at once."""
        org_customers = [OrgCustomer(**data) for data in org_customers_data]
        self.session.add_all(org_customers)
        await self.session.commit()
        return org_customers
    async def update_bulk(self, org_customer_updates: List[Dict[int, Dict]]) -> List[OrgCustomer]:
        """Update multiple org_customers at once."""
        updated_org_customers = []
        for update in org_customer_updates:
            org_customer_id = update.get("org_customer_id")
            if not org_customer_id:
                continue
            org_customer = await self.get_by_id(org_customer_id)
            if not org_customer:
                continue
            for key, value in update.items():
                if key != "org_customer_id":
                    setattr(org_customer, key, value)
            updated_org_customers.append(org_customer)
        await self.session.commit()
        return updated_org_customers
    async def delete_bulk(self, org_customer_ids: List[int]) -> bool:
        """Delete multiple org_customers by their IDs."""
        for org_customer_id in org_customer_ids:
            org_customer = await self.get_by_id(org_customer_id)
            if org_customer:
                self.session.delete(org_customer)
        await self.session.commit()
        return True
    async def count(self) -> int:
        """Return the total number of org_customers."""
        result = await self.session.execute(select(OrgCustomer))
        return len(result.scalars().all())
    async def get_sorted_list(self, sort_by: str, order: Optional[str] = "asc") -> List[OrgCustomer]:
        """Retrieve org_customers sorted by a particular attribute."""
        if order == "asc":
            result = await self.session.execute(select(OrgCustomer).order_by(getattr(OrgCustomer, sort_by).asc()))
        else:
            result = await self.session.execute(select(OrgCustomer).order_by(getattr(OrgCustomer, sort_by).desc()))
        return result.scalars().all()
    async def refresh(self, org_customer: OrgCustomer) -> OrgCustomer:
        """Refresh the state of a given org_customer instance from the database."""
        self.session.refresh(org_customer)
        return org_customer
    async def exists(self, org_customer_id: int) -> bool:
        """Check if a org_customer with the given ID exists."""
        org_customer = await self.get_by_id(org_customer_id)
        return bool(org_customer)

    async def get_by_customer_id(self, customer_id: int): # CustomerID
        result = await self.session.execute(select(OrgCustomer).filter(OrgCustomer.customer_id == customer_id))
        return result.scalars().all()
    async def get_by_organization_id(self, organization_id: int): # OrganizationID
        result = await self.session.execute(select(OrgCustomer).filter(OrgCustomer.organization_id == organization_id))
        return result.scalars().all()

