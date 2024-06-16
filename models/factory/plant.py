"""
    #TODO add comment
"""

from datetime import datetime
import uuid
import factory
from factory import Faker
from models import Plant
from services.logging_config import get_logger
from .flavor import FlavorFactory  # flvr_foreign_key_id
from .land import LandFactory  # land_id

logger = get_logger(__name__)


class PlantFactory(factory.Factory):
    """
    #TODO add comment
    """

    class Meta:
        """
        #TODO add comment
        """

        model = Plant

    # plant_id = factory.Sequence(lambda n: n)
    code = factory.LazyFunction(uuid.uuid4)
    last_change_code = 0
    insert_user_id = factory.LazyFunction(uuid.uuid4)
    last_update_user_id = factory.LazyFunction(uuid.uuid4)
    # flvr_foreign_key_id = 0 #factory.LazyAttribute(lambda obj: obj.flavor.flavor_id)
    is_delete_allowed = Faker('boolean')
    is_edit_allowed = Faker('boolean')
    # land_id = 0 #factory.LazyAttribute(lambda obj: obj.land.land_id)
    other_flavor = Faker('sentence', nb_words=4)
    some_big_int_val = Faker('random_int')
    some_bit_val = Faker('boolean')
    some_date_val = Faker('date_object')
    some_decimal_val = Faker(
        'pydecimal',
        left_digits=18,
        right_digits=6,
        positive=True
    )
    some_email_address = Faker('email')
    some_float_val = Faker('pyfloat', positive=True)
    some_int_val = Faker('random_int')
    some_money_val = Faker(
        'pydecimal',
        left_digits=18,
        right_digits=2,
        positive=True
    )
    some_n_var_char_val = Faker('sentence', nb_words=4)
    some_phone_number = Faker('phone_number')
    some_text_val = Faker('text')
    some_uniqueidentifier_val = factory.LazyFunction(uuid.uuid4)
    some_utc_date_time_val = factory.LazyFunction(datetime.utcnow)
    some_var_char_val = Faker('sentence', nb_words=4)
    insert_utc_date_time = factory.LazyFunction(datetime.utcnow)
    last_update_utc_date_time = factory.LazyFunction(datetime.utcnow)
# endset

    flvr_foreign_key_code_peek = factory.LazyFunction(  # FlvrForeignKeyID
        uuid.uuid4
    )
    land_code_peek = factory.LazyFunction(  # LandID
        uuid.uuid4
    )
# endset

    @classmethod
    def _build(cls, model_class, session=None, *args, **kwargs) -> Plant:
        """
        #TODO add comment
        """

        if session is None:
            obj2 = model_class(*args, **kwargs)
            return obj2

        land_id_land_instance = LandFactory.create(  # LandID
            session=session)
        flvr_foreign_key_id_flavor_instance = FlavorFactory.create(  # FlvrForeignKeyID
            session=session)
# endset

        kwargs["land_id"] = (  # LandID
            land_id_land_instance.land_id)
        kwargs["flvr_foreign_key_id"] = (  # FlvrForeignKeyID
            flvr_foreign_key_id_flavor_instance.flavor_id)
# endset

        kwargs["land_code_peek"] = land_id_land_instance.code  # LandID
        kwargs["flvr_foreign_key_code_peek"] = (  # FlvrForeignKeyID
            flvr_foreign_key_id_flavor_instance.code)
# endset

        obj = model_class(*args, **kwargs)

        obj.land_id = (  # LandID
            land_id_land_instance.land_id)
        obj.flvr_foreign_key_id = (  # FlvrForeignKeyID
            flvr_foreign_key_id_flavor_instance.flavor_id)
# endset
        obj.land_code_peek = land_id_land_instance.code  # LandID
        obj.flvr_foreign_key_code_peek = (  # FlvrForeignKeyID
            flvr_foreign_key_id_flavor_instance.code)
# endset

        # session.add(obj)
        # session.commit()
        return obj

    @classmethod
    def _create(cls, model_class, session, *args, **kwargs) -> Plant:
        """
        #TODO add comment
        """

        logger.info("factory create")
        land_id_land_instance = LandFactory.create(  # LandID
            session=session)
        flvr_foreign_key_id_flavor_instance = FlavorFactory.create(  # FlvrForeignKeyID
            session=session)
