# apis/models/factory/pac_user_role_list.py
# pylint: disable=unused-import
"""
This module contains the factory class for creating
instances of the PacUserRoleListGetModelRequest model.
"""
import uuid
from datetime import datetime
import factory
from factory import Faker
from sqlalchemy.ext.asyncio import AsyncSession

from ..pac_user_role_list import (
    PacUserRoleListGetModelRequest)
class PacUserRoleListGetModelRequestFactory(
    factory.base.Factory
):
    """
    Factory class for creating instances of the
    PacUserRoleListGetModelRequest model.
    """
    class Meta:
        """
        Meta class for the factory.
        """
        model = PacUserRoleListGetModelRequest

# endset
    @classmethod
    def _build(
        cls,
        model_class,
        session=None,
        *args, **kwargs
    ) -> PacUserRoleListGetModelRequest:
        """
        Build a PacUserRoleListGetModelRequest instance.
        Args:
            model_class: The model class to build an instance of.
            session: The session to use for creating related objects.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        Returns:
            PacUserRoleListGetModelRequest: The built
                instance of PacUserRoleListGetModelRequest.
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
    ) -> PacUserRoleListGetModelRequest:
        """
        Create a PacUserRoleListGetModelRequest instance.
        Args:
            model_class: The model class to create an instance of.
            session: The session to use for creating related objects.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        Returns:
            PacUserRoleListGetModelRequest: The created
                instance of PacUserRoleListGetModelRequest.
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
    ) -> PacUserRoleListGetModelRequest:
        """
        Asynchronously create a PacUserRoleListGetModelRequest instance.
        Args:
            session: The session to use for creating related objects.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        Returns:
            PacUserRoleListGetModelRequest: The created
                instance of PacUserRoleListGetModelRequest.
        """

# endset

# endset
        obj = PacUserRoleListGetModelRequestFactory.build(
            session=None,
            *args, **kwargs
        )

# endset
        return obj
