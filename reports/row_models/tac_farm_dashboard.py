import uuid
from pydantic import BaseModel, Field , UUID4
from decimal import Decimal
from datetime import datetime, date
from helpers.type_conversion import TypeConversion
class ReportItemTacFarmDashboard(BaseModel):
    field_one_plant_list_link_land_code: UUID4 =  uuid.UUID(int=0)
    conditional_btn_example_link_land_code: UUID4 =  uuid.UUID(int=0)
    is_conditional_btn_available: bool = False

    def load_data_provider_dict(self,data:dict):
            self.field_one_plant_list_link_land_code = TypeConversion.get_uuid(data["field_one_plant_list_link_land_code"])
            self.conditional_btn_example_link_land_code = TypeConversion.get_uuid(data["conditional_btn_example_link_land_code"])
            self.is_conditional_btn_available = bool(data["is_conditional_btn_available"])

