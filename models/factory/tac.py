# models/factory/tac.py
"""
This module contains the TacFactory
class, which is responsible
for creating instances of the Tac
model using the Factory pattern.
"""

from datetime import datetime
import uuid
import factory
from factory import Faker
from models import Tac
from services.logging_config import get_logger
from .pac import PacFactory  # pac_id
logger = get_logger(__name__)


class TacFactory(factory.Factory):
    """
    Factory class for creating instances of
    the Tac model.
    """

    class Meta:
        """
        Meta class for the TacFactory.
        """

        model = Tac

    # tac_id = factory.Sequence(lambda n: n)
    code = factory.LazyFunction(uuid.uuid4)
    last_change_code = 0
    insert_user_id = factory.LazyFunction(uuid.uuid4)
    last_update_user_id = factory.LazyFunction(uuid.uuid4)
    description = Faker('sentence', nb_words=4)
    display_order = Faker('random_int')
    is_active = Faker('boolean')
    lookup_enum_name = Faker('sentence', nb_words=4)
    name = Faker('sentence', nb_words=4)
    # pac_id = 0
    pac_code_peek = factory.LazyFunction(  # PacID
        uuid.uuid4
    )

    @classmethod
    def _build(cls, model_class, *args, session=None, **kwargs) -> Tac:
        """
            Builds and returns an instance
            of the Tac model.

            Args:
                model_class (class): The class of the model to be built.
                session (Session, optional): The SQLAlchemy
                session to be used. Defaults to None.
                *args: Variable length argument list.
                **kwargs: Arbitrary keyword arguments.

            Returns:
                Tac: An instance of the
                    Tac model.

        """

        if session is None:
            obj2 = model_class(*args, **kwargs)
            return obj2
        pac_id_pac_instance = (  # PacID
            PacFactory.create(session=session))
        kwargs["pac_id"] = (  # PacID
            pac_id_pac_instance.pac_id)
        kwargs["pac_code_peek"] = pac_id_pac_instance.code  # PacID

        obj = model_class(*args, **kwargs)
        obj.pac_id = (  # PacID
            pac_id_pac_instance.pac_id)
        obj.pac_code_peek = pac_id_pac_instance.code  # PacID

        # session.add(obj)
        # session.commit()
        return obj

    @classmethod
    def _create(cls, model_class, *args, session=None, **kwargs) -> Tac:
        """
        Create a new Tac object
        and save it to the database.

        Args:
            model_class (class): The class of the model to create.
            session (Session): The SQLAlchemy session object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Tac: The created
                Tac object.

        """

        logger.info("factory create")

        if not session:
            raise AttributeError(
                "Session not available"
            )
        pac_id_pac_instance = (  # PacID
            PacFactory.create(session=session))
        kwargs["pac_id"] = (  # PacID
            pac_id_pac_instance.pac_id)
        kwargs["pac_code_peek"] = pac_id_pac_instance.code  # PacID

        obj = model_class(*args, **kwargs)
        obj.pac_id = (  # PacID
            pac_id_pac_instance.pac_id)
        obj.pac_code_peek = pac_id_pac_instance.code  # PacID

        session.add(obj)
        session.commit()
        return obj

    @classmethod
    async def create_async(cls, session, *args, **kwargs) -> Tac:
        """
        Create a new Tac object
        asynchronously.

        Args:
            session: The SQLAlchemy session object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The newly created Tac object.

        """
        pac_id_pac_instance = await (  # PacID
            PacFactory.create_async(session=session))
        kwargs["pac_id"] = (  # PacID
            pac_id_pac_instance.pac_id)
        kwargs["pac_code_peek"] = pac_id_pac_instance.code  # PacID

        obj = TacFactory.build(session=None, *args, **kwargs)
        obj.pac_id = (  # PacID
            pac_id_pac_instance.pac_id)
        obj.pac_code_peek = pac_id_pac_instance.code  # PacID

        session.add(obj)
        await session.flush()
        return obj

    @classmethod
    async def build_async(cls, session, *args, **kwargs) -> Tac:
        """
        Build a new Tac object
        asynchronously.

        Args:
            session: The SQLAlchemy session object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The newly created Tac object.

        """
        pac_id_pac_instance = await (  # PacID
            PacFactory.create_async(session=session))
        kwargs["pac_id"] = (  # PacID
            pac_id_pac_instance.pac_id)
        kwargs["pac_code_peek"] = pac_id_pac_instance.code  # PacID

        obj = TacFactory.build(session=None, *args, **kwargs)
        obj.pac_id = (  # PacID
            pac_id_pac_instance.pac_id)
        obj.pac_code_peek = pac_id_pac_instance.code  # PacID

        # session.add(obj)
        # await session.flush()
        return obj

