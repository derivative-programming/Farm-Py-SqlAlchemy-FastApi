# farm/models/factories.py
from datetime import timezone
import uuid
import factory
import random
from factory.alchemy import SQLAlchemyModelFactory
from factory import Faker, SubFactory
import pytz
from models import Customer
from managers import CustomerEnum
from tac import TacFactory #tac_id
class CustomerFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Customer
        sqlalchemy_session_persistence = "commit"  # Use "commit" or "flush".
    tac = SubFactory(TacFactory) #tac_id
#endset
    code = factory.LazyFunction(uuid.uuid4)
    insert_utc_date_time = factory.LazyFunction(timezone.now)
    last_update_utc_date_time = factory.LazyFunction(timezone.now)
    insert_user_id = factory.LazyFunction(uuid.uuid4)
    last_update_user_id = factory.LazyFunction(uuid.uuid4)
    last_change_code = factory.LazyFunction(uuid.uuid4)
    active_organization_id = Faker('random_int')
    email = Faker('email')
    email_confirmed_utc_date_time = Faker('date_time', tzinfo=pytz.utc)
    first_name = Faker('sentence', nb_words=4)
    forgot_password_key_expiration_utc_date_time = Faker('date_time', tzinfo=pytz.utc)
    forgot_password_key_value = Faker('sentence', nb_words=4)
    fs_user_code_value = factory.LazyFunction(uuid.uuid4)
    is_active = Faker('boolean')
    is_email_allowed = Faker('boolean')
    is_email_confirmed = Faker('boolean')
    is_email_marketing_allowed = Faker('boolean')
    is_locked = Faker('boolean')
    is_multiple_organizations_allowed = Faker('boolean')
    is_verbose_logging_forced = Faker('boolean')
    last_login_utc_date_time = Faker('date_time', tzinfo=pytz.utc)
    last_name = Faker('sentence', nb_words=4)
    password = Faker('sentence', nb_words=4)
    phone = Faker('phone_number')
    province = Faker('sentence', nb_words=4)
    registration_utc_date_time = Faker('date_time', tzinfo=pytz.utc)
    tac_id = tac.id # factory.SelfAttribute('tac.id')
    utc_offset_in_minutes = Faker('random_int')
    zip = Faker('sentence', nb_words=4)
