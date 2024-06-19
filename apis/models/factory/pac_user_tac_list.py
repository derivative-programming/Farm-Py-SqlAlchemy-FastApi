# apis/models/factory/pac_user_tac_list.py
# pylint: disable=unused-import
"""
This module contains the factory class for creating
instances of the PacUserTacListGetModelRequest model.
"""
import uuid
from datetime import datetime
import factory
from factory import Faker
from sqlalchemy.ext.asyncio import AsyncSession

from ..pac_user_tac_list import (
    PacUserTacListGetModelRequest)
class PacUserTacListGetModelRequestFactory(
    factory.base.Factory
):
    """
    Factory class for creating instances of the
    PacUserTacListGetModelRequest model.
    """
    class Meta:
        """
        Meta class for the factory.
        """
        model = PacUserTacListGetModelRequest

# endset
    @classmethod
    def _build(
        cls,
        model_class,
        session=None,
        *args, **kwargs
    ) -> PacUserTacListGetModelRequest:
        """
        Build a PacUserTacListGetModelRequest instance.
        Args:
            model_class: The model class to build an instance of.
            session: The session to use for creating related objects.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        Returns:
            PacUserTacListGetModelRequest: The built
                instance of PacUserTacListGetModelRequest.
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
    ) -> PacUserTacListGetModelRequest:
        """
        Create a PacUserTacListGetModelRequest instance.
        Args:
            model_class: The model class to create an instance of.
            session: The session to use for creating related objects.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        Returns:
            PacUserTacListGetModelRequest: The created
                instance of PacUserTacListGetModelRequest.
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
    ) -> PacUserTacListGetModelRequest:
        """
        Asynchronously create a PacUserTacListGetModelRequest instance.
        Args:
            session: The session to use for creating related objects.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        Returns:
            PacUserTacListGetModelRequest: The created
                instance of PacUserTacListGetModelRequest.
        """

# endset

# endset
        obj = PacUserTacListGetModelRequestFactory.build(
            session=None,
            *args, **kwargs
        )

# endset
        return obj
