
from helpers.pydantic_serialization import CamelModel,SnakeModel


class ValidationError(CamelModel):
    property:str = ""
    message:str  = ""