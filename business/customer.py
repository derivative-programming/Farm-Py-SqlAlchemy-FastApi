import uuid
from datetime import datetime, date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Index, event, BigInteger, Boolean, Column, Date, DateTime, Float, Integer, Numeric, String, ForeignKey, Uuid, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from business.tac import TacBusObj #TacID
from services.db_config import db_dialect,generate_uuid
from managers import TacManager as TacIDManager #TacID
from managers import CustomerManager
from models import Customer
import managers as managers_and_enums
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
class CustomerBusObj:
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
    #last_update_user_id
    @property
    def last_update_user_id(self):
        return self.customer.last_update_user_id
    @last_update_user_id.setter
    def last_update_user_id(self, value: uuid.UUID):
        if not isinstance(value, uuid.UUID):
            raise ValueError("last_update_user_id must be a UUID.")
        self.customer.last_update_user_id = value

    #ActiveOrganizationID
    @property
    def active_organization_id(self):
        return self.customer.active_organization_id
    @active_organization_id.setter
    def active_organization_id(self, value):
        assert isinstance(value, int), "active_organization_id must be an integer"
        self.customer.active_organization_id = value
    #Email
    @property
    def email(self):
        return self.customer.email
    @email.setter
    def email(self, value):
        assert isinstance(value, str), "email must be a string"
        self.customer.email = value
    #EmailConfirmedUTCDateTime
    @property
    def email_confirmed_utc_date_time(self):
        return self.customer.email_confirmed_utc_date_time
    @email_confirmed_utc_date_time.setter
    def email_confirmed_utc_date_time(self, value):
        assert isinstance(value, datetime), "email_confirmed_utc_date_time must be a datetime object"
        self.customer.email_confirmed_utc_date_time = value
    #FirstName
    @property
    def first_name(self):
        return self.customer.first_name
    @first_name.setter
    def first_name(self, value):
        assert isinstance(value, str), "first_name must be a string"
        self.customer.first_name = value
    #ForgotPasswordKeyExpirationUTCDateTime
    @property
    def forgot_password_key_expiration_utc_date_time(self):
        return self.customer.forgot_password_key_expiration_utc_date_time
    @forgot_password_key_expiration_utc_date_time.setter
    def forgot_password_key_expiration_utc_date_time(self, value):
        assert isinstance(value, datetime), "forgot_password_key_expiration_utc_date_time must be a datetime object"
        self.customer.forgot_password_key_expiration_utc_date_time = value
    #ForgotPasswordKeyValue
    @property
    def forgot_password_key_value(self):
        return self.customer.forgot_password_key_value
    @forgot_password_key_value.setter
    def forgot_password_key_value(self, value):
        assert isinstance(value, str), "forgot_password_key_value must be a string"
        self.customer.forgot_password_key_value = value
    #FSUserCodeValue
    @property
    def fs_user_code_value(self):
        return self.customer.fs_user_code_value
    @fs_user_code_value.setter
    def fs_user_code_value(self, value):
        assert isinstance(value, UUIDType), "fs_user_code_value must be a UUID"
        self.customer.fs_user_code_value = value
    #IsActive
    @property
    def is_active(self):
        return self.customer.is_active
    @is_active.setter
    def is_active(self, value: bool):
        if not isinstance(value, bool):
            raise ValueError("is_active must be a boolean.")
        self.customer.is_active = value
    #IsEmailAllowed
    @property
    def is_email_allowed(self):
        return self.customer.is_email_allowed
    @is_email_allowed.setter
    def is_email_allowed(self, value: bool):
        if not isinstance(value, bool):
            raise ValueError("is_email_allowed must be a boolean.")
        self.customer.is_email_allowed = value
    #IsEmailConfirmed
    @property
    def is_email_confirmed(self):
        return self.customer.is_email_confirmed
    @is_email_confirmed.setter
    def is_email_confirmed(self, value: bool):
        if not isinstance(value, bool):
            raise ValueError("is_email_confirmed must be a boolean.")
        self.customer.is_email_confirmed = value
    #IsEmailMarketingAllowed
    @property
    def is_email_marketing_allowed(self):
        return self.customer.is_email_marketing_allowed
    @is_email_marketing_allowed.setter
    def is_email_marketing_allowed(self, value: bool):
        if not isinstance(value, bool):
            raise ValueError("is_email_marketing_allowed must be a boolean.")
        self.customer.is_email_marketing_allowed = value
    #IsLocked
    @property
    def is_locked(self):
        return self.customer.is_locked
    @is_locked.setter
    def is_locked(self, value: bool):
        if not isinstance(value, bool):
            raise ValueError("is_locked must be a boolean.")
        self.customer.is_locked = value
    #IsMultipleOrganizationsAllowed
    @property
    def is_multiple_organizations_allowed(self):
        return self.customer.is_multiple_organizations_allowed
    @is_multiple_organizations_allowed.setter
    def is_multiple_organizations_allowed(self, value: bool):
        if not isinstance(value, bool):
            raise ValueError("is_multiple_organizations_allowed must be a boolean.")
        self.customer.is_multiple_organizations_allowed = value
    #IsVerboseLoggingForced
    @property
    def is_verbose_logging_forced(self):
        return self.customer.is_verbose_logging_forced
    @is_verbose_logging_forced.setter
    def is_verbose_logging_forced(self, value: bool):
        if not isinstance(value, bool):
            raise ValueError("is_verbose_logging_forced must be a boolean.")
        self.customer.is_verbose_logging_forced = value
    #LastLoginUTCDateTime
    @property
    def last_login_utc_date_time(self):
        return self.customer.last_login_utc_date_time
    @last_login_utc_date_time.setter
    def last_login_utc_date_time(self, value):
        assert isinstance(value, datetime), "last_login_utc_date_time must be a datetime object"
        self.customer.last_login_utc_date_time = value
    #LastName
    @property
    def last_name(self):
        return self.customer.last_name
    @last_name.setter
    def last_name(self, value):
        assert isinstance(value, str), "last_name must be a string"
        self.customer.last_name = value
    #Password
    @property
    def password(self):
        return self.customer.password
    @password.setter
    def password(self, value):
        assert isinstance(value, str), "password must be a string"
        self.customer.password = value
    #phone
    @property
    def phone(self):
        return self.customer.phone
    @phone.setter
    def phone(self, value):
        assert isinstance(value, str), "phone must be a string"
        self.customer.phone = value
    #Province
    @property
    def province(self):
        return self.customer.province
    @province.setter
    def province(self, value):
        assert isinstance(value, str), "province must be a string"
        self.customer.province = value
    #RegistrationUTCDateTime
    @property
    def registration_utc_date_time(self):
        return self.customer.registration_utc_date_time
    @registration_utc_date_time.setter
    def registration_utc_date_time(self, value):
        assert isinstance(value, datetime), "registration_utc_date_time must be a datetime object"
        self.customer.registration_utc_date_time = value
    #TacID
    #UTCOffsetInMinutes
    @property
    def utc_offset_in_minutes(self):
        return self.customer.utc_offset_in_minutes
    @utc_offset_in_minutes.setter
    def utc_offset_in_minutes(self, value):
        assert isinstance(value, int), "utc_offset_in_minutes must be an integer"
        self.customer.utc_offset_in_minutes = value
    #Zip
    @property
    def zip(self):
        return self.customer.zip
    @zip.setter
    def zip(self, value):
        assert isinstance(value, str), "zip must be a string"
        self.customer.zip = value

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

    async def refresh(self):
        customer_manager = CustomerManager(self.session)
        self.customer = await customer_manager.refresh(self.customer)
    def to_dict(self):
        customer_manager = CustomerManager(self.session)
        return customer_manager.to_dict(self.customer)
    def to_json(self):
        customer_manager = CustomerManager(self.session)
        return customer_manager.to_json(self.customer)
    async def save(self):
        if self.customer.customer_id > 0:
            customer_manager = CustomerManager(self.session)
            self.customer = await customer_manager.update(self.customer)
        if self.customer.customer_id == 0:
            customer_manager = CustomerManager(self.session)
            self.customer = await customer_manager.add(self.customer)
    async def delete(self):
        if self.customer.customer_id > 0:
            customer_manager = CustomerManager(self.session)
            self.customer = await customer_manager.delete(self.customer.customer_id)
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
    async def get_tac_id_rel_bus_obj(self) -> TacBusObj:
        tac_bus_obj = TacBusObj(self.session)
        await tac_bus_obj.load(tac_id=self.customer.tac_id)
        return tac_bus_obj
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
    async def get_parent_obj(self) -> TacBusObj:
        return await self.get_tac_id_rel_bus_obj()
    #uTCOffsetInMinutes,
    #zip,
