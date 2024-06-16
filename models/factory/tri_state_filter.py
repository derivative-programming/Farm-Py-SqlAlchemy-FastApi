"""
    #TODO add comment
"""
from datetime import datetime
import uuid
import factory
from factory import Faker
from models import TriStateFilter
from services.logging_config import get_logger
from .pac import PacFactory  # pac_id
logger = get_logger(__name__)
class TriStateFilterFactory(factory.Factory):
    """
    #TODO add comment
    """
    class Meta:
        """
        #TODO add comment
        """
        model = TriStateFilter
    # tri_state_filter_id = factory.Sequence(lambda n: n)
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
    state_int_value = Faker('random_int')
# endset
    pac_code_peek = factory.LazyFunction(  # PacID
        uuid.uuid4
    )
# endset
    @classmethod
    def _build(cls, model_class, session=None, *args, **kwargs) -> TriStateFilter:
        """
        #TODO add comment
        """
        if session is None:
            obj2 = model_class(*args, **kwargs)
            return obj2
        pac_id_pac_instance = PacFactory.create(  # PacID
            session=session)
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
    def _create(cls, model_class, session, *args, **kwargs) -> TriStateFilter:
        """
        #TODO add comment
        """
        logger.info("factory create")
        pac_id_pac_instance = PacFactory.create(  # PacID
            session=session)
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
    async def create_async(cls, session, *args, **kwargs) -> TriStateFilter:
        """
            #TODO add comment
        """
        pac_id_pac_instance = await PacFactory.create_async(  # PacID
            session=session)
# endset
        kwargs["pac_id"] = (  # PacID
            pac_id_pac_instance.pac_id)
# endset
        kwargs["pac_code_peek"] = pac_id_pac_instance.code  # PacID
# endset
        obj = TriStateFilterFactory.build(session=None, *args, **kwargs)
        obj.pac_id = (  # PacID
            pac_id_pac_instance.pac_id)
# endset
        obj.pac_code_peek = pac_id_pac_instance.code  # PacID
# endset
        session.add(obj)
        await session.flush()
        return obj
    @classmethod
    async def build_async(cls, session, *args, **kwargs) -> TriStateFilter:
        """
            #TODO add comment
        """
        pac_id_pac_instance = await PacFactory.create_async(  # PacID
            session=session)
# endset
        kwargs["pac_id"] = (  # PacID
            pac_id_pac_instance.pac_id)
# endset
        kwargs["pac_code_peek"] = pac_id_pac_instance.code  # PacID
# endset
        obj = TriStateFilterFactory.build(session=None, *args, **kwargs)
        obj.pac_id = (  # PacID
            pac_id_pac_instance.pac_id)
# endset
        obj.pac_code_peek = pac_id_pac_instance.code  # PacID
# endset
        # session.add(obj)
        # await session.flush()
        return obj
