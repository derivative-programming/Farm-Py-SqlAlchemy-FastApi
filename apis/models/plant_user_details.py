# apis/models/plant_user_details.py
"""
    #TODO add comment
"""
import json
from typing import List
from datetime import date, datetime
import uuid
import logging
from typing import Optional
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import Field, UUID4
from business.plant import PlantBusObj
from helpers import TypeConversion
from reports.row_models.plant_user_details import ReportItemPlantUserDetails
from apis.models.list_model import ListModel
from helpers import SessionContext
from helpers.formatting import snake_to_camel
from models import Plant
from reports.plant_user_details import ReportManagerPlantUserDetails
from reports.report_request_validation_error import ReportRequestValidationError
from apis.models.validation_error import ValidationErrorItem
import apis.models as view_models
from models import Plant
from helpers.pydantic_serialization import CamelModel, SnakeModel, BaseModel
# request. expect camel case. use marshmallow to validate.
class PlantUserDetailsGetModelRequest(CamelModel):
    """
        #TODO add comment
    """
    page_number: int = Field(
        default=0,
        description="Page Number")
    item_count_per_page: int = Field(
        default=0,
        description="Item Count Per Page")
    order_by_column_name: str = Field(
        default="",
        description="Order By Column Name")
    order_by_descending: bool = Field(
        default=False,
        description="Order By Decending")
    force_error_message: str = Field(
        default="",
        description="Force Error Message")

# endset
    class Config:
        """
            #TODO add comment
        """
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
    def to_dict_snake(self):
        """
            #TODO add comment
        """
        data = self.model_dump()
        return data
    def to_dict_snake_serialized(self):
        """
            #TODO add comment
        """
        data = json.loads(self.model_dump_json())
        return data
    def to_dict_camel(self):
        """
            #TODO add comment
        """
        data = self.model_dump()
        return {snake_to_camel(k): v for k, v in data.items()}
    def to_dict_camel_serialized(self):
        """
            #TODO add comment
        """
        data = json.loads(self.model_dump_json())
        return {snake_to_camel(k): v for k, v in data.items()}
class PlantUserDetailsGetModelResponseItem(CamelModel):
    """
        #TODO add comment
    """
    flavor_name: str = Field(
        default="",
        description="Flavor Name")
    is_delete_allowed: bool = Field(
        default=False,
        description="Is Delete Allowed")
    is_edit_allowed: bool = Field(
        default=False,
        description="Is Edit Allowed")
    other_flavor: str = Field(
        default="",
        description="Other Flavor")
    some_big_int_val: int = Field(
        default=0,
        description="Some Big Int Val")
    some_bit_val: bool = Field(
        default=False,
        description="Some Bit Val")
    some_date_val: date = Field(
        default_factory=TypeConversion.get_default_date,
        description="Some Date Val")
    some_decimal_val: Decimal = Field(
        default=Decimal(0),
        description="Some Decimal Val")
    some_email_address: str = Field(
        default="",
        description="Some Email Address")
    some_float_val: float = Field(
        default=0,
        description="Some Float Val")
    some_int_val: int = Field(
        default=0,
        description="Some Int Val")
    some_money_val: Decimal = Field(
        default=Decimal(0),
        description="Some Money Val")
    some_n_var_char_val: str = Field(
        default="",
        description="Some N Var Char Val")
    some_phone_number: str = Field(
        default="",
        description="Some Phone Number")
    some_text_val: str = Field(
        default="",
        description="Some Text Val")
    some_uniqueidentifier_val: UUID4 = Field(
        default_factory=lambda: uuid.UUID(
            '00000000-0000-0000-0000-000000000000'
        ),
        description="Some Uniqueidentifier Val")
    some_utc_date_time_val: datetime = Field(
        default_factory=TypeConversion.get_default_date_time,
        description="Some UTC Date Time Val")
    some_var_char_val: str = Field(
        default="",
        description="Some Var Char Val")
    phone_num_conditional_on_is_editable: str = Field(
        default="",
        description="Phone Num Conditional On Is Editable")
    n_var_char_as_url: str = Field(
        default="",
        description="N Var Char As Url")
    update_button_text_link_plant_code: UUID4 = Field(
        default_factory=lambda: uuid.UUID(
            '00000000-0000-0000-0000-000000000000'
        ),
        description="Update Button Text Link Plant Code")
    random_property_updates_link_plant_code: UUID4 = Field(
        default_factory=lambda: uuid.UUID(
            '00000000-0000-0000-0000-000000000000'
        ),
        description="Random Property Updates Link Plant Code")
    back_to_dashboard_link_tac_code: UUID4 = Field(
        default_factory=lambda: uuid.UUID(
            '00000000-0000-0000-0000-000000000000'
        ),
        description="Back To Dashboard Link Tac Code")
