# farm/models/factories.py
import datetime
import uuid
import factory
from factory import Faker, SubFactory
import pytz
from models import Organization
from .tac import TacFactory #tac_id
class OrganizationFactory(factory.Factory):
    class Meta:
        model = Organization
    # organization_id = factory.Sequence(lambda n: n)
    code = factory.LazyFunction(uuid.uuid4)
    insert_utc_date_time = factory.LazyFunction(datetime.datetime.utcnow)
    last_update_utc_date_time = factory.LazyFunction(datetime.datetime.utcnow)
    insert_user_id = factory.LazyFunction(uuid.uuid4)
    last_update_user_id = factory.LazyFunction(uuid.uuid4)
    last_change_code = factory.LazyFunction(uuid.uuid4)
    name = Faker('sentence', nb_words=4)
    tac_id = factory.LazyAttribute(lambda obj: obj.tac.tac_id)
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
