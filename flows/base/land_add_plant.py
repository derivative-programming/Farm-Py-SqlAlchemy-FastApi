# flows/base/land_add_plant.py  # pylint: disable=duplicate-code
# pylint: disable=unused-import

"""
This module contains the implementation
of the BaseFlow
Land Add Plant class
"""

import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401

import flows.constants.land_add_plant \
    as FlowConstants
from business.customer import CustomerBusObj  # noqa: F401
from business.factory import BusObjFactory
from business.land import LandBusObj
from flows.base import LogSeverity
from helpers import SessionContext, TypeConversion  # noqa: F401
from managers.org_customer import OrgCustomerManager  # noqa: F401

from .base_flow import BaseFlow


class BaseFlowLandAddPlant(BaseFlow):  # pylint: disable=too-few-public-methods
    """
    Base class for LandAddPlant
    flow. Contains
    some validaiton and security check logic
    """

    def __init__(self, session_context: SessionContext):
        """
        Initializes a new instance of the
        BaseFlowLandAddPlant class.

        Args:
            session_context (SessionContext): The session context for the flow.
        """

        super(BaseFlowLandAddPlant, self).__init__(
            "LandAddPlant",
            session_context,
        )

    async def _process_validation_rules(
        self,
        land_bus_obj: LandBusObj,
        request_flavor_code: uuid.UUID = uuid.UUID(int=0),
        request_other_flavor: str = "",
        request_some_int_val: int = 0,
        request_some_big_int_val: int = 0,
        request_some_bit_val: bool = False,
        request_is_edit_allowed: bool = False,
        request_is_delete_allowed: bool = False,
        request_some_float_val: float = 0,
        request_some_decimal_val: Decimal = Decimal(0),
        request_some_utc_date_time_val: datetime = (
            TypeConversion.get_default_date_time()
        ),
        request_some_date_val: date = TypeConversion.get_default_date(),
        request_some_money_val: Decimal = Decimal(0),
        request_some_n_var_char_val: str = "",
        request_some_var_char_val: str = "",
        request_some_text_val: str = "",
        request_some_phone_number: str = "",
        request_some_email_address: str = "",
        request_sample_image_upload_file: str = "",
    ):
        """
        Processes the validation rules for adding plants to land.

        """

        super()._log_message_and_severity(
            LogSeverity.INFORMATION_HIGH_DETAIL,
            "Validating...")

        if request_flavor_code == uuid.UUID(int=0) and \
            FlowConstants.PARAM_REQUEST_FLAVOR_CODE_IS_REQUIRED \
                is True:
            self._add_field_validation_error(
                "requestFlavorCode",
                "Please select a Flavor"
            )

        if request_other_flavor == "" and \
            FlowConstants.PARAM_REQUEST_OTHER_FLAVOR_IS_REQUIRED \
                is True:
            self._add_field_validation_error(
                "requestOtherFlavor",
                "Please enter a Other Flavor"
            )

        if request_some_int_val == 0 and \
            FlowConstants.PARAM_REQUEST_SOME_INT_VAL_IS_REQUIRED \
                is True:
            self._add_field_validation_error(
                "requestSomeIntVal",
                "Please enter a Some Int Val"
            )

        if request_some_big_int_val == 0 and \
            FlowConstants.PARAM_REQUEST_SOME_BIG_INT_VAL_IS_REQUIRED \
                is True:
            self._add_field_validation_error(
                "requestSomeBigIntVal",
                "Please enter a Some Big Int Val"
            )

        if request_some_bit_val is None and \
            FlowConstants.PARAM_REQUEST_SOME_BIT_VAL_IS_REQUIRED \
                is True:
            self._add_field_validation_error(
                "requestSomeBitVal",
                "Please enter a Some Bit Val"
            )

        if request_is_edit_allowed is None and \
            FlowConstants.PARAM_REQUEST_IS_EDIT_ALLOWED_IS_REQUIRED \
                is True:
            self._add_field_validation_error(
                "requestIsEditAllowed",
                "Please enter a Is Edit Allowed"
            )

        if request_is_delete_allowed is None and \
            FlowConstants.PARAM_REQUEST_IS_DELETE_ALLOWED_IS_REQUIRED \
                is True:
            self._add_field_validation_error(
                "requestIsDeleteAllowed",
                "Please enter a Is Delete Allowed"
            )

        if request_some_float_val == 0 and \
            FlowConstants.PARAM_REQUEST_SOME_FLOAT_VAL_IS_REQUIRED \
                is True:
            self._add_field_validation_error(
                "requestSomeFloatVal",
                "Please enter a Some Float Val"
            )

        if request_some_decimal_val == 0 and \
            FlowConstants.PARAM_REQUEST_SOME_DECIMAL_VAL_IS_REQUIRED \
                is True:
            self._add_field_validation_error(
                "requestSomeDecimalVal",
                "Please enter a Some Decimal Val"
            )

        if request_some_utc_date_time_val == \
            TypeConversion.get_default_date_time() and \
            FlowConstants.PARAM_REQUEST_SOME_UTC_DATE_TIME_VAL_IS_REQUIRED \
                is True:
            self._add_field_validation_error(
                "requestSomeUTCDateTimeVal",
                "Please enter a Some UTC Date Time Val"
            )

        if request_some_date_val == TypeConversion.get_default_date() and \
            FlowConstants.PARAM_REQUEST_SOME_DATE_VAL_IS_REQUIRED \
                is True:
            self._add_field_validation_error(
                "requestSomeDateVal",
                "Please enter a Some Date Val"
            )

        if request_some_money_val == 0 and \
            FlowConstants.PARAM_REQUEST_SOME_MONEY_VAL_IS_REQUIRED \
                is True:
            self._add_field_validation_error(
                "requestSomeMoneyVal",
                "Please enter a Some Money Val"
            )

        if request_some_n_var_char_val == "" and \
            FlowConstants.PARAM_REQUEST_SOME_N_VAR_CHAR_VAL_IS_REQUIRED \
                is True:
            self._add_field_validation_error(
                "requestSomeNVarCharVal",
                "Please enter a Some N Var Char Val"
            )

        if request_some_var_char_val == "" and \
            FlowConstants.PARAM_REQUEST_SOME_VAR_CHAR_VAL_IS_REQUIRED \
                is True:
            self._add_field_validation_error(
                "requestSomeVarCharVal",
                "Please enter a Some Var Char Val"
            )

        if request_some_text_val == "" and \
            FlowConstants.PARAM_REQUEST_SOME_TEXT_VAL_IS_REQUIRED \
                is True:
            self._add_field_validation_error(
                "requestSomeTextVal",
                "Please enter a Some Text Val"
            )

        if request_some_phone_number == "" and \
            FlowConstants.PARAM_REQUEST_SOME_PHONE_NUMBER_IS_REQUIRED \
                is True:
            self._add_field_validation_error(
                "requestSomePhoneNumber",
                "Please enter a Some Phone Number"
            )

        if request_some_email_address == "" and \
            FlowConstants.PARAM_REQUEST_SOME_EMAIL_ADDRESS_IS_REQUIRED \
                is True:
            self._add_field_validation_error(
                "requestSomeEmailAddress",
                "Please enter a Some Email Address"
            )

        if request_sample_image_upload_file == "" and \
            FlowConstants.PARAM_REQUEST_SAMPLE_IMAGE_UPLOAD_FILE_IS_REQUIRED \
                is True:
            self._add_field_validation_error(
                "requestSampleImageUploadFile",
                "Please enter a image file"
            )

