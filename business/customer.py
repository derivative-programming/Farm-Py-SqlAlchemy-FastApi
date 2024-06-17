# business/customer.py
"""
    #TODO add comment
"""
from decimal import Decimal
import random
import uuid
from typing import List
from datetime import datetime, date
from helpers.session_context import SessionContext
from managers import CustomerManager
from models import Customer
import models
import managers as managers_and_enums
from .base_bus_obj import BaseBusObj

from business.customer_role import CustomerRoleBusObj

NOT_INITIALIZED_ERROR_MESSAGE = (
    "Customer object is not initialized")
class CustomerInvalidInitError(Exception):
    """
    #TODO add comment
    """
    pass
class CustomerBusObj(BaseBusObj):
    """
    This class represents the business object for a Customer.
    It requires a valid session context for initialization.
    """
    def __init__(self, session_context: SessionContext):
        if not session_context.session:
            raise ValueError("session required")
        self._session_context = session_context
        self.customer = Customer()
    @property
    def customer_id(self) -> int:
        """
        Get the customer ID from the Customer object.
        :return: The customer ID.
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.customer.customer_id
    # @customer_id.setter
    # def customer_id(self, value: int):
    #     """
    #     #TODO add comment
    #     """
    #     if not isinstance(value, int):
    #         raise ValueError("customer_id must be a int.")
    #     self.customer.customer_id = value
    # code
    @property
    def code(self):
        """
        #TODO add comment
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.customer.code
    @code.setter
    def code(self, value: uuid.UUID):  # type: ignore
        """
        #TODO add comment
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if not isinstance(value, uuid.UUID):
            raise ValueError("code must be a UUID.")
        self.customer.code = value
    # last_change_code
    @property
    def last_change_code(self):
        """
        #TODO add comment
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.customer.last_change_code
    @last_change_code.setter
    def last_change_code(self, value: int):
        """
        #TODO add comment
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if not isinstance(value, int):
            raise ValueError("last_change_code must be an integer.")
        self.customer.last_change_code = value
    # insert_user_id
    @property
    def insert_user_id(self):
        """
        #TODO add comment
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.customer.insert_user_id
    @insert_user_id.setter
    def insert_user_id(self, value: uuid.UUID):
        """
        #TODO add comment
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if not isinstance(value, uuid.UUID):
            raise ValueError("insert_user_id must be a UUID.")
        self.customer.insert_user_id = value
    # def set_prop_insert_user_id(self, value: uuid.UUID):
    #     """
    #     #TODO add comment
    #     """
    #     if not self.customer:
    #         raise AttributeError(NOT_INITIALIZED_ERROR_MESSAGE)
    #     self.insert_user_id = value
    #     return self
    # last_update_user_id
    @property
    def last_update_user_id(self):
        """
        #TODO add comment
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.customer.last_update_user_id
    @last_update_user_id.setter
    def last_update_user_id(self, value: uuid.UUID):
        """
        #TODO add comment
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if not isinstance(value, uuid.UUID):
            raise ValueError("last_update_user_id must be a UUID.")
        self.customer.last_update_user_id = value
    # def set_prop_last_update_user_id(self, value: uuid.UUID):
    #     """
    #     #TODO add comment
    #     """
    #     self.last_update_user_id = value
    #     return self
