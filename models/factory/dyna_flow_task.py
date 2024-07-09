# models/factory/dyna_flow_task.py  # pylint: disable=duplicate-code
# pylint: disable=unused-import
"""
This module contains the
DynaFlowTaskFactory
class, which is responsible
for creating instances of the
DynaFlowTask
model using the Factory pattern.
"""

from datetime import datetime  # noqa: F401
import uuid  # noqa: F401
import factory
from factory import Faker
from models import DynaFlowTask
from services.logging_config import get_logger
from .dyna_flow import DynaFlowFactory  # dyna_flow_id
from .dyna_flow_task_type import DynaFlowTaskTypeFactory  # dyna_flow_task_type_id
logger = get_logger(__name__)


class DynaFlowTaskFactory(factory.Factory):
    """
    Factory class for creating instances of
    the DynaFlowTask model.
    """

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Meta class for the DynaFlowTaskFactory.
        """

        model = DynaFlowTask

    code = factory.LazyFunction(uuid.uuid4)
    last_change_code = 0
    insert_user_id = factory.LazyFunction(uuid.uuid4)
    last_update_user_id = factory.LazyFunction(uuid.uuid4)
    completed_utc_date_time = factory.LazyFunction(datetime.utcnow)
    dependency_dyna_flow_task_id = Faker('random_int')
    description = Faker('sentence', nb_words=4)
    # dyna_flow_id
    dyna_flow_subject_code = factory.LazyFunction(uuid.uuid4)
    # dyna_flow_task_type_id
    is_canceled = Faker('boolean')
    is_cancel_requested = Faker('boolean')
    is_completed = Faker('boolean')
    is_parallel_run_allowed = Faker('boolean')
    is_run_task_debug_required = Faker('boolean')
    is_started = Faker('boolean')
    is_successful = Faker('boolean')
    max_retry_count = Faker('random_int')
    min_start_utc_date_time = factory.LazyFunction(datetime.utcnow)
    param_1 = Faker('sentence', nb_words=4)
    param_2 = Faker('sentence', nb_words=4)
    processor_identifier = Faker('sentence', nb_words=4)
    requested_utc_date_time = factory.LazyFunction(datetime.utcnow)
    result_value = Faker('sentence', nb_words=4)
    retry_count = Faker('random_int')
    started_utc_date_time = factory.LazyFunction(datetime.utcnow)
    dyna_flow_code_peek = factory.LazyFunction(  # DynaFlowID
        uuid.uuid4
    )
    dyna_flow_task_type_code_peek = factory.LazyFunction(  # DynaFlowTaskTypeID
        uuid.uuid4
    )

    @classmethod
    def _build(
        cls, model_class, *args, session=None, **kwargs
    ) -> DynaFlowTask:  # pylint: disable=unused-argument
        """
            Builds and returns an instance
            of the DynaFlowTask model.

            Args:
                model_class (class): The class of the model to be built.
                session (Session, optional): The SQLAlchemy
                session to be used. Defaults to None.
                *args: Variable length argument list.
                **kwargs: Arbitrary keyword arguments.

            Returns:
                DynaFlowTask:
                    An instance of the
                    DynaFlowTask model.

        """
        if session is None:
            obj2 = model_class(*args, **kwargs)
            return obj2
        dyna_flow_id_dyna_flow_instance = (  # DynaFlowID
            DynaFlowFactory.create(session=session))
        dyna_flow_task_type_id_dyna_flow_task_type_instance = (  # DynaFlowTaskTypeID
            DynaFlowTaskTypeFactory.create(session=session))
        kwargs["dyna_flow_id"] = (  # DynaFlowID
            dyna_flow_id_dyna_flow_instance.dyna_flow_id)
        kwargs["dyna_flow_task_type_id"] = (  # DynaFlowTaskTypeID
            dyna_flow_task_type_id_dyna_flow_task_type_instance.dyna_flow_task_type_id)
        kwargs["dyna_flow_code_peek"] = (  # DynaFlowID
            dyna_flow_id_dyna_flow_instance.code)
        kwargs["dyna_flow_task_type_code_peek"] = (  # DynaFlowTaskTypeID
            dyna_flow_task_type_id_dyna_flow_task_type_instance.code)
        obj = model_class(*args, **kwargs)
        obj.dyna_flow_id = (  # DynaFlowID
            dyna_flow_id_dyna_flow_instance.dyna_flow_id)
        obj.dyna_flow_task_type_id = (  # DynaFlowTaskTypeID
            dyna_flow_task_type_id_dyna_flow_task_type_instance.dyna_flow_task_type_id)
        obj.dyna_flow_code_peek = (  # DynaFlowID
            dyna_flow_id_dyna_flow_instance.code)
        obj.dyna_flow_task_type_code_peek = (  # DynaFlowTaskTypeID
            dyna_flow_task_type_id_dyna_flow_task_type_instance.code)
        return obj

    @classmethod
    def _create(
        cls, model_class, *args, session=None, **kwargs
    ) -> DynaFlowTask:  # pylint: disable=unused-argument
        """
        Create a new
        DynaFlowTask object
        and save it to the database.

        Args:
            model_class (class): The class of the model to create.
            session (Session): The SQLAlchemy session object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            DynaFlowTask: The created
                DynaFlowTask object.

        """
        logger.info("factory create")
        if not session:
            raise AttributeError(
                "Session not available"
            )
        dyna_flow_id_dyna_flow_instance = (  # DynaFlowID
            DynaFlowFactory.create(session=session))
        dyna_flow_task_type_id_dyna_flow_task_type_instance = (  # DynaFlowTaskTypeID
            DynaFlowTaskTypeFactory.create(session=session))
        kwargs["dyna_flow_id"] = (  # DynaFlowID
            dyna_flow_id_dyna_flow_instance.dyna_flow_id)
        kwargs["dyna_flow_task_type_id"] = (  # DynaFlowTaskTypeID
            dyna_flow_task_type_id_dyna_flow_task_type_instance.dyna_flow_task_type_id)
        kwargs["dyna_flow_code_peek"] = (  # DynaFlowID
            dyna_flow_id_dyna_flow_instance.code)
        kwargs["dyna_flow_task_type_code_peek"] = (  # DynaFlowTaskTypeID
            dyna_flow_task_type_id_dyna_flow_task_type_instance.code)
        obj = model_class(*args, **kwargs)
        obj.dyna_flow_id = (  # DynaFlowID
            dyna_flow_id_dyna_flow_instance.dyna_flow_id)
        obj.dyna_flow_task_type_id = (  # DynaFlowTaskTypeID
            dyna_flow_task_type_id_dyna_flow_task_type_instance.dyna_flow_task_type_id)
        obj.dyna_flow_code_peek = (  # DynaFlowID
            dyna_flow_id_dyna_flow_instance.code)
        obj.dyna_flow_task_type_code_peek = (  # DynaFlowTaskTypeID
            dyna_flow_task_type_id_dyna_flow_task_type_instance.code)
        session.add(obj)
        session.commit()
        return obj

    @classmethod
    async def create_async(
        cls, session, *args, **kwargs
    ) -> DynaFlowTask:  # pylint: disable=unused-argument
        """
        Create a new
        DynaFlowTask object
        asynchronously.

        Args:
            session: The SQLAlchemy session object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The newly created DynaFlowTask object.

        """
        dyna_flow_id_dyna_flow_instance = await (  # DynaFlowID
            DynaFlowFactory.create_async(session=session))
        dyna_flow_task_type_id_dyna_flow_task_type_instance = await (  # DynaFlowTaskTypeID
            DynaFlowTaskTypeFactory.create_async(session=session))
        kwargs["dyna_flow_id"] = (  # DynaFlowID
            dyna_flow_id_dyna_flow_instance.dyna_flow_id)
        kwargs["dyna_flow_task_type_id"] = (  # DynaFlowTaskTypeID
            dyna_flow_task_type_id_dyna_flow_task_type_instance.dyna_flow_task_type_id)
        kwargs["dyna_flow_code_peek"] = (  # DynaFlowID
            dyna_flow_id_dyna_flow_instance.code)
        kwargs["dyna_flow_task_type_code_peek"] = (  # DynaFlowTaskTypeID
            dyna_flow_task_type_id_dyna_flow_task_type_instance.code)
        obj = DynaFlowTaskFactory \
            .build(session=None, *args, **kwargs)
        obj.dyna_flow_id = (  # DynaFlowID
            dyna_flow_id_dyna_flow_instance.dyna_flow_id)
        obj.dyna_flow_task_type_id = (  # DynaFlowTaskTypeID
            dyna_flow_task_type_id_dyna_flow_task_type_instance.dyna_flow_task_type_id)
        obj.dyna_flow_code_peek = (  # DynaFlowID
            dyna_flow_id_dyna_flow_instance.code)
        obj.dyna_flow_task_type_code_peek = (  # DynaFlowTaskTypeID
            dyna_flow_task_type_id_dyna_flow_task_type_instance.code)
        session.add(obj)
        await session.flush()
        return obj

    @classmethod
    async def build_async(
        cls, session, *args, **kwargs
    ) -> DynaFlowTask:  # pylint: disable=unused-argument
        """
        Build a new DynaFlowTask object
        asynchronously.

        Args:
            session: The SQLAlchemy session object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The newly created DynaFlowTask object.

        """
        dyna_flow_id_dyna_flow_instance = await (  # DynaFlowID
            DynaFlowFactory.create_async(session=session))
        dyna_flow_task_type_id_dyna_flow_task_type_instance = await (  # DynaFlowTaskTypeID
            DynaFlowTaskTypeFactory.create_async(session=session))
        kwargs["dyna_flow_id"] = (  # DynaFlowID
            dyna_flow_id_dyna_flow_instance.dyna_flow_id)
        kwargs["dyna_flow_task_type_id"] = (  # DynaFlowTaskTypeID
            dyna_flow_task_type_id_dyna_flow_task_type_instance.dyna_flow_task_type_id)
        kwargs["dyna_flow_code_peek"] = (  # DynaFlowID
            dyna_flow_id_dyna_flow_instance.code)
        kwargs["dyna_flow_task_type_code_peek"] = (  # DynaFlowTaskTypeID
            dyna_flow_task_type_id_dyna_flow_task_type_instance.code)
        obj = DynaFlowTaskFactory \
            .build(session=None, *args, **kwargs)
        obj.dyna_flow_id = (  # DynaFlowID
            dyna_flow_id_dyna_flow_instance.dyna_flow_id)
        obj.dyna_flow_task_type_id = (  # DynaFlowTaskTypeID
            dyna_flow_task_type_id_dyna_flow_task_type_instance.dyna_flow_task_type_id)
        obj.dyna_flow_code_peek = (  # DynaFlowID
            dyna_flow_id_dyna_flow_instance.code)
        obj.dyna_flow_task_type_code_peek = (  # DynaFlowTaskTypeID
            dyna_flow_task_type_id_dyna_flow_task_type_instance.code)
        return obj