# end set

        await self._process_security_rules(land_bus_obj)

    async def _process_security_rules(
        self,
        land_bus_obj: LandBusObj,
    ):
        super()._log_message_and_severity(
            LogSeverity.INFORMATION_HIGH_DETAIL,
            "Processing security rules..."
        )

        customer_code_match_required = False

        role_required = "User"

        if len(role_required) > 0:
            if role_required not in self._session_context.role_name_csv:
                self._add_validation_error(
                    f"Unauthorized access. {role_required} role not found."
                )

        if FlowConstants.CALCULATED_IS_ROW_LEVEL_CUSTOMER_SECURITY_USED \
                is True:
            customer_code_match_required = True
        if FlowConstants.CALCULATED_IS_ROW_LEVEL_ORGANIZATION_SECURITY_USED \
                is True:
            customer_code_match_required = True
        if FlowConstants.CALCULATED_IS_ROW_LEVEL_ORG_CUSTOMER_SECURITY_USED \
                is True:
            customer_code_match_required = True

        if len(self.queued_validation_errors) > 0:
            return

        if customer_code_match_required is False:
            return

        val = True

        item = land_bus_obj

        while val:
            if item.get_object_name() == "pac":  # type: ignore
                val = False
##GENTrainingBlock[caseFlowLogic_calculatedIsRowLevelOrgCustomerSecurityUsed]Start
##GENLearn[calculatedIsRowLevelOrgCustomerSecurityUsed=true]Start

            if FlowConstants. \
                CALCULATED_IS_ROW_LEVEL_ORG_CUSTOMER_SECURITY_USED \
                    is True and item.get_object_name() == "org_customer":  # type: ignore  # noqa: E501
                item = item.get_customer_id_rel_obj()  # type: ignore
