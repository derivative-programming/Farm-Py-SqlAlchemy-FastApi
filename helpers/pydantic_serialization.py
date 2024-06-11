# helpers/pydantic_serialization.py

"""
    #TODO add comment
"""

from pydantic import BaseModel
import re

def to_camel(string: str) -> str:
    # Split the string into words and combine them capitalizing the first letter of each word
    # except for the first word.
    return ''.join(word.capitalize() if i else word for i, word in enumerate(string.split('_')))


# CamelCase to snake_case converter
def to_snake(string: str) -> str:
    string = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', string)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', string).lower()

class CamelModel(BaseModel):
    class Config:
        alias_generator = to_camel
        # This will tell Pydantic to use the aliases in the generated schema
        # and when parsing and serializing data.
        populate_by_name = True

# Base model with alias_generator
class SnakeModel(BaseModel):
    class Config:
        alias_generator = to_snake
        populate_by_name = True
