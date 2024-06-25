# apis/models/factory/pac_user_date_greater_than_filter_list.py
# pylint: disable=unused-import
"""
This module contains the factory class for creating
instances of the PacUserDateGreaterThanFilterListGetModelRequest model.
"""

import uuid  # noqa: F401
from datetime import datetime  # noqa: F401

import factory
from factory import Faker  # noqa: F401
from sqlalchemy.ext.asyncio import AsyncSession

from ..pac_user_date_greater_than_filter_list import (
    PacUserDateGreaterThanFilterListGetModelRequest)


class PacUserDateGreaterThanFilterListGetModelRequestFactory(
    factory.base.Factory
):
    """
    Factory class for creating instances of the
    PacUserDateGreaterThanFilterListGetModelRequest model.
    """

    class Meta:
        """
        Meta class for the factory.
        """
        model = PacUserDateGreaterThanFilterListGetModelRequest


    @classmethod
    def _build(
        cls,
        model_class,
        *args,
        session=None,
        **kwargs
    ) -> PacUserDateGreaterThanFilterListGetModelRequest:
        """
        Build a PacUserDateGreaterThanFilterListGetModelRequest instance.

        Args:
            model_class: The model class to build an instance of.
            session: The session to use for creating related objects.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            PacUserDateGreaterThanFilterListGetModelRequest: The built
                instance of PacUserDateGreaterThanFilterListGetModelRequest.
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
        session=None,
        **kwargs
    ) -> PacUserDateGreaterThanFilterListGetModelRequest:
        """
        Create a
        PacUserDateGreaterThanFilterListGetModelRequest
        instance.

        Args:
            model_class: The model class to create an instance of.
            session: The session to use for creating related objects.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            PacUserDateGreaterThanFilterListGetModelRequest: The created
                instance of PacUserDateGreaterThanFilterListGetModelRequest.
        """


        obj = model_class(*args, **kwargs)

        return obj

    @classmethod
    async def create_async(
        cls,
        session: AsyncSession,
        *args, **kwargs
    ) -> PacUserDateGreaterThanFilterListGetModelRequest:
        """
        Asynchronously create a
        PacUserDateGreaterThanFilterListGetModelRequest instance.

        Args:
            session: The session to use for creating related objects.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            PacUserDateGreaterThanFilterListGetModelRequest: The created
                instance of PacUserDateGreaterThanFilterListGetModelRequest.
        """


        obj = PacUserDateGreaterThanFilterListGetModelRequestFactory.build(
            session=None,
            *args, **kwargs
        )

        return obj

