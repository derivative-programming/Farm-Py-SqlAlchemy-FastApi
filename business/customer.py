import random
import uuid
from typing import List
from datetime import datetime, date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Index, event, BigInteger, Boolean, Column, Date, DateTime, Float, Integer, Numeric, String, ForeignKey, Uuid, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
# from business.tac import TacBusObj #TacID
from services.db_config import db_dialect,generate_uuid
# from managers import TacManager as TacIDManager #TacID
from managers import CustomerManager
from models import Customer
import models
import managers as managers_and_enums
from .base_bus_obj import BaseBusObj

from business.customer_role import CustomerRoleBusObj

class CustomerSessionNotFoundError(Exception):
    pass
class CustomerInvalidInitError(Exception):
    pass
#Conditionally set the UUID column type
if db_dialect == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif db_dialect == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  #This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)
class CustomerBusObj(BaseBusObj):
    def __init__(self, session:AsyncSession=None):
        if not session:
            raise CustomerSessionNotFoundError("session required")
        self.session = session
        self.customer = Customer()
    @property
    def customer_id(self):
        return self.customer.customer_id
    @customer_id.setter
    def code(self, value: int):
        if not isinstance(value, int):
            raise ValueError("customer_id must be a int.")
        self.customer.customer_id = value
    #code
    @property
    def code(self):
        return self.customer.code
    @code.setter
    def code(self, value: UUIDType):
        #if not isinstance(value, UUIDType):
        #raise ValueError("code must be a UUID.")
        self.customer.code = value
    #last_change_code
    @property
    def last_change_code(self):
        return self.customer.last_change_code
    @last_change_code.setter
    def last_change_code(self, value: int):
        if not isinstance(value, int):
            raise ValueError("last_change_code must be an integer.")
        self.customer.last_change_code = value
    #insert_user_id
    @property
    def insert_user_id(self):
        return self.customer.insert_user_id
    @insert_user_id.setter
    def insert_user_id(self, value: uuid.UUID):
        if not isinstance(value, uuid.UUID):
            raise ValueError("insert_user_id must be a UUID.")
        self.customer.insert_user_id = value
    def set_prop_insert_user_id(self, value: uuid.UUID):
        self.insert_user_id = value
        return self
    #last_update_user_id
    @property
    def last_update_user_id(self):
        return self.customer.last_update_user_id
    @last_update_user_id.setter
    def last_update_user_id(self, value: uuid.UUID):
        if not isinstance(value, uuid.UUID):
            raise ValueError("last_update_user_id must be a UUID.")
        self.customer.last_update_user_id = value
    def set_prop_last_update_user_id(self, value: uuid.UUID):
        self.last_update_user_id = value
        return self

    #ActiveOrganizationID
    @property
    def active_organization_id(self):
        return self.customer.active_organization_id
    @active_organization_id.setter
    def active_organization_id(self, value):
        assert isinstance(value, int), "active_organization_id must be an integer"
        self.customer.active_organization_id = value
    def set_prop_active_organization_id(self, value):
        self.active_organization_id = value
        return self
    #Email
    @property
    def email(self):
        return self.customer.email
    @email.setter
    def email(self, value):
        assert isinstance(value, str), "email must be a string"
        self.customer.email = value
    def set_prop_email(self, value):
        self.email = value
        return self
    #EmailConfirmedUTCDateTime
    @property
    def email_confirmed_utc_date_time(self):
        return self.customer.email_confirmed_utc_date_time
    @email_confirmed_utc_date_time.setter
    def email_confirmed_utc_date_time(self, value):
        assert isinstance(value, datetime), "email_confirmed_utc_date_time must be a datetime object"
        self.customer.email_confirmed_utc_date_time = value
    def set_prop_email_confirmed_utc_date_time(self, value):
        self.email_confirmed_utc_date_time = value
        return self
    #FirstName
    @property
    def first_name(self):
        return self.customer.first_name
    @first_name.setter
    def first_name(self, value):
        assert isinstance(value, str), "first_name must be a string"
        self.customer.first_name = value
    def set_prop_first_name(self, value):
        self.first_name = value
        return self
    #ForgotPasswordKeyExpirationUTCDateTime
    @property
    def forgot_password_key_expiration_utc_date_time(self):
        return self.customer.forgot_password_key_expiration_utc_date_time
    @forgot_password_key_expiration_utc_date_time.setter
    def forgot_password_key_expiration_utc_date_time(self, value):
        assert isinstance(value, datetime), "forgot_password_key_expiration_utc_date_time must be a datetime object"
        self.customer.forgot_password_key_expiration_utc_date_time = value
    def set_prop_forgot_password_key_expiration_utc_date_time(self, value):
        self.forgot_password_key_expiration_utc_date_time = value
        return self
    #ForgotPasswordKeyValue
    @property
    def forgot_password_key_value(self):
        return self.customer.forgot_password_key_value
    @forgot_password_key_value.setter
    def forgot_password_key_value(self, value):
        assert isinstance(value, str), "forgot_password_key_value must be a string"
        self.customer.forgot_password_key_value = value
    def set_prop_forgot_password_key_value(self, value):
        self.forgot_password_key_value = value
        return self
    #FSUserCodeValue
    @property
    def fs_user_code_value(self):
        return self.customer.fs_user_code_value
    @fs_user_code_value.setter
    def fs_user_code_value(self, value):
        assert isinstance(value, UUIDType), "fs_user_code_value must be a UUID"
        self.customer.fs_user_code_value = value
    def set_prop_fs_user_code_value(self, value):
        self.fs_user_code_value = value
        return self
    #IsActive
    @property
    def is_active(self):
        return self.customer.is_active
    @is_active.setter
    def is_active(self, value: bool):
        if not isinstance(value, bool):
            raise ValueError("is_active must be a boolean.")
        self.customer.is_active = value
    def set_prop_is_active(self, value: bool):
        self.is_active = value
        return self
    #IsEmailAllowed
    @property
    def is_email_allowed(self):
        return self.customer.is_email_allowed
    @is_email_allowed.setter
    def is_email_allowed(self, value: bool):
        if not isinstance(value, bool):
            raise ValueError("is_email_allowed must be a boolean.")
        self.customer.is_email_allowed = value
    def set_prop_is_email_allowed(self, value: bool):
        self.is_email_allowed = value
        return self
    #IsEmailConfirmed
    @property
    def is_email_confirmed(self):
        return self.customer.is_email_confirmed
    @is_email_confirmed.setter
    def is_email_confirmed(self, value: bool):
        if not isinstance(value, bool):
            raise ValueError("is_email_confirmed must be a boolean.")
        self.customer.is_email_confirmed = value
    def set_prop_is_email_confirmed(self, value: bool):
        self.is_email_confirmed = value
        return self
    #IsEmailMarketingAllowed
    @property
    def is_email_marketing_allowed(self):
        return self.customer.is_email_marketing_allowed
    @is_email_marketing_allowed.setter
    def is_email_marketing_allowed(self, value: bool):
        if not isinstance(value, bool):
            raise ValueError("is_email_marketing_allowed must be a boolean.")
        self.customer.is_email_marketing_allowed = value
    def set_prop_is_email_marketing_allowed(self, value: bool):
        self.is_email_marketing_allowed = value
        return self
    #IsLocked
    @property
    def is_locked(self):
        return self.customer.is_locked
    @is_locked.setter
    def is_locked(self, value: bool):
        if not isinstance(value, bool):
            raise ValueError("is_locked must be a boolean.")
        self.customer.is_locked = value
    def set_prop_is_locked(self, value: bool):
        self.is_locked = value
        return self
    #IsMultipleOrganizationsAllowed
    @property
    def is_multiple_organizations_allowed(self):
        return self.customer.is_multiple_organizations_allowed
    @is_multiple_organizations_allowed.setter
    def is_multiple_organizations_allowed(self, value: bool):
        if not isinstance(value, bool):
            raise ValueError("is_multiple_organizations_allowed must be a boolean.")
        self.customer.is_multiple_organizations_allowed = value
    def set_prop_is_multiple_organizations_allowed(self, value: bool):
        self.is_multiple_organizations_allowed = value
        return self
    #IsVerboseLoggingForced
    @property
    def is_verbose_logging_forced(self):
        return self.customer.is_verbose_logging_forced
    @is_verbose_logging_forced.setter
    def is_verbose_logging_forced(self, value: bool):
        if not isinstance(value, bool):
            raise ValueError("is_verbose_logging_forced must be a boolean.")
        self.customer.is_verbose_logging_forced = value
    def set_prop_is_verbose_logging_forced(self, value: bool):
        self.is_verbose_logging_forced = value
        return self
    #LastLoginUTCDateTime
    @property
    def last_login_utc_date_time(self):
        return self.customer.last_login_utc_date_time
    @last_login_utc_date_time.setter
    def last_login_utc_date_time(self, value):
        assert isinstance(value, datetime), "last_login_utc_date_time must be a datetime object"
        self.customer.last_login_utc_date_time = value
    def set_prop_last_login_utc_date_time(self, value):
        self.last_login_utc_date_time = value
        return self
    #LastName
    @property
    def last_name(self):
        return self.customer.last_name
    @last_name.setter
    def last_name(self, value):
        assert isinstance(value, str), "last_name must be a string"
        self.customer.last_name = value
    def set_prop_last_name(self, value):
        self.last_name = value
        return self
    #Password
    @property
    def password(self):
        return self.customer.password
    @password.setter
    def password(self, value):
        assert isinstance(value, str), "password must be a string"
        self.customer.password = value
    def set_prop_password(self, value):
        self.password = value
        return self
    #phone
    @property
    def phone(self):
        return self.customer.phone
    @phone.setter
    def phone(self, value):
        assert isinstance(value, str), "phone must be a string"
        self.customer.phone = value
    def set_prop_phone(self, value):
        self.phone = value
        return self
    #Province
    @property
    def province(self):
        return self.customer.province
    @province.setter
    def province(self, value):
        assert isinstance(value, str), "province must be a string"
        self.customer.province = value
    def set_prop_province(self, value):
        self.province = value
        return self
    #RegistrationUTCDateTime
    @property
    def registration_utc_date_time(self):
        return self.customer.registration_utc_date_time
    @registration_utc_date_time.setter
    def registration_utc_date_time(self, value):
        assert isinstance(value, datetime), "registration_utc_date_time must be a datetime object"
        self.customer.registration_utc_date_time = value
    def set_prop_registration_utc_date_time(self, value):
        self.registration_utc_date_time = value
        return self
    #TacID
    #UTCOffsetInMinutes
    @property
    def utc_offset_in_minutes(self):
        return self.customer.utc_offset_in_minutes
    @utc_offset_in_minutes.setter
    def utc_offset_in_minutes(self, value):
        assert isinstance(value, int), "utc_offset_in_minutes must be an integer"
        self.customer.utc_offset_in_minutes = value
    def set_prop_utc_offset_in_minutes(self, value):
        self.utc_offset_in_minutes = value
        return self
    #Zip
    @property
    def zip(self):
        return self.customer.zip
    @zip.setter
    def zip(self, value):
        assert isinstance(value, str), "zip must be a string"
        self.customer.zip = value
    def set_prop_zip(self, value):
        self.zip = value
        return self

    #activeOrganizationID,
    #email,
    #emailConfirmedUTCDateTime
    #firstName,
    #forgotPasswordKeyExpirationUTCDateTime
    #forgotPasswordKeyValue,
    #fSUserCodeValue,
    #isActive,
    #isEmailAllowed,
    #isEmailConfirmed,
    #isEmailMarketingAllowed,
    #isLocked,
    #isMultipleOrganizationsAllowed,
    #isVerboseLoggingForced,
    #lastLoginUTCDateTime
    #lastName,
    #password,
    #phone,
    #province,
    #registrationUTCDateTime
    #TacID
    @property
    def tac_id(self):
        return self.customer.tac_id
    @tac_id.setter
    def tac_id(self, value):
        assert isinstance(value, int) or value is None, "tac_id must be an integer or None"
        self.customer.tac_id = value
    def set_prop_tac_id(self, value):
        self.tac_id = value
        return self
    @property
    def tac_code_peek(self):
        return self.customer.tac_code_peek
    # @tac_code_peek.setter
    # def tac_code_peek(self, value):
    #     assert isinstance(value, UUIDType), "tac_code_peek must be a UUID"
    #     self.customer.tac_code_peek = value
    #uTCOffsetInMinutes,
    #zip,

    #insert_utc_date_time
    @property
    def insert_utc_date_time(self):
        return self.customer.insert_utc_date_time
    @insert_utc_date_time.setter
    def insert_utc_date_time(self, value):
        assert isinstance(value, datetime) or value is None, "insert_utc_date_time must be a datetime object or None"
        self.customer.insert_utc_date_time = value
    #update_utc_date_time
    @property
    def last_update_utc_date_time(self):
        return self.customer.last_update_utc_date_time
    @last_update_utc_date_time.setter
    def last_update_utc_date_time(self, value):
        assert isinstance(value, datetime) or value is None, "last_update_utc_date_time must be a datetime object or None"
        self.customer.last_update_utc_date_time = value

    async def load(self, json_data:str=None,
                   code:uuid.UUID=None,
                   customer_id:int=None,
                   customer_obj_instance:Customer=None,
                   customer_dict:dict=None):
        if customer_id and self.customer.customer_id is None:
            customer_manager = CustomerManager(self.session)
            customer_obj = await customer_manager.get_by_id(customer_id)
            self.customer = customer_obj
        if code and self.customer.customer_id is None:
            customer_manager = CustomerManager(self.session)
            customer_obj = await customer_manager.get_by_code(code)
            self.customer = customer_obj
        if customer_obj_instance and self.customer.customer_id is None:
            customer_manager = CustomerManager(self.session)
            customer_obj = await customer_manager.get_by_id(customer_obj_instance.customer_id)
            self.customer = customer_obj
        if json_data and self.customer.customer_id is None:
            customer_manager = CustomerManager(self.session)
            self.customer = customer_manager.from_json(json_data)
        if customer_dict and self.customer.customer_id is None:
            customer_manager = CustomerManager(self.session)
            self.customer = customer_manager.from_dict(customer_dict)
        return self
    @staticmethod
    async def get(session:AsyncSession,
                    json_data:str=None,
                   code:uuid.UUID=None,
                   customer_id:int=None,
                   customer_obj_instance:Customer=None,
                   customer_dict:dict=None):
        result = CustomerBusObj(session=session)
        await result.load(
            json_data,
            code,
            customer_id,
            customer_obj_instance,
            customer_dict
        )
        return result

    async def refresh(self):
        customer_manager = CustomerManager(self.session)
        self.customer = await customer_manager.refresh(self.customer)
        return self
    def is_valid(self):
        return (self.customer is not None)
    def to_dict(self):
        customer_manager = CustomerManager(self.session)
        return customer_manager.to_dict(self.customer)
    def to_json(self):
        customer_manager = CustomerManager(self.session)
        return customer_manager.to_json(self.customer)
    async def save(self):
        if self.customer.customer_id is not None and self.customer.customer_id > 0:
            customer_manager = CustomerManager(self.session)
            self.customer = await customer_manager.update(self.customer)
        if self.customer.customer_id is None or self.customer.customer_id == 0:
            customer_manager = CustomerManager(self.session)
            self.customer = await customer_manager.add(self.customer)
        return self
    async def delete(self):
        if self.customer.customer_id > 0:
            customer_manager = CustomerManager(self.session)
            await customer_manager.delete(self.customer.customer_id)
            self.customer = None
    async def randomize_properties(self):
        self.customer.active_organization_id = random.randint(0, 100)
        self.customer.email = f"user{random.randint(1, 1000)}@example.com"
        self.customer.email_confirmed_utc_date_time = datetime(random.randint(2000, 2023), random.randint(1, 12), random.randint(1, 28))
        self.customer.first_name = "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        self.customer.forgot_password_key_expiration_utc_date_time = datetime(random.randint(2000, 2023), random.randint(1, 12), random.randint(1, 28))
        self.customer.forgot_password_key_value = "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        self.customer.fs_user_code_value = generate_uuid()
        self.customer.is_active = random.choice([True, False])
        self.customer.is_email_allowed = random.choice([True, False])
        self.customer.is_email_confirmed = random.choice([True, False])
        self.customer.is_email_marketing_allowed = random.choice([True, False])
        self.customer.is_locked = random.choice([True, False])
        self.customer.is_multiple_organizations_allowed = random.choice([True, False])
        self.customer.is_verbose_logging_forced = random.choice([True, False])
        self.customer.last_login_utc_date_time = datetime(random.randint(2000, 2023), random.randint(1, 12), random.randint(1, 28))
        self.customer.last_name = "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        self.customer.password = "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        self.customer.phone = f"+1{random.randint(1000000000, 9999999999)}"
        self.customer.province = "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        self.customer.registration_utc_date_time = datetime(random.randint(2000, 2023), random.randint(1, 12), random.randint(1, 28))
        # self.customer.tac_id = random.randint(0, 100)
        self.customer.utc_offset_in_minutes = random.randint(0, 100)
        self.customer.zip = "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        return self
    def get_customer_obj(self) -> Customer:
        return self.customer
    def is_equal(self,customer:Customer) -> Customer:
        customer_manager = CustomerManager(self.session)
        my_customer = self.get_customer_obj()
        return customer_manager.is_equal(customer, my_customer)

    #activeOrganizationID,
    #email,
    #emailConfirmedUTCDateTime
    #firstName,
    #forgotPasswordKeyExpirationUTCDateTime
    #forgotPasswordKeyValue,
    #fSUserCodeValue,
    #isActive,
    #isEmailAllowed,
    #isEmailConfirmed,
    #isEmailMarketingAllowed,
    #isLocked,
    #isMultipleOrganizationsAllowed,
    #isVerboseLoggingForced,
    #lastLoginUTCDateTime
    #lastName,
    #password,
    #phone,
    #province,
    #registrationUTCDateTime
    #TacID
    async def get_tac_id_rel_obj(self) -> models.Tac:
        tac_manager = managers_and_enums.TacManager(self.session)
        tac_obj = await tac_manager.get_by_id(self.tac_id)
        return tac_obj
    #uTCOffsetInMinutes,
    #zip,

    def get_obj(self) -> Customer:
        return self.customer
    def get_object_name(self) -> str:
        return "customer"
    def get_id(self) -> int:
        return self.customer_id
    #activeOrganizationID,
    #email,
    #emailConfirmedUTCDateTime
    #firstName,
    #forgotPasswordKeyExpirationUTCDateTime
    #forgotPasswordKeyValue,
    #fSUserCodeValue,
    #isActive,
    #isEmailAllowed,
    #isEmailConfirmed,
    #isEmailMarketingAllowed,
    #isLocked,
    #isMultipleOrganizationsAllowed,
    #isVerboseLoggingForced,
    #lastLoginUTCDateTime
    #lastName,
    #password,
    #phone,
    #province,
    #registrationUTCDateTime
    #TacID
    # async def get_parent_obj(self) -> TacBusObj:
    #     return await self.get_tac_id_rel_bus_obj()
    async def get_parent_name(self) -> str:
        return 'Tac'
    async def get_parent_code(self) -> uuid.UUID:
        return self.tac_code_peek
    #uTCOffsetInMinutes,
    #zip,

    async def build_customer_role(self) -> CustomerRoleBusObj:
        item = CustomerRoleBusObj(self.session)
        role_manager = managers_and_enums.RoleManager(self.session)
        role_id_role = await role_manager.from_enum(
            managers_and_enums.RoleEnum.Unknown)
        item.role_id = role_id_role.role_id
        item.customer_role.role_id_code_peek = role_id_role.code

        item.customer_id = self.customer_id
        item.customer_role.customer_code_peek = self.code

        return item

    async def get_all_customer_role(self) -> List[CustomerRoleBusObj]:
        results = list()
        customer_role_manager = managers_and_enums.CustomerRoleManager(self.session)
        obj_list = await customer_role_manager.get_by_customer_id(self.customer_id)
        for obj_item in obj_list:
            bus_obj_item = CustomerRoleBusObj(self.session)
            await bus_obj_item.load(customer_role_obj_instance=obj_item)
            results.append(bus_obj_item)
        return results

