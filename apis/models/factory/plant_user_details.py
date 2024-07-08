# apis/models/factory/plant_user_details.py  # pylint: disable=duplicate-code
# pylint: disable=unused-import
"""
This module contains the factory class for creating
instances of the PlantUserDetailsGetModelRequest model.
"""

import uuid  # noqa: F401
from datetime import datetime, timezone  # noqa: F401

import factory
from factory import Faker  # noqa: F401
from sqlalchemy.ext.asyncio import AsyncSession

from ..plant_user_details import (
    PlantUserDetailsGetModelRequest)


class PlantUserDetailsGetModelRequestFactory(
    factory.base.Factory
):
    """
    Factory class for creating instances of the
    PlantUserDetailsGetModelRequest model.
    """

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Meta class for the factory.
        """
        model = PlantUserDetailsGetModelRequest


    @classmethod
    def _build(
        cls,
        model_class,
        *args,
        session=None,  # pylint: disable=unused-argument
        **kwargs
    ) -> PlantUserDetailsGetModelRequest:
        """
        Build a PlantUserDetailsGetModelRequest instance.

        Args:
            model_class: The model class to build an instance of.
            session: The session to use for creating related objects.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            PlantUserDetailsGetModelRequest: The built
                instance of PlantUserDetailsGetModelRequest.
        """
        if session is None:
            obj2 = model_class(*args, **kwargs)
            return obj2


        obj = model_class(*args, **kwargs)

        return obj

    @classmethod
    def _create(
        cls,
        model_class,
        *args,
        session=None,  # pylint: disable=unused-argument
        **kwargs
    ) -> PlantUserDetailsGetModelRequest:
        """
        Create a
        PlantUserDetailsGetModelRequest
        instance.

        Args:
            model_class: The model class to create an instance of.
            session: The session to use for creating related objects.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            PlantUserDetailsGetModelRequest: The created
                instance of PlantUserDetailsGetModelRequest.
        """


        obj = model_class(*args, **kwargs)

        return obj

    @classmethod
    async def create_async(
        cls,
        session: AsyncSession,  # pylint: disable=unused-argument
        *args, **kwargs
    ) -> PlantUserDetailsGetModelRequest:
        """
        Asynchronously create a
        PlantUserDetailsGetModelRequest instance.

        Args:
            session: The session to use for creating related objects.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            PlantUserDetailsGetModelRequest: The created
                instance of PlantUserDetailsGetModelRequest.
        """


        obj = PlantUserDetailsGetModelRequestFactory \
            .build(
                session=None,
                *args, **kwargs
            )

        return obj
