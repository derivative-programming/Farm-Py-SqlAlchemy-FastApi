import unittest 
import uuid
from flows.base import BaseFlowLandAddPlant
from helpers import SessionContext
from models.factories import LandFactory
from decimal import Decimal
from factory import Faker
from django.utils import timezone
from datetime import date, datetime
from models.factories import FlavorFactory #request_flavor_code
from models import CurrentRuntime


class BaseFlowLandAddPlantTestCase(unittest.TestCase):
    def setUp(self):
        CurrentRuntime.initialize()
        session_context = SessionContext(dict())
        self.flow = BaseFlowLandAddPlant(session_context)
    
    def test_process_validation_rules(self): 
        land = LandFactory.create()  
        request_flavor_code:uuid = FlavorFactory.create().code  
        request_other_flavor:str = ""    
        request_some_int_val:int = Faker('random_int')    
        request_some_big_int_val:int = Faker('random_int') 
        request_some_bit_val:bool = Faker('boolean')    
        request_is_edit_allowed:bool = Faker('boolean')    
        request_is_delete_allowed:bool = Faker('boolean')    
        request_some_float_val:float = Faker('pyfloat', positive=True) 
        request_some_decimal_val:Decimal = Faker('pydecimal', left_digits=5, right_digits=2, positive=True) 
        request_some_utc_date_time_val:datetime = Faker('date_time', tzinfo=timezone.utc)   
        request_some_date_val:date = Faker('date_object')    
        request_some_money_val:Decimal = Faker('pydecimal', left_digits=5, right_digits=2, positive=True)  
        request_some_n_var_char_val:str = Faker('sentence', nb_words=4)    
        request_some_var_char_val:str = Faker('sentence', nb_words=4)    
        request_some_text_val:str = Faker('text')  
        request_some_phone_number:str = Faker('phone_number')    
        request_some_email_address:str = Faker('email')    
        request_sample_image_upload_file:str = ""
        
        # Call the method being tested
        self.flow._process_validation_rules(
            land,
            request_flavor_code,    
            request_other_flavor,    
            request_some_int_val,   
            request_some_big_int_val,   
            request_some_bit_val,    
            request_is_edit_allowed,    
            request_is_delete_allowed,    
            request_some_float_val, 
            request_some_decimal_val,  
            request_some_utc_date_time_val,    
            request_some_date_val,    
            request_some_money_val,  
            request_some_n_var_char_val,    
            request_some_var_char_val,    
            request_some_text_val,    
            request_some_phone_number,    
            request_some_email_address,    
            request_sample_image_upload_file,
            )
        # Add assertions here to validate the expected behavior
        #TODO add validation checks - is required,  
        #TODO add validation checks - is email 
        #TODO add validation checks - is phone, 
        #TODO add validation checks - calculatedIsRowLevelCustomerSecurityUsed 
        #TODO add validation checks - calculatedIsRowLevelOrgCustomerSecurityUsed
        #TODO add validation checks - calculatedIsRowLevelOrganizationSecurityUsed
    
    def test_process_security_rules(self): 
        land = LandFactory.create() 
        
        # Call the method being tested
        self.flow._process_security_rules(land)
        
        # Add assertions here to validate the expected behavior
