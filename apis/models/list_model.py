
from helpers.pydantic_serialization import CamelModel,SnakeModel

 

### response 
class ListModel(CamelModel):
    page_number:int = 0
    item_count_per_page:int = 0
    order_by_column_name:str = ""
    order_by_descending:bool = False
    success:bool = False
    records_total:int = 0
    records_filtered:int = 0
    message:str = ""
    app_version:str = ""

