# farm/models/factories.py 
import datetime
import uuid
import factory 
from factory import Faker, SubFactory
import pytz
from models import Plant
from .flavor import FlavorFactory #flvr_foreign_key_id
from .land import LandFactory #land_id

class PlantFactory(factory.Factory):
    class Meta:
        model = Plant 
  
    # plant_id = factory.Sequence(lambda n: n)
    code = factory.LazyFunction(uuid.uuid4)
    insert_utc_date_time = factory.LazyFunction(datetime.datetime.utcnow)
    last_update_utc_date_time = factory.LazyFunction(datetime.datetime.utcnow)
    insert_user_id = factory.LazyFunction(uuid.uuid4)
    last_update_user_id = factory.LazyFunction(uuid.uuid4)
    last_change_code = factory.LazyFunction(uuid.uuid4)
    flvr_foreign_key_id = factory.LazyAttribute(lambda obj: obj.flavor.flavor_id) 
    is_delete_allowed = Faker('boolean')
    is_edit_allowed = Faker('boolean')
    land_id = factory.LazyAttribute(lambda obj: obj.land.land_id)
    other_flavor = Faker('sentence', nb_words=4)
    some_big_int_val = Faker('random_int')
    some_bit_val = Faker('boolean')
    some_date_val = Faker('date_object')
    some_decimal_val = Faker('pydecimal', left_digits=5, right_digits=2, positive=True)
    some_email_address = Faker('email')
    some_float_val = Faker('pyfloat', positive=True)
    some_int_val = Faker('random_int')
    some_money_val = Faker('pydecimal', left_digits=5, right_digits=2, positive=True)
    some_n_var_char_val = Faker('sentence', nb_words=4)
    some_phone_number = Faker('phone_number')
    some_text_val = Faker('text')
    some_uniqueidentifier_val = factory.LazyFunction(uuid.uuid4)
    some_utc_date_time_val = Faker('date_time', tzinfo=pytz.utc)
    some_var_char_val = Faker('sentence', nb_words=4)
 
 
    @classmethod
    def _build(cls, model_class, session, *args, **kwargs):

        land_instance = LandFactory.create(session)  #LandID
        kwargs["land"] = land_instance
        
        flavor_instance = FlavorFactory.create(session) #FlvrForeignKeyID
        kwargs["flavor"] = flavor_instance
#endset

        obj = model_class(*args, **kwargs)
        session.add(obj) 
        # session.commit() 
        return obj
 
    @classmethod
    def _create(cls, model_class, session, *args, **kwargs):

        land_instance = LandFactory.create(session)  #LandID
        kwargs["land"] = land_instance
        
        flavor_instance = FlavorFactory.create(session) #FlvrForeignKeyID
        kwargs["flavor"] = flavor_instance
#endset

        obj = model_class(*args, **kwargs)
        session.add(obj) 
        session.commit() 
        return obj
    
    @classmethod
    async def create_async(cls, model_class, session, *args, **kwargs):
        
        land_instance = await LandFactory.create_async(session)  #LandID
        kwargs["land"] = land_instance
        
        flavor_instance = await FlavorFactory.create_async(session) #FlvrForeignKeyID
        kwargs["flavor"] = flavor_instance
#endset

        obj = model_class(*args, **kwargs)
        async with session.begin():
            session.add(obj) 
        await session.flush()
        return obj
    
    
    @classmethod
    async def build_async(cls, model_class, session, *args, **kwargs):
        
        land_instance = await LandFactory.create_async(session)  #LandID
        kwargs["land"] = land_instance
        
        flavor_instance = await FlavorFactory.create_async(session) #FlvrForeignKeyID
        kwargs["flavor"] = flavor_instance
#endset

        obj = model_class(*args, **kwargs)
        async with session.begin():
            session.add(obj) 
        # await session.flush()
        return obj