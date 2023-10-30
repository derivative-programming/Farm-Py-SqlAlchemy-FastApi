# farm/models/factories.py
from datetime import timezone
import uuid
import factory
import random
from factory.alchemy import SQLAlchemyModelFactory
from factory import Faker, SubFactory
import pytz
from models import Organization
from managers import OrganizationEnum
from tac import TacFactory #tac_id
class OrganizationFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Organization
        sqlalchemy_session_persistence = "commit"  # Use "commit" or "flush".
    tac = SubFactory(TacFactory) #tac_id
#endset
    code = factory.LazyFunction(uuid.uuid4)
    insert_utc_date_time = factory.LazyFunction(timezone.now)
    last_update_utc_date_time = factory.LazyFunction(timezone.now)
    insert_user_id = factory.LazyFunction(uuid.uuid4)
    last_update_user_id = factory.LazyFunction(uuid.uuid4)
    last_change_code = factory.LazyFunction(uuid.uuid4)
    name = Faker('sentence', nb_words=4)
    tac_id = tac.id # factory.SelfAttribute('tac.id')
