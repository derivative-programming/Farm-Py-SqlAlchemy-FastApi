from dataclasses import dataclass, field
from datetime import date, datetime
from decimal import Decimal
from apis.models import ValidationError
from typing import List
import uuid
from dataclasses_json import dataclass_json, LetterCase, config    
from helpers import TypeConversion 
from flows import FlowTacLoginInitObjWFResult 
from helpers import SessionContext 
from models import Tac 
from flows import FlowTacLoginInitObjWF 
from flows import FlowValidationError
import apis.models as view_models
import logging
from models import Tac 
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class TacLoginInitObjWFGetInitModelResponse():
    success:bool = False
    message:str = ""
    validation_errors:List[ValidationError] = field(default_factory=list)
    email:str = ""
    password:str = ""
#endset
    def load_flow_response(self,data:FlowTacLoginInitObjWFResult): 
        self.validation_errors = list()
        self.success = False
        self.message = ""
        self.email = data.email
        self.password = data.password
@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class TacLoginInitObjWFGetInitModelRequest():
    def process_request(self,
                        session_context:SessionContext,
                        tac_code:uuid,
                        response:TacLoginInitObjWFGetInitModelResponse) -> TacLoginInitObjWFGetInitModelResponse:
        try:
            logging.debug("loading model...")
            tac = Tac.objects.get(code=tac_code)
            logging.debug("process request...") 
            flow = FlowTacLoginInitObjWF(session_context)
            flowResponse = flow.process(
                tac
            )  
            response.load_flow_response(flowResponse); 
            response.success = True
            response.message = "Success."
        except FlowValidationError as ve:
            response.success = False 
            response.validation_errors = list()
            for key in ve.error_dict:
                response.validation_errors.append(view_models.ValidationError(key,ve.error_dict[key]))
        return response

