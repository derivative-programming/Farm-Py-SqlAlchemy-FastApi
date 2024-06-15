"""
    #TODO add comment
"""
import logging
from datetime import datetime
import uuid
import factory
from factory import Faker, SubFactory
import pytz
from models import Pac
from services.logging_config import get_logger

logger = get_logger(__name__)
class PacFactory(factory.Factory):
    class Meta:
        model = Pac
    # pac_id = factory.Sequence(lambda n: n)
    code = factory.LazyFunction(uuid.uuid4)
    last_change_code = 0
    insert_user_id = factory.LazyFunction(uuid.uuid4)
    last_update_user_id = factory.LazyFunction(uuid.uuid4)
    description = Faker('sentence', nb_words=4)
    display_order = Faker('random_int')
    is_active = Faker('boolean')
    lookup_enum_name = Faker('sentence', nb_words=4)
    name = Faker('sentence', nb_words=4)
    insert_utc_date_time = factory.LazyFunction(datetime.utcnow)
    last_update_utc_date_time = factory.LazyFunction(datetime.utcnow)
    # endset

    @classmethod
    def _build(cls, model_class, session=None, *args, **kwargs) -> Pac:
        if session is None:
            obj2 = model_class(*args, **kwargs)
            return obj2

# endset

# endset

# endset
        obj = model_class(*args, **kwargs)

# endset

# endset
        # session.add(obj)
        # session.commit()
        return obj
    @classmethod
    def _create(cls, model_class, session=None, *args, **kwargs) -> Pac:
        logger.info("factory create")

# endset

# endset

# endset
        obj = model_class(*args, **kwargs)

# endset

# endset
        session.add(obj)
        session.commit()
        return obj
    @classmethod
    async def create_async(cls, session, *args, **kwargs) -> Pac:
        """
            #TODO add comment
        """

# endset

# endset

# endset
        obj = PacFactory.build(session=None, *args, **kwargs)

# endset

# endset
        session.add(obj)
        await session.flush()
        return obj
    @classmethod
    async def build_async(cls, session, *args, **kwargs) -> Pac:
        """
            #TODO add comment
        """

# endset

# endset

# endset
        obj = PacFactory.build(session=None, *args, **kwargs)

# endset

# endset
        # session.add(obj)
        # await session.flush()
        return obj
