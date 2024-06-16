# apis/models/factory/customer_user_log_out.py
# pylint: disable=unused-import
"""
Factory module for creating instances of CustomerUserLogOutPostModelRequest with
various field values for testing.
"""
import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
import factory
from factory import Faker

from ..customer_user_log_out import CustomerUserLogOutPostModelRequest
class CustomerUserLogOutPostModelRequestFactory(factory.base.Factory):
    """
    Factory class for CustomerUserLogOutPostModelRequest. Generates
    instances with randomized field values for testing.
    """
    class Meta:
        """
        Metadata for the factory class. Specifies the model to be used.
        """
        model = CustomerUserLogOutPostModelRequest
    force_error_message = ""

# endset
    @classmethod
    def _build(
        cls, model_class, session=None, *args, **kwargs
    ) -> CustomerUserLogOutPostModelRequest:
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
            An instance of CustomerUserLogOutPostModelRequest.
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
    ) -> CustomerUserLogOutPostModelRequest:
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
            An instance of CustomerUserLogOutPostModelRequest.
        """

# endset

# endset
        obj = model_class(*args, **kwargs)

# endset
        return obj
    @classmethod
    async def create_async(
        cls, session: AsyncSession, *args, **kwargs
    ) -> CustomerUserLogOutPostModelRequest:
        """
        Asynchronous create method for the factory. Uses the
        session to create related objects and persists the instance.
        Args:
            session: The asynchronous database session to be
                used for related object creation.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        Returns:
            An instance of CustomerUserLogOutPostModelRequest.
        """

# endset

# endset
        obj = CustomerUserLogOutPostModelRequestFactory.build(
            session=None, *args, **kwargs
        )

# endset
        return obj

