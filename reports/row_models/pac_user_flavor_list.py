import uuid
from decimal import Decimal
from datetime import datetime, date
from helpers.type_conversion import TypeConversion
class ReportItemPacUserFlavorList():
    flavor_code: uuid.UUID =  uuid.UUID(int=0)
    flavor_description: str = ""
    flavor_display_order: int = 0
    flavor_is_active: bool = False
    flavor_lookup_enum_name: str = ""
    flavor_name: str = ""
    pac_name: str = ""

    def load_data_provider_dict(self, data: dict):
            self.flavor_code = TypeConversion.get_uuid(data["flavor_code"])
            self.flavor_description = str(data["flavor_description"])
            self.flavor_display_order = int(data["flavor_display_order"])
            self.flavor_is_active = bool(data["flavor_is_active"])
            self.flavor_lookup_enum_name = str(data["flavor_lookup_enum_name"])
            self.flavor_name = str(data["flavor_name"])
            self.pac_name = str(data["pac_name"])

