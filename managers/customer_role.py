# models/managers/customer_role.py
# pylint: disable=unused-import
"""
    #TODO add comment
"""
import json
import logging
import uuid
from enum import Enum  # noqa: F401
from typing import List, Optional, Dict
from sqlalchemy import and_
from sqlalchemy.future import select
from helpers.session_context import SessionContext
from models.customer import Customer  # CustomerID
from models.role import Role  # RoleID
from models.customer_role import CustomerRole
from models.serialization_schema.customer_role import CustomerRoleSchema
from services.logging_config import get_logger
logger = get_logger(__name__)
class CustomerRoleNotFoundError(Exception):
    """
    Exception raised when a specified customer_role is not found.
    Attributes:
        message (str):Explanation of the error.
    """
    def __init__(self, message="CustomerRole not found"):
        self.message = message
        super().__init__(self.message)

class CustomerRoleManager:
    """
    #TODO add comment
    """
    def __init__(self, session_context: SessionContext):
        """
            #TODO add comment
        """
        if not session_context.session:
            raise ValueError("session required")
        self._session_context = session_context
    def convert_uuid_to_model_uuid(self, value: uuid.UUID):
        """
            #TODO add comment
        """
        # Conditionally set the UUID column type
        return value

    async def initialize(self):
        """
            #TODO add comment
        """
        logging.info("CustomerRoleManager.Initialize")

    async def build(self, **kwargs) -> CustomerRole:
        """
            #TODO add comment
        """
        logging.info("CustomerRoleManager.build")
        return CustomerRole(**kwargs)
    async def add(self, customer_role: CustomerRole) -> CustomerRole:
        """
            #TODO add comment
        """
        logging.info("CustomerRoleManager.add")
        customer_role.insert_user_id = self.convert_uuid_to_model_uuid(
            self._session_context.customer_code)
        customer_role.last_update_user_id = self.convert_uuid_to_model_uuid(
            self._session_context.customer_code)
        self._session_context.session.add(customer_role)
        await self._session_context.session.flush()
        return customer_role
    def _build_query(self):
        """
            #TODO add comment
        """
        logging.info("CustomerRoleManager._build_query")
#         join_condition = None
# # endset
#         join_condition = outerjoin(join_condition, Customer, and_(CustomerRole.customer_id == Customer.customer_id, CustomerRole.customer_id != 0))
#         join_condition = outerjoin(CustomerRole, Role, and_(CustomerRole.role_id == Role.role_id, CustomerRole.role_id != 0))
# # endset
#         if join_condition is not None:
#             query = select(CustomerRole
#                         , Customer  # customer_id
#                         , Role  # role_id
#                         ).select_from(join_condition)
#         else:
#             query = select(CustomerRole)
        query = select(
            CustomerRole,
            Customer,  # customer_id
            Role,  # role_id
        )
# endset
        query = query.outerjoin(  # customer_id
            Customer,
            and_(CustomerRole.customer_id == Customer.customer_id,
                 CustomerRole.customer_id != 0)
        )
        query = query.outerjoin(  # role_id
            Role,
            and_(CustomerRole.role_id == Role.role_id,
                 CustomerRole.role_id != 0)
        )
# endset
        return query
    async def _run_query(self, query_filter) -> List[CustomerRole]:
        """
            #TODO add comment
        """
        logging.info("CustomerRoleManager._run_query")
        customer_role_query_all = self._build_query()
        if query_filter is not None:
            query = customer_role_query_all.filter(query_filter)
        else:
            query = customer_role_query_all
        result_proxy = await self._session_context.session.execute(query)
        query_results = result_proxy.all()
        result = list()
        for query_result_row in query_results:
            i = 0
            customer_role = query_result_row[i]
            i = i + 1
# endset
            customer = query_result_row[i]  # customer_id
            i = i + 1
            role = query_result_row[i]  # role_id
            i = i + 1
# endset
            customer_role.customer_code_peek = customer.code if customer else uuid.UUID(int=0)  # customer_id
            customer_role.role_code_peek = role.code if role else uuid.UUID(int=0)  # role_id
