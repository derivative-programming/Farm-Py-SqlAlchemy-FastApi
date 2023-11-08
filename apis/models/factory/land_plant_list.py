# farm/models/factories.py
import uuid
import factory 
from factory import Faker
from models.factory import FlavorFactory #requestFlavorCode
from ..land_plant_list import LandPlantListGetModelRequest
from datetime import date, datetime
from decimal import Decimal
from pydantic import Field,UUID4
from sqlalchemy.ext.asyncio import AsyncSession

class LandPlantListGetModelRequestFactory(factory.base.Factory):
    class Meta:
        model = LandPlantListGetModelRequest
    flavor_code:UUID4 = uuid.UUID(int=0) 
    some_int_val:int = Faker('random_int')
    some_big_int_val:int = Faker('random_int')
    some_float_val:float = Faker('pyfloat', positive=True)
    some_bit_val:bool = Faker('boolean')
    is_edit_allowed:bool = Faker('boolean')
    is_delete_allowed:bool = Faker('boolean')
    some_decimal_val:Decimal = Faker('pydecimal', left_digits=5, right_digits=2, positive=True)
    some_min_utc_date_time_val:datetime = factory.LazyFunction(datetime.datetime.utcnow)
    some_min_date_val:date = Faker('date_object')
    some_money_val:Decimal = Faker('pydecimal', left_digits=5, right_digits=2, positive=True)
    some_n_var_char_val:str = Faker('sentence', nb_words=4)
    some_var_char_val:str = Faker('sentence', nb_words=4)
    some_text_val:str = Faker('text')
    some_phone_number:str = Faker('sentence', nb_words=4)
    some_email_address:str = Faker('sentence', nb_words=4)
    page_number = 1
    item_count_per_page = 1
    
    @classmethod
    def _build(cls, model_class, session=None, *args, **kwargs) -> LandPlantListGetModelRequest:

        if session is None:
                obj2 = model_class(*args, **kwargs)   
                return obj2
 
        request_flavor_code_instance = FlavorFactory.create(session=session) #requestFlavorCode  
#endset
 
        kwargs["request_flavor_code"] = request_flavor_code_instance.code #requestFlavorCode 
#endset

        obj = model_class(*args, **kwargs) 
          
        obj.request_flavor_code = request_flavor_code_instance.code #requestFlavorCode 
#endset  

        return obj
 
    @classmethod
    def _create(cls, model_class, session=None, *args, **kwargs) -> LandPlantListGetModelRequest:
 
        request_flavor_code_instance = FlavorFactory.create(session=session) #requestFlavorCode  
#endset
 
        kwargs["request_flavor_code"] = request_flavor_code_instance.code #requestFlavorCode 
#endset

        obj = model_class(*args, **kwargs) 
          
        obj.request_flavor_code = request_flavor_code_instance.code #requestFlavorCode 
#endset  
 
        return obj
    
    @classmethod
    async def create_async(cls, session:AsyncSession, *args, **kwargs) -> LandPlantListGetModelRequest:
  
        request_flavor_code_instance = await FlavorFactory.create_async(session=session) #requestFlavorCode 
#endset
  
        kwargs["request_flavor_code"] = request_flavor_code_instance.code #requestFlavorCode 
#endset

        obj = LandPlantListGetModelRequestFactory.build(session=None, *args, **kwargs)  
          
        obj.request_flavor_code = request_flavor_code_instance.code #requestFlavorCode 
#endset
 
        return obj 
