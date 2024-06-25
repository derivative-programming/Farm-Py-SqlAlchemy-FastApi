# business/tests/customer_fluent_test.py
# pylint: disable=unused-import
"""
Unit tests for the
CustomerFluentBusObj class.
"""
import math
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
    def customer(self, session):
        """
        Return a CustomerFluentBusObj
        object.
        """
        session_context = SessionContext(dict(), session=session)
        return CustomerFluentBusObj(session_context)
    def test_set_prop_active_organization_id(self, customer):
        """
        Test setting the active_organization_id property.
        """
        result = customer.set_prop_active_organization_id(42)
        assert customer.active_organization_id == 42
        assert result is customer
    def test_set_prop_email(self, customer):
        """
        Test setting the email property.
        """
        result = customer.set_prop_email("test@example.com")
        assert customer.email == "test@example.com"
        assert result is customer
    def test_set_prop_email_confirmed_utc_date_time(self, customer):
        """
        Test setting the email_confirmed_utc_date_time property.
        """
        test_datetime = datetime(2023, 1, 1, 12, 0, 0)
        result = customer.set_prop_email_confirmed_utc_date_time(test_datetime)
        assert customer.email_confirmed_utc_date_time == test_datetime
        assert result is customer
    def test_set_prop_first_name(self, customer):
        """
        Test setting the first_name property.
        """
        result = customer.set_prop_first_name("Vanilla")
        assert customer.first_name == "Vanilla"
        assert result is customer
    def test_set_prop_forgot_password_key_expiration_utc_date_time(self, customer):
        """
        Test setting the forgot_password_key_expiration_utc_date_time property.
        """
        test_datetime = datetime(2023, 1, 1, 12, 0, 0)
        result = customer.set_prop_forgot_password_key_expiration_utc_date_time(test_datetime)
        assert customer.forgot_password_key_expiration_utc_date_time == test_datetime
        assert result is customer
    def test_set_prop_forgot_password_key_value(self, customer):
        """
        Test setting the forgot_password_key_value property.
        """
        result = customer.set_prop_forgot_password_key_value("Vanilla")
        assert customer.forgot_password_key_value == "Vanilla"
        assert result is customer
    def test_set_prop_fs_user_code_value(self, customer):
        """
        Test setting the fs_user_code_value property.
        """
        test_uuid = uuid4()
        result = customer.set_prop_fs_user_code_value(test_uuid)
        assert customer.fs_user_code_value == test_uuid
        assert result is customer
    def test_set_prop_is_active(self, customer):
        """
        Test setting the is_active property.
        """
        result = customer.set_prop_is_active(True)
        assert customer.is_active is True
        assert result is customer
    def test_set_prop_is_email_allowed(self, customer):
        """
        Test setting the is_email_allowed property.
        """
        result = customer.set_prop_is_email_allowed(True)
        assert customer.is_email_allowed is True
        assert result is customer
    def test_set_prop_is_email_confirmed(self, customer):
        """
        Test setting the is_email_confirmed property.
        """
        result = customer.set_prop_is_email_confirmed(True)
        assert customer.is_email_confirmed is True
        assert result is customer
    def test_set_prop_is_email_marketing_allowed(self, customer):
        """
        Test setting the is_email_marketing_allowed property.
        """
        result = customer.set_prop_is_email_marketing_allowed(True)
        assert customer.is_email_marketing_allowed is True
        assert result is customer
    def test_set_prop_is_locked(self, customer):
        """
        Test setting the is_locked property.
        """
        result = customer.set_prop_is_locked(True)
        assert customer.is_locked is True
        assert result is customer
    def test_set_prop_is_multiple_organizations_allowed(self, customer):
        """
        Test setting the is_multiple_organizations_allowed property.
        """
        result = customer.set_prop_is_multiple_organizations_allowed(True)
        assert customer.is_multiple_organizations_allowed is True
        assert result is customer
    def test_set_prop_is_verbose_logging_forced(self, customer):
        """
        Test setting the is_verbose_logging_forced property.
        """
        result = customer.set_prop_is_verbose_logging_forced(True)
        assert customer.is_verbose_logging_forced is True
        assert result is customer
    def test_set_prop_last_login_utc_date_time(self, customer):
        """
        Test setting the last_login_utc_date_time property.
        """
        test_datetime = datetime(2023, 1, 1, 12, 0, 0)
        result = customer.set_prop_last_login_utc_date_time(test_datetime)
        assert customer.last_login_utc_date_time == test_datetime
        assert result is customer
    def test_set_prop_last_name(self, customer):
        """
        Test setting the last_name property.
        """
        result = customer.set_prop_last_name("Vanilla")
        assert customer.last_name == "Vanilla"
        assert result is customer
    def test_set_prop_password(self, customer):
        """
        Test setting the password property.
        """
        result = customer.set_prop_password("Vanilla")
        assert customer.password == "Vanilla"
        assert result is customer
    def test_set_prop_phone(self, customer):
        """
        Test setting the phone property.
        """
        result = customer.set_prop_phone("123-456-7890")
        assert customer.phone == "123-456-7890"
        assert result is customer
    def test_set_prop_province(self, customer):
        """
        Test setting the province property.
        """
        result = customer.set_prop_province("Vanilla")
        assert customer.province == "Vanilla"
        assert result is customer
    def test_set_prop_registration_utc_date_time(self, customer):
        """
        Test setting the registration_utc_date_time property.
        """
        test_datetime = datetime(2023, 1, 1, 12, 0, 0)
        result = customer.set_prop_registration_utc_date_time(test_datetime)
        assert customer.registration_utc_date_time == test_datetime
        assert result is customer
    def test_set_prop_tac_id(self, customer):
        """
        Test setting the tac_id property.
        """
        result = customer.set_prop_tac_id(1)
        assert customer.tac_id == 1
        assert result is customer
    def test_set_prop_utc_offset_in_minutes(self, customer):
        """
        Test setting the utc_offset_in_minutes property.
        """
        result = customer.set_prop_utc_offset_in_minutes(42)
        assert customer.utc_offset_in_minutes == 42
        assert result is customer
    def test_set_prop_zip(self, customer):
        """
        Test setting the zip property.
        """
        result = customer.set_prop_zip("Vanilla")
        assert customer.zip == "Vanilla"
        assert result is customer

