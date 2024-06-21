# apis/models/factory/plant_user_details.py
# pylint: disable=unused-import
"""
This module contains the factory class for creating
instances of the PlantUserDetailsGetModelRequest model.
"""
import uuid
from datetime import datetime
import factory
from factory import Faker
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
    class Meta:
        """
        Meta class for the factory.
        """
        model = PlantUserDetailsGetModelRequest

# endset
    @classmethod
    def _build(
        cls,
        model_class,
        *args,
        session=None,
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

# endset

# endset
        obj = model_class(*args, **kwargs)

# endset
        return obj
    @classmethod
    def _create(
        cls,
        model_class,
        *args,
        session=None,
        **kwargs
    ) -> PlantUserDetailsGetModelRequest:
        """
        Create a PlantUserDetailsGetModelRequest instance.
        Args:
            model_class: The model class to create an instance of.
            session: The session to use for creating related objects.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        Returns:
            PlantUserDetailsGetModelRequest: The created
                instance of PlantUserDetailsGetModelRequest.
        """

# endset

# endset
        obj = model_class(*args, **kwargs)

# endset
        return obj
    @classmethod
    async def create_async(
        cls,
        session: AsyncSession,
        *args, **kwargs
    ) -> PlantUserDetailsGetModelRequest:
        """
        Asynchronously create a PlantUserDetailsGetModelRequest instance.
        Args:
            session: The session to use for creating related objects.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        Returns:
            PlantUserDetailsGetModelRequest: The created
                instance of PlantUserDetailsGetModelRequest.
        """

# endset

# endset
        obj = PlantUserDetailsGetModelRequestFactory.build(
            session=None,
            *args, **kwargs
        )

# endset
        return obj
