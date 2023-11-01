import json
import uuid
from typing import List, Optional, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.customer_role import CustomerRole
from models.serialization_schema.customer_role import CustomerRoleSchema
class CustomerRoleManager:
    def __init__(self, session: AsyncSession):
        self.session = session
    def build(self, **kwargs) -> CustomerRole:
        return CustomerRole(**kwargs)
    async def add(self, customer_role: CustomerRole) -> CustomerRole:
        self.session.add(customer_role)
        await self.session.commit()
        return customer_role
    async def get_by_id(self, customer_role_id: int) -> Optional[CustomerRole]:
        result = await self.session.execute(select(CustomerRole).filter(CustomerRole.customer_role_id == customer_role_id))
        return result.scalars().first()
    async def get_by_code(self, code: uuid.UUID) -> Optional[CustomerRole]:
        result = await self.session.execute(select(CustomerRole).filter_by(code=code))
        return result.scalars().one_or_none()
    async def update(self, customer_role: CustomerRole, **kwargs) -> Optional[CustomerRole]:
        if customer_role:
            for key, value in kwargs.items():
                setattr(customer_role, key, value)
            await self.session.commit()
        return customer_role
    async def delete(self, customer_role_id: int) -> Optional[CustomerRole]:
        customer_role = await self.get_by_id(customer_role_id)
        if customer_role:
            self.session.delete(customer_role)
            await self.session.commit()
        return customer_role
    async def get_list(self) -> List[CustomerRole]:
        result = await self.session.execute(select(CustomerRole))
        return result.scalars().all()
    def to_json(self, customer_role:CustomerRole) -> str:
        """
        Serialize the CustomerRole object to a JSON string using the CustomerRoleSchema.
        """
        schema = CustomerRoleSchema()
        customer_role_data = schema.dump(customer_role)
        return json.dumps(customer_role_data)
    def from_json(self, json_str: str) -> CustomerRole:
        """
        Deserialize a JSON string into a CustomerRole object using the CustomerRoleSchema.
        """
        schema = CustomerRoleSchema()
        data = json.loads(json_str)
        customer_role_dict = schema.load(data)
        new_customer_role = CustomerRole(**customer_role_dict)
        return new_customer_role
    async def add_bulk(self, customer_roles_data: List[Dict]) -> List[CustomerRole]:
        """Add multiple customer_roles at once."""
        customer_roles = [CustomerRole(**data) for data in customer_roles_data]
        self.session.add_all(customer_roles)
        await self.session.commit()
        return customer_roles
    async def update_bulk(self, customer_role_updates: List[Dict[int, Dict]]) -> List[CustomerRole]:
        """Update multiple customer_roles at once."""
        updated_customer_roles = []
        for update in customer_role_updates:
            customer_role_id = update.get("customer_role_id")
            if not customer_role_id:
                continue
            customer_role = await self.get_by_id(customer_role_id)
            if not customer_role:
                continue
            for key, value in update.items():
                if key != "customer_role_id":
                    setattr(customer_role, key, value)
            updated_customer_roles.append(customer_role)
        await self.session.commit()
        return updated_customer_roles
    async def delete_bulk(self, customer_role_ids: List[int]) -> bool:
        """Delete multiple customer_roles by their IDs."""
        for customer_role_id in customer_role_ids:
            customer_role = await self.get_by_id(customer_role_id)
            if customer_role:
                self.session.delete(customer_role)
        await self.session.commit()
        return True
    async def count(self) -> int:
        """Return the total number of customer_roles."""
        result = await self.session.execute(select(CustomerRole))
        return len(result.scalars().all())
    async def get_sorted_list(self, sort_by: str, order: Optional[str] = "asc") -> List[CustomerRole]:
        """Retrieve customer_roles sorted by a particular attribute."""
        if order == "asc":
            result = await self.session.execute(select(CustomerRole).order_by(getattr(CustomerRole, sort_by).asc()))
        else:
            result = await self.session.execute(select(CustomerRole).order_by(getattr(CustomerRole, sort_by).desc()))
        return result.scalars().all()
    async def refresh(self, customer_role: CustomerRole) -> CustomerRole:
        """Refresh the state of a given customer_role instance from the database."""
        self.session.refresh(customer_role)
        return customer_role
    async def exists(self, customer_role_id: int) -> bool:
        """Check if a customer_role with the given ID exists."""
        customer_role = await self.get_by_id(customer_role_id)
        return bool(customer_role)

    async def get_by_customer_id(self, customer_id: int): # CustomerID
        result = await self.session.execute(select(CustomerRole).filter(CustomerRole.customer_id == customer_id))
        return result.scalars().all()
    async def get_by_role_id(self, role_id: int): # RoleID
        result = await self.session.execute(select(CustomerRole).filter(CustomerRole.role_id == role_id))
        return result.scalars().all()

