
from helpers.pydantic_serialization import CamelModel,SnakeModel
from pydantic import Field


class ValidationErrorItem(CamelModel):
    property:str = Field(default="",description="Property")
    message:str  = Field(default="",description="Message")
     