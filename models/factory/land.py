"""
    #TODO add comment
"""
import logging
from datetime import datetime
import uuid
import factory
from factory import Faker, SubFactory
import pytz
from models import Land
from services.logging_config import get_logger
from .pac import PacFactory  # pac_id
logger = get_logger(__name__)
class LandFactory(factory.Factory):
    class Meta:
        model = Land
    # land_id = factory.Sequence(lambda n: n)
    code = factory.LazyFunction(uuid.uuid4)
    last_change_code = 0
    insert_user_id = factory.LazyFunction(uuid.uuid4)
    last_update_user_id = factory.LazyFunction(uuid.uuid4)
    description = Faker('sentence', nb_words=4)
    display_order = Faker('random_int')
    is_active = Faker('boolean')
    lookup_enum_name = Faker('sentence', nb_words=4)
    name = Faker('sentence', nb_words=4)
    # pac_id = 0 #factory.LazyAttribute(lambda obj: obj.pac.pac_id)
    insert_utc_date_time = factory.LazyFunction(datetime.utcnow)
    last_update_utc_date_time = factory.LazyFunction(datetime.utcnow)
    # endset
    pac_code_peek = factory.LazyFunction(uuid.uuid4)  # PacID
    @classmethod
    def _build(cls, model_class, session=None, *args, **kwargs) -> Land:
        if session is None:
            obj2 = model_class(*args, **kwargs)
            return obj2
        pac_id_pac_instance = PacFactory.create(session=session)  # PacID
# endset
        kwargs["pac_id"] = pac_id_pac_instance.pac_id  # PacID
# endset
        kwargs["pac_code_peek"] = pac_id_pac_instance.code  # PacID
# endset
        obj = model_class(*args, **kwargs)
        obj.pac_id = pac_id_pac_instance.pac_id  # PacID
# endset
        obj.pac_code_peek = pac_id_pac_instance.code  # PacID
# endset
        # session.add(obj)
        # session.commit()
        return obj
    @classmethod
    def _create(cls, model_class, session=None, *args, **kwargs) -> Land:
        logger.info("factory create")
        pac_id_pac_instance = PacFactory.create(session=session)  # PacID
# endset
        kwargs["pac_id"] = pac_id_pac_instance.pac_id  # PacID
# endset
        kwargs["pac_code_peek"] = pac_id_pac_instance.code  # PacID
# endset
        obj = model_class(*args, **kwargs)
        obj.pac_id = pac_id_pac_instance.pac_id  # PacID
# endset
        obj.pac_code_peek = pac_id_pac_instance.code  # PacID
# endset
        session.add(obj)
        session.commit()
        return obj
    @classmethod
    async def create_async(cls, session, *args, **kwargs) -> Land:
        """
            #TODO add comment
        """
        pac_id_pac_instance = await PacFactory.create_async(session=session)  # PacID
# endset
        kwargs["pac_id"] = pac_id_pac_instance.pac_id  # PacID
# endset
        kwargs["pac_code_peek"] = pac_id_pac_instance.code  # PacID
# endset
        obj = LandFactory.build(session=None, *args, **kwargs)
        obj.pac_id = pac_id_pac_instance.pac_id  # PacID
# endset
        obj.pac_code_peek = pac_id_pac_instance.code  # PacID
# endset
        session.add(obj)
        await session.flush()
        return obj
    @classmethod
    async def build_async(cls, session, *args, **kwargs) -> Land:
        """
            #TODO add comment
        """
        pac_id_pac_instance = await PacFactory.create_async(session=session)  # PacID
# endset
        kwargs["pac_id"] = pac_id_pac_instance.pac_id  # PacID
# endset
        kwargs["pac_code_peek"] = pac_id_pac_instance.code  # PacID
# endset
        obj = LandFactory.build(session=None, *args, **kwargs)
        obj.pac_id = pac_id_pac_instance.pac_id  # PacID
# endset
        obj.pac_code_peek = pac_id_pac_instance.code  # PacID
# endset
        # session.add(obj)
        # await session.flush()
        return obj
