import uuid
from models import Tac 
from dataclasses import dataclass, asdict
from dataclasses_json import dataclass_json,LetterCase 
 
 
@dataclass
class FlowValidationError(Exception): 
    error_dict:dict
 

    def __init__(self, field_name:str, message:str, error_dict:dict):  
        if error_dict is not None:
            self.error_dict = error_dict 
            message = next(iter(error_dict.values()))
            super().__init__(message)
        elif field_name is not None and message is not None: 
            self.error_dict = dict()
            self.error_dict[field_name] = message
            super().__init__(message)
        elif message is not None: 
            self.error_dict = dict()
            self.error_dict[""] = message
            super().__init__(message) 

 
 
    