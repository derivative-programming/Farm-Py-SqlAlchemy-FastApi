# flows/default/land_plant_list_init_report.py  # pylint: disable=duplicate-code
# pylint: disable=unused-import
"""
This module contains the
FlowLandPlantListInitReport class
and related classes
that handle the addition of a
 to a specific
land in the flow process.
"""

import json
import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401

from business.land import LandBusObj
from flows.base import LogSeverity
from flows.base.land_plant_list_init_report import \
    BaseFlowLandPlantListInitReport
from helpers import SessionContext  # noqa: F401
from helpers import TypeConversion  # noqa: F401


class FlowLandPlantListInitReportResult():
    """
    Represents the result of the
    FlowLandPlantListInitReport process.
    """
    some_int_val: int = 0
    some_big_int_val: int = 0
    some_bit_val: bool = False
    is_edit_allowed: bool = False
    is_delete_allowed: bool = False
    some_float_val: float = 0
    some_decimal_val: Decimal = Decimal(0)
    some_min_utc_date_time_val: datetime = (
        TypeConversion.get_default_date_time())
    some_min_date_val: date = (
        TypeConversion.get_default_date())
    some_money_val: Decimal = Decimal(0)
    some_n_var_char_val: str = ""
    some_var_char_val: str = ""
    some_text_val: str = ""
    some_phone_number: str = ""
    some_email_address: str = ""
    flavor_code: uuid.UUID = uuid.UUID(int=0)
    land_code: uuid.UUID = uuid.UUID(int=0)
    tac_code: uuid.UUID = uuid.UUID(int=0)
    land_name: str = ""
    context_object_code: uuid.UUID = uuid.UUID(int=0)

    def __init__(self):
        """
        Initializes a new instance of the
        FlowLandPlantListInitReportResult class.
        """

    def to_json(self):
        """
        Converts the FlowLandPlantListInitReportResult
        instance to a JSON string.

        Returns:
            str: The JSON representation of the instance.
        """
        # Create a dictionary representation of the instance
        data = {
            'context_object_code':
                str(self.context_object_code),
            'some_int_val':
                self.some_int_val,
            'some_big_int_val':
                self.some_big_int_val,
            'some_bit_val':
                self.some_bit_val,
            'is_edit_allowed':
                self.is_edit_allowed,
            'is_delete_allowed':
                self.is_delete_allowed,
            'some_float_val':
                self.some_float_val,
            'some_decimal_val':
                str(self.some_decimal_val),
            'some_min_utc_date_time_val':
                self.some_min_utc_date_time_val.isoformat(),
            'some_min_date_val':
                self.some_min_date_val.isoformat(),
            'some_money_val':
                str(self.some_money_val),
            'some_n_var_char_val':
                self.some_n_var_char_val,
            'some_var_char_val':
                self.some_var_char_val,
            'some_text_val':
                self.some_text_val,
            'some_phone_number':
                self.some_phone_number,
            'some_email_address':
                self.some_email_address,
            'flavor_code':
                str(self.flavor_code),
            'land_code':
                str(self.land_code),
            'tac_code':
                str(self.tac_code),
            'land_name':
                self.land_name,
# endset  # noqa: E122
        }
        # Serialize the dictionary to JSON
        return json.dumps(data)


class FlowLandPlantListInitReport(
    BaseFlowLandPlantListInitReport
):
    """
    FlowLandPlantListInitReport handles the addition of
    a  to
    a specific land in the flow process.

    This class extends the
    BaseFlowLandPlantListInitReportclass and
    initializes it with the provided session context.
    """

    async def process(
        self,
        land_bus_obj: LandBusObj,

# endset  # noqa: E122
    ) -> FlowLandPlantListInitReportResult:
        """
        Processes the addition of a
         to a specific land.

        Returns:
            FlowLandPlantListInitReportResult:
                The result of the
                FlowLandPlantListInitReport process.
        """
        super()._log_message_and_severity(
            LogSeverity.INFORMATION_HIGH_DETAIL,
            "Start"
        )
        super()._log_message_and_severity(
            LogSeverity.INFORMATION_HIGH_DETAIL,
            "Code::" + str(land_bus_obj.code)
        )
        await super()._process_validation_rules(
            land_bus_obj,

# endset  # noqa: E122
        )
        super()._throw_queued_validation_errors()
        some_int_val_output: int = 0
        some_big_int_val_output: int = 0
        some_bit_val_output: bool = False
        is_edit_allowed_output: bool = False
        is_delete_allowed_output: bool = False
        some_float_val_output: float = 0
        some_decimal_val_output: Decimal = Decimal(0)
        some_min_utc_date_time_val_output: datetime = (
            TypeConversion.get_default_date_time())
        some_min_date_val_output: date = (
            TypeConversion.get_default_date())
        some_money_val_output: Decimal = Decimal(0)
        some_n_var_char_val_output: str = ""
        some_var_char_val_output: str = ""
        some_text_val_output: str = ""
        some_phone_number_output: str = ""
        some_email_address_output: str = ""
        flavor_code_output: uuid.UUID = uuid.UUID(int=0)
        land_code_output: uuid.UUID = uuid.UUID(int=0)
        tac_code_output: uuid.UUID = uuid.UUID(int=0)
        land_name_output: str = ""
        flavor_bus_obj = business.FlavorBusObj(
            land_bus_obj.get_session_context())
        await flavor_bus_obj.load_from_enum(
            flavor_enum=farm_managers.FlavorEnum.UNKNOWN)
        flavor_code_output = flavor_bus_obj.code

        land_code_output = land_bus_obj.code

        tac_code_output = self._session_context.tac_code


        super()._log_message_and_severity(
            LogSeverity.INFORMATION_HIGH_DETAIL,
            "Building result")
        result = FlowLandPlantListInitReportResult()
        result.context_object_code = land_bus_obj.code
        result.some_int_val = (
            some_int_val_output)
        result.some_big_int_val = (
            some_big_int_val_output)
        result.some_bit_val = (
            some_bit_val_output)
        result.is_edit_allowed = (
            is_edit_allowed_output)
        result.is_delete_allowed = (
            is_delete_allowed_output)
        result.some_float_val = (
            some_float_val_output)
        result.some_decimal_val = (
            some_decimal_val_output)
        result.some_min_utc_date_time_val = (
            some_min_utc_date_time_val_output)
        result.some_min_date_val = (
            some_min_date_val_output)
        result.some_money_val = (
            some_money_val_output)
        result.some_n_var_char_val = (
            some_n_var_char_val_output)
        result.some_var_char_val = (
            some_var_char_val_output)
        result.some_text_val = (
            some_text_val_output)
        result.some_phone_number = (
            some_phone_number_output)
        result.some_email_address = (
            some_email_address_output)
        result.flavor_code = (
            flavor_code_output)
        result.land_code = (
            land_code_output)
        result.tac_code = (
            tac_code_output)
        result.land_name = (
            land_name_output)
        super()._log_message_and_severity(
            LogSeverity.INFORMATION_HIGH_DETAIL,
            "Result:" + result.to_json())

        super()._log_message_and_severity(
            LogSeverity.INFORMATION_HIGH_DETAIL,
            "End")
        return result
