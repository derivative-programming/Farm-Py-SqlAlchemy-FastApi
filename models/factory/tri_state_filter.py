# farm/models/factories.py
import datetime
import uuid
import factory
from factory import Faker, SubFactory
import pytz
from models import TriStateFilter
from .pac import PacFactory #pac_id
class TriStateFilterFactory(factory.Factory):
    class Meta:
        model = TriStateFilter
    # tri_state_filter_id = factory.Sequence(lambda n: n)
    code = factory.LazyFunction(uuid.uuid4)
    insert_utc_date_time = factory.LazyFunction(datetime.datetime.utcnow)
    last_update_utc_date_time = factory.LazyFunction(datetime.datetime.utcnow)
    insert_user_id = factory.LazyFunction(uuid.uuid4)
    last_update_user_id = factory.LazyFunction(uuid.uuid4)
    last_change_code = factory.LazyFunction(uuid.uuid4)
    description = Faker('sentence', nb_words=4)
    display_order = Faker('random_int')
    is_active = Faker('boolean')
    lookup_enum_name = Faker('sentence', nb_words=4)
    name = Faker('sentence', nb_words=4)
    pac_id = factory.LazyAttribute(lambda obj: obj.pac.pac_id)
    state_int_value = Faker('random_int')
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
