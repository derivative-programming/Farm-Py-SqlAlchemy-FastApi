# farm/models/factories.py
from datetime import timezone
import uuid
import factory
import random
from factory.alchemy import SQLAlchemyModelFactory
from factory import Faker, SubFactory
import pytz
from models import Land
from managers import LandEnum
from pac import PacFactory #pac_id
class LandFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Land
        sqlalchemy_session_persistence = "commit"  # Use "commit" or "flush".
    pac = SubFactory(PacFactory) #pac_id
#endset
    code = factory.LazyFunction(uuid.uuid4)
    insert_utc_date_time = factory.LazyFunction(timezone.now)
    last_update_utc_date_time = factory.LazyFunction(timezone.now)
    insert_user_id = factory.LazyFunction(uuid.uuid4)
    last_update_user_id = factory.LazyFunction(uuid.uuid4)
    last_change_code = factory.LazyFunction(uuid.uuid4)
    description = Faker('sentence', nb_words=4)
    display_order = Faker('random_int')
    is_active = Faker('boolean')
    lookup_enum_name = Faker('sentence', nb_words=4)
    name = Faker('sentence', nb_words=4)
    pac_id = pac.id # factory.SelfAttribute('pac.id')
