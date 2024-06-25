# business/customer_base.py

"""
This module contains the CustomerBaseBusObj class,
which represents the base business object for a Customer.
"""

from decimal import Decimal
import random
from typing import Optional
import uuid
from datetime import datetime, date
from helpers.session_context import SessionContext
from managers import CustomerManager
from models import Customer
import models
import managers as managers_and_enums
from .base_bus_obj import BaseBusObj

NOT_INITIALIZED_ERROR_MESSAGE = (
    "Customer object is not initialized")


class CustomerInvalidInitError(Exception):
    """
    Exception raised when the
    Customer object
    is not initialized properly.
    """


class CustomerBaseBusObj(BaseBusObj):
    """
    This class represents the base business object
    for a Customer.
    It requires a valid session context for initialization.
    """

    def __init__(
        self,
        session_context: SessionContext,
        customer: Optional[Customer] = None
    ):
        """
        Initializes a new instance of the
        CustomerBusObj class.

        :param session_context: The session context.
        :raises ValueError: If the session is not provided.
        """

        if not session_context.session:
            raise ValueError("session required")

        if customer is None:
            customer = Customer()

        self._session_context = session_context

        self.customer = customer

    @property
    def customer_id(self) -> int:
        """
        Get the customer ID from the
        Customer object.

        :return: The customer ID.
        :raises AttributeError: If the
            Customer object is not initialized.
        """

        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.customer.customer_id

    # code
    @property
    def code(self):
        """
        Get the code from the
        Customer object.

        :return: The code.
        :raises AttributeError: If the
            Customer object is not initialized.
        """

        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.customer.code

    @code.setter
    def code(self, value: uuid.UUID):  # type: ignore
        """
        Set the code for the Customer object.

        :param value: The code value.
        :raises AttributeError: If the
            Customer object is not initialized.
        :raises ValueError: If the code is not a UUID.
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
        Get the last change code from the
        Customer object.

        :return: The last change code.
        :raises AttributeError: If the
            Customer object is not initialized.
        """

        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.customer.last_change_code

    @last_change_code.setter
    def last_change_code(self, value: int):
        """
        Set the last change code for the
        Customer object.

        :param value: The last change code value.
        :raises AttributeError: If the
            Customer object is not initialized.
        :raises ValueError: If the last change code is not an integer.
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
        Get the insert user ID from the
        Customer object.

        :return: The insert user ID.
        :raises AttributeError: If the
            Customer object is not initialized.
        """

        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.customer.insert_user_id

    @insert_user_id.setter
    def insert_user_id(self, value: uuid.UUID):
        """
        Set the insert user ID for the
        Customer object.

        :param value: The insert user ID value.
        :raises AttributeError: If the
            Customer object is not initialized.
        :raises ValueError: If the insert user ID is not a UUID.
        """

        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, uuid.UUID):
            raise ValueError("insert_user_id must be a UUID.")

        self.customer.insert_user_id = value

    # last_update_user_id
    @property
    def last_update_user_id(self):
        """
        Get the last update user ID from the
        Customer object.

        :return: The last update user ID.
        :raises AttributeError: If the
            Customer object is not initialized.
        """

        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.customer.last_update_user_id

    @last_update_user_id.setter
    def last_update_user_id(self, value: uuid.UUID):
        """
        Set the last update user ID for the
        Customer object.

        :param value: The last update user ID value.
        :raises AttributeError: If the
            Customer object is not initialized.
        :raises ValueError: If the last update user ID is not a UUID.
        """

        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, uuid.UUID):
            raise ValueError("last_update_user_id must be a UUID.")

        self.customer.last_update_user_id = value

    # activeOrganizationID

    @property
    def active_organization_id(self):
        """
        Returns the value of
        active_organization_id attribute of the
        customer.

        Raises:
            AttributeError: If the
                customer is not initialized.

        Returns:
            int: The value of
                active_organization_id attribute.
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.customer.active_organization_id

    @active_organization_id.setter
    def active_organization_id(self, value):
        """
        Sets the value of
        active_organization_id for the
        customer.

        Args:
            value (int): The integer value to set for
                active_organization_id.

        Raises:
            AttributeError: If the
                customer is not initialized.

        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, int), (
            "active_organization_id must be an integer")
        self.customer.active_organization_id = value
    # email

    @property
    def email(self):
        """
        Returns the Email
        associated with the customer.

        :return: The Email
            of the customer.
        :rtype: str
        :raises AttributeError: If the
            customer is not initialized.
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
        Sets the Email
        for the customer.

        Args:
            value (str): The Email
                to be set.

        Raises:
            AttributeError: If the
                customer is not initialized.

        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, str), (
            "email must be a string")
        self.customer.email = value
    # emailConfirmedUTCDateTime

    @property
    def email_confirmed_utc_date_time(self):
        """
        Returns the value of
        email_confirmed_utc_date_time attribute of the
        customer.

        Raises:
            AttributeError: If the
                customer is not initialized.

        Returns:
            The value of
            email_confirmed_utc_date_time
            attribute.
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.customer.email_confirmed_utc_date_time

    @email_confirmed_utc_date_time.setter
    def email_confirmed_utc_date_time(self, value):
        """
        Sets the value of
        email_confirmed_utc_date_time attribute
        for the customer.

        Args:
            value (datetime): The datetime value to be set.

        Raises:
            AttributeError: If the
                customer is not initialized.

        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, datetime), (
            "email_confirmed_utc_date_time must be a datetime object")
        self.customer.email_confirmed_utc_date_time = value
    # firstName

    @property
    def first_name(self):
        """
        Get the First Name from the
        Customer object.

        :return: The First Name.
        :raises AttributeError: If the
            Customer object is not initialized.
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
        Set the First Name for the
        Customer object.

        :param value: The First Name value.
        :raises AttributeError: If the
            Customer object is not initialized.
        :raises AssertionError: If the First Name is not a string.
        """

        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, str), "first_name must be a string"
        self.customer.first_name = value
    # forgotPasswordKeyExpirationUTCDateTime

    @property
    def forgot_password_key_expiration_utc_date_time(self):
        """
        Returns the value of
        forgot_password_key_expiration_utc_date_time attribute of the
        customer.

        Raises:
            AttributeError: If the
                customer is not initialized.

        Returns:
            The value of
            forgot_password_key_expiration_utc_date_time
            attribute.
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.customer.forgot_password_key_expiration_utc_date_time

    @forgot_password_key_expiration_utc_date_time.setter
    def forgot_password_key_expiration_utc_date_time(self, value):
        """
        Sets the value of
        forgot_password_key_expiration_utc_date_time attribute
        for the customer.

        Args:
            value (datetime): The datetime value to be set.

        Raises:
            AttributeError: If the
                customer is not initialized.

        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, datetime), (
            "forgot_password_key_expiration_utc_date_time must be a datetime object")
        self.customer.forgot_password_key_expiration_utc_date_time = value
    # forgotPasswordKeyValue

    @property
    def forgot_password_key_value(self):
        """
        Get the Forgot Password Key Value from the
        Customer object.

        :return: The Forgot Password Key Value.
        :raises AttributeError: If the
            Customer object is not initialized.
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
        Set the Forgot Password Key Value for the
        Customer object.

        :param value: The Forgot Password Key Value value.
        :raises AttributeError: If the
            Customer object is not initialized.
        :raises AssertionError: If the Forgot Password Key Value is not a string.
        """

        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, str), "forgot_password_key_value must be a string"
        self.customer.forgot_password_key_value = value
    # fSUserCodeValue

    @property
    def fs_user_code_value(self):
        """
        Returns the value of the
        some unique identifier for the
        customer.

        Raises:
            AttributeError: If the
                customer is not initialized.

        Returns:
            The value of the some unique identifier for the
            customer.
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.customer.fs_user_code_value

    @fs_user_code_value.setter
    def fs_user_code_value(self, value):
        """
        Sets the value of the
        'fs_user_code_value'
        attribute for the
        customer.

        Args:
            value (uuid.UUID): The UUID value to set for
                'fs_user_code_value'.

        Raises:
            AttributeError: If the
                customer is not initialized.

        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, uuid.UUID), (
            "fs_user_code_value must be a UUID")
        self.customer.fs_user_code_value = value
    # isActive

    @property
    def is_active(self):
        """
        Get the Is Active flag from the
        Customer object.

        :return: The Is Active flag.
        :raises AttributeError: If the
            Customer object is not initialized.
        """

        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.customer.is_active

    @is_active.setter
    def is_active(self, value: bool):
        """
        Set the Is Active flag for the
        Customer object.

        :param value: The Is Active flag value.
        :raises AttributeError: If the
            Customer object is not initialized.
        :raises ValueError: If the Is Active flag is not a boolean.
        """

        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, bool):
            raise ValueError("is_active must be a boolean.")

        self.customer.is_active = value
    # isEmailAllowed

    @property
    def is_email_allowed(self):
        """
        Get the Is Email Allowed flag from the
        Customer object.

        :return: The Is Email Allowed flag.
        :raises AttributeError: If the
            Customer object is not initialized.
        """

        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.customer.is_email_allowed

    @is_email_allowed.setter
    def is_email_allowed(self, value: bool):
        """
        Set the Is Email Allowed flag for the
        Customer object.

        :param value: The Is Email Allowed flag value.
        :raises AttributeError: If the
            Customer object is not initialized.
        :raises ValueError: If the Is Email Allowed flag is not a boolean.
        """

        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, bool):
            raise ValueError("is_email_allowed must be a boolean.")

        self.customer.is_email_allowed = value
    # isEmailConfirmed

    @property
    def is_email_confirmed(self):
        """
        Get the Is Email Confirmed flag from the
        Customer object.

        :return: The Is Email Confirmed flag.
        :raises AttributeError: If the
            Customer object is not initialized.
        """

        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.customer.is_email_confirmed

    @is_email_confirmed.setter
    def is_email_confirmed(self, value: bool):
        """
        Set the Is Email Confirmed flag for the
        Customer object.

        :param value: The Is Email Confirmed flag value.
        :raises AttributeError: If the
            Customer object is not initialized.
        :raises ValueError: If the Is Email Confirmed flag is not a boolean.
        """

        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, bool):
            raise ValueError("is_email_confirmed must be a boolean.")

        self.customer.is_email_confirmed = value
    # isEmailMarketingAllowed

    @property
    def is_email_marketing_allowed(self):
        """
        Get the Is Email Marketing Allowed flag from the
        Customer object.

        :return: The Is Email Marketing Allowed flag.
        :raises AttributeError: If the
            Customer object is not initialized.
        """

        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.customer.is_email_marketing_allowed

    @is_email_marketing_allowed.setter
    def is_email_marketing_allowed(self, value: bool):
        """
        Set the Is Email Marketing Allowed flag for the
        Customer object.

        :param value: The Is Email Marketing Allowed flag value.
        :raises AttributeError: If the
            Customer object is not initialized.
        :raises ValueError: If the Is Email Marketing Allowed flag is not a boolean.
        """

        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, bool):
            raise ValueError("is_email_marketing_allowed must be a boolean.")

        self.customer.is_email_marketing_allowed = value
    # isLocked

    @property
    def is_locked(self):
        """
        Get the Is Locked flag from the
        Customer object.

        :return: The Is Locked flag.
        :raises AttributeError: If the
            Customer object is not initialized.
        """

        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.customer.is_locked

    @is_locked.setter
    def is_locked(self, value: bool):
        """
        Set the Is Locked flag for the
        Customer object.

        :param value: The Is Locked flag value.
        :raises AttributeError: If the
            Customer object is not initialized.
        :raises ValueError: If the Is Locked flag is not a boolean.
        """

        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, bool):
            raise ValueError("is_locked must be a boolean.")

        self.customer.is_locked = value
    # isMultipleOrganizationsAllowed

    @property
    def is_multiple_organizations_allowed(self):
        """
        Get the Is Multiple Organizations Allowed flag from the
        Customer object.

        :return: The Is Multiple Organizations Allowed flag.
        :raises AttributeError: If the
            Customer object is not initialized.
        """

        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.customer.is_multiple_organizations_allowed

    @is_multiple_organizations_allowed.setter
    def is_multiple_organizations_allowed(self, value: bool):
        """
        Set the Is Multiple Organizations Allowed flag for the
        Customer object.

        :param value: The Is Multiple Organizations Allowed flag value.
        :raises AttributeError: If the
            Customer object is not initialized.
        :raises ValueError: If the Is Multiple Organizations Allowed flag is not a boolean.
        """

        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, bool):
            raise ValueError("is_multiple_organizations_allowed must be a boolean.")

        self.customer.is_multiple_organizations_allowed = value
    # isVerboseLoggingForced

    @property
    def is_verbose_logging_forced(self):
        """
        Get the Is Verbose Logging Forced flag from the
        Customer object.

        :return: The Is Verbose Logging Forced flag.
        :raises AttributeError: If the
            Customer object is not initialized.
        """

        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.customer.is_verbose_logging_forced

    @is_verbose_logging_forced.setter
    def is_verbose_logging_forced(self, value: bool):
        """
        Set the Is Verbose Logging Forced flag for the
        Customer object.

        :param value: The Is Verbose Logging Forced flag value.
        :raises AttributeError: If the
            Customer object is not initialized.
        :raises ValueError: If the Is Verbose Logging Forced flag is not a boolean.
        """

        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, bool):
            raise ValueError("is_verbose_logging_forced must be a boolean.")

        self.customer.is_verbose_logging_forced = value
    # lastLoginUTCDateTime

    @property
    def last_login_utc_date_time(self):
        """
        Returns the value of
        last_login_utc_date_time attribute of the
        customer.

        Raises:
            AttributeError: If the
                customer is not initialized.

        Returns:
            The value of
            last_login_utc_date_time
            attribute.
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.customer.last_login_utc_date_time

    @last_login_utc_date_time.setter
    def last_login_utc_date_time(self, value):
        """
        Sets the value of
        last_login_utc_date_time attribute
        for the customer.

        Args:
            value (datetime): The datetime value to be set.

        Raises:
            AttributeError: If the
                customer is not initialized.

        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, datetime), (
            "last_login_utc_date_time must be a datetime object")
        self.customer.last_login_utc_date_time = value
    # lastName

    @property
    def last_name(self):
        """
        Get the Last Name from the
        Customer object.

        :return: The Last Name.
        :raises AttributeError: If the
            Customer object is not initialized.
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
        Set the Last Name for the
        Customer object.

        :param value: The Last Name value.
        :raises AttributeError: If the
            Customer object is not initialized.
        :raises AssertionError: If the Last Name is not a string.
        """

        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, str), "last_name must be a string"
        self.customer.last_name = value
    # password

    @property
    def password(self):
        """
        Get the Password from the
        Customer object.

        :return: The Password.
        :raises AttributeError: If the
            Customer object is not initialized.
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
        Set the Password for the
        Customer object.

        :param value: The Password value.
        :raises AttributeError: If the
            Customer object is not initialized.
        :raises AssertionError: If the Password is not a string.
        """

        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, str), "password must be a string"
        self.customer.password = value
    # phone

    @property
    def phone(self):
        """
        Returns the Phone
        associated with the
        customer.

        If the customer is not initialized,
        an AttributeError is raised.
        If the Phone is None,
        an empty string is returned.

        Returns:
            str: The Phone
                associated with the
                customer,
                or an empty string if it is None.

        Raises:
            AttributeError: If the
                customer is not initialized.
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
        Sets the Phone
        for the customer.

        Args:
            value (str): The
                Phone
                to set.

        Raises:
            AttributeError: If the
            customer is not initialized.

        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, str), (
            "phone must be a string")
        self.customer.phone = value
    # province

    @property
    def province(self):
        """
        Get the Province from the
        Customer object.

        :return: The Province.
        :raises AttributeError: If the
            Customer object is not initialized.
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
        Set the Province for the
        Customer object.

        :param value: The Province value.
        :raises AttributeError: If the
            Customer object is not initialized.
        :raises AssertionError: If the Province is not a string.
        """

        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, str), "province must be a string"
        self.customer.province = value
    # registrationUTCDateTime

    @property
    def registration_utc_date_time(self):
        """
        Returns the value of
        registration_utc_date_time attribute of the
        customer.

        Raises:
            AttributeError: If the
                customer is not initialized.

        Returns:
            The value of
            registration_utc_date_time
            attribute.
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.customer.registration_utc_date_time

    @registration_utc_date_time.setter
    def registration_utc_date_time(self, value):
        """
        Sets the value of
        registration_utc_date_time attribute
        for the customer.

        Args:
            value (datetime): The datetime value to be set.

        Raises:
            AttributeError: If the
                customer is not initialized.

        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, datetime), (
            "registration_utc_date_time must be a datetime object")
        self.customer.registration_utc_date_time = value
    # TacID
    # uTCOffsetInMinutes

    @property
    def utc_offset_in_minutes(self):
        """
        Returns the value of
        utc_offset_in_minutes attribute of the
        customer.

        Raises:
            AttributeError: If the
                customer is not initialized.

        Returns:
            int: The value of
                utc_offset_in_minutes attribute.
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.customer.utc_offset_in_minutes

    @utc_offset_in_minutes.setter
    def utc_offset_in_minutes(self, value):
        """
        Sets the value of
        utc_offset_in_minutes for the
        customer.

        Args:
            value (int): The integer value to set for
                utc_offset_in_minutes.

        Raises:
            AttributeError: If the
                customer is not initialized.

        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, int), (
            "utc_offset_in_minutes must be an integer")
        self.customer.utc_offset_in_minutes = value
    # zip

    @property
    def zip(self):
        """
        Get the Zip from the
        Customer object.

        :return: The Zip.
        :raises AttributeError: If the
            Customer object is not initialized.
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
        Set the Zip for the
        Customer object.

        :param value: The Zip value.
        :raises AttributeError: If the
            Customer object is not initialized.
        :raises AssertionError: If the Zip is not a string.
        """

        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, str), "zip must be a string"
        self.customer.zip = value
    # isDeleteAllowed,
    # isEditAllowed,
    # otherFlavor,
    # someBigIntVal,
    # someBitVal,
    # someDecimalVal,
    # someEmailAddress,
    # someFloatVal,
    # someIntVal,
    # someMoneyVal,
    # someNVarCharVal,
    # someDateVal
    # someUTCDateTimeVal
    # TacID
    @property
    def tac_id(self):
        """
        Returns the tac ID
        associated with the
        customer.

        Raises:
            AttributeError: If the
                customer is not initialized.

        Returns:
            int: The tac ID of the customer.
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.customer.tac_id

    @tac_id.setter
    def tac_id(self, value):
        """
        Sets the tac ID
        for the customer.

        Args:
            value (int or None): The
                tac ID to be set.
                Must be an integer or None.

        Raises:
            AttributeError: If the
                customer is not initialized.

        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, int) or value is None, (
            "tac_id must be an integer or None")

        self.customer.tac_id = value

    @property
    def tac_code_peek(self) -> uuid.UUID:
        """
        Returns the tac id code peek
        of the customer.

        Raises:
            AttributeError: If the
            customer is not initialized.

        Returns:
            uuid.UUID: The tac id code peek
            of the customer.
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.customer.tac_code_peek
    # insert_utc_date_time

    @property
    def insert_utc_date_time(self):
        """
        Inserts the UTC date and time into
        the customer object.

        Raises:
            AttributeError: If the
                customer object is not initialized.

        Returns:
            The UTC date and time inserted into the
            customer object.
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.customer.insert_utc_date_time

    @insert_utc_date_time.setter
    def insert_utc_date_time(self, value):
        """
        Inserts the UTC date and time for the
        customer.

        Args:
            value (datetime): The UTC date and time to be inserted.
                It should be a datetime object or None.

        Raises:
            AttributeError: If the
                customer is not initialized.

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
        Returns the last update UTC date and time
        of the customer.

        Raises:
            AttributeError: If the
                customer is not initialized.

        Returns:
            datetime: The last update UTC date and time
                of the customer.
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.customer.last_update_utc_date_time

    @last_update_utc_date_time.setter
    def last_update_utc_date_time(self, value):
        """
        Sets the last update UTC date and time
        for the customer.

        Args:
            value (datetime): The datetime object
                representing the last update UTC date and time.
                Pass None to unset the value.

        Raises:
            AttributeError: If the
                customer is not initialized.

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
        Load customer data
        from JSON string.

        :param json_data: JSON string containing
            customer data.
        :raises ValueError: If json_data is not a string
            or if no customer
            data is found.
        """

        if not isinstance(json_data, str):
            raise ValueError("json_data must be a string")

        customer_manager = CustomerManager(
            self._session_context)
        self.customer = customer_manager.from_json(json_data)

        return self

    async def load_from_code(
        self,
        code: uuid.UUID
    ):
        """
        Load customer
        data from UUID code.

        :param code: UUID code for loading a specific
            customer.
        :raises ValueError: If code is not a UUID or if no
            customer data is found.
        """
        if not isinstance(code, uuid.UUID):
            raise ValueError("code must be a UUID")

        customer_manager = CustomerManager(
            self._session_context)
        customer_obj = await customer_manager.get_by_code(
            code)
        self.customer = customer_obj

        return self

    async def load_from_id(
        self,
        customer_id: int
    ):
        """
        Load customer data from
        customer ID.

        :param customer_id: Integer ID for loading a specific
            customer.
        :raises ValueError: If customer_id
            is not an integer or
            if no customer
            data is found.
        """

        if not isinstance(customer_id, int):
            raise ValueError("customer_id must be an integer")

        customer_manager = CustomerManager(
            self._session_context)
        customer_obj = await customer_manager.get_by_id(
            customer_id)
        self.customer = customer_obj

        return self

    def load_from_obj_instance(
        self,
        customer_obj_instance: Customer
    ):
        """
        Use the provided
        Customer instance.

        :param customer_obj_instance: Instance of the
            Customer class.
        :raises ValueError: If customer_obj_instance
            is not an instance of
            Customer.
        """

        if not isinstance(customer_obj_instance,
                          Customer):
            raise ValueError("customer_obj_instance must be an instance of Customer")

        # customer_manager = CustomerManager(
        #     self._session_context)

        # customer_dict = customer_manager.to_dict(customer_obj_instance)

        # self.customer = customer_manager.from_dict(customer_dict)

        self.customer = customer_obj_instance

        return self

    async def load_from_dict(
        self,
        customer_dict: dict
    ):
        """
        Load customer data
        from dictionary.

        :param customer_dict: Dictionary containing
            customer data.
        :raises ValueError: If customer_dict
            is not a
            dictionary or if no
            customer data is found.
        """
        if not isinstance(customer_dict, dict):
            raise ValueError("customer_dict must be a dictionary")

        customer_manager = CustomerManager(
            self._session_context)

        self.customer = customer_manager.from_dict(
            customer_dict)

        return self


    def get_session_context(self):
        """
        Returns the session context.

        :return: The session context.
        :rtype: SessionContext
        """
        return self._session_context

    async def refresh(self):
        """
        Refreshes the customer
        object by fetching
        the latest data from the database.

        Returns:
            The updated
            customer object.
        """
        customer_manager = CustomerManager(
            self._session_context)
        self.customer = await customer_manager.refresh(
            self.customer)

        return self

    def is_valid(self):
        """
        Check if the customer
        is valid.

        Returns:
            bool: True if the customer
                is valid, False otherwise.
        """
        return self.customer is not None

    def to_dict(self):
        """
        Converts the Customer
        object to a dictionary representation.

        Returns:
            dict: A dictionary representation of the
                Customer object.
        """
        customer_manager = CustomerManager(
            self._session_context)
        return customer_manager.to_dict(
            self.customer)

    def to_json(self):
        """
        Converts the customer
        object to a JSON representation.

        Returns:
            str: The JSON representation of the
                customer object.
        """
        customer_manager = CustomerManager(
            self._session_context)
        return customer_manager.to_json(
            self.customer)

    async def save(self):
        """
        Saves the customer object
        to the database.

        If the customer object
        is not initialized, an AttributeError is raised.
        If the customer_id
        is greater than 0, the
        customer is
        updated in the database.
        If the customer_id is 0,
        the customer is
        added to the database.

        Returns:
            The updated or added
            customer object.

        Raises:
            AttributeError: If the customer
            object is not initialized.
        """
        if not self.customer:
            raise AttributeError(NOT_INITIALIZED_ERROR_MESSAGE)

        customer_id = self.customer.customer_id

        if customer_id > 0:
            customer_manager = CustomerManager(
                self._session_context)
            self.customer = await customer_manager.update(
                self.customer)

        if customer_id == 0:
            customer_manager = CustomerManager(
                self._session_context)
            self.customer = await customer_manager.add(
                self.customer)

        return self

    async def delete(self):
        """
        Deletes the customer
        from the database.

        Raises:
            AttributeError: If the customer
                is not initialized.
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if self.customer.customer_id > 0:
            customer_manager = CustomerManager(
                self._session_context)
            await customer_manager.delete(
                self.customer.customer_id)
            self.customer = None

    async def randomize_properties(self):
        """
        Randomizes the properties of the
        customer object.

        This method generates random values for various
        properties of the customer
        object

        Returns:
            self: The current instance of the
                Customer class.

        Raises:
            AttributeError: If the customer
                object is not initialized.
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        self.customer.active_organization_id = (
            random.randint(0, 100))
        self.customer.email = (
            f"user{random.randint(1, 100)}@abc.com")
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
        self.customer.is_active = (
            random.choice([True, False]))
        self.customer.is_email_allowed = (
            random.choice([True, False]))
        self.customer.is_email_confirmed = (
            random.choice([True, False]))
        self.customer.is_email_marketing_allowed = (
            random.choice([True, False]))
        self.customer.is_locked = (
            random.choice([True, False]))
        self.customer.is_multiple_organizations_allowed = (
            random.choice([True, False]))
        self.customer.is_verbose_logging_forced = (
            random.choice([True, False]))
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
        self.customer.utc_offset_in_minutes = (
            random.randint(0, 100))
        self.customer.zip = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))

        return self

    def get_customer_obj(self) -> Customer:
        """
        Returns the customer
        object.

        Raises:
            AttributeError: If the customer
                object is not initialized.

        Returns:
            Customer: The customer
                object.
        """
        if not self.customer:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.customer

    def is_equal(
        self,
        customer: Customer
    ) -> bool:
        """
        Checks if the current customer
        is equal to the given customer.

        Args:
            customer (Customer): The
                customer to compare with.

        Returns:
            bool: True if the customers
                are equal, False otherwise.
        """
        customer_manager = CustomerManager(
            self._session_context)
        my_customer = self.get_customer_obj()
        return customer_manager.is_equal(
            customer, my_customer)
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
        Retrieves the related Tac object based
        on the tac_id.

        Returns:
            An instance of the Tac model
            representing the related tac.

        """
        tac_manager = managers_and_enums.TacManager(self._session_context)
        tac_obj = await tac_manager.get_by_id(self.tac_id)
        return tac_obj
    # uTCOffsetInMinutes,
    # zip,

    def get_obj(self) -> Customer:
        """
        Returns the Customer object.

        :return: The Customer object.
        :rtype: Customer
        """

        return self.customer

    def get_object_name(self) -> str:
        """
        Returns the name of the object.

        :return: The name of the object.
        :rtype: str
        """
        return "customer"

    def get_id(self) -> int:
        """
        Returns the ID of the customer.

        :return: The ID of the customer.
        :rtype: int
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
        Get the name of the parent customer.

        Returns:
            str: The name of the parent customer.
        """
        return 'Tac'

    async def get_parent_code(self) -> uuid.UUID:
        """
        Get the parent code of the customer.

        Returns:
            The parent code of the customer
            as a UUID.
        """
        return self.tac_code_peek

    async def get_parent_obj(self) -> models.Tac:
        """
        Get the parent object of the current
        customer.

        Returns:
            The parent object of the current
            customer,
            which is an instance of the
            Tac model.
        """
        tac = await self.get_tac_id_rel_obj()

        return tac
    # uTCOffsetInMinutes,
    # zip,

