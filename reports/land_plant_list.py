import json
import csv
import uuid
from typing import List
from reports.providers.land_plant_list import ReportProviderLandPlantList
from reports.row_models.land_plant_list import ReportItemLandPlantList
import logging
from .report_request_validation_error import ReportRequestValidationError
from helpers import SessionContext
from datetime import date, datetime 
from decimal import Decimal 
from helpers import SessionContext,TypeConversion 
 

class ReportManagerLandPlantList():
    _session_context:SessionContext 
    def __init__(self, session_context:SessionContext):
        self._session_context = session_context
        if session_context.session is None:
            raise TypeError("ReportManagerLandPlantList.init session_context has no session assigned")
         
     
    async def generate(self, 
                land_code:uuid,
                some_int_val: int = 0,
                some_big_int_val: int = 0,
                some_bit_val: bool = False,
                is_edit_allowed: bool = False,
                is_delete_allowed: bool = False,
                some_float_val: float = 0,
                some_decimal_val: Decimal = Decimal(0),
                some_min_utc_date_time_val: datetime = TypeConversion.get_default_date_time(),
                some_min_date_val: date  = TypeConversion.get_default_date(),
                some_money_val: Decimal = Decimal(0),
                some_n_var_char_val: str = "",
                some_var_char_val: str = "",
                some_text_val: str = "",
                some_phone_number: str = "",
                some_email_address: str = "",
                flavor_code: uuid = uuid.UUID(int=0),
#endset
                page_number:int = 1,
                item_count_per_page:int = 1,
                order_by_column_name:str ="",
                order_by_descending:bool = False,
                ) -> List[ReportItemLandPlantList]:
        logging.info('ReportManagerLandPlantList.generate Start')

        role_required = "User"

        if len(role_required) > 0:
            if role_required not in self._session_context.role_name_csv:
                raise ReportRequestValidationError("","Unautorized access. " + role_required + " role not found.") 



        if item_count_per_page <= 0:
            raise ReportRequestValidationError("item_count_per_page","Minimum count per page is 1")
        
        if page_number <= 0:
            raise ReportRequestValidationError("page_number","Minimum page number is 1")
        
        provider = ReportProviderLandPlantList(self._session_context)

        dataList = await provider.generate_list(
            land_code,
            some_int_val, 
            some_big_int_val,
            some_bit_val,
            is_edit_allowed,
            is_delete_allowed,
            some_float_val,
            some_decimal_val, 
            some_min_utc_date_time_val,
            some_min_date_val,
            some_money_val, 
            some_n_var_char_val,
            some_var_char_val,
            some_text_val,
            some_phone_number,
            some_email_address,
            flavor_code, 
#endset
            page_number,
            item_count_per_page,
            order_by_column_name,
            order_by_descending,
            )

        result = list()
 
        for dataItem in dataList:
            reportItem:ReportItemLandPlantList = ReportItemLandPlantList()
            reportItem.load_data_provider_dict(dataItem)
            result.append(reportItem) 
            
        logging.info("ReportManagerLandPlantList.generate Results: " + json.dumps(dataList))

        logging.info('ReportManagerLandPlantList.generate End')
        return result
     

    async def build_csv(self, file_name:str, data_list:List[ReportItemLandPlantList]):
        with open(file_name, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=vars(ReportItemLandPlantList()).keys(), quoting=csv.QUOTE_ALL)
            writer.writeheader()

            for obj in data_list:
                writer.writerow(obj.__dict__)


    def _parse_bool(self, value):
        return value.lower() in ['true', '1', 'yes']
    
    async def read_csv(self, file_name:str) -> List[ReportItemLandPlantList]:
        objects = []    
        with open(file_name, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                obj = ReportItemLandPlantList()
                for key, value in row.items():
                    if value is not None and value != '':
                        if hasattr(obj, key):
                            # Convert the value to the correct type based on the attribute
                            attr_type = type(getattr(obj, key))
                            if attr_type == int:
                                setattr(obj, key, int(value))
                            elif attr_type == bool:
                                setattr(obj, key, self.parse_bool(value))
                            elif attr_type == float:
                                setattr(obj, key, float(value))
                            elif attr_type == Decimal:
                                setattr(obj, key, Decimal(value))
                            elif attr_type == datetime:
                                setattr(obj, key, datetime.fromisoformat(value))
                            elif attr_type == date:
                                setattr(obj, key, date.fromisoformat(value))
                            elif attr_type == uuid.UUID:
                                setattr(obj, key, uuid.UUID(value))
                            else:
                                setattr(obj, key, value)
                objects.append(obj)

        return objects