# endset

        kwargs["land_id"] = (  # LandID
            land_id_land_instance.land_id)
        kwargs["flvr_foreign_key_id"] = (  # FlvrForeignKeyID
            flvr_foreign_key_id_flavor_instance.flavor_id)
# endset

        kwargs["land_code_peek"] = land_id_land_instance.code  # LandID
        kwargs["flvr_foreign_key_code_peek"] = (  # FlvrForeignKeyID
            flvr_foreign_key_id_flavor_instance.code)
# endset

        obj = model_class(*args, **kwargs)

        obj.land_id = (  # LandID
            land_id_land_instance.land_id)
        obj.flvr_foreign_key_id = (  # FlvrForeignKeyID
            flvr_foreign_key_id_flavor_instance.flavor_id)
# endset
        obj.land_code_peek = land_id_land_instance.code  # LandID
        obj.flvr_foreign_key_code_peek = (  # FlvrForeignKeyID
            flvr_foreign_key_id_flavor_instance.code)
# endset

        session.add(obj)
        session.commit()
        return obj

    @classmethod
    async def create_async(cls, session, *args, **kwargs) -> Plant:
        """
            #TODO add comment
        """

        land_id_land_instance = await LandFactory.create_async(  # LandID
            session=session)
        flvr_foreign_key_id_flavor_instance = await FlavorFactory.create_async(  # FlvrForeignKeyID
            session=session)
# endset

        kwargs["land_id"] = (  # LandID
            land_id_land_instance.land_id)
        kwargs["flvr_foreign_key_id"] = (  # FlvrForeignKeyID
            flvr_foreign_key_id_flavor_instance.flavor_id)
# endset

        kwargs["land_code_peek"] = land_id_land_instance.code  # LandID
        kwargs["flvr_foreign_key_code_peek"] = (  # FlvrForeignKeyID
            flvr_foreign_key_id_flavor_instance.code)
# endset

        obj = PlantFactory.build(session=None, *args, **kwargs)

        obj.land_id = (  # LandID
            land_id_land_instance.land_id)
        obj.flvr_foreign_key_id = (  # FlvrForeignKeyID
            flvr_foreign_key_id_flavor_instance.flavor_id)
# endset
        obj.land_code_peek = land_id_land_instance.code  # LandID
        obj.flvr_foreign_key_code_peek = (  # FlvrForeignKeyID
            flvr_foreign_key_id_flavor_instance.code)
# endset

        session.add(obj)
        await session.flush()
        return obj

    @classmethod
    async def build_async(cls, session, *args, **kwargs) -> Plant:
        """
            #TODO add comment
        """

        land_id_land_instance = await LandFactory.create_async(  # LandID
            session=session)
        flvr_foreign_key_id_flavor_instance = await FlavorFactory.create_async(  # FlvrForeignKeyID
            session=session)
# endset

        kwargs["land_id"] = (  # LandID
            land_id_land_instance.land_id)
        kwargs["flvr_foreign_key_id"] = (  # FlvrForeignKeyID
            flvr_foreign_key_id_flavor_instance.flavor_id)
# endset

        kwargs["land_code_peek"] = land_id_land_instance.code  # LandID
        kwargs["flvr_foreign_key_code_peek"] = (  # FlvrForeignKeyID
            flvr_foreign_key_id_flavor_instance.code)
# endset

        obj = PlantFactory.build(session=None, *args, **kwargs)

        obj.land_id = (  # LandID
            land_id_land_instance.land_id)
        obj.flvr_foreign_key_id = (  # FlvrForeignKeyID
            flvr_foreign_key_id_flavor_instance.flavor_id)
# endset
        obj.land_code_peek = land_id_land_instance.code  # LandID
        obj.flvr_foreign_key_code_peek = (  # FlvrForeignKeyID
            flvr_foreign_key_id_flavor_instance.code)
# endset

        # session.add(obj)
        # await session.flush()
        return obj
