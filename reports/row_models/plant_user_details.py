import uuid
from decimal import Decimal
from datetime import datetime, date
from helpers.type_conversion import TypeConversion
class ReportItemPlantUserDetails():
    flavor_name: str = ""
    is_delete_allowed: bool = False
    is_edit_allowed: bool = False
    other_flavor: str = ""
    some_big_int_val: int = 0
    some_bit_val: bool = False
    some_date_val: date = TypeConversion.get_default_date()
    some_decimal_val: Decimal = Decimal(0)
    some_email_address: str = ""
    some_float_val: float = 0.0
    some_int_val: int = 0
    some_money_val: Decimal = Decimal(0)
    some_n_var_char_val: str = ""
    some_phone_number: str = ""
    some_text_val: str = ""
    some_uniqueidentifier_val: uuid.UUID =  uuid.UUID(int=0)
    some_utc_date_time_val: datetime = TypeConversion.get_default_date_time()
    some_var_char_val: str = ""
    phone_num_conditional_on_is_editable: str = ""
    n_var_char_as_url: str = ""
    update_button_text_link_plant_code: uuid.UUID =  uuid.UUID(int=0)
    random_property_updates_link_plant_code: uuid.UUID =  uuid.UUID(int=0)
    back_to_dashboard_link_tac_code: uuid.UUID =  uuid.UUID(int=0)

    def load_data_provider_dict(self, data: dict):
            self.flavor_name = str(data["flavor_name"])
            self.is_delete_allowed = bool(data["is_delete_allowed"])
            self.is_edit_allowed = bool(data["is_edit_allowed"])
            self.other_flavor = str(data["other_flavor"])
            self.some_big_int_val = int(data["some_big_int_val"])
            self.some_bit_val = bool(data["some_bit_val"])
            self.some_date_val = (data["some_date_val"])
            self.some_decimal_val = Decimal(data["some_decimal_val"])
            self.some_email_address = str(data["some_email_address"])
            self.some_float_val = float(data["some_float_val"])
            self.some_int_val = int(data["some_int_val"])
            self.some_money_val = Decimal(data["some_money_val"])
            self.some_n_var_char_val = str(data["some_n_var_char_val"])
            self.some_phone_number = str(data["some_phone_number"])
            self.some_text_val = str(data["some_text_val"])
            self.some_uniqueidentifier_val = TypeConversion.get_uuid(data["some_uniqueidentifier_val"])
            self.some_utc_date_time_val = (data["some_utc_date_time_val"])
            self.some_var_char_val = str(data["some_var_char_val"])
            self.phone_num_conditional_on_is_editable = str(data["phone_num_conditional_on_is_editable"])
            self.n_var_char_as_url = str(data["n_var_char_as_url"])
            self.update_button_text_link_plant_code = TypeConversion.get_uuid(data["update_button_text_link_plant_code"])
            self.random_property_updates_link_plant_code = TypeConversion.get_uuid(data["random_property_updates_link_plant_code"])
            self.back_to_dashboard_link_tac_code = TypeConversion.get_uuid(data["back_to_dashboard_link_tac_code"])

