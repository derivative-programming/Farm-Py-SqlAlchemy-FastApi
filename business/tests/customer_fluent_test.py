# business/tests/customer_fluent_test.py
# pylint: disable=unused-import
"""
Unit tests for the
CustomerFluentBusObj class.
"""
import math  # noqa: F401
from datetime import date, datetime  # noqa: F401
from decimal import Decimal  # noqa: F401
from uuid import uuid4  # noqa: F401

import pytest

from business.customer_fluent import (
    CustomerFluentBusObj)
from helpers.session_context import SessionContext


class MockCustomerBaseBusObj:
    """
    A mock base class for the
    CustomerFluentBusObj class.
    """
    def __init__(self):
        self.active_organization_id = None
        self.email = None
        self.email_confirmed_utc_date_time = None
        self.first_name = None
        self.forgot_password_key_expiration_utc_date_time = None
        self.forgot_password_key_value = None
        self.fs_user_code_value = None
        self.is_active = None
        self.is_email_allowed = None
        self.is_email_confirmed = None
        self.is_email_marketing_allowed = None
        self.is_locked = None
        self.is_multiple_organizations_allowed = None
        self.is_verbose_logging_forced = None
        self.last_login_utc_date_time = None
        self.last_name = None
        self.password = None
        self.phone = None
        self.province = None
        self.registration_utc_date_time = None
        self.tac_id = None
        self.utc_offset_in_minutes = None
        self.zip = None
