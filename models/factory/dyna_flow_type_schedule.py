# models/factory/dyna_flow_type_schedule.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import
"""
This module contains the
DynaFlowTypeScheduleFactory
class, which is responsible
for creating instances of the
DynaFlowTypeSchedule
model using the Factory pattern.
"""

from datetime import datetime  # noqa: F401
import uuid  # noqa: F401
import factory
from factory import Faker
from models import DynaFlowTypeSchedule
from services.logging_config import get_logger
from .dyna_flow_type import DynaFlowTypeFactory  # dyna_flow_type_id
from .pac import PacFactory  # pac_id
logger = get_logger(__name__)


class DynaFlowTypeScheduleFactory(factory.Factory):
    """
    Factory class for creating instances of
    the DynaFlowTypeSchedule model.
    """

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Meta class for the DynaFlowTypeScheduleFactory.
        """

        model = DynaFlowTypeSchedule

    code = factory.LazyFunction(uuid.uuid4)
    last_change_code = 0
    insert_user_id = factory.LazyFunction(uuid.uuid4)
    last_update_user_id = factory.LazyFunction(uuid.uuid4)
    # dyna_flow_type_id
    frequency_in_hours = Faker('random_int')
    is_active = Faker('boolean')
    last_utc_date_time = factory.LazyFunction(datetime.utcnow)
    next_utc_date_time = factory.LazyFunction(datetime.utcnow)
    # pac_id
    dyna_flow_type_code_peek = factory.LazyFunction(  # DynaFlowTypeID
        uuid.uuid4
    )
    pac_code_peek = factory.LazyFunction(  # PacID
        uuid.uuid4
    )

    @classmethod
    def _build(
        cls, model_class, *args, session=None, **kwargs
    ) -> DynaFlowTypeSchedule:  # pylint: disable=unused-argument
        """
            Builds and returns an instance
            of the DynaFlowTypeSchedule model.

            Args:
                model_class (class): The class of the model to be built.
                session (Session, optional): The SQLAlchemy
                session to be used. Defaults to None.
                *args: Variable length argument list.
                **kwargs: Arbitrary keyword arguments.

            Returns:
                DynaFlowTypeSchedule:
                    An instance of the
                    DynaFlowTypeSchedule model.

        """
        if session is None:
            obj2 = model_class(*args, **kwargs)
            return obj2
        dyna_flow_type_id_dyna_flow_type_instance = (  # DynaFlowTypeID
            DynaFlowTypeFactory.create(session=session))
        pac_id_pac_instance = (  # PacID
            PacFactory.create(session=session))
        kwargs["dyna_flow_type_id"] = (  # DynaFlowTypeID
            dyna_flow_type_id_dyna_flow_type_instance.dyna_flow_type_id)
        kwargs["pac_id"] = (  # PacID
            pac_id_pac_instance.pac_id)
        kwargs["dyna_flow_type_code_peek"] = (  # DynaFlowTypeID
            dyna_flow_type_id_dyna_flow_type_instance.code)
        kwargs["pac_code_peek"] = (  # PacID
            pac_id_pac_instance.code)
        obj = model_class(*args, **kwargs)
        obj.dyna_flow_type_id = (  # DynaFlowTypeID
            dyna_flow_type_id_dyna_flow_type_instance.dyna_flow_type_id)
        obj.pac_id = (  # PacID
            pac_id_pac_instance.pac_id)
        obj.dyna_flow_type_code_peek = (  # DynaFlowTypeID
            dyna_flow_type_id_dyna_flow_type_instance.code)
        obj.pac_code_peek = (  # PacID
            pac_id_pac_instance.code)
        return obj

    @classmethod
    def _create(
        cls, model_class, *args, session=None, **kwargs
    ) -> DynaFlowTypeSchedule:  # pylint: disable=unused-argument
        """
        Create a new
        DynaFlowTypeSchedule object
        and save it to the database.

        Args:
            model_class (class): The class of the model to create.
            session (Session): The SQLAlchemy session object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            DynaFlowTypeSchedule: The created
                DynaFlowTypeSchedule object.

        """
        logger.info("factory create")
        if not session:
            raise AttributeError(
                "Session not available"
            )
        dyna_flow_type_id_dyna_flow_type_instance = (  # DynaFlowTypeID
            DynaFlowTypeFactory.create(session=session))
        pac_id_pac_instance = (  # PacID
            PacFactory.create(session=session))
        kwargs["dyna_flow_type_id"] = (  # DynaFlowTypeID
            dyna_flow_type_id_dyna_flow_type_instance.dyna_flow_type_id)
        kwargs["pac_id"] = (  # PacID
            pac_id_pac_instance.pac_id)
        kwargs["dyna_flow_type_code_peek"] = (  # DynaFlowTypeID
            dyna_flow_type_id_dyna_flow_type_instance.code)
        kwargs["pac_code_peek"] = (  # PacID
            pac_id_pac_instance.code)
        obj = model_class(*args, **kwargs)
        obj.dyna_flow_type_id = (  # DynaFlowTypeID
            dyna_flow_type_id_dyna_flow_type_instance.dyna_flow_type_id)
        obj.pac_id = (  # PacID
            pac_id_pac_instance.pac_id)
        obj.dyna_flow_type_code_peek = (  # DynaFlowTypeID
            dyna_flow_type_id_dyna_flow_type_instance.code)
        obj.pac_code_peek = (  # PacID
            pac_id_pac_instance.code)
        session.add(obj)
        session.commit()
        return obj

    @classmethod
    async def create_async(
        cls, session, *args, **kwargs
    ) -> DynaFlowTypeSchedule:  # pylint: disable=unused-argument
        """
        Create a new
        DynaFlowTypeSchedule object
        asynchronously.

        Args:
            session: The SQLAlchemy session object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The newly created DynaFlowTypeSchedule object.

        """
        dyna_flow_type_id_dyna_flow_type_instance = await (  # DynaFlowTypeID
            DynaFlowTypeFactory.create_async(session=session))
        pac_id_pac_instance = await (  # PacID
            PacFactory.create_async(session=session))
        kwargs["dyna_flow_type_id"] = (  # DynaFlowTypeID
            dyna_flow_type_id_dyna_flow_type_instance.dyna_flow_type_id)
        kwargs["pac_id"] = (  # PacID
            pac_id_pac_instance.pac_id)
        kwargs["dyna_flow_type_code_peek"] = (  # DynaFlowTypeID
            dyna_flow_type_id_dyna_flow_type_instance.code)
        kwargs["pac_code_peek"] = (  # PacID
            pac_id_pac_instance.code)
        obj = DynaFlowTypeScheduleFactory \
            .build(session=None, *args, **kwargs)
        obj.dyna_flow_type_id = (  # DynaFlowTypeID
            dyna_flow_type_id_dyna_flow_type_instance.dyna_flow_type_id)
        obj.pac_id = (  # PacID
            pac_id_pac_instance.pac_id)
        obj.dyna_flow_type_code_peek = (  # DynaFlowTypeID
            dyna_flow_type_id_dyna_flow_type_instance.code)
        obj.pac_code_peek = (  # PacID
            pac_id_pac_instance.code)
        session.add(obj)
        await session.flush()
        return obj

    @classmethod
    async def build_async(
        cls, session, *args, **kwargs
    ) -> DynaFlowTypeSchedule:  # pylint: disable=unused-argument
        """
        Build a new DynaFlowTypeSchedule object
        asynchronously.

        Args:
            session: The SQLAlchemy session object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The newly created DynaFlowTypeSchedule object.

        """
        dyna_flow_type_id_dyna_flow_type_instance = await (  # DynaFlowTypeID
            DynaFlowTypeFactory.create_async(session=session))
        pac_id_pac_instance = await (  # PacID
            PacFactory.create_async(session=session))
        kwargs["dyna_flow_type_id"] = (  # DynaFlowTypeID
            dyna_flow_type_id_dyna_flow_type_instance.dyna_flow_type_id)
        kwargs["pac_id"] = (  # PacID
            pac_id_pac_instance.pac_id)
        kwargs["dyna_flow_type_code_peek"] = (  # DynaFlowTypeID
            dyna_flow_type_id_dyna_flow_type_instance.code)
        kwargs["pac_code_peek"] = (  # PacID
            pac_id_pac_instance.code)
        obj = DynaFlowTypeScheduleFactory \
            .build(session=None, *args, **kwargs)
        obj.dyna_flow_type_id = (  # DynaFlowTypeID
            dyna_flow_type_id_dyna_flow_type_instance.dyna_flow_type_id)
        obj.pac_id = (  # PacID
            pac_id_pac_instance.pac_id)
        obj.dyna_flow_type_code_peek = (  # DynaFlowTypeID
            dyna_flow_type_id_dyna_flow_type_instance.code)
        obj.pac_code_peek = (  # PacID
            pac_id_pac_instance.code)
        return obj
