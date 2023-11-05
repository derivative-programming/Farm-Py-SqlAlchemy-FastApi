import uuid
from models import Tac 
from dataclasses import dataclass, asdict
# from dataclasses_json import dataclass_json,LetterCase
 
 
# @dataclass
class ReportRequestValidationError(Exception): 
    error_dict:dict
 

    def __init__(self, field_name:str, message:str):  
        if field_name is not None and message is not None: 
            self.error_dict = dict()
            self.error_dict[field_name] = message
            super().__init__(message)
        elif message is not None: 
            self.error_dict = dict()
            self.error_dict[""] = message
            super().__init__(message) 

 
 
    