# apis/models/factory/pac_user_tri_state_filter_list.py
# pylint: disable=unused-import
"""
This module contains the factory class for creating
instances of the PacUserTriStateFilterListGetModelRequest model.
"""
import uuid
from datetime import datetime
import factory
from factory import Faker
from sqlalchemy.ext.asyncio import AsyncSession

from ..pac_user_tri_state_filter_list import (
    PacUserTriStateFilterListGetModelRequest)
class PacUserTriStateFilterListGetModelRequestFactory(
    factory.base.Factory
):
    """
    Factory class for creating instances of the
    PacUserTriStateFilterListGetModelRequest model.
    """
    class Meta:
        """
        Meta class for the factory.
        """
        model = PacUserTriStateFilterListGetModelRequest

# endset
    @classmethod
    def _build(
        cls,
        model_class,
        *args,
        session=None,
        **kwargs
    ) -> PacUserTriStateFilterListGetModelRequest:
        """
        Build a PacUserTriStateFilterListGetModelRequest instance.
        Args:
            model_class: The model class to build an instance of.
            session: The session to use for creating related objects.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        Returns:
            PacUserTriStateFilterListGetModelRequest: The built
                instance of PacUserTriStateFilterListGetModelRequest.
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
    ) -> PacUserTriStateFilterListGetModelRequest:
        """
        Create a PacUserTriStateFilterListGetModelRequest instance.
        Args:
            model_class: The model class to create an instance of.
            session: The session to use for creating related objects.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        Returns:
            PacUserTriStateFilterListGetModelRequest: The created
                instance of PacUserTriStateFilterListGetModelRequest.
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
    ) -> PacUserTriStateFilterListGetModelRequest:
        """
        Asynchronously create a PacUserTriStateFilterListGetModelRequest instance.
        Args:
            session: The session to use for creating related objects.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        Returns:
            PacUserTriStateFilterListGetModelRequest: The created
                instance of PacUserTriStateFilterListGetModelRequest.
        """

# endset

# endset
        obj = PacUserTriStateFilterListGetModelRequestFactory.build(
            session=None,
            *args, **kwargs
        )

# endset
        return obj
