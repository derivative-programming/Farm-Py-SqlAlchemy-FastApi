import uuid
from decimal import Decimal
from datetime import datetime, date
from helpers.type_conversion import TypeConversion
class ReportItemPacUserTacList():
    tac_code: uuid.UUID =  uuid.UUID(int=0)
    tac_description: str = ""
    tac_display_order: int = 0
    tac_is_active: bool = False
    tac_lookup_enum_name: str = ""
    tac_name: str = ""
    pac_name: str = ""

    def load_data_provider_dict(self, data: dict):
            self.tac_code = TypeConversion.get_uuid(data["tac_code"])
            self.tac_description = str(data["tac_description"])
            self.tac_display_order = int(data["tac_display_order"])
            self.tac_is_active = bool(data["tac_is_active"])
            self.tac_lookup_enum_name = str(data["tac_lookup_enum_name"])
            self.tac_name = str(data["tac_name"])
            self.pac_name = str(data["pac_name"])

