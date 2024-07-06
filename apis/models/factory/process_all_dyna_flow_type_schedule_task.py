# apis/models/factory/process_all_dyna_flow_type_schedule_task.py  # pylint: disable=duplicate-code
# pylint: disable=unused-import
"""
Factory module for creating instances of
ProcessAllDynaFlowTypeScheduleTaskPostModelRequest with
various field values for testing.
"""

import uuid  # noqa: F401
from datetime import datetime, timezone  # noqa: F401
from sqlalchemy.ext.asyncio import AsyncSession
import factory
from factory import Faker  # noqa: F401

from ..process_all_dyna_flow_type_schedule_task import (
    ProcessAllDynaFlowTypeScheduleTaskPostModelRequest)


class ProcessAllDynaFlowTypeScheduleTaskPostModelRequestFactory(
    factory.base.Factory
):
    """
    Factory class for
    ProcessAllDynaFlowTypeScheduleTaskPostModelRequest.
    Generates instances with randomized
    field values for testing.
    """

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Metadata for the factory class. Specifies the model to be used.
        """
        model = ProcessAllDynaFlowTypeScheduleTaskPostModelRequest

    force_error_message = ""


    @classmethod
    def _build(
        cls, model_class, *args, session=None, **kwargs
    ) -> ProcessAllDynaFlowTypeScheduleTaskPostModelRequest:
        """
        Build method for the factory. If a session is provided,
        it uses the session to create related objects.

        Args:
            model_class: The model class to be instantiated.
            session: The database session to be used for related
                object creation.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            An instance of
            ProcessAllDynaFlowTypeScheduleTaskPostModelRequest.
        """
        if session is None:
            obj2 = model_class(*args, **kwargs)
            return obj2


        obj = model_class(*args, **kwargs)

        return obj

    @classmethod
    def _create(
        cls, model_class, *args, session=None, **kwargs
    ) -> ProcessAllDynaFlowTypeScheduleTaskPostModelRequest:
        """
        Create method for the factory. Uses the session to
        create related objects and persists the instance.

        Args:
            model_class: The model class to be instantiated.
            session: The database session to be used for related
                object creation.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            An instance of
            ProcessAllDynaFlowTypeScheduleTaskPostModelRequest.
        """


        obj = model_class(*args, **kwargs)

        return obj

    @classmethod
    async def create_async(
        cls, session: AsyncSession, *args, **kwargs
    ) -> ProcessAllDynaFlowTypeScheduleTaskPostModelRequest:
        """
        Asynchronous create method for the factory. Uses the
        session to create related objects and persists the instance.

        Args:
            session: The asynchronous database session to be
                used for related object creation.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            An instance of
            ProcessAllDynaFlowTypeScheduleTaskPostModelRequest.
        """


        obj = ProcessAllDynaFlowTypeScheduleTaskPostModelRequestFactory \
            .build(
                session=None, *args, **kwargs
            )

        return obj
