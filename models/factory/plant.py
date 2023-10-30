# farm/models/factories.py
from datetime import timezone
import uuid
import factory
import random
from factory.alchemy import SQLAlchemyModelFactory
from factory import Faker, SubFactory
import pytz
from models import Plant
from flavor import FlavorFactory #flvr_foreign_key_id
from land import LandFactory #land_id
class PlantFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Plant
        sqlalchemy_session_persistence = "commit"  # Use "commit" or "flush". 

    land = SubFactory(LandFactory) #land_id
    flvr_foreign_key = SubFactory(FlavorFactory) #flvr_foreign_key_id
#endset

    code = factory.LazyFunction(uuid.uuid4)
    insert_utc_date_time = factory.LazyFunction(timezone.now)
    last_update_utc_date_time = factory.LazyFunction(timezone.now)
    insert_user_id = factory.LazyFunction(uuid.uuid4)
    last_update_user_id = factory.LazyFunction(uuid.uuid4)
    last_change_code = factory.LazyFunction(uuid.uuid4)
    flvr_foreign_key = flvr_foreign_key.id #flvr_foreign_key_id
    is_delete_allowed = Faker('boolean')
    is_edit_allowed = Faker('boolean')
    land_id = land.id # factory.SelfAttribute('land.id') 
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
 