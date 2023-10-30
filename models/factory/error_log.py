# farm/models/factories.py
import datetime
import uuid
import factory
from factory import Faker, SubFactory
import pytz
from models import ErrorLog
from .pac import PacFactory #pac_id
class ErrorLogFactory(factory.Factory):
    class Meta:
        model = ErrorLog
    # error_log_id = factory.Sequence(lambda n: n)
    code = factory.LazyFunction(uuid.uuid4)
    insert_utc_date_time = factory.LazyFunction(datetime.datetime.utcnow)
    last_update_utc_date_time = factory.LazyFunction(datetime.datetime.utcnow)
    insert_user_id = factory.LazyFunction(uuid.uuid4)
    last_update_user_id = factory.LazyFunction(uuid.uuid4)
    last_change_code = factory.LazyFunction(uuid.uuid4)
    browser_code = factory.LazyFunction(uuid.uuid4)
    context_code = factory.LazyFunction(uuid.uuid4)
    created_utc_date_time = Faker('date_time', tzinfo=pytz.utc)
    description = Faker('sentence', nb_words=4)
    is_client_side_error = Faker('boolean')
    is_resolved = Faker('boolean')
    pac_id = factory.LazyAttribute(lambda obj: obj.pac.pac_id)
    url = Faker('sentence', nb_words=4)
    @classmethod
    def _build(cls, model_class, session, *args, **kwargs):
        pac_instance = PacFactory.create(session)  #PacID
        kwargs["pac"] = pac_instance
        kwargs["flavor"] = flavor_instance
#endset
        obj = model_class(*args, **kwargs)
        session.add(obj)
        # session.commit()
        return obj
    @classmethod
    def _create(cls, model_class, session, *args, **kwargs):
        pac_instance = PacFactory.create(session)  #PacID
        kwargs["pac"] = pac_instance
        kwargs["flavor"] = flavor_instance
#endset
        obj = model_class(*args, **kwargs)
        session.add(obj)
        session.commit()
        return obj
    @classmethod
    async def create_async(cls, model_class, session, *args, **kwargs):
        pac_instance = await PacFactory.create_async(session)  #PacID
        kwargs["pac"] = pac_instance
        kwargs["flavor"] = flavor_instance
#endset
        obj = model_class(*args, **kwargs)
        async with session.begin():
            session.add(obj)
        await session.flush()
        return obj
    @classmethod
    async def build_async(cls, model_class, session, *args, **kwargs):
        pac_instance = await PacFactory.create_async(session)  #PacID
        kwargs["pac"] = pac_instance
        kwargs["flavor"] = flavor_instance
#endset
        obj = model_class(*args, **kwargs)
        async with session.begin():
            session.add(obj)
        # await session.flush()
        return obj
