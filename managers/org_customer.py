import json
import uuid
from typing import List, Optional, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.customer import Customer # CustomerID
from models.organization import Organization # OrganizationID
from models.org_customer import OrgCustomer
from models.serialization_schema.org_customer import OrgCustomerSchema
from services.logging_config import get_logger
logger = get_logger(__name__)
class OrgCustomerNotFoundError(Exception):
    pass
class OrgCustomerManager:
    def __init__(self, session: AsyncSession):
        self.session = session
    async def build(self, **kwargs) -> OrgCustomer:
        return OrgCustomer(**kwargs)
    async def add(self, org_customer: OrgCustomer) -> OrgCustomer:
        self.session.add(org_customer)
        await self.session.commit()
        return org_customer
    async def get_by_id(self, org_customer_id: int) -> Optional[OrgCustomer]:
        if not isinstance(org_customer_id, int):
            raise TypeError(f"The org_customer_id must be an integer, got {type(org_customer_id)} instead.")
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
    async def delete(self, org_customer_id: int):
        if not isinstance(org_customer_id, int):
            raise TypeError(f"The org_customer_id must be an integer, got {type(org_customer_id)} instead.")
        org_customer = await self.get_by_id(org_customer_id)
        if not org_customer:
            raise OrgCustomerNotFoundError(f"OrgCustomer with ID {org_customer_id} not found!")
        await self.session.delete(org_customer)
        await self.session.commit()
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
    def to_dict(self, org_customer:OrgCustomer) -> dict:
        """
        Serialize the OrgCustomer object to a JSON string using the OrgCustomerSchema.
        """
        schema = OrgCustomerSchema()
        org_customer_data = schema.dump(org_customer)
        return org_customer_data
    def from_json(self, json_str: str) -> OrgCustomer:
        """
        Deserialize a JSON string into a OrgCustomer object using the OrgCustomerSchema.
        """
        schema = OrgCustomerSchema()
        data = json.loads(json_str)
        org_customer_dict = schema.load(data)
        new_org_customer = OrgCustomer(**org_customer_dict)
        return new_org_customer
    def from_dict(self, org_customer_dict: str) -> OrgCustomer:
        schema = OrgCustomerSchema()
        org_customer_dict_converted = schema.load(org_customer_dict)
        new_org_customer = OrgCustomer(**org_customer_dict_converted)
        return new_org_customer
    async def add_bulk(self, org_customers: List[OrgCustomer]) -> List[OrgCustomer]:
        """Add multiple org_customers at once."""
        self.session.add_all(org_customers)
        await self.session.commit()
        return org_customers
    async def update_bulk(self, org_customer_updates: List[Dict[int, Dict]]) -> List[OrgCustomer]:
        """Update multiple org_customers at once."""
        updated_org_customers = []
        for update in org_customer_updates:
            org_customer_id = update.get("org_customer_id")
            if not isinstance(org_customer_id, int):
                raise TypeError(f"The org_customer_id must be an integer, got {type(org_customer_id)} instead.")
            if not org_customer_id:
                continue
            org_customer = await self.get_by_id(org_customer_id)
            if not org_customer:
                raise OrgCustomerNotFoundError(f"OrgCustomer with ID {org_customer_id} not found!")
            for key, value in update.items():
                if key != "org_customer_id":
                    setattr(org_customer, key, value)
            updated_org_customers.append(org_customer)
        await self.session.commit()
        return updated_org_customers
    async def delete_bulk(self, org_customer_ids: List[int]) -> bool:
        """Delete multiple org_customers by their IDs."""
        for org_customer_id in org_customer_ids:
            if not isinstance(org_customer_id, int):
                raise TypeError(f"The org_customer_id must be an integer, got {type(org_customer_id)} instead.")
            org_customer = await self.get_by_id(org_customer_id)
            if not org_customer:
                raise OrgCustomerNotFoundError(f"OrgCustomer with ID {org_customer_id} not found!")
            if org_customer:
                await self.session.delete(org_customer)
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
        await self.session.refresh(org_customer)
        return org_customer
    async def exists(self, org_customer_id: int) -> bool:
        """Check if a org_customer with the given ID exists."""
        if not isinstance(org_customer_id, int):
            raise TypeError(f"The org_customer_id must be an integer, got {type(org_customer_id)} instead.")
        org_customer = await self.get_by_id(org_customer_id)
        return bool(org_customer)
    def is_equal(self, org_customer1:OrgCustomer, org_customer2:OrgCustomer) -> bool:
        if not org_customer1:
            raise TypeError("OrgCustomer1 required.")
        if not org_customer2:
            raise TypeError("OrgCustomer2 required.")
        if not isinstance(org_customer1, OrgCustomer):
            raise TypeError("The org_customer1 must be an OrgCustomer instance.")
        if not isinstance(org_customer2, OrgCustomer):
            raise TypeError("The org_customer2 must be an OrgCustomer instance.")
        dict1 = self.to_dict(org_customer1)
        dict2 = self.to_dict(org_customer2)
        logger.info("vrtest")
        logger.info(dict1)
        logger.info(dict2)
        return dict1 == dict2

    async def get_by_customer_id(self, customer_id: int) -> List[Customer]: # CustomerID
        if not isinstance(customer_id, int):
            raise TypeError(f"The org_customer_id must be an integer, got {type(customer_id)} instead.")
        result = await self.session.execute(select(OrgCustomer).filter(OrgCustomer.customer_id == customer_id))
        return result.scalars().all()
    async def get_by_organization_id(self, organization_id: int) -> List[Organization]: # OrganizationID
        if not isinstance(organization_id, int):
            raise TypeError(f"The org_customer_id must be an integer, got {type(organization_id)} instead.")
        result = await self.session.execute(select(OrgCustomer).filter(OrgCustomer.organization_id == organization_id))
        return result.scalars().all()

