# models/factory/customer.py
"""
    #TODO add comment
"""
from datetime import datetime
import uuid
import factory
from factory import Faker, SubFactory
import pytz
from models import Customer
from .tac import TacFactory  # tac_id
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from services.db_config import DB_DIALECT, generate_uuid
from sqlalchemy import String
from services.logging_config import get_logger
logger = get_logger(__name__)
# Conditionally set the UUID column type
if DB_DIALECT == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif DB_DIALECT == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  # This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)
class CustomerFactory(factory.Factory):
    class Meta:
        model = Customer
    # customer_id = factory.Sequence(lambda n: n)
    code = factory.LazyFunction(generate_uuid)
    last_change_code = 0
    insert_user_id = factory.LazyFunction(generate_uuid)
    last_update_user_id = factory.LazyFunction(generate_uuid)
    active_organization_id = Faker('random_int')
    email = Faker('email')
    email_confirmed_utc_date_time = factory.LazyFunction(datetime.utcnow)#Faker('date_time', tzinfo=pytz.utc)
    first_name = Faker('sentence', nb_words=4)
    forgot_password_key_expiration_utc_date_time = factory.LazyFunction(datetime.utcnow)#Faker('date_time', tzinfo=pytz.utc)
    forgot_password_key_value = Faker('sentence', nb_words=4)
    fs_user_code_value = factory.LazyFunction(generate_uuid)
    is_active = Faker('boolean')
    is_email_allowed = Faker('boolean')
    is_email_confirmed = Faker('boolean')
    is_email_marketing_allowed = Faker('boolean')
    is_locked = Faker('boolean')
    is_multiple_organizations_allowed = Faker('boolean')
    is_verbose_logging_forced = Faker('boolean')
    last_login_utc_date_time = factory.LazyFunction(datetime.utcnow)#Faker('date_time', tzinfo=pytz.utc)
    last_name = Faker('sentence', nb_words=4)
    password = Faker('sentence', nb_words=4)
    phone = Faker('phone_number')
    province = Faker('sentence', nb_words=4)
    registration_utc_date_time = factory.LazyFunction(datetime.utcnow)#Faker('date_time', tzinfo=pytz.utc)
    # tac_id = 0 #factory.LazyAttribute(lambda obj: obj.tac.tac_id)
    utc_offset_in_minutes = Faker('random_int')
    zip = Faker('sentence', nb_words=4)
    insert_utc_date_time = factory.LazyFunction(datetime.utcnow)
    last_update_utc_date_time = factory.LazyFunction(datetime.utcnow)

    tac_code_peek = factory.LazyFunction(generate_uuid) # TacID
    @classmethod
    def _build(cls, model_class, session = None, *args, **kwargs) -> Customer:
        if session is None:
                obj2 = model_class(*args, **kwargs)
                return obj2
        tac_id_tac_instance = TacFactory.create(session=session)   # TacID

        kwargs["tac_id"] = tac_id_tac_instance.tac_id  # TacID

        kwargs["tac_code_peek"] = tac_id_tac_instance.code  # TacID

        obj = model_class(*args, **kwargs)
        obj.tac_id = tac_id_tac_instance.tac_id  # TacID

        obj.tac_code_peek = tac_id_tac_instance.code  # TacID

        # session.add(obj)
        # session.commit()
        return obj
    @classmethod
    def _create(cls, model_class, session = None, *args, **kwargs) -> Customer:
        tac_id_tac_instance = TacFactory.create(session=session)   # TacID

        kwargs["tac_id"] = tac_id_tac_instance.tac_id  # TacID

        kwargs["tac_code_peek"] = tac_id_tac_instance.code  # TacID

        obj = model_class(*args, **kwargs)
        obj.tac_id = tac_id_tac_instance.tac_id  # TacID

        obj.tac_code_peek = tac_id_tac_instance.code  # TacID

        session.add(obj)
        session.commit()
        return obj
    @classmethod
    async def create_async(cls, session, *args, **kwargs) -> Customer:
        tac_id_tac_instance = await TacFactory.create_async(session=session)   # TacID

        kwargs["tac_id"] = tac_id_tac_instance.tac_id  # TacID

        kwargs["tac_code_peek"] = tac_id_tac_instance.code  # TacID

        obj = CustomerFactory.build(session = None, *args, **kwargs)
        obj.tac_id = tac_id_tac_instance.tac_id  # TacID

        obj.tac_code_peek = tac_id_tac_instance.code  # TacID

        session.add(obj)
        await session.flush()
        return obj
    @classmethod
    async def build_async(cls, session, *args, **kwargs) -> Customer:
        tac_id_tac_instance = await TacFactory.create_async(session=session)   # TacID

        kwargs["tac_id"] = tac_id_tac_instance.tac_id  # TacID

        kwargs["tac_code_peek"] = tac_id_tac_instance.code  # TacID

        obj = CustomerFactory.build(session = None, *args, **kwargs)
        obj.tac_id = tac_id_tac_instance.tac_id  # TacID

        obj.tac_code_peek = tac_id_tac_instance.code  # TacID

        # session.add(obj)
        # await session.flush()
        return obj
