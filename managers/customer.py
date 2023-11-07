import json
import uuid
from typing import List, Optional, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.tac import Tac # TacID
from models.customer import Customer
from models.serialization_schema.customer import CustomerSchema
from services.logging_config import get_logger
logger = get_logger(__name__)
class CustomerNotFoundError(Exception):
    pass
class CustomerManager:
    def __init__(self, session: AsyncSession):
        self.session = session
    async def build(self, **kwargs) -> Customer:
        return Customer(**kwargs)
    async def add(self, customer: Customer) -> Customer:
        self.session.add(customer)
        await self.session.commit()
        return customer
    async def get_by_id(self, customer_id: int) -> Optional[Customer]:
        if not isinstance(customer_id, int):
            raise TypeError(f"The customer_id must be an integer, got {type(customer_id)} instead.")
        result = await self.session.execute(select(Customer).filter(Customer.customer_id == customer_id))
        return result.scalars().first()
    async def get_by_code(self, code: uuid.UUID) -> Optional[Customer]:
        result = await self.session.execute(select(Customer).filter_by(code=code))
        return result.scalars().one_or_none()
    async def update(self, customer: Customer, **kwargs) -> Optional[Customer]:
        if customer:
            for key, value in kwargs.items():
                setattr(customer, key, value)
            await self.session.commit()
        return customer
    async def delete(self, customer_id: int):
        if not isinstance(customer_id, int):
            raise TypeError(f"The customer_id must be an integer, got {type(customer_id)} instead.")
        customer = await self.get_by_id(customer_id)
        if not customer:
            raise CustomerNotFoundError(f"Customer with ID {customer_id} not found!")
        await self.session.delete(customer)
        await self.session.commit()
    async def get_list(self) -> List[Customer]:
        result = await self.session.execute(select(Customer))
        return result.scalars().all()
    def to_json(self, customer:Customer) -> str:
        """
        Serialize the Customer object to a JSON string using the CustomerSchema.
        """
        schema = CustomerSchema()
        customer_data = schema.dump(customer)
        return json.dumps(customer_data)
    def to_dict(self, customer:Customer) -> dict:
        """
        Serialize the Customer object to a JSON string using the CustomerSchema.
        """
        schema = CustomerSchema()
        customer_data = schema.dump(customer)
        return customer_data
    def from_json(self, json_str: str) -> Customer:
        """
        Deserialize a JSON string into a Customer object using the CustomerSchema.
        """
        schema = CustomerSchema()
        data = json.loads(json_str)
        customer_dict = schema.load(data)
        new_customer = Customer(**customer_dict)
        return new_customer
    def from_dict(self, customer_dict: str) -> Customer:
        schema = CustomerSchema()
        customer_dict_converted = schema.load(customer_dict)
        new_customer = Customer(**customer_dict_converted)
        return new_customer
    async def add_bulk(self, customers: List[Customer]) -> List[Customer]:
        """Add multiple customers at once."""
        self.session.add_all(customers)
        await self.session.commit()
        return customers
    async def update_bulk(self, customer_updates: List[Dict[int, Dict]]) -> List[Customer]:
        """Update multiple customers at once."""
        updated_customers = []
        for update in customer_updates:
            customer_id = update.get("customer_id")
            if not isinstance(customer_id, int):
                raise TypeError(f"The customer_id must be an integer, got {type(customer_id)} instead.")
            if not customer_id:
                continue
            customer = await self.get_by_id(customer_id)
            if not customer:
                raise CustomerNotFoundError(f"Customer with ID {customer_id} not found!")
            for key, value in update.items():
                if key != "customer_id":
                    setattr(customer, key, value)
            updated_customers.append(customer)
        await self.session.commit()
        return updated_customers
    async def delete_bulk(self, customer_ids: List[int]) -> bool:
        """Delete multiple customers by their IDs."""
        for customer_id in customer_ids:
            if not isinstance(customer_id, int):
                raise TypeError(f"The customer_id must be an integer, got {type(customer_id)} instead.")
            customer = await self.get_by_id(customer_id)
            if not customer:
                raise CustomerNotFoundError(f"Customer with ID {customer_id} not found!")
            if customer:
                await self.session.delete(customer)
        await self.session.commit()
        return True
    async def count(self) -> int:
        """Return the total number of customers."""
        result = await self.session.execute(select(Customer))
        return len(result.scalars().all())
    async def get_sorted_list(self, sort_by: str, order: Optional[str] = "asc") -> List[Customer]:
        """Retrieve customers sorted by a particular attribute."""
        if order == "asc":
            result = await self.session.execute(select(Customer).order_by(getattr(Customer, sort_by).asc()))
        else:
            result = await self.session.execute(select(Customer).order_by(getattr(Customer, sort_by).desc()))
        return result.scalars().all()
    async def refresh(self, customer: Customer) -> Customer:
        """Refresh the state of a given customer instance from the database."""
        await self.session.refresh(customer)
        return customer
    async def exists(self, customer_id: int) -> bool:
        """Check if a customer with the given ID exists."""
        if not isinstance(customer_id, int):
            raise TypeError(f"The customer_id must be an integer, got {type(customer_id)} instead.")
        customer = await self.get_by_id(customer_id)
        return bool(customer)
    def is_equal(self, customer1:Customer, customer2:Customer) -> bool:
        if not customer1:
            raise TypeError("Customer1 required.")
        if not customer2:
            raise TypeError("Customer2 required.")
        if not isinstance(customer1, Customer):
            raise TypeError("The customer1 must be an Customer instance.")
        if not isinstance(customer2, Customer):
            raise TypeError("The customer2 must be an Customer instance.")
        dict1 = self.to_dict(customer1)
        dict2 = self.to_dict(customer2)
        logger.info("vrtest")
        logger.info(dict1)
        logger.info(dict2)
        return dict1 == dict2

    async def get_by_tac_id(self, tac_id: int) -> List[Tac]: # TacID
        if not isinstance(tac_id, int):
            raise TypeError(f"The customer_id must be an integer, got {type(tac_id)} instead.")
        result = await self.session.execute(select(Customer).filter(Customer.tac_id == tac_id))
        return result.scalars().all()

