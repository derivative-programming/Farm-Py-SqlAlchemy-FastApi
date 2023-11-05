
import uuid
 
class SessionContext:
    user_name:str = "" 
    customer_code:uuid = uuid.UUID(int=0) 
    tac_code:uuid = uuid.UUID(int=0) 
    pac_code:uuid = uuid.UUID(int=0) 
    api_key_dict:dict = dict()
    session_code:uuid = uuid.UUID(int=0) 
    role_name_csv:str = ""

    def __init__(self, api_key_dict:dict) -> None:
        self.api_key_dict = api_key_dict
        self.session_code = uuid.uuid4()

    
    def check_context_code(self, 
                           context_code_name:str = "", 
                           context_code_value:uuid = uuid.UUID(int=0)) -> uuid:
        # if code dne or unknown then use the one in the api token
        if context_code_value == uuid.UUID(int=0) and self.api_key_dict[context_code_name] != None:
            return self.api_key_dict[context_code_name]
        
        if'CustomerCode' in self.api_key_dict:
            self.customer_code = self.api_key_dict['CustomerCode']
        
        if'TacCode' in self.api_key_dict:
            self.tac_code = self.api_key_dict['TacCode']
        
        if'PacCode' in self.api_key_dict:
            self.pac_code = self.api_key_dict['PacCode']
        
        if'UserName' in self.api_key_dict:
            self.user_name = self.api_key_dict['UserName'] 
            
        if'role_name_csv' in self.api_key_dict:
            self.role_name_csv = self.api_key_dict['role_name_csv'] 
        
        return context_code_value



        