# models/factory/organization.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import
"""
This module contains the
OrganizationFactory
class, which is responsible
for creating instances of the
Organization
model using the Factory pattern.
"""

from datetime import datetime  # noqa: F401
import uuid  # noqa: F401
import factory
from factory import Faker
from models import Organization
from services.logging_config import get_logger
from .tac import TacFactory  # tac_id
logger = get_logger(__name__)


class OrganizationFactory(factory.Factory):
    """
    Factory class for creating instances of
    the Organization model.
    """

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Meta class for the OrganizationFactory.
        """

        model = Organization

    code = factory.LazyFunction(uuid.uuid4)
    last_change_code = 0
    insert_user_id = factory.LazyFunction(uuid.uuid4)
    last_update_user_id = factory.LazyFunction(uuid.uuid4)
    name = Faker('sentence', nb_words=4)
    # tac_id
    tac_code_peek = factory.LazyFunction(  # TacID
        uuid.uuid4
    )

    @classmethod
    def _build(
        cls, model_class, *args, session=None, **kwargs
    ) -> Organization:  # pylint: disable=unused-argument
        """
            Builds and returns an instance
            of the Organization model.

            Args:
                model_class (class): The class of the model to be built.
                session (Session, optional): The SQLAlchemy
                session to be used. Defaults to None.
                *args: Variable length argument list.
                **kwargs: Arbitrary keyword arguments.

            Returns:
                Organization:
                    An instance of the
                    Organization model.

        """
        if session is None:
            obj2 = model_class(*args, **kwargs)
            return obj2
        tac_id_tac_instance = (  # TacID
            TacFactory.create(session=session))
        kwargs["tac_id"] = (  # TacID
            tac_id_tac_instance.tac_id)
        kwargs["tac_code_peek"] = (  # TacID
            tac_id_tac_instance.code)
        obj = model_class(*args, **kwargs)
        obj.tac_id = (  # TacID
            tac_id_tac_instance.tac_id)
        obj.tac_code_peek = (  # TacID
            tac_id_tac_instance.code)
        return obj

    @classmethod
    def _create(
        cls, model_class, *args, session=None, **kwargs
    ) -> Organization:  # pylint: disable=unused-argument
        """
        Create a new
        Organization object
        and save it to the database.

        Args:
            model_class (class): The class of the model to create.
            session (Session): The SQLAlchemy session object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Organization: The created
                Organization object.

        """
        logger.info("factory create")
        if not session:
            raise AttributeError(
                "Session not available"
            )
        tac_id_tac_instance = (  # TacID
            TacFactory.create(session=session))
        kwargs["tac_id"] = (  # TacID
            tac_id_tac_instance.tac_id)
        kwargs["tac_code_peek"] = (  # TacID
            tac_id_tac_instance.code)
        obj = model_class(*args, **kwargs)
        obj.tac_id = (  # TacID
            tac_id_tac_instance.tac_id)
        obj.tac_code_peek = (  # TacID
            tac_id_tac_instance.code)
        session.add(obj)
        session.commit()
        return obj

    @classmethod
    async def create_async(
        cls, session, *args, **kwargs
    ) -> Organization:  # pylint: disable=unused-argument
        """
        Create a new
        Organization object
        asynchronously.

        Args:
            session: The SQLAlchemy session object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The newly created Organization object.

        """
        tac_id_tac_instance = await (  # TacID
            TacFactory.create_async(session=session))
        kwargs["tac_id"] = (  # TacID
            tac_id_tac_instance.tac_id)
        kwargs["tac_code_peek"] = (  # TacID
            tac_id_tac_instance.code)
        obj = OrganizationFactory \
            .build(session=None, *args, **kwargs)
        obj.tac_id = (  # TacID
            tac_id_tac_instance.tac_id)
        obj.tac_code_peek = (  # TacID
            tac_id_tac_instance.code)
        session.add(obj)
        await session.flush()
        return obj

    @classmethod
    async def build_async(
        cls, session, *args, **kwargs
    ) -> Organization:  # pylint: disable=unused-argument
        """
        Build a new Organization object
        asynchronously.

        Args:
            session: The SQLAlchemy session object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The newly created Organization object.

        """
        tac_id_tac_instance = await (  # TacID
            TacFactory.create_async(session=session))
        kwargs["tac_id"] = (  # TacID
            tac_id_tac_instance.tac_id)
        kwargs["tac_code_peek"] = (  # TacID
            tac_id_tac_instance.code)
        obj = OrganizationFactory \
            .build(session=None, *args, **kwargs)
        obj.tac_id = (  # TacID
            tac_id_tac_instance.tac_id)
        obj.tac_code_peek = (  # TacID
            tac_id_tac_instance.code)
        return obj
