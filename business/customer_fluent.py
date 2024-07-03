# business/customer_fluent.py
# pylint: disable=unused-import

"""
This module contains the
CustomerFluentBusObj class,
which adds fluent properties
to the business object for a
Customer.
"""

import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401

import managers as managers_and_enums

from .customer_base import CustomerBaseBusObj


class CustomerFluentBusObj(CustomerBaseBusObj):
    """
    This class add fluent properties to the
    Base Customer Business Object
    """

    # activeOrganizationID

    def set_prop_active_organization_id(self, value: int):
        """
        Set the value of
        active_organization_id property.

        Args:
            value (int): The value to set for
                active_organization_id.

        Returns:
            self: Returns the instance of the class.

        """
        self.active_organization_id = value
        return self
    # email

    def set_prop_email(self, value: str):
        """
        Set the value of the
        email property.

        Args:
            value (str): The Email
                to set.

        Returns:
            self: The current instance of the class.
        """
        self.email = value
        return self
    # emailConfirmedUTCDateTime

    def set_prop_email_confirmed_utc_date_time(self, value: datetime):
        """
        Sets the value of the
        'email_confirmed_utc_date_time' property.

        Args:
            value (datetime): The datetime value to set.

        Returns:
            self: The current instance of the class.
        """
        self.email_confirmed_utc_date_time = value
        return self
    # firstName

    def set_prop_first_name(self, value: str):
        """
        Set the First Name for the
        Customer object.

        :param value: The First Name value.
        :return: The updated
            CustomerBusObj instance.
        """

        self.first_name = value
        return self
    # forgotPasswordKeyExpirationUTCDateTime

    def set_prop_forgot_password_key_expiration_utc_date_time(self, value: datetime):
        """
        Sets the value of the
        'forgot_password_key_expiration_utc_date_time' property.

        Args:
            value (datetime): The datetime value to set.

        Returns:
            self: The current instance of the class.
        """
        self.forgot_password_key_expiration_utc_date_time = value
        return self
    # forgotPasswordKeyValue

    def set_prop_forgot_password_key_value(self, value: str):
        """
        Set the Forgot Password Key Value for the
        Customer object.

        :param value: The Forgot Password Key Value value.
        :return: The updated
            CustomerBusObj instance.
        """

        self.forgot_password_key_value = value
        return self
    # fSUserCodeValue

    def set_prop_fs_user_code_value(self, value: uuid.UUID):
        """
        Set the value of the
        'fs_user_code_value' property.

        Args:
            value (uuid.UUID): The value to set.

        Returns:
            self: The current instance of the class.
        """
        self.fs_user_code_value = value
        return self
    # isActive

    def set_prop_is_active(self, value: bool):
        """
        Set the Is Active flag for the
        Customer object.

        :param value: The Is Active flag value.
        :return: The updated
            CustomerBusObj instance.
        """

        self.is_active = value
        return self
    # isEmailAllowed

    def set_prop_is_email_allowed(self, value: bool):
        """
        Set the Is Email Allowed flag for the
        Customer object.

        :param value: The Is Email Allowed flag value.
        :return: The updated
            CustomerBusObj instance.
        """

        self.is_email_allowed = value
        return self
    # isEmailConfirmed

    def set_prop_is_email_confirmed(self, value: bool):
        """
        Set the Is Email Confirmed flag for the
        Customer object.

        :param value: The Is Email Confirmed flag value.
        :return: The updated
            CustomerBusObj instance.
        """

        self.is_email_confirmed = value
        return self
    # isEmailMarketingAllowed

    def set_prop_is_email_marketing_allowed(self, value: bool):
        """
        Set the Is Email Marketing Allowed flag for the
        Customer object.

        :param value: The Is Email Marketing Allowed flag value.
        :return: The updated
            CustomerBusObj instance.
        """

        self.is_email_marketing_allowed = value
        return self
    # isLocked

    def set_prop_is_locked(self, value: bool):
        """
        Set the Is Locked flag for the
        Customer object.

        :param value: The Is Locked flag value.
        :return: The updated
            CustomerBusObj instance.
        """

        self.is_locked = value
        return self
    # isMultipleOrganizationsAllowed

    def set_prop_is_multiple_organizations_allowed(self, value: bool):
        """
        Set the Is Multiple Organizations Allowed flag for the
        Customer object.

        :param value: The Is Multiple Organizations Allowed flag value.
        :return: The updated
            CustomerBusObj instance.
        """

        self.is_multiple_organizations_allowed = value
        return self
    # isVerboseLoggingForced

    def set_prop_is_verbose_logging_forced(self, value: bool):
        """
        Set the Is Verbose Logging Forced flag for the
        Customer object.

        :param value: The Is Verbose Logging Forced flag value.
        :return: The updated
            CustomerBusObj instance.
        """

        self.is_verbose_logging_forced = value
        return self
    # lastLoginUTCDateTime

    def set_prop_last_login_utc_date_time(self, value: datetime):
        """
        Sets the value of the
        'last_login_utc_date_time' property.

        Args:
            value (datetime): The datetime value to set.

        Returns:
            self: The current instance of the class.
        """
        self.last_login_utc_date_time = value
        return self
    # lastName

    def set_prop_last_name(self, value: str):
        """
        Set the Last Name for the
        Customer object.

        :param value: The Last Name value.
        :return: The updated
            CustomerBusObj instance.
        """

        self.last_name = value
        return self
    # password

    def set_prop_password(self, value: str):
        """
        Set the Password for the
        Customer object.

        :param value: The Password value.
        :return: The updated
            CustomerBusObj instance.
        """

        self.password = value
        return self
    # phone

    def set_prop_phone(self, value: str):
        """
        Set the value of the
        'phone' property.

        Args:
            value (str): The
                Phone to set.

        Returns:
            Customer: The updated
                Customer instance.

        """

        self.phone = value
        return self
    # province

    def set_prop_province(self, value: str):
        """
        Set the Province for the
        Customer object.

        :param value: The Province value.
        :return: The updated
            CustomerBusObj instance.
        """

        self.province = value
        return self
    # registrationUTCDateTime

    def set_prop_registration_utc_date_time(self, value: datetime):
        """
        Sets the value of the
        'registration_utc_date_time' property.

        Args:
            value (datetime): The datetime value to set.

        Returns:
            self: The current instance of the class.
        """
        self.registration_utc_date_time = value
        return self
    # TacID
    # uTCOffsetInMinutes

    def set_prop_utc_offset_in_minutes(self, value: int):
        """
        Set the value of
        utc_offset_in_minutes property.

        Args:
            value (int): The value to set for
                utc_offset_in_minutes.

        Returns:
            self: Returns the instance of the class.

        """
        self.utc_offset_in_minutes = value
        return self
    # zip

    def set_prop_zip(self, value: str):
        """
        Set the Zip for the
        Customer object.

        :param value: The Zip value.
        :return: The updated
            CustomerBusObj instance.
        """

        self.zip = value
        return self
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

    def set_prop_tac_id(self, value: int):
        """
        Set the tac ID for the
        customer.

        Args:
            value (int): The tac id value.

        Returns:
            Customer: The updated
                Customer object.
        """

        self.tac_id = value
        return self
    # uTCOffsetInMinutes,
    # zip,
