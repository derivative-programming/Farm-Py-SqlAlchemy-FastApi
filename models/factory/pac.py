# models/factory/pac.py
# pylint: disable=unused-import
"""
This module contains the
PacFactory
class, which is responsible
for creating instances of the
Pac
model using the Factory pattern.
"""

from datetime import datetime  # noqa: F401
import uuid  # noqa: F401
import factory
from factory import Faker
from models import Pac
from services.logging_config import get_logger

logger = get_logger(__name__)


class PacFactory(factory.Factory):
    """
    Factory class for creating instances of
    the Pac model.
    """

    class Meta:
        """
        Meta class for the PacFactory.
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


    @classmethod
    def _build(
        cls, model_class, *args, session=None, **kwargs
    ) -> Pac:
        """
            Builds and returns an instance
            of the Pac model.

            Args:
                model_class (class): The class of the model to be built.
                session (Session, optional): The SQLAlchemy
                session to be used. Defaults to None.
                *args: Variable length argument list.
                **kwargs: Arbitrary keyword arguments.

            Returns:
                Pac:
                    An instance of the
                    Pac model.

        """
        if session is None:
            obj2 = model_class(*args, **kwargs)
            return obj2


        obj = model_class(*args, **kwargs)


        # session.add(obj)
        # session.commit()
        return obj

    @classmethod
    def _create(
        cls, model_class, *args, session=None, **kwargs
    ) -> Pac:
        """
        Create a new
        Pac object
        and save it to the database.

        Args:
            model_class (class): The class of the model to create.
            session (Session): The SQLAlchemy session object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Pac: The created
                Pac object.

        """
        logger.info("factory create")
        if not session:
            raise AttributeError(
                "Session not available"
            )


        obj = model_class(*args, **kwargs)


        session.add(obj)
        session.commit()
        return obj

    @classmethod
    async def create_async(
        cls, session, *args, **kwargs
    ) -> Pac:
        """
        Create a new
        Pac object
        asynchronously.

        Args:
            session: The SQLAlchemy session object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The newly created Pac object.

        """


        obj = PacFactory \
            .build(session=None, *args, **kwargs)


        session.add(obj)
        await session.flush()
        return obj

    @classmethod
    async def build_async(
        cls, session, *args, **kwargs
    ) -> Pac:
        """
        Build a new Pac object
        asynchronously.

        Args:
            session: The SQLAlchemy session object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The newly created Pac object.

        """


        obj = PacFactory \
            .build(session=None, *args, **kwargs)


        # session.add(obj)
        # await session.flush()
        return obj
