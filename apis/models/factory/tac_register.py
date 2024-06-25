# apis/models/factory/tac_register.py
# pylint: disable=unused-import
"""
Factory module for creating instances of TacRegisterPostModelRequest with
various field values for testing.
"""

import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
import factory
from factory import Faker

from ..tac_register import (
    TacRegisterPostModelRequest)


class TacRegisterPostModelRequestFactory(factory.base.Factory):
    """
    Factory class for TacRegisterPostModelRequest. Generates
    instances with randomized field values for testing.
    """

    class Meta:
        """
        Metadata for the factory class. Specifies the model to be used.
        """
        model = TacRegisterPostModelRequest

    force_error_message = ""
    email = Faker('email')
    password = Faker(
        'sentence',
        nb_words=4
    )
    confirm_password = Faker(
        'sentence',
        nb_words=4
    )
    first_name = Faker(
        'sentence',
        nb_words=4
    )
    last_name = Faker(
        'sentence',
        nb_words=4
    )

    @classmethod
    def _build(
        cls, model_class, *args, session=None, **kwargs
    ) -> TacRegisterPostModelRequest:
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
            An instance of
            TacRegisterPostModelRequest.
        """

        if session is None:
            obj2 = model_class(*args, **kwargs)
            return obj2


        obj = model_class(*args, **kwargs)


        return obj

    @classmethod
    def _create(
        cls, model_class, *args, session=None, **kwargs
    ) -> TacRegisterPostModelRequest:
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
            An instance of
            TacRegisterPostModelRequest.
        """


        obj = model_class(*args, **kwargs)


        return obj

    @classmethod
    async def create_async(
        cls, session: AsyncSession, *args, **kwargs
    ) -> TacRegisterPostModelRequest:
        """
        Asynchronous create method for the factory. Uses the
        session to create related objects and persists the instance.

        Args:
            session: The asynchronous database session to be
                used for related object creation.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            An instance of
            TacRegisterPostModelRequest.
        """


        obj = TacRegisterPostModelRequestFactory.build(
            session=None, *args, **kwargs
        )


        return obj

