import uuid 
from decimal import Decimal
from datetime import datetime, date

from helpers.type_conversion import TypeConversion 

class ReportItemLandPlantList():
    plant_code:uuid.UUID =  uuid.UUID(int=0)
    some_int_val: int = 0
    some_big_int_val: int = 0
    some_bit_val: bool = False
    is_edit_allowed: bool = False
    is_delete_allowed: bool = False
    some_float_val: float = 0.0
    some_decimal_val: Decimal = Decimal(0)
    some_utc_date_time_val: datetime = TypeConversion.get_default_date_time()
    some_date_val: date = TypeConversion.get_default_date()
    some_money_val: Decimal = Decimal(0)
    some_n_var_char_val: str = ""
    some_var_char_val: str = ""
    some_text_val: str = ""
    some_phone_number: str = ""
    some_email_address: str = ""
    flavor_name: str = ""
    flavor_code: uuid.UUID =  uuid.UUID(int=0)
    some_int_conditional_on_deletable: int = 0
    n_var_char_as_url: str = ""
    update_link_plant_code: uuid.UUID =  uuid.UUID(int=0)
    delete_async_button_link_plant_code: uuid.UUID =  uuid.UUID(int=0)
    details_link_plant_code: uuid.UUID =  uuid.UUID(int=0)
#endset

    def load_data_provider_dict(self,data:dict):
            self.plant_code = TypeConversion.get_uuid(data["plant_code"])
            self.some_int_val = int(data["some_int_val"])
            self.some_big_int_val = int(data["some_big_int_val"])
            self.some_bit_val = bool(data["some_bit_val"])
            self.is_edit_allowed = bool(data["is_edit_allowed"])
            self.is_delete_allowed = bool(data["is_delete_allowed"])
            self.some_float_val = float(data["some_float_val"])
            self.some_decimal_val = Decimal(data["some_decimal_val"])
            self.some_utc_date_time_val = (data["some_utc_date_time_val"])
            self.some_date_val = (data["some_date_val"])
            self.some_money_val = Decimal(data["some_money_val"])
            self.some_n_var_char_val = str(data["some_n_var_char_val"])
            self.some_var_char_val = str(data["some_var_char_val"])
            self.some_text_val = str(data["some_text_val"])
            self.some_phone_number = str(data["some_phone_number"])
            self.some_email_address = str(data["some_email_address"])
            self.flavor_name = str(data["flavor_name"])
            self.flavor_code = TypeConversion.get_uuid(data["flavor_code"])
            self.some_int_conditional_on_deletable = int(data["some_int_conditional_on_deletable"])
            self.n_var_char_as_url = str(data["n_var_char_as_url"])
            self.update_link_plant_code = TypeConversion.get_uuid(data["update_link_plant_code"])
            self.delete_async_button_link_plant_code = TypeConversion.get_uuid(data["delete_async_button_link_plant_code"])
            self.details_link_plant_code = TypeConversion.get_uuid(data["details_link_plant_code"])
 