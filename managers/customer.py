import json
import uuid
from enum import Enum
from typing import List, Optional, Dict
from sqlalchemy import and_, outerjoin
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select#, join, outerjoin, and_
from models.tac import Tac # TacID
from models.customer import Customer
from models.serialization_schema.customer import CustomerSchema
from services.logging_config import get_logger
import logging
logger = get_logger(__name__)
class CustomerNotFoundError(Exception):
    pass

class CustomerManager:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def initialize(self):
        logging.info("CustomerManager.Initialize")

    async def build(self, **kwargs) -> Customer:
        logging.info("CustomerManager.build")
        return Customer(**kwargs)
    async def add(self, customer: Customer) -> Customer:
        logging.info("CustomerManager.add")
        self.session.add(customer)
        await self.session.flush()
        return customer
    def _build_query(self):
        logging.info("CustomerManager._build_query")
#         join_condition = None
#
#         join_condition = outerjoin(join_condition, Tac, and_(Customer.tac_id == Tac.tac_id, Customer.tac_id != 0))
#
#         if join_condition is not None:
#             query = select(Customer
#                         ,Tac #tac_id
#                         ).select_from(join_condition)
#         else:
#             query = select(Customer)
        query = select(Customer
                    ,Tac #tac_id
                    )

        query = query.outerjoin(Tac, and_(Customer.tac_id == Tac.tac_id, Customer.tac_id != 0))

        return query
    async def _run_query(self, query_filter) -> List[Customer]:
        logging.info("CustomerManager._run_query")
        customer_query_all = self._build_query()
        if query_filter is not None:
            query = customer_query_all.filter(query_filter)
        else:
            query = customer_query_all
        result_proxy = await self.session.execute(query)
        query_results = result_proxy.all()
        result = list()
        for query_result_row in query_results:
            i = 0
            customer = query_result_row[i]
            i = i + 1

            tac = query_result_row[i] #tac_id
            i = i + 1

            customer.tac_code_peek = tac.code if tac else uuid.UUID(int=0) #tac_id

            result.append(customer)
        return result
    def _first_or_none(self,customer_list:List) -> Customer:
        return customer_list[0] if customer_list else None
    async def get_by_id(self, customer_id: int) -> Optional[Customer]:
        logging.info("CustomerManager.get_by_id start customer_id:" + str(customer_id))
        if not isinstance(customer_id, int):
            raise TypeError(f"The customer_id must be an integer, got {type(customer_id)} instead.")
        # result = await self.session.execute(select(Customer).filter(Customer.customer_id == customer_id))
        # result = await self.session.execute(select(Customer).filter(Customer.customer_id == customer_id))
        # return result.scalars().first()
        query_filter = Customer.customer_id == customer_id
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)
    async def get_by_code(self, code: uuid.UUID) -> Optional[Customer]:
        logging.info(f"CustomerManager.get_by_code {code}")
        # result = await self.session.execute(select(Customer).filter_by(code=code))
        # return result.scalars().one_or_none()
        query_filter = Customer.code==code
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)
    async def update(self, customer: Customer, **kwargs) -> Optional[Customer]:
        logging.info("CustomerManager.update")
        if customer:
            for key, value in kwargs.items():
                setattr(customer, key, value)
            await self.session.flush()
        return customer
    async def delete(self, customer_id: int):
        logging.info(f"CustomerManager.delete {customer_id}")
        if not isinstance(customer_id, int):
            raise TypeError(f"The customer_id must be an integer, got {type(customer_id)} instead.")
        customer = await self.get_by_id(customer_id)
        if not customer:
            raise CustomerNotFoundError(f"Customer with ID {customer_id} not found!")
        await self.session.delete(customer)
        await self.session.flush()
    async def get_list(self) -> List[Customer]:
        logging.info("CustomerManager.get_list")
        # result = await self.session.execute(select(Customer))
        # return result.scalars().all()
        query_results = await self._run_query(None)
        return query_results
    def to_json(self, customer:Customer) -> str:
        logging.info("CustomerManager.to_json")
        """
        Serialize the Customer object to a JSON string using the CustomerSchema.
        """
        schema = CustomerSchema()
        customer_data = schema.dump(customer)
        return json.dumps(customer_data)
    def to_dict(self, customer:Customer) -> dict:
        logging.info("CustomerManager.to_dict")
        """
        Serialize the Customer object to a JSON string using the CustomerSchema.
        """
        schema = CustomerSchema()
        customer_data = schema.dump(customer)
        return customer_data
    def from_json(self, json_str: str) -> Customer:
        logging.info("CustomerManager.from_json")
        """
        Deserialize a JSON string into a Customer object using the CustomerSchema.
        """
        schema = CustomerSchema()
        data = json.loads(json_str)
        customer_dict = schema.load(data)
        new_customer = Customer(**customer_dict)
        return new_customer
    def from_dict(self, customer_dict: str) -> Customer:
        logging.info("CustomerManager.from_dict")
        schema = CustomerSchema()
        customer_dict_converted = schema.load(customer_dict)
        new_customer = Customer(**customer_dict_converted)
        return new_customer
    async def add_bulk(self, customers: List[Customer]) -> List[Customer]:
        logging.info("CustomerManager.add_bulk")
        """Add multiple customers at once."""
        self.session.add_all(customers)
        await self.session.flush()
        return customers
    async def update_bulk(self, customer_updates: List[Dict[int, Dict]]) -> List[Customer]:
        logging.info("CustomerManager.update_bulk start")
        updated_customers = []
        for update in customer_updates:
            customer_id = update.get("customer_id")
            if not isinstance(customer_id, int):
                raise TypeError(f"The customer_id must be an integer, got {type(customer_id)} instead.")
            if not customer_id:
                continue
            logging.info(f"CustomerManager.update_bulk customer_id:{customer_id}")
            customer = await self.get_by_id(customer_id)
            if not customer:
                raise CustomerNotFoundError(f"Customer with ID {customer_id} not found!")
            for key, value in update.items():
                if key != "customer_id":
                    setattr(customer, key, value)
            updated_customers.append(customer)
        await self.session.flush()
        logging.info("CustomerManager.update_bulk end")
        return updated_customers
    async def delete_bulk(self, customer_ids: List[int]) -> bool:
        logging.info("CustomerManager.delete_bulk")
        """Delete multiple customers by their IDs."""
        for customer_id in customer_ids:
            if not isinstance(customer_id, int):
                raise TypeError(f"The customer_id must be an integer, got {type(customer_id)} instead.")
            customer = await self.get_by_id(customer_id)
            if not customer:
                raise CustomerNotFoundError(f"Customer with ID {customer_id} not found!")
            if customer:
                await self.session.delete(customer)
        await self.session.flush()
        return True
    async def count(self) -> int:
        logging.info("CustomerManager.count")
        """Return the total number of customers."""
        result = await self.session.execute(select(Customer))
        return len(result.scalars().all())
    #TODO fix. needs to populate peek props. use getall and sort List
    async def get_sorted_list(self, sort_by: str, order: Optional[str] = "asc") -> List[Customer]:
        """Retrieve customers sorted by a particular attribute."""
        if order == "asc":
            result = await self.session.execute(select(Customer).order_by(getattr(Customer, sort_by).asc()))
        else:
            result = await self.session.execute(select(Customer).order_by(getattr(Customer, sort_by).desc()))
        return result.scalars().all()
    async def refresh(self, customer: Customer) -> Customer:
        logging.info("CustomerManager.refresh")
        """Refresh the state of a given customer instance from the database."""
        await self.session.refresh(customer)
        return customer
    async def exists(self, customer_id: int) -> bool:
        logging.info(f"CustomerManager.exists {customer_id}")
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
        return dict1 == dict2

    async def get_by_tac_id(self, tac_id: int) -> List[Customer]: # TacID
        logging.info("CustomerManager.get_by_tac_id")
        if not isinstance(tac_id, int):
            raise TypeError(f"The customer_id must be an integer, got {type(tac_id)} instead.")
        # result = await self.session.execute(select(Customer).filter(Customer.tac_id == tac_id))
        # return result.scalars().all()
        query_filter = Customer.tac_id == tac_id
        query_results = await self._run_query(query_filter)
        return query_results

