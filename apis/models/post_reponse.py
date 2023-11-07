
from helpers.pydantic_serialization import CamelModel,SnakeModel
from .validation_error import ValidationError
from typing import List
from pydantic import Field

class PostResponse(CamelModel):
    success:bool = False
    message:str = ""
    validation_errors:List[ValidationError] = Field(default_factory=list)