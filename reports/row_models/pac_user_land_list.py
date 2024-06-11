# pac_user_land_list.py
"""
    #TODO add comment
"""
import uuid
from decimal import Decimal
from datetime import datetime, date
from helpers.type_conversion import TypeConversion
class ReportItemPacUserLandList():
    land_code: uuid.UUID =  uuid.UUID(int=0)
    land_description: str = ""
    land_display_order: int = 0
    land_is_active: bool = False
    land_lookup_enum_name: str = ""
    land_name: str = ""
    pac_name: str = ""

    def load_data_provider_dict(self, data: dict):
        self.land_code = TypeConversion.get_uuid(data["land_code"])
        self.land_description = str(data["land_description"])
        self.land_display_order = int(data["land_display_order"])
        self.land_is_active = bool(data["land_is_active"])
        self.land_lookup_enum_name = str(data["land_lookup_enum_name"])
        self.land_name = str(data["land_name"])
        self.pac_name = str(data["pac_name"])

