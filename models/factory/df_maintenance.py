# models/factory/df_maintenance.py
# pylint: disable=unused-import
"""
This module contains the
DFMaintenanceFactory
class, which is responsible
for creating instances of the
DFMaintenance
model using the Factory pattern.
"""

from datetime import datetime  # noqa: F401
import uuid  # noqa: F401
import factory
from factory import Faker
from models import DFMaintenance
from services.logging_config import get_logger
from .pac import PacFactory  # pac_id
logger = get_logger(__name__)


class DFMaintenanceFactory(factory.Factory):
    """
    Factory class for creating instances of
    the DFMaintenance model.
    """

    class Meta:
        """
        Meta class for the DFMaintenanceFactory.
        """

        model = DFMaintenance

    # df_maintenance_id = factory.Sequence(lambda n: n)
    code = factory.LazyFunction(uuid.uuid4)
    last_change_code = 0
    insert_user_id = factory.LazyFunction(uuid.uuid4)
    last_update_user_id = factory.LazyFunction(uuid.uuid4)
    is_paused = Faker('boolean')
    is_scheduled_df_process_request_completed = Faker('boolean')
    is_scheduled_df_process_request_started = Faker('boolean')
    last_scheduled_df_process_request_utc_date_time = factory.LazyFunction(datetime.utcnow)
    next_scheduled_df_process_request_utc_date_time = factory.LazyFunction(datetime.utcnow)
    # pac_id = 0
    paused_by_username = Faker('sentence', nb_words=4)
    paused_utc_date_time = factory.LazyFunction(datetime.utcnow)
    scheduled_df_process_request_processor_identifier = Faker('sentence', nb_words=4)
    pac_code_peek = factory.LazyFunction(  # PacID
        uuid.uuid4
    )

    @classmethod
    def _build(
        cls, model_class, *args, session=None, **kwargs
    ) -> DFMaintenance:
        """
            Builds and returns an instance
            of the DFMaintenance model.

            Args:
                model_class (class): The class of the model to be built.
                session (Session, optional): The SQLAlchemy
                session to be used. Defaults to None.
                *args: Variable length argument list.
                **kwargs: Arbitrary keyword arguments.

            Returns:
                DFMaintenance:
                    An instance of the
                    DFMaintenance model.

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
    def _create(
        cls, model_class, *args, session=None, **kwargs
    ) -> DFMaintenance:
        """
        Create a new
        DFMaintenance object
        and save it to the database.

        Args:
            model_class (class): The class of the model to create.
            session (Session): The SQLAlchemy session object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            DFMaintenance: The created
                DFMaintenance object.

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
    async def create_async(
        cls, session, *args, **kwargs
    ) -> DFMaintenance:
        """
        Create a new
        DFMaintenance object
        asynchronously.

        Args:
            session: The SQLAlchemy session object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The newly created DFMaintenance object.

        """
        pac_id_pac_instance = await (  # PacID
            PacFactory.create_async(session=session))
        kwargs["pac_id"] = (  # PacID
            pac_id_pac_instance.pac_id)
        kwargs["pac_code_peek"] = pac_id_pac_instance.code  # PacID
        obj = DFMaintenanceFactory \
            .build(session=None, *args, **kwargs)
        obj.pac_id = (  # PacID
            pac_id_pac_instance.pac_id)
        obj.pac_code_peek = pac_id_pac_instance.code  # PacID
        session.add(obj)
        await session.flush()
        return obj

    @classmethod
    async def build_async(
        cls, session, *args, **kwargs
    ) -> DFMaintenance:
        """
        Build a new DFMaintenance object
        asynchronously.

        Args:
            session: The SQLAlchemy session object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The newly created DFMaintenance object.

        """
        pac_id_pac_instance = await (  # PacID
            PacFactory.create_async(session=session))
        kwargs["pac_id"] = (  # PacID
            pac_id_pac_instance.pac_id)
        kwargs["pac_code_peek"] = pac_id_pac_instance.code  # PacID
        obj = DFMaintenanceFactory \
            .build(session=None, *args, **kwargs)
        obj.pac_id = (  # PacID
            pac_id_pac_instance.pac_id)
        obj.pac_code_peek = pac_id_pac_instance.code  # PacID
        # session.add(obj)
        # await session.flush()
        return obj
