from pydantic import BaseModel, Field
from typing import List
from decimal import Decimal
from datetime import datetime, date
from uuid import UUID
import uuid
class ReportItemPacUserFlavorList(BaseModel):
    flavor_code: UUID = Field(default_factory=lambda: uuid.UUID(int=0))
    flavor_description: str = ""
    flavor_display_order: int = 0
    flavor_is_active: bool = False
    flavor_lookup_enum_name: str = ""
    flavor_name: str = ""
    pac_name: str = ""

    def __init__(self):
        pass
    def load_data_provider_dict(self,data:dict):
            self.flavor_code = uuid.UUID(data["flavor_code"])
            self.flavor_description = str(data["flavor_description"])
            self.flavor_display_order = int(data["flavor_display_order"])
            self.flavor_is_active = bool(data["flavor_is_active"])
            self.flavor_lookup_enum_name = str(data["flavor_lookup_enum_name"])
            self.flavor_name = str(data["flavor_name"])
            self.pac_name = str(data["pac_name"])