class TestCustomerFluentBusObj:
    """
    Unit tests for the
    CustomerFluentBusObj class.
    """
    @pytest.fixture
    def new_fluent_bus_obj(self, session):
        """
        Return a CustomerFluentBusObj
        object.
        """
        session_context = SessionContext(dict(), session=session)
        return CustomerFluentBusObj(
            session_context)
    # activeOrganizationID

    def test_set_prop_active_organization_id(self, new_fluent_bus_obj):
        """
        Test setting the active_organization_id property.
        """
        result = new_fluent_bus_obj.set_prop_active_organization_id(42)
        assert new_fluent_bus_obj.active_organization_id == 42
        assert result is new_fluent_bus_obj
    # email

    def test_set_prop_email(self, new_fluent_bus_obj):
        """
        Test setting the email property.
        """
        result = new_fluent_bus_obj.set_prop_email(
            "test@example.com")
        assert new_fluent_bus_obj.email == \
            "test@example.com"
        assert result is new_fluent_bus_obj
    # emailConfirmedUTCDateTime

    def test_set_prop_email_confirmed_utc_date_time(self, new_fluent_bus_obj):
        """
        Test setting the email_confirmed_utc_date_time property.
        """
        test_datetime = datetime(2023, 1, 1, 12, 0, 0)
        result = new_fluent_bus_obj.set_prop_email_confirmed_utc_date_time(
            test_datetime)
        assert new_fluent_bus_obj.email_confirmed_utc_date_time == \
            test_datetime
        assert result is new_fluent_bus_obj
    # firstName

    def test_set_prop_first_name(self, new_fluent_bus_obj):
        """
        Test setting the first_name property.
        """
        result = new_fluent_bus_obj.set_prop_first_name(
            "Vanilla")
        assert new_fluent_bus_obj.first_name == \
            "Vanilla"
        assert result is new_fluent_bus_obj
    # forgotPasswordKeyExpirationUTCDateTime

    def test_set_prop_forgot_password_key_expiration_utc_date_time(self, new_fluent_bus_obj):
        """
        Test setting the forgot_password_key_expiration_utc_date_time property.
        """
        test_datetime = datetime(2023, 1, 1, 12, 0, 0)
        result = new_fluent_bus_obj.set_prop_forgot_password_key_expiration_utc_date_time(
            test_datetime)
        assert new_fluent_bus_obj.forgot_password_key_expiration_utc_date_time == \
            test_datetime
        assert result is new_fluent_bus_obj
    # forgotPasswordKeyValue

    def test_set_prop_forgot_password_key_value(self, new_fluent_bus_obj):
        """
        Test setting the forgot_password_key_value property.
        """
        result = new_fluent_bus_obj.set_prop_forgot_password_key_value(
            "Vanilla")
        assert new_fluent_bus_obj.forgot_password_key_value == \
            "Vanilla"
        assert result is new_fluent_bus_obj
    # fSUserCodeValue

    def test_set_prop_fs_user_code_value(self, new_fluent_bus_obj):
        """
        Test setting the fs_user_code_value property.
        """
        test_uuid = uuid4()
        result = new_fluent_bus_obj.set_prop_fs_user_code_value(
            test_uuid)
        assert new_fluent_bus_obj.fs_user_code_value == \
            test_uuid
        assert result is new_fluent_bus_obj
    # isActive

    def test_set_prop_is_active(self, new_fluent_bus_obj):
        """
        Test setting the is_active property.
        """
        result = new_fluent_bus_obj.set_prop_is_active(True)
        assert new_fluent_bus_obj.is_active is True
        assert result is new_fluent_bus_obj
    # isEmailAllowed

    def test_set_prop_is_email_allowed(self, new_fluent_bus_obj):
        """
        Test setting the is_email_allowed property.
        """
        result = new_fluent_bus_obj.set_prop_is_email_allowed(True)
        assert new_fluent_bus_obj.is_email_allowed is True
        assert result is new_fluent_bus_obj
    # isEmailConfirmed

    def test_set_prop_is_email_confirmed(self, new_fluent_bus_obj):
        """
        Test setting the is_email_confirmed property.
        """
        result = new_fluent_bus_obj.set_prop_is_email_confirmed(True)
        assert new_fluent_bus_obj.is_email_confirmed is True
        assert result is new_fluent_bus_obj
    # isEmailMarketingAllowed

    def test_set_prop_is_email_marketing_allowed(self, new_fluent_bus_obj):
        """
        Test setting the is_email_marketing_allowed property.
        """
        result = new_fluent_bus_obj.set_prop_is_email_marketing_allowed(True)
        assert new_fluent_bus_obj.is_email_marketing_allowed is True
        assert result is new_fluent_bus_obj
    # isLocked

    def test_set_prop_is_locked(self, new_fluent_bus_obj):
        """
        Test setting the is_locked property.
        """
        result = new_fluent_bus_obj.set_prop_is_locked(True)
        assert new_fluent_bus_obj.is_locked is True
        assert result is new_fluent_bus_obj
    # isMultipleOrganizationsAllowed

    def test_set_prop_is_multiple_organizations_allowed(self, new_fluent_bus_obj):
        """
        Test setting the is_multiple_organizations_allowed property.
        """
        result = new_fluent_bus_obj.set_prop_is_multiple_organizations_allowed(True)
        assert new_fluent_bus_obj.is_multiple_organizations_allowed is True
        assert result is new_fluent_bus_obj
    # isVerboseLoggingForced

    def test_set_prop_is_verbose_logging_forced(self, new_fluent_bus_obj):
        """
        Test setting the is_verbose_logging_forced property.
        """
        result = new_fluent_bus_obj.set_prop_is_verbose_logging_forced(True)
        assert new_fluent_bus_obj.is_verbose_logging_forced is True
        assert result is new_fluent_bus_obj
    # lastLoginUTCDateTime

    def test_set_prop_last_login_utc_date_time(self, new_fluent_bus_obj):
        """
        Test setting the last_login_utc_date_time property.
        """
        test_datetime = datetime(2023, 1, 1, 12, 0, 0)
        result = new_fluent_bus_obj.set_prop_last_login_utc_date_time(
            test_datetime)
        assert new_fluent_bus_obj.last_login_utc_date_time == \
            test_datetime
        assert result is new_fluent_bus_obj
    # lastName

    def test_set_prop_last_name(self, new_fluent_bus_obj):
        """
        Test setting the last_name property.
        """
        result = new_fluent_bus_obj.set_prop_last_name(
            "Vanilla")
        assert new_fluent_bus_obj.last_name == \
            "Vanilla"
        assert result is new_fluent_bus_obj
    # password

    def test_set_prop_password(self, new_fluent_bus_obj):
        """
        Test setting the password property.
        """
        result = new_fluent_bus_obj.set_prop_password(
            "Vanilla")
        assert new_fluent_bus_obj.password == \
            "Vanilla"
        assert result is new_fluent_bus_obj
    # phone

    def test_set_prop_phone(self, new_fluent_bus_obj):
        """
        Test setting the phone property.
        """
        result = new_fluent_bus_obj.set_prop_phone(
            "123-456-7890")
        assert new_fluent_bus_obj.phone == \
            "123-456-7890"
        assert result is new_fluent_bus_obj
    # province

    def test_set_prop_province(self, new_fluent_bus_obj):
        """
        Test setting the province property.
        """
        result = new_fluent_bus_obj.set_prop_province(
            "Vanilla")
        assert new_fluent_bus_obj.province == \
            "Vanilla"
        assert result is new_fluent_bus_obj
    # registrationUTCDateTime

    def test_set_prop_registration_utc_date_time(self, new_fluent_bus_obj):
        """
        Test setting the registration_utc_date_time property.
        """
        test_datetime = datetime(2023, 1, 1, 12, 0, 0)
        result = new_fluent_bus_obj.set_prop_registration_utc_date_time(
            test_datetime)
        assert new_fluent_bus_obj.registration_utc_date_time == \
            test_datetime
        assert result is new_fluent_bus_obj
    # TacID
    # uTCOffsetInMinutes

    def test_set_prop_utc_offset_in_minutes(self, new_fluent_bus_obj):
        """
        Test setting the utc_offset_in_minutes property.
        """
        result = new_fluent_bus_obj.set_prop_utc_offset_in_minutes(42)
        assert new_fluent_bus_obj.utc_offset_in_minutes == 42
        assert result is new_fluent_bus_obj
    # zip

    def test_set_prop_zip(self, new_fluent_bus_obj):
        """
        Test setting the zip property.
        """
        result = new_fluent_bus_obj.set_prop_zip(
            "Vanilla")
        assert new_fluent_bus_obj.zip == \
            "Vanilla"
        assert result is new_fluent_bus_obj
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

    def test_set_prop_tac_id(self, new_fluent_bus_obj):
        """
        Test setting the tac_id property.
        """
        result = new_fluent_bus_obj.set_prop_tac_id(1)
        assert new_fluent_bus_obj.tac_id == 1
        assert result is new_fluent_bus_obj
    # uTCOffsetInMinutes,
    # zip,
