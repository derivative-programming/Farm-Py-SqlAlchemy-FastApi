"""
    #TODO add comment
"""
from datetime import datetime
import uuid
import factory
from factory import Faker
from models import Pac
from services.logging_config import get_logger

logger = get_logger(__name__)
class PacFactory(factory.Factory):
    """
    #TODO add comment
    """
    class Meta:
        """
        #TODO add comment
        """
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
# endset

# endset
    @classmethod
    def _build(cls, model_class, session=None, *args, **kwargs) -> Pac:
        """
        #TODO add comment
        """
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
    def _create(cls, model_class, session, *args, **kwargs) -> Pac:
        """
        #TODO add comment
        """
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
