# farm/models/factories.py 
from datetime import datetime
import uuid
import factory 
from factory import Faker, SubFactory
import pytz
from models import Plant
from .flavor import FlavorFactory #flvr_foreign_key_id
from .land import LandFactory #land_id
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from services.db_config import db_dialect,generate_uuid
from sqlalchemy import String
from services.logging_config import get_logger

logger = get_logger(__name__)


# Conditionally set the UUID column type
if db_dialect == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif db_dialect == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  # This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)

class PlantFactory(factory.Factory):
    class Meta:
        model = Plant 
  
    # plant_id = factory.Sequence(lambda n: n)
    code = factory.LazyFunction(generate_uuid)
    last_change_code = 0
    insert_user_id = factory.LazyFunction(generate_uuid)
    last_update_user_id = factory.LazyFunction(generate_uuid)
    #flvr_foreign_key_id = 0 #factory.LazyAttribute(lambda obj: obj.flavor.flavor_id) 
    is_delete_allowed = Faker('boolean')
    is_edit_allowed = Faker('boolean')
    #land_id = 0 #factory.LazyAttribute(lambda obj: obj.land.land_id)
    other_flavor = Faker('sentence', nb_words=4)
    some_big_int_val = Faker('random_int')
    some_bit_val = Faker('boolean')
    some_date_val = Faker('date_object')
    some_decimal_val = Faker('pydecimal', left_digits=18, right_digits=6, positive=True)
    some_email_address = Faker('email')
    some_float_val = Faker('pyfloat', positive=True)
    some_int_val = Faker('random_int')
    some_money_val = Faker('pydecimal', left_digits=18, right_digits=2, positive=True)
    some_n_var_char_val = Faker('sentence', nb_words=4)
    some_phone_number = Faker('phone_number')
    some_text_val = Faker('text')
    some_uniqueidentifier_val = factory.LazyFunction(generate_uuid)
    some_utc_date_time_val = factory.LazyFunction(datetime.utcnow)#Faker('date_time', tzinfo=pytz.utc)
    some_var_char_val = Faker('sentence', nb_words=4)
    insert_utc_date_time = factory.LazyFunction(datetime.utcnow)
    last_update_utc_date_time = factory.LazyFunction(datetime.utcnow)
#endset
 
    flvr_foreign_key_code_peek = factory.LazyFunction(generate_uuid)  # FlvrForeignKeyID
    land_code_peek = factory.LazyFunction(generate_uuid) # LandID
 
    @classmethod
    def _build(cls, model_class, session=None, *args, **kwargs) -> Plant:

        if session is None:
                obj2 = model_class(*args, **kwargs)   
                return obj2

        land_id_land_instance = LandFactory.create(session=session)  #LandID 
        flvr_foreign_key_id_flavor_instance = FlavorFactory.create(session=session) #FlvrForeignKeyID 
#endset

        kwargs["land_id"] = land_id_land_instance.land_id #LandID 
        kwargs["flvr_foreign_key_id"] = flvr_foreign_key_id_flavor_instance.flavor_id #FlvrForeignKeyID 
#endset

        kwargs["land_code_peek"] = land_id_land_instance.code #LandID 
        kwargs["flvr_foreign_key_code_peek"] = flvr_foreign_key_id_flavor_instance.code #FlvrForeignKeyID 
#endset

        obj = model_class(*args, **kwargs) 
        
        obj.land_id = land_id_land_instance.land_id #LandID 
        obj.flvr_foreign_key_id = flvr_foreign_key_id_flavor_instance.flavor_id #FlvrForeignKeyID 
#endset
        obj.land_code_peek = land_id_land_instance.code #LandID 
        obj.flvr_foreign_key_code_peek = flvr_foreign_key_id_flavor_instance.code #FlvrForeignKeyID 
