# apis/models/land_plant_list.py

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
from business.land import LandBusObj
from helpers import TypeConversion
from reports.row_models.land_plant_list import ReportItemLandPlantList
from apis.models.list_model import ListModel
from helpers import SessionContext
from helpers.formatting import snake_to_camel
from models import Land
from reports.land_plant_list import ReportManagerLandPlantList
from reports.report_request_validation_error import ReportRequestValidationError
from apis.models.validation_error import ValidationErrorItem
import apis.models as view_models
from models import Land
from helpers.pydantic_serialization import CamelModel, SnakeModel, BaseModel
# request. expect camel case. use marshmallow to validate.


class LandPlantListGetModelRequest(CamelModel):
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
    flavor_code: Optional[UUID4] = Field(
        default_factory=lambda: uuid.UUID(
            '00000000-0000-0000-0000-000000000000'
        ),
        description="Flavor Code")
    some_int_val: int = Field(
        default=0,
        description="Some Int Val")
    some_big_int_val: int = Field(
        default=0,
        description="Some Big Int Val")
    some_float_val: float = Field(
        default=0,
        description="Some Float Val")
    some_bit_val: bool = Field(
        default=False,
        description="Some Bit Val")
    is_edit_allowed: bool = Field(
        default=False,
        description="Is Edit Allowed")
    is_delete_allowed: bool = Field(
        default=False,
        description="Is Delete Allowed")
    some_decimal_val: Decimal = Field(
        default=Decimal(0),
        description="Some Decimal Val")
    some_min_utc_date_time_val: Optional[datetime] = Field(
        default_factory=TypeConversion.get_default_date_time,
        description="Some Min UTC Date Time Val")
    some_min_date_val: Optional[date] = Field(
        default_factory=TypeConversion.get_default_date,
        description="Some Min Date Val")
    some_money_val: Decimal = Field(
        default=Decimal(0),
        description="Some Money Val")
    some_n_var_char_val: str = Field(
        default="",
        description="Some N Var Char Val")
    some_var_char_val: str = Field(
        default="",
        description="Some Var Char Val")
    some_text_val: str = Field(
        default="",
        description="Some Text Val")
    some_phone_number: str = Field(
        default="",
        description="Some Phone Number")
    some_email_address: str = Field(
        default="",
        description="Some Email Address")
#endset

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


class LandPlantListGetModelResponseItem(CamelModel):
    """
        #TODO add comment
    """
    plant_code: UUID4 = Field(
        default_factory=lambda: uuid.UUID(
            '00000000-0000-0000-0000-000000000000'
        ),
        description="Plant Code")
    some_int_val: int = Field(
        default=0,
        description="Some Int Val")
    some_big_int_val: int = Field(
        default=0,
        description="Some Big Int Val")
    some_bit_val: bool = Field(
        default=False,
        description="Some Bit Val")
    is_edit_allowed: bool = Field(
        default=False,
        description="Is Edit Allowed")
    is_delete_allowed: bool = Field(
        default=False,
        description="Is Delete Allowed")
    some_float_val: float = Field(
        default=0,
        description="Some Float Val")
    some_decimal_val: Decimal = Field(
        default=Decimal(0),
        description="Some Decimal Val")
    some_utc_date_time_val: datetime = Field(
        default_factory=TypeConversion.get_default_date_time,
        description="Some UTC Date Time Val")
    some_date_val: date = Field(
        default_factory=TypeConversion.get_default_date,
        description="Some Date Val")
    some_money_val: Decimal = Field(
        default=Decimal(0),
        description="Some Money Val")
    some_n_var_char_val: str = Field(
        default="",
        description="Some N Var Char Val")
    some_var_char_val: str = Field(
        default="",
        description="Some Var Char Val")
    some_text_val: str = Field(
        default="",
        description="Some Text Val")
    some_phone_number: str = Field(
        default="",
        description="Some Phone Number")
    some_email_address: str = Field(
        default="",
        description="Some Email Address")
    flavor_name: str = Field(
        default="",
        description="Flavor Name")
    flavor_code: UUID4 = Field(
        default_factory=lambda: uuid.UUID(
            '00000000-0000-0000-0000-000000000000'
        ),
        description="Flavor Code")
    some_int_conditional_on_deletable: int = Field(
        default=0,
        description="Some Int Conditional On Deleteable")
    n_var_char_as_url: str = Field(
        default="",
        description="N Var Char As Url")
    update_link_plant_code: UUID4 = Field(
        default_factory=lambda: uuid.UUID(
            '00000000-0000-0000-0000-000000000000'
        ),
        description="Update Link Plant Code")
    delete_async_button_link_plant_code: UUID4 = Field(
        default_factory=lambda: uuid.UUID(
            '00000000-0000-0000-0000-000000000000'
        ),
        description="Delete Async Button Link Plant Code")
    details_link_plant_code: UUID4 = Field(
        default_factory=lambda: uuid.UUID(
            '00000000-0000-0000-0000-000000000000'
        ),
        description="Details Link Plant Code")
