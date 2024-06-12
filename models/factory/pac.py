"""
    #TODO add comment
"""
from datetime import datetime
import uuid
import factory
from factory import Faker, SubFactory
import pytz
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy import String
from models import Pac
from services.db_config import DB_DIALECT, generate_uuid
from services.logging_config import get_logger

logger = get_logger(__name__)
# Conditionally set the UUID column type
if DB_DIALECT == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif DB_DIALECT == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  # This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)
class PacFactory(factory.Factory):
    class Meta:
        model = Pac
    # pac_id = factory.Sequence(lambda n: n)
    code = factory.LazyFunction(generate_uuid)
    last_change_code = 0
    insert_user_id = factory.LazyFunction(generate_uuid)
    last_update_user_id = factory.LazyFunction(generate_uuid)
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

# endset

# endset

# endset
        obj = PacFactory.build(session=None, *args, **kwargs)

# endset

# endset
        # session.add(obj)
        # await session.flush()
        return obj
