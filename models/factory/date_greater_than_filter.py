# models/factory/date_greater_than_filter.py  # pylint: disable=duplicate-code
# pylint: disable=unused-import
"""
This module contains the
DateGreaterThanFilterFactory
class, which is responsible
for creating instances of the
DateGreaterThanFilter
model using the Factory pattern.
"""

from datetime import datetime  # noqa: F401
import uuid  # noqa: F401
import factory
from factory import Faker
from models import DateGreaterThanFilter
from services.logging_config import get_logger
from .pac import PacFactory  # pac_id
logger = get_logger(__name__)


class DateGreaterThanFilterFactory(factory.Factory):
    """
    Factory class for creating instances of
    the DateGreaterThanFilter model.
    """

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Meta class for the DateGreaterThanFilterFactory.
        """

        model = DateGreaterThanFilter

    code = factory.LazyFunction(uuid.uuid4)
    last_change_code = 0
    insert_user_id = factory.LazyFunction(uuid.uuid4)
    last_update_user_id = factory.LazyFunction(uuid.uuid4)
    day_count = Faker('random_int')
    description = Faker('sentence', nb_words=4)
    display_order = Faker('random_int')
    is_active = Faker('boolean')
    lookup_enum_name = Faker('sentence', nb_words=4)
    name = Faker('sentence', nb_words=4)
    # pac_id
    pac_code_peek = factory.LazyFunction(  # PacID
        uuid.uuid4
    )

    @classmethod
    def _build(
        cls, model_class, *args, session=None, **kwargs
    ) -> DateGreaterThanFilter:  # pylint: disable=unused-argument
        """
            Builds and returns an instance
            of the DateGreaterThanFilter model.

            Args:
                model_class (class): The class of the model to be built.
                session (Session, optional): The SQLAlchemy
                session to be used. Defaults to None.
                *args: Variable length argument list.
                **kwargs: Arbitrary keyword arguments.

            Returns:
                DateGreaterThanFilter:
                    An instance of the
                    DateGreaterThanFilter model.

        """
        if session is None:
            obj2 = model_class(*args, **kwargs)
            return obj2
        pac_id_pac_instance = (  # PacID
            PacFactory.create(session=session))
        kwargs["pac_id"] = (  # PacID
            pac_id_pac_instance.pac_id)
        kwargs["pac_code_peek"] = (  # PacID
            pac_id_pac_instance.code)
        obj = model_class(*args, **kwargs)
        obj.pac_id = (  # PacID
            pac_id_pac_instance.pac_id)
        obj.pac_code_peek = (  # PacID
            pac_id_pac_instance.code)
        return obj

    @classmethod
    def _create(
        cls, model_class, *args, session=None, **kwargs
    ) -> DateGreaterThanFilter:  # pylint: disable=unused-argument
        """
        Create a new
        DateGreaterThanFilter object
        and save it to the database.

        Args:
            model_class (class): The class of the model to create.
            session (Session): The SQLAlchemy session object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            DateGreaterThanFilter: The created
                DateGreaterThanFilter object.

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
        kwargs["pac_code_peek"] = (  # PacID
            pac_id_pac_instance.code)
        obj = model_class(*args, **kwargs)
        obj.pac_id = (  # PacID
            pac_id_pac_instance.pac_id)
        obj.pac_code_peek = (  # PacID
            pac_id_pac_instance.code)
        session.add(obj)
        session.commit()
        return obj

    @classmethod
    async def create_async(
        cls, session, *args, **kwargs
    ) -> DateGreaterThanFilter:  # pylint: disable=unused-argument
        """
        Create a new
        DateGreaterThanFilter object
        asynchronously.

        Args:
            session: The SQLAlchemy session object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The newly created DateGreaterThanFilter object.

        """
        pac_id_pac_instance = await (  # PacID
            PacFactory.create_async(session=session))
        kwargs["pac_id"] = (  # PacID
            pac_id_pac_instance.pac_id)
        kwargs["pac_code_peek"] = (  # PacID
            pac_id_pac_instance.code)
        obj = DateGreaterThanFilterFactory \
            .build(session=None, *args, **kwargs)
        obj.pac_id = (  # PacID
            pac_id_pac_instance.pac_id)
        obj.pac_code_peek = (  # PacID
            pac_id_pac_instance.code)
        session.add(obj)
        await session.flush()
        return obj

    @classmethod
    async def build_async(
        cls, session, *args, **kwargs
    ) -> DateGreaterThanFilter:  # pylint: disable=unused-argument
        """
        Build a new DateGreaterThanFilter object
        asynchronously.

        Args:
            session: The SQLAlchemy session object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The newly created DateGreaterThanFilter object.

        """
        pac_id_pac_instance = await (  # PacID
            PacFactory.create_async(session=session))
        kwargs["pac_id"] = (  # PacID
            pac_id_pac_instance.pac_id)
        kwargs["pac_code_peek"] = (  # PacID
            pac_id_pac_instance.code)
        obj = DateGreaterThanFilterFactory \
            .build(session=None, *args, **kwargs)
        obj.pac_id = (  # PacID
            pac_id_pac_instance.pac_id)
        obj.pac_code_peek = (  # PacID
            pac_id_pac_instance.code)
        return obj
