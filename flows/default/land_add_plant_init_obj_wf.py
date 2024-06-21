# flows/default/land_add_plant_init_obj_wf.py
"""
This module contains the
FlowLandAddPlantInitObjWF class and related classes
that handle the addition of a
plant to a specific
land in the flow process.
"""
import uuid
import json
from datetime import date, datetime
from decimal import Decimal
from flows.base.land_add_plant_init_obj_wf import BaseFlowLandAddPlantInitObjWF
from flows.base import LogSeverity
from business.land import LandBusObj
from helpers import SessionContext
from helpers import TypeConversion
class FlowLandAddPlantInitObjWFResult():
    """
    Represents the result of the
    FlowLandAddPlantInitObjWF process.
    """
    context_object_code: uuid.UUID = uuid.UUID(int=0)
    request_flavor_code: uuid.UUID = uuid.UUID(int=0)
    request_other_flavor: str = ""
    request_some_int_val: int = 0
    request_some_big_int_val: int = 0
    request_some_bit_val: bool = False
    request_is_delete_allowed: bool = False
    request_is_edit_allowed: bool = False
    request_some_float_val: float = 0
    request_some_decimal_val: Decimal = Decimal(0)
    request_some_utc_date_time_val: datetime = (
        TypeConversion.get_default_date_time())
    request_some_date_val: date = (
        TypeConversion.get_default_date())
    request_some_money_val: Decimal = Decimal(0)
    request_some_n_var_char_val: str = ""
    request_some_var_char_val: str = ""
    request_some_text_val: str = ""
    request_some_phone_number: str = ""
    request_some_email_address: str = ""
    land_name: str = ""
    tac_code: uuid.UUID = uuid.UUID(int=0)
# endset
    def __init__(self):
        """
        Initializes a new instance of the
        FlowLandAddPlantInitObjWFResult class.
        """
    def to_json(self):
        """
        Converts the FlowLandAddPlantInitObjWFResult
        instance to a JSON string.
        Returns:
            str: The JSON representation of the instance.
        """
        # Create a dictionary representation of the instance
        data = {
            'context_object_code':
                str(self.context_object_code),
            'request_flavor_code':
                str(self.request_flavor_code),
            'request_other_flavor':
                self.request_other_flavor,
            'request_some_int_val':
                self.request_some_int_val,
            'request_some_big_int_val':
                self.request_some_big_int_val,
            'request_some_bit_val':
                self.request_some_bit_val,
            'request_is_delete_allowed':
                self.request_is_delete_allowed,
            'request_is_edit_allowed':
                self.request_is_edit_allowed,
            'request_some_float_val':
                self.request_some_float_val,
            'request_some_decimal_val':
                str(self.request_some_decimal_val),
            'request_some_utc_date_time_val':
                self.request_some_utc_date_time_val.isoformat(),
            'request_some_date_val':
                self.request_some_date_val.isoformat(),
            'request_some_money_val':
                str(self.request_some_money_val),
            'request_some_n_var_char_val':
                self.request_some_n_var_char_val,
            'request_some_var_char_val':
                self.request_some_var_char_val,
            'request_some_text_val':
                self.request_some_text_val,
            'request_some_phone_number':
                self.request_some_phone_number,
            'request_some_email_address':
                self.request_some_email_address,
            'land_name':
                self.land_name,
            'tac_code':
                str(self.tac_code),
# endset  # noqa: E122
        }
        # Serialize the dictionary to JSON
        return json.dumps(data)
class FlowLandAddPlantInitObjWF(BaseFlowLandAddPlantInitObjWF):
    """
    FlowLandAddPlantInitObjWF handles the addition of
    a plant to
    a specific land in the flow process.
    This class extends the BaseFlowLandAddPlantInitObjWF class and
    initializes it with the provided session context.
    """
    def __init__(self, session_context: SessionContext):
        """
        Initializes a new instance of the FlowLandAddPlantInitObjWF class.
        Args:
            session_context (SessionContext): The session
                context to be used for this flow.
        """
        super().__init__(session_context)
    async def process(
        self,
        land_bus_obj: LandBusObj,

# endset  # noqa: E122
    ) -> FlowLandAddPlantInitObjWFResult:
        """
        Processes the addition of a
        plant to a specific land.
        Returns:
            FlowLandAddPlantInitObjWFResult: The result of the
                FlowLandAddPlantInitObjWF process.
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
        request_flavor_code_output: uuid.UUID = uuid.UUID(int=0)
        request_other_flavor_output: str = ""
        request_some_int_val_output: int = 0
        request_some_big_int_val_output: int = 0
        request_some_bit_val_output: bool = False
        request_is_delete_allowed_output: bool = False
        request_is_edit_allowed_output: bool = False
        request_some_float_val_output: float = 0
        request_some_decimal_val_output: Decimal = Decimal(0)
        request_some_utc_date_time_val_output: datetime = (
            TypeConversion.get_default_date_time())
        request_some_date_val_output: date = (
            TypeConversion.get_default_date())
        request_some_money_val_output: Decimal = Decimal(0)
        request_some_n_var_char_val_output: str = ""
        request_some_var_char_val_output: str = ""
        request_some_text_val_output: str = ""
        request_some_phone_number_output: str = ""
        request_some_email_address_output: str = ""
        land_name_output: str = ""
        tac_code_output: uuid.UUID = uuid.UUID(int=0)
# endset
        # TODO: add flow logic

        super()._log_message_and_severity(
            LogSeverity.INFORMATION_HIGH_DETAIL,
            "Building result")
        result = FlowLandAddPlantInitObjWFResult()
        result.context_object_code = land_bus_obj.code
        result.request_flavor_code = (
            request_flavor_code_output)
        result.request_other_flavor = (
            request_other_flavor_output)
        result.request_some_int_val = (
            request_some_int_val_output)
        result.request_some_big_int_val = (
            request_some_big_int_val_output)
        result.request_some_bit_val = (
            request_some_bit_val_output)
        result.request_is_delete_allowed = (
            request_is_delete_allowed_output)
        result.request_is_edit_allowed = (
            request_is_edit_allowed_output)
        result.request_some_float_val = (
            request_some_float_val_output)
        result.request_some_decimal_val = (
            request_some_decimal_val_output)
        result.request_some_utc_date_time_val = (
            request_some_utc_date_time_val_output)
        result.request_some_date_val = (
            request_some_date_val_output)
        result.request_some_money_val = (
            request_some_money_val_output)
        result.request_some_n_var_char_val = (
            request_some_n_var_char_val_output)
        result.request_some_var_char_val = (
            request_some_var_char_val_output)
        result.request_some_text_val = (
            request_some_text_val_output)
        result.request_some_phone_number = (
            request_some_phone_number_output)
        result.request_some_email_address = (
            request_some_email_address_output)
        result.land_name = (
            land_name_output)
        result.tac_code = (
            tac_code_output)
# endset
        super()._log_message_and_severity(
            LogSeverity.INFORMATION_HIGH_DETAIL,
            "Result:" + result.to_json())
        super()._log_message_and_severity(
            LogSeverity.INFORMATION_HIGH_DETAIL,
            "End")
        return result