# endset
    # activeOrganizationID
    @property
    def active_organization_id(self):
        """
        #TODO add comment
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.customer.active_organization_id
    @active_organization_id.setter
    def active_organization_id(self, value):
        """
        #TODO add comment
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, int), (
            "active_organization_id must be an integer")
        self.customer.active_organization_id = value
    def set_prop_active_organization_id(self, value: int):
        """
        #TODO add comment
        """
        self.active_organization_id = value
        return self
    # email
    @property
    def email(self):
        """
        #TODO add comment
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if self.customer.email is None:
            return ""
        return self.customer.email
    @email.setter
    def email(self, value):
        """
        #TODO add comment
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, str), (
            "email must be a string")
        self.customer.email = value
    def set_prop_email(self, value: str):
        """
        #TODO add comment
        """
        self.email = value
        return self
    # emailConfirmedUTCDateTime
    @property
    def email_confirmed_utc_date_time(self):
        """
        #TODO add comment
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.customer.email_confirmed_utc_date_time
    @email_confirmed_utc_date_time.setter
    def email_confirmed_utc_date_time(self, value):
        """
        #TODO add comment
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, datetime), (
            "email_confirmed_utc_date_time must be a datetime object")
        self.customer.email_confirmed_utc_date_time = value
    def set_prop_email_confirmed_utc_date_time(self, value: datetime):
        """
        #TODO add comment
        """
        self.email_confirmed_utc_date_time = value
        return self
    # firstName
    @property
    def first_name(self):
        """
        #TODO add comment
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if self.customer.first_name is None:
            return ""
        return self.customer.first_name
    @first_name.setter
    def first_name(self, value):
        """
        #TODO add comment
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, str), "first_name must be a string"
        self.customer.first_name = value
    def set_prop_first_name(self, value: str):
        """
        #TODO add comment
        """
        self.first_name = value
        return self
    # forgotPasswordKeyExpirationUTCDateTime
    @property
    def forgot_password_key_expiration_utc_date_time(self):
        """
        #TODO add comment
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.customer.forgot_password_key_expiration_utc_date_time
    @forgot_password_key_expiration_utc_date_time.setter
    def forgot_password_key_expiration_utc_date_time(self, value):
        """
        #TODO add comment
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, datetime), (
            "forgot_password_key_expiration_utc_date_time must be a datetime object")
        self.customer.forgot_password_key_expiration_utc_date_time = value
    def set_prop_forgot_password_key_expiration_utc_date_time(self, value: datetime):
        """
        #TODO add comment
        """
        self.forgot_password_key_expiration_utc_date_time = value
        return self
    # forgotPasswordKeyValue
    @property
    def forgot_password_key_value(self):
        """
        #TODO add comment
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if self.customer.forgot_password_key_value is None:
            return ""
        return self.customer.forgot_password_key_value
    @forgot_password_key_value.setter
    def forgot_password_key_value(self, value):
        """
        #TODO add comment
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, str), "forgot_password_key_value must be a string"
        self.customer.forgot_password_key_value = value
    def set_prop_forgot_password_key_value(self, value: str):
        """
        #TODO add comment
        """
        self.forgot_password_key_value = value
        return self
    # fSUserCodeValue
    @property
    def fs_user_code_value(self):
        """
        #TODO add comment
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.customer.fs_user_code_value
    @fs_user_code_value.setter
    def fs_user_code_value(self, value):
        """
        #TODO add comment
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, uuid.UUID), (
            "fs_user_code_value must be a UUID")
        self.customer.fs_user_code_value = value
    def set_prop_fs_user_code_value(self, value: uuid.UUID):
        """
        #TODO add comment
        """
        self.fs_user_code_value = value
        return self
    # isActive
    @property
    def is_active(self):
        """
        #TODO add comment
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.customer.is_active
    @is_active.setter
    def is_active(self, value: bool):
        """
        #TODO add comment
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if not isinstance(value, bool):
            raise ValueError("is_active must be a boolean.")
        self.customer.is_active = value
    def set_prop_is_active(self, value: bool):
        """
        #TODO add comment
        """
        self.is_active = value
        return self
    # isEmailAllowed
    @property
    def is_email_allowed(self):
        """
        #TODO add comment
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.customer.is_email_allowed
    @is_email_allowed.setter
    def is_email_allowed(self, value: bool):
        """
        #TODO add comment
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if not isinstance(value, bool):
            raise ValueError("is_email_allowed must be a boolean.")
        self.customer.is_email_allowed = value
    def set_prop_is_email_allowed(self, value: bool):
        """
        #TODO add comment
        """
        self.is_email_allowed = value
        return self
    # isEmailConfirmed
    @property
    def is_email_confirmed(self):
        """
        #TODO add comment
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.customer.is_email_confirmed
    @is_email_confirmed.setter
    def is_email_confirmed(self, value: bool):
        """
        #TODO add comment
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if not isinstance(value, bool):
            raise ValueError("is_email_confirmed must be a boolean.")
        self.customer.is_email_confirmed = value
    def set_prop_is_email_confirmed(self, value: bool):
        """
        #TODO add comment
        """
        self.is_email_confirmed = value
        return self
    # isEmailMarketingAllowed
    @property
    def is_email_marketing_allowed(self):
        """
        #TODO add comment
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.customer.is_email_marketing_allowed
    @is_email_marketing_allowed.setter
    def is_email_marketing_allowed(self, value: bool):
        """
        #TODO add comment
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if not isinstance(value, bool):
            raise ValueError("is_email_marketing_allowed must be a boolean.")
        self.customer.is_email_marketing_allowed = value
    def set_prop_is_email_marketing_allowed(self, value: bool):
        """
        #TODO add comment
        """
        self.is_email_marketing_allowed = value
        return self
    # isLocked
    @property
    def is_locked(self):
        """
        #TODO add comment
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.customer.is_locked
    @is_locked.setter
    def is_locked(self, value: bool):
        """
        #TODO add comment
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if not isinstance(value, bool):
            raise ValueError("is_locked must be a boolean.")
        self.customer.is_locked = value
    def set_prop_is_locked(self, value: bool):
        """
        #TODO add comment
        """
        self.is_locked = value
        return self
    # isMultipleOrganizationsAllowed
    @property
    def is_multiple_organizations_allowed(self):
        """
        #TODO add comment
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.customer.is_multiple_organizations_allowed
    @is_multiple_organizations_allowed.setter
    def is_multiple_organizations_allowed(self, value: bool):
        """
        #TODO add comment
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if not isinstance(value, bool):
            raise ValueError("is_multiple_organizations_allowed must be a boolean.")
        self.customer.is_multiple_organizations_allowed = value
    def set_prop_is_multiple_organizations_allowed(self, value: bool):
        """
        #TODO add comment
        """
        self.is_multiple_organizations_allowed = value
        return self
    # isVerboseLoggingForced
    @property
    def is_verbose_logging_forced(self):
        """
        #TODO add comment
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.customer.is_verbose_logging_forced
    @is_verbose_logging_forced.setter
    def is_verbose_logging_forced(self, value: bool):
        """
        #TODO add comment
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if not isinstance(value, bool):
            raise ValueError("is_verbose_logging_forced must be a boolean.")
        self.customer.is_verbose_logging_forced = value
    def set_prop_is_verbose_logging_forced(self, value: bool):
        """
        #TODO add comment
        """
        self.is_verbose_logging_forced = value
        return self
    # lastLoginUTCDateTime
    @property
    def last_login_utc_date_time(self):
        """
        #TODO add comment
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.customer.last_login_utc_date_time
    @last_login_utc_date_time.setter
    def last_login_utc_date_time(self, value):
        """
        #TODO add comment
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, datetime), (
            "last_login_utc_date_time must be a datetime object")
        self.customer.last_login_utc_date_time = value
    def set_prop_last_login_utc_date_time(self, value: datetime):
        """
        #TODO add comment
        """
        self.last_login_utc_date_time = value
        return self
    # lastName
    @property
    def last_name(self):
        """
        #TODO add comment
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if self.customer.last_name is None:
            return ""
        return self.customer.last_name
    @last_name.setter
    def last_name(self, value):
        """
        #TODO add comment
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, str), "last_name must be a string"
        self.customer.last_name = value
    def set_prop_last_name(self, value: str):
        """
        #TODO add comment
        """
        self.last_name = value
        return self
    # password
    @property
    def password(self):
        """
        #TODO add comment
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if self.customer.password is None:
            return ""
        return self.customer.password
    @password.setter
    def password(self, value):
        """
        #TODO add comment
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, str), "password must be a string"
        self.customer.password = value
    def set_prop_password(self, value: str):
        """
        #TODO add comment
        """
        self.password = value
        return self
    # phone
    @property
    def phone(self):
        """
        #TODO add comment
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if self.customer.phone is None:
            return ""
        return self.customer.phone
    @phone.setter
    def phone(self, value):
        """
        #TODO add comment
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, str), (
            "phone must be a string")
        self.customer.phone = value
    def set_prop_phone(self, value: str):
        """
        #TODO add comment
        """
        self.phone = value
        return self
    # province
    @property
    def province(self):
        """
        #TODO add comment
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if self.customer.province is None:
            return ""
        return self.customer.province
    @province.setter
    def province(self, value):
        """
        #TODO add comment
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, str), "province must be a string"
        self.customer.province = value
    def set_prop_province(self, value: str):
        """
        #TODO add comment
        """
        self.province = value
        return self
    # registrationUTCDateTime
    @property
    def registration_utc_date_time(self):
        """
        #TODO add comment
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.customer.registration_utc_date_time
    @registration_utc_date_time.setter
    def registration_utc_date_time(self, value):
        """
        #TODO add comment
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, datetime), (
            "registration_utc_date_time must be a datetime object")
        self.customer.registration_utc_date_time = value
    def set_prop_registration_utc_date_time(self, value: datetime):
        """
        #TODO add comment
        """
        self.registration_utc_date_time = value
        return self
    # TacID
    # uTCOffsetInMinutes
    @property
    def utc_offset_in_minutes(self):
        """
        #TODO add comment
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.customer.utc_offset_in_minutes
    @utc_offset_in_minutes.setter
    def utc_offset_in_minutes(self, value):
        """
        #TODO add comment
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, int), (
            "utc_offset_in_minutes must be an integer")
        self.customer.utc_offset_in_minutes = value
    def set_prop_utc_offset_in_minutes(self, value: int):
        """
        #TODO add comment
        """
        self.utc_offset_in_minutes = value
        return self
    # zip
    @property
    def zip(self):
        """
        #TODO add comment
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if self.customer.zip is None:
            return ""
        return self.customer.zip
    @zip.setter
    def zip(self, value):
        """
        #TODO add comment
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, str), "zip must be a string"
        self.customer.zip = value
    def set_prop_zip(self, value: str):
        """
        #TODO add comment
        """
        self.zip = value
        return self