#endset

    def load_report_item(self, data: ReportItemLandPlantList):
        """
            #TODO add comment
        """
        self.plant_code = data.plant_code
        self.some_int_val = data.some_int_val
        self.some_big_int_val = data.some_big_int_val
        self.some_bit_val = data.some_bit_val
        self.is_edit_allowed = data.is_edit_allowed
        self.is_delete_allowed = data.is_delete_allowed
        self.some_float_val = data.some_float_val
        self.some_decimal_val = data.some_decimal_val
        self.some_utc_date_time_val = data.some_utc_date_time_val
        self.some_date_val = data.some_date_val
        self.some_money_val = data.some_money_val
        self.some_n_var_char_val = data.some_n_var_char_val
        self.some_var_char_val = data.some_var_char_val
        self.some_text_val = data.some_text_val
        self.some_phone_number = data.some_phone_number
        self.some_email_address = data.some_email_address
        self.flavor_name = data.flavor_name
        self.flavor_code = data.flavor_code
        self.some_int_conditional_on_deletable = data.some_int_conditional_on_deletable
        self.n_var_char_as_url = data.n_var_char_as_url
        self.update_link_plant_code = data.update_link_plant_code
        self.delete_async_button_link_plant_code = data.delete_async_button_link_plant_code
        self.details_link_plant_code = data.details_link_plant_code
#endset


class LandPlantListGetModelResponse(ListModel):
    """
        #TODO add comment
    """
    request: LandPlantListGetModelRequest = None
    items: List[LandPlantListGetModelResponseItem] = Field(
        default_factory=list)

    async def process_request(
        self,
        session_context: SessionContext,
        land_code: uuid,
        request: LandPlantListGetModelRequest
    ):
        """
            #TODO add comment
        """
        try:
            logging.info("loading model...LandPlantListGetModelResponse")
            generator = ReportManagerLandPlantList(session_context)
            logging.info("processing...LandPlantListGetModelResponse")
            items = await generator.generate(
                    land_code,
                    request.flavor_code,
                    request.some_int_val,
                    request.some_big_int_val,
                    request.some_float_val,
                    request.some_bit_val,
                    request.is_edit_allowed,
                    request.is_delete_allowed,
                    request.some_decimal_val,
                    request.some_min_utc_date_time_val,
                    request.some_min_date_val,
                    request.some_money_val,
                    request.some_n_var_char_val,
                    request.some_var_char_val,
                    request.some_text_val,
                    request.some_phone_number,
                    request.some_email_address,
#endset
                    request.page_number,
                    request.item_count_per_page,
                    request.order_by_column_name,
                    request.order_by_descending)
            self.items = list()
            for item in items:
                report_item = LandPlantListGetModelResponseItem()
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
