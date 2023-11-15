
from helpers.pydantic_serialization import CamelModel,SnakeModel
from pydantic import Field
from .validation_error import ValidationErrorItem
from typing import List
 

### response 
class ListModel(CamelModel):
    page_number:int = Field(default=0,description="Page Number")
    item_count_per_page:int = Field(default=0,description="Item Count Per Page")
    order_by_column_name:str = Field(default="",description="Order By Column Name")
    order_by_descending:bool = Field(default=False,description="Order By Descending")
    success:bool = Field(default=False,description="Success")
    records_total:int = Field(default=0,description="Records Total")
    records_filtered:int = Field(default=0,description="Records Filtered")
    message:str = Field(default="",description="Message")
    app_version:str = Field(default="",description="App Version") 
    validation_errors:List[ValidationErrorItem] = Field(default_factory=list, description="Validation Errors")