# endset
    # activeOrganizationID,
    # email,
    # emailConfirmedUTCDateTime
    # firstName,
    # forgotPasswordKeyExpirationUTCDateTime
    # forgotPasswordKeyValue,
    # fSUserCodeValue,
    # isActive,
    # isEmailAllowed,
    # isEmailConfirmed,
    # isEmailMarketingAllowed,
    # isLocked,
    # isMultipleOrganizationsAllowed,
    # isVerboseLoggingForced,
    # lastLoginUTCDateTime
    # lastName,
    # password,
    # phone,
    # province,
    # registrationUTCDateTime
    # TacID
    @property
    def tac_id(self):
        """
        #TODO add comment
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.customer.tac_id
    @tac_id.setter
    def tac_id(self, value):
        """
        #TODO add comment
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, int) or value is None, (
            "tac_id must be an integer or None")
        self.customer.tac_id = value
    def set_prop_tac_id(self, value: int):
        """
        #TODO add comment
        """
        self.tac_id = value
        return self
    @property
    def tac_code_peek(self):
        """
        #TODO add comment
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.customer.tac_code_peek
    # @tac_code_peek.setter
    # def tac_code_peek(self, value):
    #     assert isinstance(value, uuid.UUID),
    #           "tac_code_peek must be a UUID"
    #     self.customer.tac_code_peek = value
    # uTCOffsetInMinutes,
    # zip,
# endset
    # insert_utc_date_time
    @property
    def insert_utc_date_time(self):
        """
        #TODO add comment
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.customer.insert_utc_date_time
    @insert_utc_date_time.setter
    def insert_utc_date_time(self, value):
        """
        #TODO add comment
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, datetime) or value is None, (
            "insert_utc_date_time must be a datetime object or None")
        self.customer.insert_utc_date_time = value
    # update_utc_date_time
    @property
    def last_update_utc_date_time(self):
        """
        #TODO add comment
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.customer.last_update_utc_date_time
    @last_update_utc_date_time.setter
    def last_update_utc_date_time(self, value):
        """
        #TODO add comment
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        assert isinstance(value, datetime) or value is None, (
            "last_update_utc_date_time must be a datetime object or None")
        self.customer.last_update_utc_date_time = value
    async def load_from_json(
        self,
        json_data: str
    ):
        """
        Load customer data from JSON string.
        :param json_data: JSON string containing customer data.
        :raises ValueError: If json_data is not a string
            or if no customer data is found.
        """
        if not isinstance(json_data, str):
            raise ValueError("json_data must be a string")
        customer_manager = CustomerManager(self._session_context)
        self.customer = customer_manager.from_json(json_data)
        return self
    async def load_from_code(
        self,
        code: uuid.UUID
    ):
        """
        Load customer data from UUID code.
        :param code: UUID code for loading a specific customer.
        :raises ValueError: If code is not a UUID or if no customer data is found.
        """
        if not isinstance(code, uuid.UUID):
            raise ValueError("code must be a UUID")
        customer_manager = CustomerManager(self._session_context)
        customer_obj = await customer_manager.get_by_code(code)
        self.customer = customer_obj
        return self
    async def load_from_id(
        self,
        customer_id: int
    ):
        """
        Load customer data from customer ID.
        :param customer_id: Integer ID for loading a specific customer.
        :raises ValueError: If customer_id is not an integer or
            if no customer data is found.
        """
        if not isinstance(customer_id, int):
            raise ValueError("customer_id must be an integer")
        customer_manager = CustomerManager(self._session_context)
        customer_obj = await customer_manager.get_by_id(customer_id)
        self.customer = customer_obj
        return self
    async def load_from_obj_instance(
        self,
        customer_obj_instance: Customer
    ):
        """
        Use the provided Customer instance.
        :param customer_obj_instance: Instance of the Customer class.
        :raises ValueError: If customer_obj_instance is not an instance of Customer.
        """
        if not isinstance(customer_obj_instance, Customer):
            raise ValueError("customer_obj_instance must be an instance of Customer")
        customer_manager = CustomerManager(self._session_context)
        customer_obj_instance_customer_id = customer_obj_instance.customer_id
        customer_obj = await customer_manager.get_by_id(
            customer_obj_instance_customer_id
        )
        self.customer = customer_obj
        return self
    async def load_from_dict(
        self,
        customer_dict: dict
    ):
        """
        Load customer data from dictionary.
        :param customer_dict: Dictionary containing customer data.
        :raises ValueError: If customer_dict is not a
            dictionary or if no customer data is found.
        """
        if not isinstance(customer_dict, dict):
            raise ValueError("customer_dict must be a dictionary")
        customer_manager = CustomerManager(self._session_context)
        self.customer = customer_manager.from_dict(customer_dict)
        return self

    def get_session_context(self):
        """
        #TODO add comment
        """
        return self._session_context
    async def refresh(self):
        """
        #TODO add comment
        """
        customer_manager = CustomerManager(self._session_context)
        self.customer = await customer_manager.refresh(self.customer)
        return self
    def is_valid(self):
        """
        #TODO add comment
        """
        return self.customer is not None
    def to_dict(self):
        """
        #TODO add comment
        """
        customer_manager = CustomerManager(self._session_context)
        return customer_manager.to_dict(self.customer)
    def to_json(self):
        """
        #TODO add comment
        """
        customer_manager = CustomerManager(self._session_context)
        return customer_manager.to_json(self.customer)
    async def save(self):
        """
        #TODO add comment
        """
        if not self.customer:
            raise AttributeError(NOT_INITIALIZED_ERROR_MESSAGE)
        if self.customer.customer_id > 0:
            customer_manager = CustomerManager(self._session_context)
            self.customer = await customer_manager.update(self.customer)
        if self.customer.customer_id == 0:
            customer_manager = CustomerManager(self._session_context)
            self.customer = await customer_manager.add(self.customer)
        return self
    async def delete(self):
        """
        #TODO add comment
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        if self.customer.customer_id > 0:
            customer_manager = CustomerManager(self._session_context)
            await customer_manager.delete(self.customer.customer_id)
            self.customer = None
    async def randomize_properties(self):
        """
        #TODO add comment
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        self.customer.active_organization_id = random.randint(0, 100)
        self.customer.email = f"user{random.randint(1, 100)}@abc.com"
        self.customer.email_confirmed_utc_date_time = datetime(
            random.randint(2000, 2023),
            random.randint(1, 12),
            random.randint(1, 28))
        self.customer.first_name = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        self.customer.forgot_password_key_expiration_utc_date_time = datetime(
            random.randint(2000, 2023),
            random.randint(1, 12),
            random.randint(1, 28))
        self.customer.forgot_password_key_value = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        self.customer.fs_user_code_value = uuid.uuid4()
        self.customer.is_active = random.choice([True, False])
        self.customer.is_email_allowed = random.choice([True, False])
        self.customer.is_email_confirmed = random.choice([True, False])
        self.customer.is_email_marketing_allowed = random.choice([True, False])
        self.customer.is_locked = random.choice([True, False])
        self.customer.is_multiple_organizations_allowed = random.choice([True, False])
        self.customer.is_verbose_logging_forced = random.choice([True, False])
        self.customer.last_login_utc_date_time = datetime(
            random.randint(2000, 2023),
            random.randint(1, 12),
            random.randint(1, 28))
        self.customer.last_name = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        self.customer.password = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        self.customer.phone = (
            f"+1{random.randint(1000000000, 9999999999)}")
        self.customer.province = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        self.customer.registration_utc_date_time = datetime(
            random.randint(2000, 2023),
            random.randint(1, 12),
            random.randint(1, 28))
        # self.customer.tac_id = random.randint(0, 100)
        self.customer.utc_offset_in_minutes = random.randint(0, 100)
        self.customer.zip = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
# endset
        return self
    def get_customer_obj(self) -> Customer:
        """
        #TODO add comment
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return self.customer
    def is_equal(self, customer: Customer) -> bool:
        """
        #TODO add comment
        """
        customer_manager = CustomerManager(self._session_context)
        my_customer = self.get_customer_obj()
        return customer_manager.is_equal(customer, my_customer)