##GENLearn[calculatedIsRowLevelOrgCustomerSecurityUsed=true]End
##GENTrainingBlock[caseFlowLogic_calculatedIsRowLevelOrgCustomerSecurityUsed]End
##GENTrainingBlock[caseFlowLogic_calculatedIsRowLevelCustomerSecurityUsed]Start
##GENLearn[calculatedIsRowLevelCustomerSecurityUsed=true]Start

            if FlowConstants.CALCULATED_IS_ROW_LEVEL_CUSTOMER_SECURITY_USED \
                    is True and item.get_object_name() == "customer":  # type: ignore  # noqa: E501
                if item.code != self._session_context.customer_code:  # type: ignore  # noqa: E501
                    self._add_validation_error(
                        "Unauthorized access.  Invalid User.")
##GENLearn[calculatedIsRowLevelCustomerSecurityUsed=true]End
##GENTrainingBlock[caseFlowLogic_calculatedIsRowLevelCustomerSecurityUsed]End
##GENTrainingBlock[caseFlowLogic_calculatedIsRowLevelOrganizationSecurityUsed]Start
##GENLearn[calculatedIsRowLevelOrganizationSecurityUsed=true]Start

            if FlowConstants. \
                CALCULATED_IS_ROW_LEVEL_ORGANIZATION_SECURITY_USED \
                    is True and item.get_object_name() == "organization":  # type: ignore # noqa: E501

                organization_id = item.get_id()  # type: ignore

                customer_bus_obj = CustomerBusObj(
                    land_bus_obj.get_session_context())

                await customer_bus_obj.load_from_code(
                    self._session_context.customer_code)

                org_customer_manager = OrgCustomerManager(
                    land_bus_obj.get_session_context())
                org_customers = await org_customer_manager.get_by_customer_id(
                    customer_bus_obj.customer_id)

                if not any(
                    org_customer.organization_id == organization_id
                    for org_customer in org_customers
                ):
                    self._add_validation_error(
                        "Unauthorized access. Invalid user in organization."
                    )
##GENLearn[calculatedIsRowLevelOrganizationSecurityUsed=true]End
##GENTrainingBlock[caseFlowLogic_calculatedIsRowLevelOrganizationSecurityUsed]End

            if val is True:
                item = await BusObjFactory.create_from_code(
                    item.get_session_context(),  # type: ignore
                    item.get_parent_name(),  # type: ignore
                    item.get_parent_code()  # type: ignore
                )
