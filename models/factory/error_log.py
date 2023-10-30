# farm/models/factories.py
from datetime import timezone
import uuid
import factory
import random
from factory.alchemy import SQLAlchemyModelFactory
from factory import Faker, SubFactory
import pytz
from models import ErrorLog
from managers import ErrorLogEnum
from pac import PacFactory #pac_id
class ErrorLogFactory(SQLAlchemyModelFactory):
    class Meta:
        model = ErrorLog
        sqlalchemy_session_persistence = "commit"  # Use "commit" or "flush".
    pac = SubFactory(PacFactory) #pac_id
#endset
    code = factory.LazyFunction(uuid.uuid4)
    insert_utc_date_time = factory.LazyFunction(timezone.now)
    last_update_utc_date_time = factory.LazyFunction(timezone.now)
    insert_user_id = factory.LazyFunction(uuid.uuid4)
    last_update_user_id = factory.LazyFunction(uuid.uuid4)
    last_change_code = factory.LazyFunction(uuid.uuid4)
    browser_code = factory.LazyFunction(uuid.uuid4)
    context_code = factory.LazyFunction(uuid.uuid4)
    created_utc_date_time = Faker('date_time', tzinfo=pytz.utc)
    description = Faker('sentence', nb_words=4)
    is_client_side_error = Faker('boolean')
    is_resolved = Faker('boolean')
    pac_id = pac.id # factory.SelfAttribute('pac.id')
    url = Faker('sentence', nb_words=4)