#endset


        session.add(obj) 
        # session.commit() 
        return obj
 
    @classmethod
    def _create(cls, model_class, session=None, *args, **kwargs) -> Plant:

        land_id_land_instance = LandFactory.create(session=session)  #LandID 
        flvr_foreign_key_id_flavor_instance = FlavorFactory.create(session=session) #FlvrForeignKeyID 
#endset

        kwargs["land_id"] = land_id_land_instance.land_id #LandID 
        kwargs["flvr_foreign_key_id"] = flvr_foreign_key_id_flavor_instance.flavor_id #FlvrForeignKeyID 
#endset

        kwargs["land_code_peek"] = land_id_land_instance.code #LandID 
        kwargs["flvr_foreign_key_code_peek"] = flvr_foreign_key_id_flavor_instance.code #FlvrForeignKeyID 
#endset

        obj = model_class(*args, **kwargs) 

        obj.land_id = land_id_land_instance.land_id #LandID 
        obj.flvr_foreign_key_id = flvr_foreign_key_id_flavor_instance.flavor_id #FlvrForeignKeyID 
#endset
        obj.land_code_peek = land_id_land_instance.code #LandID 
        obj.flvr_foreign_key_code_peek = flvr_foreign_key_id_flavor_instance.code #FlvrForeignKeyID 
#endset

        
        session.add(obj) 
        session.commit() 
        return obj
    
    @classmethod
    async def create_async(cls, session, *args, **kwargs) -> Plant:
 
        land_id_land_instance = await LandFactory.create_async(session=session)  #LandID 
        flvr_foreign_key_id_flavor_instance = await FlavorFactory.create_async(session=session) #FlvrForeignKeyID 
#endset

        kwargs["land_id"] = land_id_land_instance.land_id #LandID 
        kwargs["flvr_foreign_key_id"] = flvr_foreign_key_id_flavor_instance.flavor_id #FlvrForeignKeyID 
#endset

        kwargs["land_code_peek"] = land_id_land_instance.code #LandID 
        kwargs["flvr_foreign_key_code_peek"] = flvr_foreign_key_id_flavor_instance.code #FlvrForeignKeyID 
#endset

        obj = PlantFactory.build(session=None, *args, **kwargs)  
        
        obj.land_id = land_id_land_instance.land_id #LandID 
        obj.flvr_foreign_key_id = flvr_foreign_key_id_flavor_instance.flavor_id #FlvrForeignKeyID 
#endset
        obj.land_code_peek = land_id_land_instance.code #LandID 
        obj.flvr_foreign_key_code_peek = flvr_foreign_key_id_flavor_instance.code #FlvrForeignKeyID 
#endset

        session.add(obj) 
        await session.flush()
        return obj
    
    
    @classmethod
    async def build_async(cls, session, *args, **kwargs) -> Plant:
        
        land_id_land_instance = await LandFactory.create_async(session=session)  #LandID 
        flvr_foreign_key_id_flavor_instance = await FlavorFactory.create_async(session=session) #FlvrForeignKeyID 
#endset

        kwargs["land_id"] = land_id_land_instance.land_id #LandID 
        kwargs["flvr_foreign_key_id"] = flvr_foreign_key_id_flavor_instance.flavor_id #FlvrForeignKeyID 
#endset

        kwargs["land_code_peek"] = land_id_land_instance.code #LandID 
        kwargs["flvr_foreign_key_code_peek"] = flvr_foreign_key_id_flavor_instance.code #FlvrForeignKeyID 
#endset

        obj = PlantFactory.build(session=None, *args, **kwargs)  
        
        obj.land_id = land_id_land_instance.land_id #LandID 
        obj.flvr_foreign_key_id = flvr_foreign_key_id_flavor_instance.flavor_id #FlvrForeignKeyID 
#endset
        obj.land_code_peek = land_id_land_instance.code #LandID 
        obj.flvr_foreign_key_code_peek = flvr_foreign_key_id_flavor_instance.code #FlvrForeignKeyID 
#endset

        session.add(obj) 
        # await session.flush()
        return obj