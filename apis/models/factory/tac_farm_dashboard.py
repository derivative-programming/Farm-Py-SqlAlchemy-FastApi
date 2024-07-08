# apis/models/factory/tac_farm_dashboard.py  # pylint: disable=duplicate-code
# pylint: disable=unused-import
"""
This module contains the factory class for creating
instances of the TacFarmDashboardGetModelRequest model.
"""

import uuid  # noqa: F401
from datetime import datetime, timezone  # noqa: F401

import factory
from factory import Faker  # noqa: F401
from sqlalchemy.ext.asyncio import AsyncSession

from ..tac_farm_dashboard import (
    TacFarmDashboardGetModelRequest)


class TacFarmDashboardGetModelRequestFactory(
    factory.base.Factory
):
    """
    Factory class for creating instances of the
    TacFarmDashboardGetModelRequest model.
    """

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Meta class for the factory.
        """
        model = TacFarmDashboardGetModelRequest


    @classmethod
    def _build(
        cls,
        model_class,
        *args,
        session=None,  # pylint: disable=unused-argument
        **kwargs
    ) -> TacFarmDashboardGetModelRequest:
        """
        Build a TacFarmDashboardGetModelRequest instance.

        Args:
            model_class: The model class to build an instance of.
            session: The session to use for creating related objects.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            TacFarmDashboardGetModelRequest: The built
                instance of TacFarmDashboardGetModelRequest.
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
    ) -> TacFarmDashboardGetModelRequest:
        """
        Create a
        TacFarmDashboardGetModelRequest
        instance.

        Args:
            model_class: The model class to create an instance of.
            session: The session to use for creating related objects.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            TacFarmDashboardGetModelRequest: The created
                instance of TacFarmDashboardGetModelRequest.
        """


        obj = model_class(*args, **kwargs)

        return obj

    @classmethod
    async def create_async(
        cls,
        session: AsyncSession,  # pylint: disable=unused-argument
        *args, **kwargs
    ) -> TacFarmDashboardGetModelRequest:
        """
        Asynchronously create a
        TacFarmDashboardGetModelRequest instance.

        Args:
            session: The session to use for creating related objects.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            TacFarmDashboardGetModelRequest: The created
                instance of TacFarmDashboardGetModelRequest.
        """


        obj = TacFarmDashboardGetModelRequestFactory \
            .build(
                session=None,
                *args, **kwargs
            )

        return obj
