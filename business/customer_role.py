import uuid
from datetime import datetime, date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Index, event, BigInteger, Boolean, Column, Date, DateTime, Float, Integer, Numeric, String, ForeignKey, Uuid, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from services.db_config import db_dialect,generate_uuid
from managers import CustomerManager as CustomerIDManager #CustomerID
from managers import RoleManager as RoleIDManager #RoleID
from managers import CustomerRoleManager
from models import CustomerRole
class CustomerRoleSessionNotFoundError(Exception):
    pass
class CustomerRoleInvalidInitError(Exception):
    pass
#Conditionally set the UUID column type
if db_dialect == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif db_dialect == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  #This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)
class CustomerRoleBusObj:
    def __init__(self, session:AsyncSession=None):
        if not session:
            raise CustomerRoleSessionNotFoundError("session required")
        self.session = session
        self.customer_role = CustomerRole()
    @property
    def customer_role_id(self):
        return self.customer_role.customer_role_id
    @customer_role_id.setter
    def code(self, value: int):
        if not isinstance(value, int):
            raise ValueError("customer_role_id must be a int.")
        self.customer_role.customer_role_id = value
    #code
    @property
    def code(self):
        return self.customer_role.code
    @code.setter
    def code(self, value: UUIDType):
        #if not isinstance(value, UUIDType):
        #raise ValueError("code must be a UUID.")
        self.customer_role.code = value
    #last_change_code
    @property
    def last_change_code(self):
        return self.customer_role.last_change_code
    @last_change_code.setter
    def last_change_code(self, value: int):
        if not isinstance(value, int):
            raise ValueError("last_change_code must be an integer.")
        self.customer_role.last_change_code = value
    #insert_user_id
    @property
    def insert_user_id(self):
        return self.customer_role.insert_user_id
    @insert_user_id.setter
    def insert_user_id(self, value: uuid.UUID):
        if not isinstance(value, uuid.UUID):
            raise ValueError("insert_user_id must be a UUID.")
        self.customer_role.insert_user_id = value
    #last_update_user_id
    @property
    def last_update_user_id(self):
        return self.customer_role.last_update_user_id
    @last_update_user_id.setter
    def last_update_user_id(self, value: uuid.UUID):
        if not isinstance(value, uuid.UUID):
            raise ValueError("last_update_user_id must be a UUID.")
        self.customer_role.last_update_user_id = value

    #CustomerID
    #IsPlaceholder
    @property
    def is_placeholder(self):
        return self.customer_role.is_placeholder
    @is_placeholder.setter
    def is_placeholder(self, value: bool):
        if not isinstance(value, bool):
            raise ValueError("is_placeholder must be a boolean.")
        self.customer_role.is_placeholder = value
    #Placeholder
    @property
    def placeholder(self):
        return self.customer_role.placeholder
    @placeholder.setter
    def placeholder(self, value: bool):
        if not isinstance(value, bool):
            raise ValueError("placeholder must be a boolean.")
        self.customer_role.placeholder = value
    #RoleID

    #CustomerID
    @property
    def customer_id(self):
        return self.customer_role.customer_id
    @customer_id.setter
    def customer_id(self, value):
        assert isinstance(value, int) or value is None, "customer_id must be an integer or None"
        self.customer_role.customer_id = value
    @property
    def customer_code_peek(self):
        return self.customer_role.customer_code_peek
    @customer_code_peek.setter
    def customer_code_peek(self, value):
        assert isinstance(value, UUIDType), "customer_code_peek must be a UUID"
        self.customer_role.customer_code_peek = value
    #isPlaceholder,
    #placeholder,
    #RoleID
    @property
    def role_id(self):
        return self.customer_role.role_id
    @role_id.setter
    def role_id(self, value: int):
        if not isinstance(value, int):
            raise ValueError("role_id must be an integer.")
        self.customer_role.role_id = value
    @property
    def role_code_peek(self):
        return self.customer_role.role_code_peek
    @role_code_peek.setter
    def role_code_peek(self, value):
        assert isinstance(value, UUIDType), "role_code_peek must be a UUID"
        self.customer_role.role_code_peek = value

    #insert_utc_date_time
    @property
    def insert_utc_date_time(self):
        return self.customer_role.insert_utc_date_time
    @insert_utc_date_time.setter
    def insert_utc_date_time(self, value):
        assert isinstance(value, datetime) or value is None, "insert_utc_date_time must be a datetime object or None"
        self.customer_role.insert_utc_date_time = value
    #update_utc_date_time
    @property
    def last_update_utc_date_time(self):
        return self.customer_role.last_update_utc_date_time
    @last_update_utc_date_time.setter
    def last_update_utc_date_time(self, value):
        assert isinstance(value, datetime) or value is None, "last_update_utc_date_time must be a datetime object or None"
        self.customer_role.last_update_utc_date_time = value
    async def load(self, json_data:str=None, code:uuid.UUID=None, customer_role_id:int=None, customer_role_obj_instance:CustomerRole=None, customer_role_dict:dict=None):
        if customer_role_id and self.customer_role.customer_role_id is None:
            customer_role_manager = CustomerRoleManager(self.session)
            customer_role_obj = await customer_role_manager.get_by_id(customer_role_id)
            self.customer_role = customer_role_obj
        if code and self.customer_role.customer_role_id is None:
            customer_role_manager = CustomerRoleManager(self.session)
            customer_role_obj = await customer_role_manager.get_by_code(code)
            self.customer_role = customer_role_obj
        if customer_role_obj_instance and self.customer_role.customer_role_id is None:
            customer_role_manager = CustomerRoleManager(self.session)
            customer_role_obj = await customer_role_manager.get_by_id(customer_role_obj_instance.customer_role_id)
            self.customer_role = customer_role_obj
        if json_data and self.customer_role.customer_role_id is None:
            customer_role_manager = CustomerRoleManager(self.session)
            self.customer_role = customer_role_manager.from_json(json_data)
        if customer_role_dict and self.customer_role.customer_role_id is None:
            customer_role_manager = CustomerRoleManager(self.session)
            self.customer_role = customer_role_manager.from_dict(customer_role_dict)
    async def refresh(self):
        customer_role_manager = CustomerRoleManager(self.session)
        self.customer_role = await customer_role_manager.refresh(self.customer_role)
    def to_dict(self):
        customer_role_manager = CustomerRoleManager(self.session)
        return customer_role_manager.to_dict(self.customer_role)
    def to_json(self):
        customer_role_manager = CustomerRoleManager(self.session)
        return customer_role_manager.to_json(self.customer_role)
    async def save(self):
        if self.customer_role.customer_role_id > 0:
            customer_role_manager = CustomerRoleManager(self.session)
            self.customer_role = await customer_role_manager.update(self.customer_role)
        if self.customer_role.customer_role_id == 0:
            customer_role_manager = CustomerRoleManager(self.session)
            self.customer_role = await customer_role_manager.add(self.customer_role)
    async def delete(self):
        if self.customer_role.customer_role_id > 0:
            customer_role_manager = CustomerRoleManager(self.session)
            self.customer_role = await customer_role_manager.delete(self.customer_role.customer_role_id)
    def get_customer_role_obj(self) -> CustomerRole:
        return self.customer_role
    def is_equal(self,customer_role:CustomerRole) -> CustomerRole:
        customer_role_manager = CustomerRoleManager(self.session)
        my_customer_role = self.get_customer_role_obj()
        return customer_role_manager.is_equal(customer_role, my_customer_role)

    async def get_customer_id_rel_obj(self, customer_id: int): #CustomerID
        customer_manager = CustomerIDManager(self.session)
        return await customer_manager.get_by_id(self.customer_role.customer_id)
    async def get_role_id_rel_obj(self, role_id: int): #RoleID
        role_manager = RoleIDManager(self.session)
        return await role_manager.get_by_id(self.customer_role.role_id)

