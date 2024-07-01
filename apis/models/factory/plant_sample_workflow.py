# apis/models/factory/plant_sample_workflow.py
# pylint: disable=unused-import
"""
Factory module for creating instances of
PlantSampleWorkflowPostModelRequest with
various field values for testing.
"""

import uuid  # noqa: F401
from datetime import datetime  # noqa: F401
from sqlalchemy.ext.asyncio import AsyncSession
import factory
from factory import Faker  # noqa: F401

from ..plant_sample_workflow import (
    PlantSampleWorkflowPostModelRequest)


class PlantSampleWorkflowPostModelRequestFactory(
    factory.base.Factory
):
    """
    Factory class for
    PlantSampleWorkflowPostModelRequest.
    Generates instances with randomized
    field values for testing.
    """

    class Meta:
        """
        Metadata for the factory class. Specifies the model to be used.
        """
        model = PlantSampleWorkflowPostModelRequest

    force_error_message = ""


    @classmethod
    def _build(
        cls, model_class, *args, session=None, **kwargs
    ) -> PlantSampleWorkflowPostModelRequest:
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
            PlantSampleWorkflowPostModelRequest.
        """
        if session is None:
            obj2 = model_class(*args, **kwargs)
            return obj2


        obj = model_class(*args, **kwargs)

        return obj

    @classmethod
    def _create(
        cls, model_class, *args, session=None, **kwargs
    ) -> PlantSampleWorkflowPostModelRequest:
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
            PlantSampleWorkflowPostModelRequest.
        """


        obj = model_class(*args, **kwargs)

        return obj

    @classmethod
    async def create_async(
        cls, session: AsyncSession, *args, **kwargs
    ) -> PlantSampleWorkflowPostModelRequest:
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
            PlantSampleWorkflowPostModelRequest.
        """


        obj = PlantSampleWorkflowPostModelRequestFactory \
            .build(
                session=None, *args, **kwargs
            )

        return obj
