"""
    #TODO add comment
"""
from datetime import datetime
import uuid
import factory
from factory import Faker
from models import Customer
from services.logging_config import get_logger
from .tac import TacFactory  # tac_id
logger = get_logger(__name__)
class CustomerFactory(factory.Factory):
    """
    #TODO add comment
    """
    class Meta:
        """
        #TODO add comment
        """
        model = Customer
    # customer_id = factory.Sequence(lambda n: n)
    code = factory.LazyFunction(uuid.uuid4)
    last_change_code = 0
    insert_user_id = factory.LazyFunction(uuid.uuid4)
    last_update_user_id = factory.LazyFunction(uuid.uuid4)
    active_organization_id = Faker('random_int')
    email = Faker('email')
    email_confirmed_utc_date_time = factory.LazyFunction(datetime.utcnow)
    first_name = Faker('sentence', nb_words=4)
    forgot_password_key_expiration_utc_date_time = factory.LazyFunction(datetime.utcnow)
    forgot_password_key_value = Faker('sentence', nb_words=4)
    fs_user_code_value = factory.LazyFunction(uuid.uuid4)
    is_active = Faker('boolean')
    is_email_allowed = Faker('boolean')
    is_email_confirmed = Faker('boolean')
    is_email_marketing_allowed = Faker('boolean')
    is_locked = Faker('boolean')
    is_multiple_organizations_allowed = Faker('boolean')
    is_verbose_logging_forced = Faker('boolean')
    last_login_utc_date_time = factory.LazyFunction(datetime.utcnow)
    last_name = Faker('sentence', nb_words=4)
    password = Faker('sentence', nb_words=4)
    phone = Faker('phone_number')
    province = Faker('sentence', nb_words=4)
    registration_utc_date_time = factory.LazyFunction(datetime.utcnow)
    # tac_id = 0 #factory.LazyAttribute(lambda obj: obj.tac.tac_id)
    utc_offset_in_minutes = Faker('random_int')
    zip = Faker('sentence', nb_words=4)
# endset
    tac_code_peek = factory.LazyFunction(  # TacID
        uuid.uuid4
    )
# endset
    @classmethod
    def _build(cls, model_class, session=None, *args, **kwargs) -> Customer:
        """
        #TODO add comment
        """
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
        session.add(obj)
        # session.commit()
        return obj
    @classmethod
    def _create(cls, model_class, session=None, *args, **kwargs) -> Customer:
        """
        #TODO add comment
        """
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
    async def create_async(cls, session, *args, **kwargs) -> Customer:
        """
            #TODO add comment
        """
        tac_id_tac_instance = await TacFactory.create_async(session=session)  # TacID
# endset
        kwargs["tac_id"] = tac_id_tac_instance.tac_id  # TacID
# endset
        kwargs["tac_code_peek"] = tac_id_tac_instance.code  # TacID
# endset
        obj = CustomerFactory.build(session=None, *args, **kwargs)
        obj.tac_id = tac_id_tac_instance.tac_id  # TacID
# endset
        obj.tac_code_peek = tac_id_tac_instance.code  # TacID
# endset
        session.add(obj)
        await session.flush()
        return obj
    @classmethod
    async def build_async(cls, session, *args, **kwargs) -> Customer:
        """
            #TODO add comment
        """
        tac_id_tac_instance = await TacFactory.create_async(session=session)  # TacID
# endset
        kwargs["tac_id"] = tac_id_tac_instance.tac_id  # TacID
# endset
        kwargs["tac_code_peek"] = tac_id_tac_instance.code  # TacID
# endset
        obj = CustomerFactory.build(session=None, *args, **kwargs)
        obj.tac_id = tac_id_tac_instance.tac_id  # TacID
# endset
        obj.tac_code_peek = tac_id_tac_instance.code  # TacID
# endset
        session.add(obj)
        # await session.flush()
        return obj
