# apis/models/factory/pac_user_flavor_list.py
# pylint: disable=unused-import
"""
This module contains the factory class for creating
instances of the PacUserFlavorListGetModelRequest model.
"""
import uuid
from datetime import datetime
import factory
from factory import Faker
from sqlalchemy.ext.asyncio import AsyncSession

from ..pac_user_flavor_list import (
    PacUserFlavorListGetModelRequest)
class PacUserFlavorListGetModelRequestFactory(
    factory.base.Factory
):
    """
    Factory class for creating instances of the
    PacUserFlavorListGetModelRequest model.
    """
    class Meta:
        """
        Meta class for the factory.
        """
        model = PacUserFlavorListGetModelRequest

# endset
    @classmethod
    def _build(
        cls,
        model_class,
        session=None,
        *args, **kwargs
    ) -> PacUserFlavorListGetModelRequest:
        """
        Build a PacUserFlavorListGetModelRequest instance.
        Args:
            model_class: The model class to build an instance of.
            session: The session to use for creating related objects.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        Returns:
            PacUserFlavorListGetModelRequest: The built
                instance of PacUserFlavorListGetModelRequest.
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
        session=None,
        *args, **kwargs
    ) -> PacUserFlavorListGetModelRequest:
        """
        Create a PacUserFlavorListGetModelRequest instance.
        Args:
            model_class: The model class to create an instance of.
            session: The session to use for creating related objects.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        Returns:
            PacUserFlavorListGetModelRequest: The created
                instance of PacUserFlavorListGetModelRequest.
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
    ) -> PacUserFlavorListGetModelRequest:
        """
        Asynchronously create a PacUserFlavorListGetModelRequest instance.
        Args:
            session: The session to use for creating related objects.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        Returns:
            PacUserFlavorListGetModelRequest: The created
                instance of PacUserFlavorListGetModelRequest.
        """

# endset

# endset
        obj = PacUserFlavorListGetModelRequestFactory.build(
            session=None,
            *args, **kwargs
        )

# endset
        return obj
