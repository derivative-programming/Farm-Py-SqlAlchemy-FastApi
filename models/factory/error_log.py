"""
    #TODO add comment
"""
import logging
from datetime import datetime
import uuid
import factory
from factory import Faker, SubFactory
import pytz
from models import ErrorLog
from services.logging_config import get_logger
from .pac import PacFactory  # pac_id
logger = get_logger(__name__)
class ErrorLogFactory(factory.Factory):
    class Meta:
        model = ErrorLog
    # error_log_id = factory.Sequence(lambda n: n)
    code = factory.LazyFunction(uuid.uuid4)
    last_change_code = 0
    insert_user_id = factory.LazyFunction(uuid.uuid4)
    last_update_user_id = factory.LazyFunction(uuid.uuid4)
    browser_code = factory.LazyFunction(uuid.uuid4)
    context_code = factory.LazyFunction(uuid.uuid4)
    created_utc_date_time = factory.LazyFunction(datetime.utcnow)  # Faker('date_time', tzinfo=pytz.utc)
    description = Faker('sentence', nb_words=4)
    is_client_side_error = Faker('boolean')
    is_resolved = Faker('boolean')
    # pac_id = 0 #factory.LazyAttribute(lambda obj: obj.pac.pac_id)
    url = Faker('sentence', nb_words=4)
    insert_utc_date_time = factory.LazyFunction(datetime.utcnow)
    last_update_utc_date_time = factory.LazyFunction(datetime.utcnow)
    # endset
    pac_code_peek = factory.LazyFunction(uuid.uuid4)  # PacID
    @classmethod
    def _build(cls, model_class, session=None, *args, **kwargs) -> ErrorLog:
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
    def _create(cls, model_class, session=None, *args, **kwargs) -> ErrorLog:
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
    async def create_async(cls, session, *args, **kwargs) -> ErrorLog:
        """
            #TODO add comment
        """
        pac_id_pac_instance = await PacFactory.create_async(session=session)  # PacID
# endset
        kwargs["pac_id"] = pac_id_pac_instance.pac_id  # PacID
# endset
        kwargs["pac_code_peek"] = pac_id_pac_instance.code  # PacID
# endset
        obj = ErrorLogFactory.build(session=None, *args, **kwargs)
        obj.pac_id = pac_id_pac_instance.pac_id  # PacID
# endset
        obj.pac_code_peek = pac_id_pac_instance.code  # PacID
# endset
        session.add(obj)
        await session.flush()
        return obj
    @classmethod
    async def build_async(cls, session, *args, **kwargs) -> ErrorLog:
        """
            #TODO add comment
        """
        pac_id_pac_instance = await PacFactory.create_async(session=session)  # PacID
# endset
        kwargs["pac_id"] = pac_id_pac_instance.pac_id  # PacID
# endset
        kwargs["pac_code_peek"] = pac_id_pac_instance.code  # PacID
# endset
        obj = ErrorLogFactory.build(session=None, *args, **kwargs)
        obj.pac_id = pac_id_pac_instance.pac_id  # PacID
# endset
        obj.pac_code_peek = pac_id_pac_instance.code  # PacID
# endset
        # session.add(obj)
        # await session.flush()
        return obj
