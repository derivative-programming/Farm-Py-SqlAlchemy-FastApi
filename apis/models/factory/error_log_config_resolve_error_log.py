# apis/models/factory/error_log_config_resolve_error_log.py
# pylint: disable=unused-import
"""
Factory module for creating instances of ErrorLogConfigResolveErrorLogPostModelRequest with
various field values for testing.
"""
import uuid
from datetime import date, datetime
from decimal import Decimal
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession
import factory
from factory import Faker

from ..error_log_config_resolve_error_log import ErrorLogConfigResolveErrorLogPostModelRequest
class ErrorLogConfigResolveErrorLogPostModelRequestFactory(factory.base.Factory):
    """
    Factory class for ErrorLogConfigResolveErrorLogPostModelRequest. Generates
    instances with randomized field values for testing.
    """
    class Meta:
        """
        Metadata for the factory class. Specifies the model to be used.
        """
        model = ErrorLogConfigResolveErrorLogPostModelRequest
    force_error_message = ""

# endset
    @classmethod
    def _build(
        cls, model_class, session=None, *args, **kwargs
    ) -> ErrorLogConfigResolveErrorLogPostModelRequest:
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
            An instance of ErrorLogConfigResolveErrorLogPostModelRequest.
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
        cls, model_class, session=None, *args, **kwargs
    ) -> ErrorLogConfigResolveErrorLogPostModelRequest:
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
            An instance of ErrorLogConfigResolveErrorLogPostModelRequest.
        """

# endset

# endset
        obj = model_class(*args, **kwargs)

# endset
        return obj
    @classmethod
    async def create_async(
        cls, session: AsyncSession, *args, **kwargs
    ) -> ErrorLogConfigResolveErrorLogPostModelRequest:
        """
        Asynchronous create method for the factory. Uses the
        session to create related objects and persists the instance.
        Args:
            session: The asynchronous database session to be
                used for related object creation.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        Returns:
            An instance of ErrorLogConfigResolveErrorLogPostModelRequest.
        """

# endset

# endset
        obj = ErrorLogConfigResolveErrorLogPostModelRequestFactory.build(
            session=None, *args, **kwargs
        )

# endset
        return obj