# endset
    # activeOrganizationID,
    # email,
    # emailConfirmedUTCDateTime
    # firstName,
    # forgotPasswordKeyExpirationUTCDateTime
    # forgotPasswordKeyValue,
    # fSUserCodeValue,
    # isActive,
    # isEmailAllowed,
    # isEmailConfirmed,
    # isEmailMarketingAllowed,
    # isLocked,
    # isMultipleOrganizationsAllowed,
    # isVerboseLoggingForced,
    # lastLoginUTCDateTime
    # lastName,
    # password,
    # phone,
    # province,
    # registrationUTCDateTime
    # TacID
    async def get_tac_id_rel_obj(self) -> models.Tac:
        """
        #TODO add comment
        """
        tac_manager = managers_and_enums.TacManager(self._session_context)
        tac_obj = await tac_manager.get_by_id(self.tac_id)
        return tac_obj
    # uTCOffsetInMinutes,
    # zip,
# endset
    def get_obj(self) -> Customer:
        """
        #TODO add comment
        """
        return self.customer
    def get_object_name(self) -> str:
        """
        #TODO add comment
        """
        return "customer"
    def get_id(self) -> int:
        """
        #TODO add comment
        """
        return self.customer_id
    # activeOrganizationID,
    # email,
    # emailConfirmedUTCDateTime
    # firstName,
    # forgotPasswordKeyExpirationUTCDateTime
    # forgotPasswordKeyValue,
    # fSUserCodeValue,
    # isActive,
    # isEmailAllowed,
    # isEmailConfirmed,
    # isEmailMarketingAllowed,
    # isLocked,
    # isMultipleOrganizationsAllowed,
    # isVerboseLoggingForced,
    # lastLoginUTCDateTime
    # lastName,
    # password,
    # phone,
    # province,
    # registrationUTCDateTime
    # TacID
    async def get_parent_name(self) -> str:
        """
        #TODO add comment
        """
        return 'Tac'
    async def get_parent_code(self) -> uuid.UUID:
        """
        #TODO add comment
        """
        return self.tac_code_peek
    async def get_parent_obj(self) -> models.Tac:
        """
        #TODO add comment
        """
        return self.get_tac_id_rel_obj()
    # uTCOffsetInMinutes,
    # zip,
