import uuid
from pydantic import BaseModel, Field , UUID4
from decimal import Decimal
from datetime import datetime, date
from helpers.type_conversion import TypeConversion
class ReportItemPacUserRoleList(BaseModel):
    role_code: UUID4 =  uuid.UUID(int=0)
    role_description: str = ""
    role_display_order: int = 0
    role_is_active: bool = False
    role_lookup_enum_name: str = ""
    role_name: str = ""
    pac_name: str = ""

    def load_data_provider_dict(self,data:dict):
            self.role_code = UUID4(data["role_code"])
            self.role_description = str(data["role_description"])
            self.role_display_order = int(data["role_display_order"])
            self.role_is_active = bool(data["role_is_active"])
            self.role_lookup_enum_name = str(data["role_lookup_enum_name"])
            self.role_name = str(data["role_name"])
            self.pac_name = str(data["pac_name"])

