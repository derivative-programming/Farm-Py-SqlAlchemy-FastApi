# models/factory/dft_dependency.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import
"""
This module contains the
DFTDependencyFactory
class, which is responsible
for creating instances of the
DFTDependency
model using the Factory pattern.
"""

from datetime import datetime  # noqa: F401
import uuid  # noqa: F401
import factory
from factory import Faker
from models import DFTDependency
from services.logging_config import get_logger
from .dyna_flow_task import DynaFlowTaskFactory  # dyna_flow_task_id
logger = get_logger(__name__)


class DFTDependencyFactory(factory.Factory):
    """
    Factory class for creating instances of
    the DFTDependency model.
    """

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Meta class for the DFTDependencyFactory.
        """

        model = DFTDependency

    code = factory.LazyFunction(uuid.uuid4)
    last_change_code = 0
    insert_user_id = factory.LazyFunction(uuid.uuid4)
    last_update_user_id = factory.LazyFunction(uuid.uuid4)
    dependency_df_task_id = Faker('random_int')
    # dyna_flow_task_id
    is_placeholder = Faker('boolean')
    dyna_flow_task_code_peek = factory.LazyFunction(  # DynaFlowTaskID
        uuid.uuid4
    )

    @classmethod
    def _build(
        cls, model_class, *args, session=None, **kwargs
    ) -> DFTDependency:  # pylint: disable=unused-argument
        """
            Builds and returns an instance
            of the DFTDependency model.

            Args:
                model_class (class): The class of the model to be built.
                session (Session, optional): The SQLAlchemy
                session to be used. Defaults to None.
                *args: Variable length argument list.
                **kwargs: Arbitrary keyword arguments.

            Returns:
                DFTDependency:
                    An instance of the
                    DFTDependency model.

        """
        if session is None:
            obj2 = model_class(*args, **kwargs)
            return obj2
        dyna_flow_task_id_dyna_flow_task_instance = (  # DynaFlowTaskID
            DynaFlowTaskFactory.create(session=session))
        kwargs["dyna_flow_task_id"] = (  # DynaFlowTaskID
            dyna_flow_task_id_dyna_flow_task_instance.dyna_flow_task_id)
        kwargs["dyna_flow_task_code_peek"] = (  # DynaFlowTaskID
            dyna_flow_task_id_dyna_flow_task_instance.code)
        obj = model_class(*args, **kwargs)
        obj.dyna_flow_task_id = (  # DynaFlowTaskID
            dyna_flow_task_id_dyna_flow_task_instance.dyna_flow_task_id)
        obj.dyna_flow_task_code_peek = (  # DynaFlowTaskID
            dyna_flow_task_id_dyna_flow_task_instance.code)
        return obj

    @classmethod
    def _create(
        cls, model_class, *args, session=None, **kwargs
    ) -> DFTDependency:  # pylint: disable=unused-argument
        """
        Create a new
        DFTDependency object
        and save it to the database.

        Args:
            model_class (class): The class of the model to create.
            session (Session): The SQLAlchemy session object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            DFTDependency: The created
                DFTDependency object.

        """
        logger.info("factory create")
        if not session:
            raise AttributeError(
                "Session not available"
            )
        dyna_flow_task_id_dyna_flow_task_instance = (  # DynaFlowTaskID
            DynaFlowTaskFactory.create(session=session))
        kwargs["dyna_flow_task_id"] = (  # DynaFlowTaskID
            dyna_flow_task_id_dyna_flow_task_instance.dyna_flow_task_id)
        kwargs["dyna_flow_task_code_peek"] = (  # DynaFlowTaskID
            dyna_flow_task_id_dyna_flow_task_instance.code)
        obj = model_class(*args, **kwargs)
        obj.dyna_flow_task_id = (  # DynaFlowTaskID
            dyna_flow_task_id_dyna_flow_task_instance.dyna_flow_task_id)
        obj.dyna_flow_task_code_peek = (  # DynaFlowTaskID
            dyna_flow_task_id_dyna_flow_task_instance.code)
        session.add(obj)
        session.commit()
        return obj

    @classmethod
    async def create_async(
        cls, session, *args, **kwargs
    ) -> DFTDependency:  # pylint: disable=unused-argument
        """
        Create a new
        DFTDependency object
        asynchronously.

        Args:
            session: The SQLAlchemy session object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The newly created DFTDependency object.

        """
        dyna_flow_task_id_dyna_flow_task_instance = await (  # DynaFlowTaskID
            DynaFlowTaskFactory.create_async(session=session))
        kwargs["dyna_flow_task_id"] = (  # DynaFlowTaskID
            dyna_flow_task_id_dyna_flow_task_instance.dyna_flow_task_id)
        kwargs["dyna_flow_task_code_peek"] = (  # DynaFlowTaskID
            dyna_flow_task_id_dyna_flow_task_instance.code)
        obj = DFTDependencyFactory \
            .build(session=None, *args, **kwargs)
        obj.dyna_flow_task_id = (  # DynaFlowTaskID
            dyna_flow_task_id_dyna_flow_task_instance.dyna_flow_task_id)
        obj.dyna_flow_task_code_peek = (  # DynaFlowTaskID
            dyna_flow_task_id_dyna_flow_task_instance.code)
        session.add(obj)
        await session.flush()
        return obj

    @classmethod
    async def build_async(
        cls, session, *args, **kwargs
    ) -> DFTDependency:  # pylint: disable=unused-argument
        """
        Build a new DFTDependency object
        asynchronously.

        Args:
            session: The SQLAlchemy session object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The newly created DFTDependency object.

        """
        dyna_flow_task_id_dyna_flow_task_instance = await (  # DynaFlowTaskID
            DynaFlowTaskFactory.create_async(session=session))
        kwargs["dyna_flow_task_id"] = (  # DynaFlowTaskID
            dyna_flow_task_id_dyna_flow_task_instance.dyna_flow_task_id)
        kwargs["dyna_flow_task_code_peek"] = (  # DynaFlowTaskID
            dyna_flow_task_id_dyna_flow_task_instance.code)
        obj = DFTDependencyFactory \
            .build(session=None, *args, **kwargs)
        obj.dyna_flow_task_id = (  # DynaFlowTaskID
            dyna_flow_task_id_dyna_flow_task_instance.dyna_flow_task_id)
        obj.dyna_flow_task_code_peek = (  # DynaFlowTaskID
            dyna_flow_task_id_dyna_flow_task_instance.code)
        return obj
