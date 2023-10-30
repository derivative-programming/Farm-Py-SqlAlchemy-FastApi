# farm/models/factories.py
import datetime
import uuid
import factory
from factory import Faker, SubFactory
import pytz
from models import Customer
from .tac import TacFactory #tac_id
class CustomerFactory(factory.Factory):
    class Meta:
        model = Customer
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
    tac = SubFactory(TacFactory, session=factory.SelfAttribute('..session')) #tac_id
    utc_offset_in_minutes = Faker('random_int')
    zip = Faker('sentence', nb_words=4)
    @classmethod
    def _create(cls, model_class, session, *args, **kwargs):
        """Override the _create method to use the provided session."""
        obj = model_class(*args, **kwargs)
        session.add(obj)
        session.commit()
        return obj