# endset
    @staticmethod
    async def to_bus_obj_list(
        session_context: SessionContext,
        obj_list: List[Customer]
    ):
        """
        #TODO add comment
        """
        result = list()
        for customer in obj_list:
            customer_bus_obj = CustomerBusObj(session_context)
            await customer_bus_obj.load_from_obj_instance(customer)
            result.append(customer_bus_obj)
        return result

    async def build_customer_role(self) -> CustomerRoleBusObj:
        item = CustomerRoleBusObj(self._session_context)
        role_manager = managers_and_enums.RoleManager(self._session_context)
        role_id_role = await role_manager.from_enum(
            managers_and_enums.RoleEnum.Unknown)
        item.role_id = role_id_role.role_id
        item.customer_role.role_id_code_peek = role_id_role.code

        item.customer_id = self.customer_id
        item.customer_role.customer_code_peek = self.code

        return item

    async def get_all_customer_role(self) -> List[CustomerRoleBusObj]:
        results = list()
        customer_role_manager = managers_and_enums.CustomerRoleManager(self._session_context)
        obj_list = await customer_role_manager.get_by_customer_id(self.customer_id)
        for obj_item in obj_list:
            bus_obj_item = CustomerRoleBusObj(self._session_context)
            await bus_obj_item.load_from_obj_instance(obj_item)
            results.append(bus_obj_item)
        return results

