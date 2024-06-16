# apis/models/factory/tac_login.py
# pylint: disable=unused-import
"""
Factory module for creating instances of TacLoginPostModelRequest with
various field values for testing.
"""
import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
import factory
from factory import Faker

from ..tac_login import TacLoginPostModelRequest
class TacLoginPostModelRequestFactory(factory.base.Factory):
    """
    Factory class for TacLoginPostModelRequest. Generates
    instances with randomized field values for testing.
    """
    class Meta:
        """
        Metadata for the factory class. Specifies the model to be used.
        """
        model = TacLoginPostModelRequest
    force_error_message = ""
    email = Faker('email')
    password = Faker(
        'sentence',
        nb_words=4
    )
# endset
    @classmethod
    def _build(
        cls, model_class, session=None, *args, **kwargs
    ) -> TacLoginPostModelRequest:
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
            An instance of TacLoginPostModelRequest.
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
    ) -> TacLoginPostModelRequest:
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
            An instance of TacLoginPostModelRequest.
        """

# endset

# endset
        obj = model_class(*args, **kwargs)

# endset
        return obj
    @classmethod
    async def create_async(
        cls, session: AsyncSession, *args, **kwargs
    ) -> TacLoginPostModelRequest:
        """
        Asynchronous create method for the factory. Uses the
        session to create related objects and persists the instance.
        Args:
            session: The asynchronous database session to be
                used for related object creation.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        Returns:
            An instance of TacLoginPostModelRequest.
        """

# endset

# endset
        obj = TacLoginPostModelRequestFactory.build(
            session=None, *args, **kwargs
        )

# endset
        return obj

