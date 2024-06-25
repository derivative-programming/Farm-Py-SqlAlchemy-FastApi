# flows/base/tests/land_add_plant_test.py
# pylint: disable=protected-access
# pylint: disable=unused-import
"""
This module contains the unit tests for the
`BaseFlowLandAddPlant` class.
"""
import uuid  # noqa: F401
from datetime import date, datetime  # noqa: F401
from decimal import Decimal  # noqa: F401
import pytest
import flows.constants.land_add_plant as FlowConstants
from flows.base.land_add_plant import (
    BaseFlowLandAddPlant)
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion  # noqa: F401
from models.factory.land import LandFactory


class TestBaseFlowLandAddPlant():
    """
    This class contains unit tests for the
    `BaseFlowLandAddPlant` class.
    """

    @pytest.mark.asyncio
    async def test_process_validation_rules(self, session):
        """
        Test case for the _process_validation_rules method
        of the BaseFlowLandAddPlant class.

        This method tests the validation rules for the request
        parameters of the
        land add plant flow.

        Args:
            session: The session object for the test.

        Returns:
            None
        """
        session_context = SessionContext(dict(), session)
        flow = BaseFlowLandAddPlant(session_context)
        land = await LandFactory.create_async(session)
        request_flavor_code: uuid.UUID = uuid.UUID(int=0)
        request_other_flavor: str = ""
        request_some_int_val: int = 0
        request_some_big_int_val: int = 0
        request_some_bit_val: bool = False
        request_is_edit_allowed: bool = False
        request_is_delete_allowed: bool = False
        request_some_float_val: float = 0
        request_some_decimal_val: Decimal = Decimal(0)
        request_some_utc_date_time_val: datetime = (
            TypeConversion.get_default_date_time()
        )
        request_some_date_val: date = (
            TypeConversion.get_default_date()
        )
        request_some_money_val: Decimal = Decimal(0)
        request_some_n_var_char_val: str = ""
        request_some_var_char_val: str = ""
        request_some_text_val: str = ""
        request_some_phone_number: str = ""
        request_some_email_address: str = ""
        request_sample_image_upload_file: str = ""
