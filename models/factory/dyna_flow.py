# models/factory/dyna_flow.py  # pylint: disable=duplicate-code
# pylint: disable=unused-import
"""
This module contains the
DynaFlowFactory
class, which is responsible
for creating instances of the
DynaFlow
model using the Factory pattern.
"""

from datetime import datetime  # noqa: F401
import uuid  # noqa: F401
import factory
from factory import Faker
from models import DynaFlow
from services.logging_config import get_logger
from .dyna_flow_type import DynaFlowTypeFactory  # dyna_flow_type_id
from .pac import PacFactory  # pac_id
logger = get_logger(__name__)


class DynaFlowFactory(factory.Factory):
    """
    Factory class for creating instances of
    the DynaFlow model.
    """

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Meta class for the DynaFlowFactory.
        """

        model = DynaFlow

    code = factory.LazyFunction(uuid.uuid4)
    last_change_code = 0
    insert_user_id = factory.LazyFunction(uuid.uuid4)
    last_update_user_id = factory.LazyFunction(uuid.uuid4)
    completed_utc_date_time = factory.LazyFunction(datetime.utcnow)
    dependency_dyna_flow_id = Faker('random_int')
    description = Faker('sentence', nb_words=4)
    # dyna_flow_type_id
    is_build_task_debug_required = Faker('boolean')
    is_canceled = Faker('boolean')
    is_cancel_requested = Faker('boolean')
    is_completed = Faker('boolean')
    is_paused = Faker('boolean')
    is_resubmitted = Faker('boolean')
    is_run_task_debug_required = Faker('boolean')
    is_started = Faker('boolean')
    is_successful = Faker('boolean')
    is_task_creation_started = Faker('boolean')
    is_tasks_created = Faker('boolean')
    min_start_utc_date_time = factory.LazyFunction(datetime.utcnow)
    # pac_id
    param_1 = Faker('sentence', nb_words=4)
    parent_dyna_flow_id = Faker('random_int')
    priority_level = Faker('random_int')
    requested_utc_date_time = factory.LazyFunction(datetime.utcnow)
    result_value = Faker('sentence', nb_words=4)
    root_dyna_flow_id = Faker('random_int')
    started_utc_date_time = factory.LazyFunction(datetime.utcnow)
    subject_code = factory.LazyFunction(uuid.uuid4)
    task_creation_processor_identifier = Faker('sentence', nb_words=4)
    dyna_flow_type_code_peek = factory.LazyFunction(  # DynaFlowTypeID
        uuid.uuid4
    )
    pac_code_peek = factory.LazyFunction(  # PacID
        uuid.uuid4
    )

    @classmethod
    def _build(
        cls, model_class, *args, session=None, **kwargs
    ) -> DynaFlow:  # pylint: disable=unused-argument
        """
            Builds and returns an instance
            of the DynaFlow model.

            Args:
                model_class (class): The class of the model to be built.
                session (Session, optional): The SQLAlchemy
                session to be used. Defaults to None.
                *args: Variable length argument list.
                **kwargs: Arbitrary keyword arguments.

            Returns:
                DynaFlow:
                    An instance of the
                    DynaFlow model.

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
        kwargs["pac_code_peek"] = pac_id_pac_instance.code  # PacID
        obj = model_class(*args, **kwargs)
        obj.dyna_flow_type_id = (  # DynaFlowTypeID
            dyna_flow_type_id_dyna_flow_type_instance.dyna_flow_type_id)
        obj.pac_id = (  # PacID
            pac_id_pac_instance.pac_id)
        obj.dyna_flow_type_code_peek = (  # DynaFlowTypeID
            dyna_flow_type_id_dyna_flow_type_instance.code)
        obj.pac_code_peek = pac_id_pac_instance.code  # PacID
        return obj

    @classmethod
    def _create(
        cls, model_class, *args, session=None, **kwargs
    ) -> DynaFlow:  # pylint: disable=unused-argument
        """
        Create a new
        DynaFlow object
        and save it to the database.

        Args:
            model_class (class): The class of the model to create.
            session (Session): The SQLAlchemy session object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            DynaFlow: The created
                DynaFlow object.

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
        kwargs["pac_code_peek"] = pac_id_pac_instance.code  # PacID
        obj = model_class(*args, **kwargs)
        obj.dyna_flow_type_id = (  # DynaFlowTypeID
            dyna_flow_type_id_dyna_flow_type_instance.dyna_flow_type_id)
        obj.pac_id = (  # PacID
            pac_id_pac_instance.pac_id)
        obj.dyna_flow_type_code_peek = (  # DynaFlowTypeID
            dyna_flow_type_id_dyna_flow_type_instance.code)
        obj.pac_code_peek = pac_id_pac_instance.code  # PacID
        session.add(obj)
        session.commit()
        return obj

    @classmethod
    async def create_async(
        cls, session, *args, **kwargs
    ) -> DynaFlow:  # pylint: disable=unused-argument
        """
        Create a new
        DynaFlow object
        asynchronously.

        Args:
            session: The SQLAlchemy session object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The newly created DynaFlow object.

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
        kwargs["pac_code_peek"] = pac_id_pac_instance.code  # PacID
        obj = DynaFlowFactory \
            .build(session=None, *args, **kwargs)
        obj.dyna_flow_type_id = (  # DynaFlowTypeID
            dyna_flow_type_id_dyna_flow_type_instance.dyna_flow_type_id)
        obj.pac_id = (  # PacID
            pac_id_pac_instance.pac_id)
        obj.dyna_flow_type_code_peek = (  # DynaFlowTypeID
            dyna_flow_type_id_dyna_flow_type_instance.code)
        obj.pac_code_peek = pac_id_pac_instance.code  # PacID
        session.add(obj)
        await session.flush()
        return obj

    @classmethod
    async def build_async(
        cls, session, *args, **kwargs
    ) -> DynaFlow:  # pylint: disable=unused-argument
        """
        Build a new DynaFlow object
        asynchronously.

        Args:
            session: The SQLAlchemy session object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The newly created DynaFlow object.

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
        kwargs["pac_code_peek"] = pac_id_pac_instance.code  # PacID
        obj = DynaFlowFactory \
            .build(session=None, *args, **kwargs)
        obj.dyna_flow_type_id = (  # DynaFlowTypeID
            dyna_flow_type_id_dyna_flow_type_instance.dyna_flow_type_id)
        obj.pac_id = (  # PacID
            pac_id_pac_instance.pac_id)
        obj.dyna_flow_type_code_peek = (  # DynaFlowTypeID
            dyna_flow_type_id_dyna_flow_type_instance.code)
        obj.pac_code_peek = pac_id_pac_instance.code  # PacID
        return obj
