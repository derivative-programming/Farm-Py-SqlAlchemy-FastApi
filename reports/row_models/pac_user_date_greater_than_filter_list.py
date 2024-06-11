# pac_user_date_greater_than_filter_list.py
"""
    #TODO add comment
"""
import uuid
from decimal import Decimal
from datetime import datetime, date
from helpers.type_conversion import TypeConversion
class ReportItemPacUserDateGreaterThanFilterList():
    date_greater_than_filter_code: uuid.UUID =  uuid.UUID(int=0)
    date_greater_than_filter_day_count: int = 0
    date_greater_than_filter_description: str = ""
    date_greater_than_filter_display_order: int = 0
    date_greater_than_filter_is_active: bool = False
    date_greater_than_filter_lookup_enum_name: str = ""
    date_greater_than_filter_name: str = ""

    def load_data_provider_dict(self, data: dict):
        self.date_greater_than_filter_code = TypeConversion.get_uuid(data["date_greater_than_filter_code"])
        self.date_greater_than_filter_day_count = int(data["date_greater_than_filter_day_count"])
        self.date_greater_than_filter_description = str(data["date_greater_than_filter_description"])
        self.date_greater_than_filter_display_order = int(data["date_greater_than_filter_display_order"])
        self.date_greater_than_filter_is_active = bool(data["date_greater_than_filter_is_active"])
        self.date_greater_than_filter_lookup_enum_name = str(data["date_greater_than_filter_lookup_enum_name"])
        self.date_greater_than_filter_name = str(data["date_greater_than_filter_name"])