# endset
    def load_report_item(self, data: ReportItemPlantUserDetails):
        """
            #TODO add comment
        """
        self.flavor_name = (
            data.flavor_name)
        self.is_delete_allowed = (
            data.is_delete_allowed)
        self.is_edit_allowed = (
            data.is_edit_allowed)
        self.other_flavor = (
            data.other_flavor)
        self.some_big_int_val = (
            data.some_big_int_val)
        self.some_bit_val = (
            data.some_bit_val)
        self.some_date_val = (
            data.some_date_val)
        self.some_decimal_val = (
            data.some_decimal_val)
        self.some_email_address = (
            data.some_email_address)
        self.some_float_val = (
            data.some_float_val)
        self.some_int_val = (
            data.some_int_val)
        self.some_money_val = (
            data.some_money_val)
        self.some_n_var_char_val = (
            data.some_n_var_char_val)
        self.some_phone_number = (
            data.some_phone_number)
        self.some_text_val = (
            data.some_text_val)
        self.some_uniqueidentifier_val = (
            data.some_uniqueidentifier_val)
        self.some_utc_date_time_val = (
            data.some_utc_date_time_val)
        self.some_var_char_val = (
            data.some_var_char_val)
        self.phone_num_conditional_on_is_editable = (
            data.phone_num_conditional_on_is_editable)
        self.n_var_char_as_url = (
            data.n_var_char_as_url)
        self.update_button_text_link_plant_code = (
            data.update_button_text_link_plant_code)
        self.random_property_updates_link_plant_code = (
            data.random_property_updates_link_plant_code)
        self.back_to_dashboard_link_tac_code = (
            data.back_to_dashboard_link_tac_code)
# endset
class PlantUserDetailsGetModelResponse(ListModel):
    """
        #TODO add comment
    """
    request: PlantUserDetailsGetModelRequest = None
    items: List[PlantUserDetailsGetModelResponseItem] = Field(
        default_factory=list)
    async def process_request(
        self,
        session_context: SessionContext,
        plant_code: uuid,
        request: PlantUserDetailsGetModelRequest
    ):
        """
            #TODO add comment
        """
        try:
            logging.info("loading model...PlantUserDetailsGetModelResponse")
            generator = ReportManagerPlantUserDetails(session_context)
            logging.info("processing...PlantUserDetailsGetModelResponse")
            items = await generator.generate(
                    plant_code,

# endset
                    request.page_number,
                    request.item_count_per_page,
                    request.order_by_column_name,
                    request.order_by_descending)
            self.items = list()
            for item in items:
                report_item = PlantUserDetailsGetModelResponseItem()
                report_item.load_report_item(item)
                self.items.append(report_item)
            self.success = True
            self.message = "Success."
        except ReportRequestValidationError as ve:
            self.success = False
            self.message = "Validation Error..."
            self.validation_errors = list()
            for key in ve.error_dict:
                self.message = self.message + ve.error_dict[key] + ','
                validation_error = ValidationErrorItem()
                validation_error.property = snake_to_camel(key)
                validation_error.message = ve.error_dict[key]
                self.validation_errors.append(validation_error)
    def to_json(self):
        """
            #TODO add comment
        """
        return self.model_dump_json()
