# farm/models/factories.py
import datetime
import uuid
import factory
from factory import Faker, SubFactory
import pytz
from models import TriStateFilter
from .pac import PacFactory #pac_id
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from services.db_config import db_dialect,generate_uuid
from sqlalchemy import String
from services.logging_config import get_logger
logger = get_logger(__name__)
# Conditionally set the UUID column type
if db_dialect == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif db_dialect == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  # This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)
class TriStateFilterFactory(factory.Factory):
    class Meta:
        model = TriStateFilter
    # tri_state_filter_id = factory.Sequence(lambda n: n)
    code = factory.LazyFunction(generate_uuid)
    last_change_code = 0
    insert_user_id = factory.LazyFunction(generate_uuid)
    last_update_user_id = factory.LazyFunction(generate_uuid)
    description = Faker('sentence', nb_words=4)
    display_order = Faker('random_int')
    is_active = Faker('boolean')
    lookup_enum_name = Faker('sentence', nb_words=4)
    name = Faker('sentence', nb_words=4)
    #pac_id = 0 #factory.LazyAttribute(lambda obj: obj.pac.pac_id)
    state_int_value = Faker('random_int')
    insert_utc_date_time = factory.LazyFunction(datetime.datetime.utcnow)
    last_update_utc_date_time = factory.LazyFunction(datetime.datetime.utcnow)

    pac_code_peek = factory.LazyFunction(generate_uuid) # PacID
    @classmethod
    def _build(cls, model_class, session, *args, **kwargs) -> TriStateFilter:
        pac_id_pac_instance = PacFactory.create(session=session)  #PacID

        kwargs["pac_id"] = pac_id_pac_instance.pac_id #PacID

        kwargs["pac_code_peek"] = pac_id_pac_instance.code #PacID

        obj = model_class(*args, **kwargs)
        obj.pac_id = pac_id_pac_instance.pac_id #PacID

        obj.pac_code_peek = pac_id_pac_instance.code #PacID

        session.add(obj)
        # session.commit()
        return obj
    @classmethod
    def _create(cls, model_class, session, *args, **kwargs) -> TriStateFilter:
        pac_id_pac_instance = PacFactory.create(session=session)  #PacID

        kwargs["pac_id"] = pac_id_pac_instance.pac_id #PacID

        kwargs["pac_code_peek"] = pac_id_pac_instance.code #PacID

        obj = model_class(*args, **kwargs)
        obj.pac_id = pac_id_pac_instance.pac_id #PacID

        obj.pac_code_peek = pac_id_pac_instance.code #PacID

        session.add(obj)
        session.commit()
        return obj
    @classmethod
    async def create_async(cls, session, *args, **kwargs) -> TriStateFilter:
        pac_id_pac_instance = await PacFactory.create_async(session=session)  #PacID

        kwargs["pac_id"] = pac_id_pac_instance.pac_id #PacID

        kwargs["pac_code_peek"] = pac_id_pac_instance.code #PacID

        obj = TriStateFilter(*args, **kwargs)
        obj.pac_id = pac_id_pac_instance.pac_id #PacID

        obj.pac_code_peek = pac_id_pac_instance.code #PacID

        session.add(obj)
        await session.flush()
        return obj
    @classmethod
    async def build_async(cls, session, *args, **kwargs) -> TriStateFilter:
        pac_id_pac_instance = await PacFactory.create_async(session=session)  #PacID

        kwargs["pac_id"] = pac_id_pac_instance.pac_id #PacID

        kwargs["pac_code_peek"] = pac_id_pac_instance.code #PacID

        obj = TriStateFilter(*args, **kwargs)
        obj.pac_id = pac_id_pac_instance.pac_id #PacID

        obj.pac_code_peek = pac_id_pac_instance.code #PacID

        session.add(obj)
        # await session.flush()
        return obj