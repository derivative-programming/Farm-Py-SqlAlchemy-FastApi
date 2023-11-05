from pydantic import BaseModel, Field
from typing import List
from decimal import Decimal
from datetime import datetime, date
from uuid import UUID
import uuid
class ReportItemPacUserTriStateFilterList(BaseModel):
    tri_state_filter_code: UUID = Field(default_factory=lambda: uuid.UUID(int=0))
    tri_state_filter_description: str = ""
    tri_state_filter_display_order: int = 0
    tri_state_filter_is_active: bool = False
    tri_state_filter_lookup_enum_name: str = ""
    tri_state_filter_name: str = ""
    tri_state_filter_state_int_value: int = 0

    def __init__(self):
        pass
    def load_data_provider_dict(self,data:dict):
            self.tri_state_filter_code = uuid.UUID(data["tri_state_filter_code"])
            self.tri_state_filter_description = str(data["tri_state_filter_description"])
            self.tri_state_filter_display_order = int(data["tri_state_filter_display_order"])
            self.tri_state_filter_is_active = bool(data["tri_state_filter_is_active"])
            self.tri_state_filter_lookup_enum_name = str(data["tri_state_filter_lookup_enum_name"])
            self.tri_state_filter_name = str(data["tri_state_filter_name"])
            self.tri_state_filter_state_int_value = int(data["tri_state_filter_state_int_value"])

