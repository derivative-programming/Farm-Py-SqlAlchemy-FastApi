# models/factory/error_log.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import
"""
This module contains the
ErrorLogFactory
class, which is responsible
for creating instances of the
ErrorLog
model using the Factory pattern.
"""

from datetime import datetime  # noqa: F401
import uuid  # noqa: F401
import factory
from factory import Faker
from models import ErrorLog
from services.logging_config import get_logger
from .pac import PacFactory  # pac_id
logger = get_logger(__name__)


class ErrorLogFactory(factory.Factory):
    """
    Factory class for creating instances of
    the ErrorLog model.
    """

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Meta class for the ErrorLogFactory.
        """

        model = ErrorLog

    code = factory.LazyFunction(uuid.uuid4)
    last_change_code = 0
    insert_user_id = factory.LazyFunction(uuid.uuid4)
    last_update_user_id = factory.LazyFunction(uuid.uuid4)
    browser_code = factory.LazyFunction(uuid.uuid4)
    context_code = factory.LazyFunction(uuid.uuid4)
    created_utc_date_time = factory.LazyFunction(datetime.utcnow)
    description = Faker('sentence', nb_words=4)
    is_client_side_error = Faker('boolean')
    is_resolved = Faker('boolean')
    # pac_id
    url = Faker('sentence', nb_words=4)
    pac_code_peek = factory.LazyFunction(  # PacID
        uuid.uuid4
    )

    @classmethod
    def _build(
        cls, model_class, *args, session=None, **kwargs
    ) -> ErrorLog:  # pylint: disable=unused-argument
        """
            Builds and returns an instance
            of the ErrorLog model.

            Args:
                model_class (class): The class of the model to be built.
                session (Session, optional): The SQLAlchemy
                session to be used. Defaults to None.
                *args: Variable length argument list.
                **kwargs: Arbitrary keyword arguments.

            Returns:
                ErrorLog:
                    An instance of the
                    ErrorLog model.

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
    ) -> ErrorLog:  # pylint: disable=unused-argument
        """
        Create a new
        ErrorLog object
        and save it to the database.

        Args:
            model_class (class): The class of the model to create.
            session (Session): The SQLAlchemy session object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            ErrorLog: The created
                ErrorLog object.

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
    ) -> ErrorLog:  # pylint: disable=unused-argument
        """
        Create a new
        ErrorLog object
        asynchronously.

        Args:
            session: The SQLAlchemy session object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The newly created ErrorLog object.

        """
        pac_id_pac_instance = await (  # PacID
            PacFactory.create_async(session=session))
        kwargs["pac_id"] = (  # PacID
            pac_id_pac_instance.pac_id)
        kwargs["pac_code_peek"] = (  # PacID
            pac_id_pac_instance.code)
        obj = ErrorLogFactory \
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
    ) -> ErrorLog:  # pylint: disable=unused-argument
        """
        Build a new ErrorLog object
        asynchronously.

        Args:
            session: The SQLAlchemy session object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The newly created ErrorLog object.

        """
        pac_id_pac_instance = await (  # PacID
            PacFactory.create_async(session=session))
        kwargs["pac_id"] = (  # PacID
            pac_id_pac_instance.pac_id)
        kwargs["pac_code_peek"] = (  # PacID
            pac_id_pac_instance.code)
        obj = ErrorLogFactory \
            .build(session=None, *args, **kwargs)
        obj.pac_id = (  # PacID
            pac_id_pac_instance.pac_id)
        obj.pac_code_peek = (  # PacID
            pac_id_pac_instance.code)
        return obj
