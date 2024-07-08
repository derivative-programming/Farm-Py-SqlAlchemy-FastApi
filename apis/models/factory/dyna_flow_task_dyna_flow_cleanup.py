# apis/models/factory/dyna_flow_task_dyna_flow_cleanup.py  # pylint: disable=duplicate-code
# pylint: disable=unused-import
"""
Factory module for creating instances of
DynaFlowTaskDynaFlowCleanupPostModelRequest with
various field values for testing.
"""

import uuid  # noqa: F401
from datetime import datetime, timezone  # noqa: F401
from sqlalchemy.ext.asyncio import AsyncSession
import factory
from factory import Faker  # noqa: F401

from ..dyna_flow_task_dyna_flow_cleanup import (
    DynaFlowTaskDynaFlowCleanupPostModelRequest)


class DynaFlowTaskDynaFlowCleanupPostModelRequestFactory(
    factory.base.Factory
):
    """
    Factory class for
    DynaFlowTaskDynaFlowCleanupPostModelRequest.
    Generates instances with randomized
    field values for testing.
    """

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Metadata for the factory class. Specifies the model to be used.
        """
        model = DynaFlowTaskDynaFlowCleanupPostModelRequest

    force_error_message = ""


    @classmethod
    def _build(
        cls, model_class, *args, session=None, **kwargs  # pylint: disable=unused-argument
    ) -> DynaFlowTaskDynaFlowCleanupPostModelRequest:
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
            DynaFlowTaskDynaFlowCleanupPostModelRequest.
        """
        if session is None:
            obj2 = model_class(*args, **kwargs)
            return obj2


        obj = model_class(*args, **kwargs)

        return obj

    @classmethod
    def _create(
        cls, model_class, *args, session=None, **kwargs  # pylint: disable=unused-argument
    ) -> DynaFlowTaskDynaFlowCleanupPostModelRequest:
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
            DynaFlowTaskDynaFlowCleanupPostModelRequest.
        """


        obj = model_class(*args, **kwargs)

        return obj

    @classmethod
    async def create_async(
        cls, session: AsyncSession, *args, **kwargs  # pylint: disable=unused-argument
    ) -> DynaFlowTaskDynaFlowCleanupPostModelRequest:
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
            DynaFlowTaskDynaFlowCleanupPostModelRequest.
        """


        obj = DynaFlowTaskDynaFlowCleanupPostModelRequestFactory \
            .build(
                session=None, *args, **kwargs
            )

        return obj
