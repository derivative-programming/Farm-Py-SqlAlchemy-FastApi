# models/factory/plant.py
# pylint: disable=unused-import
"""
This module contains the
PlantFactory
class, which is responsible
for creating instances of the
Plant
model using the Factory pattern.
"""

from datetime import datetime  # noqa: F401
import uuid  # noqa: F401
import factory
from factory import Faker
from models import Plant
from services.logging_config import get_logger
from .flavor import FlavorFactory  # flvr_foreign_key_id
from .land import LandFactory  # land_id

logger = get_logger(__name__)


class PlantFactory(factory.Factory):
    """
    Factory class for creating instances of
    the Plant model.
    """

    class Meta:
        """
        Meta class for the PlantFactory.
        """

        model = Plant

    # plant_id = factory.Sequence(lambda n: n)
    code = factory.LazyFunction(uuid.uuid4)
    last_change_code = 0
    insert_user_id = factory.LazyFunction(uuid.uuid4)
    last_update_user_id = factory.LazyFunction(uuid.uuid4)
    # flvr_foreign_key_id = 0
    is_delete_allowed = Faker('boolean')
    is_edit_allowed = Faker('boolean')
    # land_id = 0
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
    def _build(
        cls, model_class, *args, session=None, **kwargs
    ) -> Plant:
        """
            Builds and returns an instance
            of the Plant model.

            Args:
                model_class (class): The class of the model to be built.
                session (Session, optional): The SQLAlchemy
                session to be used. Defaults to None.
                *args: Variable length argument list.
                **kwargs: Arbitrary keyword arguments.

            Returns:
                Plant: An instance of the
                    Plant model.

        """

        if session is None:
            obj2 = model_class(*args, **kwargs)
            return obj2

        land_id_land_instance = (  # LandID
            LandFactory.create(session=session))

        flvr_foreign_key_id_flavor_instance = (  # FlvrForeignKeyID
            FlavorFactory.create(session=session))

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
    def _create(
        cls, model_class, *args, session=None, **kwargs
    ) -> Plant:
        """
        Create a new
        Plant object
        and save it to the database.

        Args:
            model_class (class): The class of the model to create.
            session (Session): The SQLAlchemy session object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Plant: The created
                Plant object.

        """

        logger.info("factory create")

        if not session:
            raise AttributeError(
                "Session not available"
            )

        land_id_land_instance = (  # LandID
            LandFactory.create(session=session))

        flvr_foreign_key_id_flavor_instance = (  # FlvrForeignKeyID
            FlavorFactory.create(session=session))
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
    async def create_async(
        cls, session, *args, **kwargs
    ) -> Plant:
        """
        Create a new
        Plant object
        asynchronously.

        Args:
            session: The SQLAlchemy session object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The newly created Plant object.

        """

        land_id_land_instance = await (  # LandID
            LandFactory.create_async(session=session))

        flvr_foreign_key_id_flavor_instance = await (  # FlvrForeignKeyID
            FlavorFactory.create_async(session=session))

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
    async def build_async(
        cls, session, *args, **kwargs
    ) -> Plant:
        """
        Build a new Plant object
        asynchronously.

        Args:
            session: The SQLAlchemy session object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The newly created Plant object.

        """

        land_id_land_instance = await (  # LandID
            LandFactory.create_async(session=session))

        flvr_foreign_key_id_flavor_instance = await (  # FlvrForeignKeyID
            FlavorFactory.create_async(session=session))
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
