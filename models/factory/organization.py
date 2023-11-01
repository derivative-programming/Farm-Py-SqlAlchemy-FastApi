# farm/models/factories.py
import datetime
import uuid
import factory
from factory import Faker, SubFactory
import pytz
from models import Organization
from .tac import TacFactory #tac_id
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
class OrganizationFactory(factory.Factory):
    class Meta:
        model = Organization
    # organization_id = factory.Sequence(lambda n: n)
    code = factory.LazyFunction(generate_uuid)
    last_change_code = 0
    insert_user_id = factory.LazyFunction(generate_uuid)
    last_update_user_id = factory.LazyFunction(generate_uuid)
    name = Faker('sentence', nb_words=4)
    #tac_id = 0 #factory.LazyAttribute(lambda obj: obj.tac.tac_id)
    insert_utc_date_time = factory.LazyFunction(datetime.datetime.utcnow)
    last_update_utc_date_time = factory.LazyFunction(datetime.datetime.utcnow)

    tac_code_peek = factory.LazyFunction(generate_uuid) # TacID
    @classmethod
    def _build(cls, model_class, session, *args, **kwargs) -> Organization:
        tac_id_tac_instance = TacFactory.create(session=session)  #TacID

        kwargs["tac_id"] = tac_id_tac_instance.tac_id #TacID

        kwargs["tac_code_peek"] = tac_id_tac_instance.code #TacID

        obj = model_class(*args, **kwargs)
        obj.tac_id = tac_id_tac_instance.tac_id #TacID

        obj.tac_code_peek = tac_id_tac_instance.code #TacID

        session.add(obj)
        # session.commit()
        return obj
    @classmethod
    def _create(cls, model_class, session, *args, **kwargs) -> Organization:
        tac_id_tac_instance = TacFactory.create(session=session)  #TacID

        kwargs["tac_id"] = tac_id_tac_instance.tac_id #TacID

        kwargs["tac_code_peek"] = tac_id_tac_instance.code #TacID

        obj = model_class(*args, **kwargs)
        obj.tac_id = tac_id_tac_instance.tac_id #TacID

        obj.tac_code_peek = tac_id_tac_instance.code #TacID

        session.add(obj)
        session.commit()
        return obj
    @classmethod
    async def create_async(cls, session, *args, **kwargs) -> Organization:
        tac_id_tac_instance = await TacFactory.create_async(session=session)  #TacID

        kwargs["tac_id"] = tac_id_tac_instance.tac_id #TacID

        kwargs["tac_code_peek"] = tac_id_tac_instance.code #TacID

        obj = Organization(*args, **kwargs)
        obj.tac_id = tac_id_tac_instance.tac_id #TacID

        obj.tac_code_peek = tac_id_tac_instance.code #TacID

        session.add(obj)
        await session.flush()
        return obj
    @classmethod
    async def build_async(cls, session, *args, **kwargs) -> Organization:
        tac_id_tac_instance = await TacFactory.create_async(session=session)  #TacID

        kwargs["tac_id"] = tac_id_tac_instance.tac_id #TacID

        kwargs["tac_code_peek"] = tac_id_tac_instance.code #TacID

        obj = Organization(*args, **kwargs)
        obj.tac_id = tac_id_tac_instance.tac_id #TacID

        obj.tac_code_peek = tac_id_tac_instance.code #TacID

        session.add(obj)
        # await session.flush()
        return obj
