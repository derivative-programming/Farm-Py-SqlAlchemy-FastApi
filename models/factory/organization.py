"""
    #TODO add comment
"""
import logging
from datetime import datetime
import uuid
import factory
from factory import Faker, SubFactory
import pytz
from models import Organization
from services.logging_config import get_logger
from .tac import TacFactory  # tac_id
logger = get_logger(__name__)
class OrganizationFactory(factory.Factory):
    class Meta:
        model = Organization
    # organization_id = factory.Sequence(lambda n: n)
    code = factory.LazyFunction(uuid.uuid4)
    last_change_code = 0
    insert_user_id = factory.LazyFunction(uuid.uuid4)
    last_update_user_id = factory.LazyFunction(uuid.uuid4)
    name = Faker('sentence', nb_words=4)
    # tac_id = 0 #factory.LazyAttribute(lambda obj: obj.tac.tac_id)
    insert_utc_date_time = factory.LazyFunction(datetime.utcnow)
    last_update_utc_date_time = factory.LazyFunction(datetime.utcnow)
    # endset
    tac_code_peek = factory.LazyFunction(uuid.uuid4)  # TacID
    @classmethod
    def _build(cls, model_class, session=None, *args, **kwargs) -> Organization:
        if session is None:
            obj2 = model_class(*args, **kwargs)
            return obj2
        tac_id_tac_instance = TacFactory.create(session=session)  # TacID
# endset
        kwargs["tac_id"] = tac_id_tac_instance.tac_id  # TacID
# endset
        kwargs["tac_code_peek"] = tac_id_tac_instance.code  # TacID
# endset
        obj = model_class(*args, **kwargs)
        obj.tac_id = tac_id_tac_instance.tac_id  # TacID
# endset
        obj.tac_code_peek = tac_id_tac_instance.code  # TacID
# endset
        # session.add(obj)
        # session.commit()
        return obj
    @classmethod
    def _create(cls, model_class, session=None, *args, **kwargs) -> Organization:
        logger.info("factory create")
        tac_id_tac_instance = TacFactory.create(session=session)  # TacID
# endset
        kwargs["tac_id"] = tac_id_tac_instance.tac_id  # TacID
# endset
        kwargs["tac_code_peek"] = tac_id_tac_instance.code  # TacID
# endset
        obj = model_class(*args, **kwargs)
        obj.tac_id = tac_id_tac_instance.tac_id  # TacID
# endset
        obj.tac_code_peek = tac_id_tac_instance.code  # TacID
# endset
        session.add(obj)
        session.commit()
        return obj
    @classmethod
    async def create_async(cls, session, *args, **kwargs) -> Organization:
        """
            #TODO add comment
        """
        tac_id_tac_instance = await TacFactory.create_async(session=session)  # TacID
# endset
        kwargs["tac_id"] = tac_id_tac_instance.tac_id  # TacID
# endset
        kwargs["tac_code_peek"] = tac_id_tac_instance.code  # TacID
# endset
        obj = OrganizationFactory.build(session=None, *args, **kwargs)
        obj.tac_id = tac_id_tac_instance.tac_id  # TacID
# endset
        obj.tac_code_peek = tac_id_tac_instance.code  # TacID
# endset
        session.add(obj)
        await session.flush()
        return obj
    @classmethod
    async def build_async(cls, session, *args, **kwargs) -> Organization:
        """
            #TODO add comment
        """
        tac_id_tac_instance = await TacFactory.create_async(session=session)  # TacID
# endset
        kwargs["tac_id"] = tac_id_tac_instance.tac_id  # TacID
# endset
        kwargs["tac_code_peek"] = tac_id_tac_instance.code  # TacID
# endset
        obj = OrganizationFactory.build(session=None, *args, **kwargs)
        obj.tac_id = tac_id_tac_instance.tac_id  # TacID
# endset
        obj.tac_code_peek = tac_id_tac_instance.code  # TacID
# endset
        # session.add(obj)
        # await session.flush()
        return obj