# endset
            result.append(customer_role)
        return result
    def _first_or_none(self, customer_role_list: List) -> CustomerRole:
        """
            #TODO add comment
        """
        return customer_role_list[0] if customer_role_list else None
    async def get_by_id(self, customer_role_id: int) -> Optional[CustomerRole]:
        """
            #TODO add comment
        """
        logging.info(
            "CustomerRoleManager.get_by_id start customer_role_id: %s",
            str(customer_role_id))
        if not isinstance(customer_role_id, int):
            raise TypeError(
                "The customer_role_id must be an integer, got %s instead.",
                type(customer_role_id))
        query_filter = CustomerRole.customer_role_id == customer_role_id
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)
    async def get_by_code(self, code: uuid.UUID) -> Optional[CustomerRole]:
        """
            #TODO add comment
        """
        logging.info("CustomerRoleManager.get_by_code %s", code)
        query_filter = CustomerRole._code == str(code)
        query_results = await self._run_query(query_filter)
        return self._first_or_none(query_results)
    async def update(self, customer_role: CustomerRole, **kwargs) -> Optional[CustomerRole]:
        """
            #TODO add comment
        """
        logging.info("CustomerRoleManager.update")
        property_list = CustomerRole.property_list()
        if customer_role:
            customer_role.last_update_user_id = self.convert_uuid_to_model_uuid(
                self._session_context.customer_code)
            for key, value in kwargs.items():
                if key not in property_list:
                    raise ValueError(f"Invalid property: {key}")
                setattr(customer_role, key, value)
            await self._session_context.session.flush()
        return customer_role
    async def delete(self, customer_role_id: int):
        """
            #TODO add comment
        """
        logging.info("CustomerRoleManager.delete %s", customer_role_id)
        if not isinstance(customer_role_id, int):
            raise TypeError(
                f"The customer_role_id must be an integer, got {type(customer_role_id)} instead."
            )
        customer_role = await self.get_by_id(customer_role_id)
        if not customer_role:
            raise CustomerRoleNotFoundError(f"CustomerRole with ID {customer_role_id} not found!")
        await self._session_context.session.delete(customer_role)
        await self._session_context.session.flush()
    async def get_list(self) -> List[CustomerRole]:
        """
            #TODO add comment
        """
        logging.info("CustomerRoleManager.get_list")
        query_results = await self._run_query(None)
        return query_results
    def to_json(self, customer_role: CustomerRole) -> str:
        """
        Serialize the CustomerRole object to a JSON string using the CustomerRoleSchema.
        """
        logging.info("CustomerRoleManager.to_json")
        schema = CustomerRoleSchema()
        customer_role_data = schema.dump(customer_role)
        return json.dumps(customer_role_data)
    def to_dict(self, customer_role: CustomerRole) -> dict:
        """
        Serialize the CustomerRole object to a JSON string using the CustomerRoleSchema.
        """
        logging.info("CustomerRoleManager.to_dict")
        schema = CustomerRoleSchema()
        customer_role_data = schema.dump(customer_role)
        return customer_role_data
    def from_json(self, json_str: str) -> CustomerRole:
        """
        Deserialize a JSON string into a CustomerRole object using the CustomerRoleSchema.
        """
        logging.info("CustomerRoleManager.from_json")
        schema = CustomerRoleSchema()
        data = json.loads(json_str)
        customer_role_dict = schema.load(data)
        new_customer_role = CustomerRole(**customer_role_dict)
        return new_customer_role
    def from_dict(self, customer_role_dict: str) -> CustomerRole:
        """
        #TODO add comment
        """
        logging.info("CustomerRoleManager.from_dict")
        schema = CustomerRoleSchema()
        customer_role_dict_converted = schema.load(customer_role_dict)
        new_customer_role = CustomerRole(**customer_role_dict_converted)
        return new_customer_role
    async def add_bulk(self, customer_roles: List[CustomerRole]) -> List[CustomerRole]:
        """
        Add multiple customer_roles at once.
        """
        logging.info("CustomerRoleManager.add_bulk")
        for customer_role in customer_roles:
            customer_role_id = customer_role.customer_role_id
            code = customer_role.code
            if customer_role.customer_role_id is not None and customer_role.customer_role_id > 0:
                raise ValueError(
                    f"CustomerRole is already added: {str(code)} {str(customer_role_id)}"
                )
            customer_role.insert_user_id = self.convert_uuid_to_model_uuid(
                self._session_context.customer_code)
            customer_role.last_update_user_id = self.convert_uuid_to_model_uuid(
                self._session_context.customer_code)
        self._session_context.session.add_all(customer_roles)
        await self._session_context.session.flush()
        return customer_roles
    async def update_bulk(
        self,
        customer_role_updates: List[Dict[int, Dict]]
    ) -> List[CustomerRole]:
        """
        #TODO add comment
        """
        logging.info("CustomerRoleManager.update_bulk start")
        updated_customer_roles = []
        for update in customer_role_updates:
            customer_role_id = update.get("customer_role_id")
            if not isinstance(customer_role_id, int):
                raise TypeError(
                    f"The customer_role_id must be an integer, got {type(customer_role_id)} instead."
                )
            if not customer_role_id:
                continue
            logging.info("CustomerRoleManager.update_bulk customer_role_id:%s", customer_role_id)
            customer_role = await self.get_by_id(customer_role_id)
            if not customer_role:
                raise CustomerRoleNotFoundError(
                    f"CustomerRole with ID {customer_role_id} not found!")
            for key, value in update.items():
                if key != "customer_role_id":
                    setattr(customer_role, key, value)
            customer_role.last_update_user_id = self.convert_uuid_to_model_uuid(
                self._session_context.customer_code)
            updated_customer_roles.append(customer_role)
        await self._session_context.session.flush()
        logging.info("CustomerRoleManager.update_bulk end")
        return updated_customer_roles
    async def delete_bulk(self, customer_role_ids: List[int]) -> bool:
        """
        Delete multiple customer_roles by their IDs.
        """
        logging.info("CustomerRoleManager.delete_bulk")
        for customer_role_id in customer_role_ids:
            if not isinstance(customer_role_id, int):
                raise TypeError(
                    f"The customer_role_id must be an integer, got {type(customer_role_id)} instead."
                )
            customer_role = await self.get_by_id(customer_role_id)
            if not customer_role:
                raise CustomerRoleNotFoundError(
                    f"CustomerRole with ID {customer_role_id} not found!"
                )
            if customer_role:
                await self._session_context.session.delete(customer_role)
        await self._session_context.session.flush()
        return True
    async def count(self) -> int:
        """
        return the total number of customer_roles.
        """
        logging.info("CustomerRoleManager.count")
        result = await self._session_context.session.execute(select(CustomerRole))
        return len(result.scalars().all())
    #TODO fix. needs to populate peek props. use getall and sort List
    async def get_sorted_list(
            self,
            sort_by: str,
            order: Optional[str] = "asc") -> List[CustomerRole]:
        """
        Retrieve customer_roles sorted by a particular attribute.
        """
        if order == "asc":
            result = await self._session_context.session.execute(
                select(CustomerRole).order_by(getattr(CustomerRole, sort_by).asc()))
        else:
            result = await self._session_context.session.execute(
                select(CustomerRole).order_by(getattr(CustomerRole, sort_by).desc()))
        return result.scalars().all()
    async def refresh(self, customer_role: CustomerRole) -> CustomerRole:
        """
        Refresh the state of a given customer_role instance from the database.
        """
        logging.info("CustomerRoleManager.refresh")
        await self._session_context.session.refresh(customer_role)
        return customer_role
    async def exists(self, customer_role_id: int) -> bool:
        """
        Check if a customer_role with the given ID exists.
        """
        logging.info("CustomerRoleManager.exists %s", customer_role_id)
        if not isinstance(customer_role_id, int):
            raise TypeError(
                f"The customer_role_id must be an integer, got {type(customer_role_id)} instead."
            )
        customer_role = await self.get_by_id(customer_role_id)
        return bool(customer_role)
    def is_equal(self, customer_role1: CustomerRole, customer_role2: CustomerRole) -> bool:
        """
        #TODO add comment
        """
        if not customer_role1:
            raise TypeError("CustomerRole1 required.")
        if not customer_role2:
            raise TypeError("CustomerRole2 required.")
        if not isinstance(customer_role1, CustomerRole):
            raise TypeError("The customer_role1 must be an CustomerRole instance.")
        if not isinstance(customer_role2, CustomerRole):
            raise TypeError("The customer_role2 must be an CustomerRole instance.")
        dict1 = self.to_dict(customer_role1)
        dict2 = self.to_dict(customer_role2)
        return dict1 == dict2
# endset
    async def get_by_customer_id(self, customer_id: int) -> List[CustomerRole]:  # CustomerID
        """
        #TODO add comment
        """
        logging.info("CustomerRoleManager.get_by_customer_id")
        if not isinstance(customer_id, int):
            raise TypeError(
                f"The customer_role_id must be an integer, got {type(customer_id)} instead."
            )
        query_filter = CustomerRole.customer_id == customer_id
        query_results = await self._run_query(query_filter)
        return query_results
    async def get_by_role_id(
        self,
        role_id: int
    ) -> List[CustomerRole]:  # RoleID
        """
        #TODO add comment
        """
        logging.info("CustomerRoleManager.get_by_role_id")
        if not isinstance(role_id, int):
            raise TypeError(
                f"The customer_role_id must be an integer, got {type(role_id)} instead."
            )
        query_filter = CustomerRole.role_id == role_id
        query_results = await self._run_query(query_filter)
        return query_results
# endset