# endset
        # Call the method being tested
        await flow._process_validation_rules(
            land,
            request_flavor_code,
            request_other_flavor,
            request_some_int_val,
            request_some_big_int_val,
            request_some_bit_val,
            request_is_edit_allowed,
            request_is_delete_allowed,
            request_some_float_val,
            request_some_decimal_val,
            request_some_utc_date_time_val,
            request_some_date_val,
            request_some_money_val,
            request_some_n_var_char_val,
            request_some_var_char_val,
            request_some_text_val,
            request_some_phone_number,
            request_some_email_address,
            request_sample_image_upload_file,
# endset  # noqa: E122
        )
        #TODO add validation checks
        # - is email
        # - is phone
        # - calculatedIsRowLevelCustomerSecurityUsed
        # - calculatedIsRowLevelOrgCustomerSecurityUsed
        # - calculatedIsRowLevelOrganizationSecurityUsed
        if FlowConstants.PARAM_REQUEST_FLAVOR_CODE_IS_REQUIRED \
                is True:
            assert 'requestFlavorCode' in flow.queued_validation_errors
            assert flow.queued_validation_errors[
                'requestFlavorCode'] == (
                'Please select a Flavor')
        if FlowConstants.PARAM_REQUEST_OTHER_FLAVOR_IS_REQUIRED \
                is True:
            assert 'requestOtherFlavor' in flow.queued_validation_errors
            assert flow.queued_validation_errors[
                'requestOtherFlavor'] == (
                'Please enter a Other Flavor')
        if FlowConstants.PARAM_REQUEST_SOME_INT_VAL_IS_REQUIRED \
                is True:
            assert 'requestSomeIntVal' in flow.queued_validation_errors
            assert flow.queued_validation_errors[
                'requestSomeIntVal'] == (
                'Please enter a Some Int Val')
        if FlowConstants.PARAM_REQUEST_SOME_BIG_INT_VAL_IS_REQUIRED \
                is True:
            assert 'requestSomeBigIntVal' in flow.queued_validation_errors
            assert flow.queued_validation_errors[
                'requestSomeBigIntVal'] == (
                'Please enter a Some Big Int Val')
        # if FlowConstants.PARAM_REQUEST_SOME_BIT_VAL_IS_REQUIRED \
        #         is True:
        #     assert 'requestSomeBitVal' in flow.queued_validation_errors
        #     assert flow.queued_validation_errors[
        #         'requestSomeBitVal'] == (
        #         'Please enter a Some Bit Val')
        if FlowConstants.PARAM_REQUEST_IS_EDIT_ALLOWED_IS_REQUIRED \
                is True:
            assert 'requestIsEditAllowed' in flow.queued_validation_errors
            assert flow.queued_validation_errors[
                'requestIsEditAllowed'] == (
                'Please enter a Is Edit Allowed')
        if FlowConstants.PARAM_REQUEST_IS_DELETE_ALLOWED_IS_REQUIRED \
                is True:
            assert 'requestIsDeleteAllowed' in flow.queued_validation_errors
            assert flow.queued_validation_errors[
                'requestIsDeleteAllowed'] == (
                'Please enter a Is Delete Allowed')
        if FlowConstants.PARAM_REQUEST_SOME_FLOAT_VAL_IS_REQUIRED \
                is True:
            assert 'requestSomeFloatVal' in flow.queued_validation_errors
            assert flow.queued_validation_errors[
                'requestSomeFloatVal'] == (
                'Please enter a Some Float Val')
        if FlowConstants.PARAM_REQUEST_SOME_DECIMAL_VAL_IS_REQUIRED \
                is True:
            assert 'requestSomeDecimalVal' in flow.queued_validation_errors
            assert flow.queued_validation_errors[
                'requestSomeDecimalVal'] == (
                'Please enter a Some Decimal Val')
        if FlowConstants.PARAM_REQUEST_SOME_UTC_DATE_TIME_VAL_IS_REQUIRED \
                is True:
            assert 'requestSomeUTCDateTimeVal' in flow.queued_validation_errors
            assert flow.queued_validation_errors[
                'requestSomeUTCDateTimeVal'] == (
                'Please enter a Some UTC Date Time Val')
        if FlowConstants.PARAM_REQUEST_SOME_DATE_VAL_IS_REQUIRED \
                is True:
            assert 'requestSomeDateVal' in flow.queued_validation_errors
            assert flow.queued_validation_errors[
                'requestSomeDateVal'] == (
                'Please enter a Some Date Val')
        if FlowConstants.PARAM_REQUEST_SOME_MONEY_VAL_IS_REQUIRED \
                is True:
            assert 'requestSomeMoneyVal' in flow.queued_validation_errors
            assert flow.queued_validation_errors[
                'requestSomeMoneyVal'] == (
                'Please enter a Some Money Val')
        if FlowConstants.PARAM_REQUEST_SOME_N_VAR_CHAR_VAL_IS_REQUIRED \
                is True:
            assert 'requestSomeNVarCharVal' in flow.queued_validation_errors
            assert flow.queued_validation_errors[
                'requestSomeNVarCharVal'] == (
                'Please enter a Some N Var Char Val')
        if FlowConstants.PARAM_REQUEST_SOME_VAR_CHAR_VAL_IS_REQUIRED \
                is True:
            assert 'requestSomeVarCharVal' in flow.queued_validation_errors
            assert flow.queued_validation_errors[
                'requestSomeVarCharVal'] == (
                'Please enter a Some Var Char Val')
        if FlowConstants.PARAM_REQUEST_SOME_TEXT_VAL_IS_REQUIRED \
                is True:
            assert 'requestSomeTextVal' in flow.queued_validation_errors
            assert flow.queued_validation_errors[
                'requestSomeTextVal'] == (
                'Please enter a Some Text Val')
        if FlowConstants.PARAM_REQUEST_SOME_PHONE_NUMBER_IS_REQUIRED \
                is True:
            assert 'requestSomePhoneNumber' in flow.queued_validation_errors
            assert flow.queued_validation_errors[
                'requestSomePhoneNumber'] == (
                'Please enter a Some Phone Number')
        if FlowConstants.PARAM_REQUEST_SOME_EMAIL_ADDRESS_IS_REQUIRED \
                is True:
            assert 'requestSomeEmailAddress' in flow.queued_validation_errors
            assert flow.queued_validation_errors[
                'requestSomeEmailAddress'] == (
                'Please enter a Some Email Address')
        if FlowConstants.PARAM_REQUEST_SAMPLE_IMAGE_UPLOAD_FILE_IS_REQUIRED \
                is True:
            assert 'requestSampleImageUploadFile' \
                in flow.queued_validation_errors
            assert flow.queued_validation_errors[
                'requestSampleImageUploadFile'] == (
                'Please enter a image file')
# endset

    @pytest.mark.asyncio
    async def test_process_security_rules(self, session):
        """
        Test the process_security_rules method of
        BaseFlowLandAddPlant.

        This method tests the behavior of the
        _process_security_rules method
        when a specific role is required. It
        creates a session context, a land
        object, and a
        BaseFlowLandAddPlant object.
        Then, it sets the role_required
        variable to "User" and calls the
        _process_security_rules method. Finally,
        it asserts that the expected validation
        errors are present in the flow's
        queued_validation_errors dictionary.

        Args:
            session: The session object for the test.

        Returns:
            None
        """
        session_context = SessionContext(dict(), session)
        land = await LandFactory.create_async(session)
        flow = BaseFlowLandAddPlant(session_context)
        role_required = "User"
        if len(role_required) > 0:
            await flow._process_security_rules(land)
            assert '' in flow.queued_validation_errors
            assert flow.queued_validation_errors[''] == (
                f"Unauthorized access. {role_required} role not found.")
            session_context.role_name_csv = role_required
