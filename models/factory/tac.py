# models/factory/tac.py
"""
This module contains the TacFactory class, which is responsible
for creating instances of the Tac model using the Factory pattern.
"""
from datetime import datetime
import uuid
import factory
from factory import Faker
from models import Tac
from services.logging_config import get_logger
from .pac import PacFactory  # pac_id
logger = get_logger(__name__)
class TacFactory(factory.Factory):
    """
    Factory class for creating instances of the Tac model.
    """
    class Meta:
        """
        #TODO add comment
        """
        model = Tac
    # tac_id = factory.Sequence(lambda n: n)
    code = factory.LazyFunction(uuid.uuid4)
    last_change_code = 0
    insert_user_id = factory.LazyFunction(uuid.uuid4)
    last_update_user_id = factory.LazyFunction(uuid.uuid4)
    description = Faker('sentence', nb_words=4)
    display_order = Faker('random_int')
    is_active = Faker('boolean')
    lookup_enum_name = Faker('sentence', nb_words=4)
    name = Faker('sentence', nb_words=4)
    # pac_id = 0
# endset
    pac_code_peek = factory.LazyFunction(  # PacID
        uuid.uuid4
    )
# endset
    @classmethod
    def _build(cls, model_class, session=None, *args, **kwargs) -> Tac:
        """
        #TODO add comment
        """
        if session is None:
            obj2 = model_class(*args, **kwargs)
            return obj2
        pac_id_pac_instance = (  # PacID
            PacFactory.create(session=session))
# endset
        kwargs["pac_id"] = (  # PacID
            pac_id_pac_instance.pac_id)
# endset
        kwargs["pac_code_peek"] = pac_id_pac_instance.code  # PacID
# endset
        obj = model_class(*args, **kwargs)
        obj.pac_id = (  # PacID
            pac_id_pac_instance.pac_id)
# endset
        obj.pac_code_peek = pac_id_pac_instance.code  # PacID
# endset
        # session.add(obj)
        # session.commit()
        return obj
    @classmethod
    def _create(cls, model_class, session, *args, **kwargs) -> Tac:
        """
        #TODO add comment
        """
        logger.info("factory create")
        pac_id_pac_instance = (  # PacID
            PacFactory.create(session=session))
# endset
        kwargs["pac_id"] = (  # PacID
            pac_id_pac_instance.pac_id)
# endset
        kwargs["pac_code_peek"] = pac_id_pac_instance.code  # PacID
# endset
        obj = model_class(*args, **kwargs)
        obj.pac_id = (  # PacID
            pac_id_pac_instance.pac_id)
# endset
        obj.pac_code_peek = pac_id_pac_instance.code  # PacID
# endset
        session.add(obj)
        session.commit()
        return obj
    @classmethod
    async def create_async(cls, session, *args, **kwargs) -> Tac:
        """
            #TODO add comment
        """
        pac_id_pac_instance = await (  # PacID
            PacFactory.create_async(session=session))
# endset
        kwargs["pac_id"] = (  # PacID
            pac_id_pac_instance.pac_id)
# endset
        kwargs["pac_code_peek"] = pac_id_pac_instance.code  # PacID
# endset
        obj = TacFactory.build(session=None, *args, **kwargs)
        obj.pac_id = (  # PacID
            pac_id_pac_instance.pac_id)
# endset
        obj.pac_code_peek = pac_id_pac_instance.code  # PacID
# endset
        session.add(obj)
        await session.flush()
        return obj
    @classmethod
    async def build_async(cls, session, *args, **kwargs) -> Tac:
        """
            #TODO add comment
        """
        pac_id_pac_instance = await (  # PacID
            PacFactory.create_async(session=session))
# endset
        kwargs["pac_id"] = (  # PacID
            pac_id_pac_instance.pac_id)
# endset
        kwargs["pac_code_peek"] = pac_id_pac_instance.code  # PacID
# endset
        obj = TacFactory.build(session=None, *args, **kwargs)
        obj.pac_id = (  # PacID
            pac_id_pac_instance.pac_id)
# endset
        obj.pac_code_peek = pac_id_pac_instance.code  # PacID
# endset
        # session.add(obj)
        # await session.flush()
        return obj
