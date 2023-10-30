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
    # customer_id = factory.Sequence(lambda n: n)
    code = factory.LazyFunction(uuid.uuid4)
    insert_utc_date_time = factory.LazyFunction(datetime.datetime.utcnow)
    last_update_utc_date_time = factory.LazyFunction(datetime.datetime.utcnow)
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
    tac_id = factory.LazyAttribute(lambda obj: obj.tac.tac_id)
    utc_offset_in_minutes = Faker('random_int')
    zip = Faker('sentence', nb_words=4)
    @classmethod
    def _build(cls, model_class, session, *args, **kwargs):
        tac_instance = TacFactory.create(session)  #TacID
        kwargs["tac"] = tac_instance
        kwargs["flavor"] = flavor_instance
#endset
        obj = model_class(*args, **kwargs)
        session.add(obj)
        # session.commit()
        return obj
    @classmethod
    def _create(cls, model_class, session, *args, **kwargs):
        tac_instance = TacFactory.create(session)  #TacID
        kwargs["tac"] = tac_instance
        kwargs["flavor"] = flavor_instance
#endset
        obj = model_class(*args, **kwargs)
        session.add(obj)
        session.commit()
        return obj
    @classmethod
    async def create_async(cls, model_class, session, *args, **kwargs):
        tac_instance = await TacFactory.create_async(session)  #TacID
        kwargs["tac"] = tac_instance
        kwargs["flavor"] = flavor_instance
#endset
        obj = model_class(*args, **kwargs)
        async with session.begin():
            session.add(obj)
        await session.flush()
        return obj
    @classmethod
    async def build_async(cls, model_class, session, *args, **kwargs):
        tac_instance = await TacFactory.create_async(session)  #TacID
        kwargs["tac"] = tac_instance
        kwargs["flavor"] = flavor_instance
#endset
        obj = model_class(*args, **kwargs)
        async with session.begin():
            session.add(obj)
        # await session.flush()
        return obj
