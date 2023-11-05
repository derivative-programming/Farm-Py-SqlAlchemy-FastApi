from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import datetime, date
from uuid import UUID
import uuid
class ReportItemTacFarmDashboard(BaseModel):
    field_one_plant_list_link_land_code: UUID = Field(default_factory=lambda: uuid.UUID(int=0))
    conditional_btn_example_link_land_code: UUID = Field(default_factory=lambda: uuid.UUID(int=0))
    is_conditional_btn_available: bool = False

    # def __init__(self):
    #     pass
    def load_data_provider_dict(self,data:dict):
            self.field_one_plant_list_link_land_code = uuid.UUID(data["field_one_plant_list_link_land_code"])
            self.conditional_btn_example_link_land_code = uuid.UUID(data["conditional_btn_example_link_land_code"])
            self.is_conditional_btn_available = bool(data["is_conditional_btn_available"])

