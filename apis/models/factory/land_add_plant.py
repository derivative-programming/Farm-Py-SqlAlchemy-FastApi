# apis/models/factory/land_add_plant.py
# pylint: disable=unused-import
"""
Factory module for creating instances of LandAddPlantPostModelRequest with
various field values for testing.
"""

import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
import factory
from factory import Faker
from models.factory import FlavorFactory  # requestFlavorCode
from ..land_add_plant import LandAddPlantPostModelRequest


class LandAddPlantPostModelRequestFactory(factory.base.Factory):
    """
    Factory class for LandAddPlantPostModelRequest. Generates
    instances with randomized field values for testing.
    """

    class Meta:
        """
        Metadata for the factory class. Specifies the model to be used.
        """
        model = LandAddPlantPostModelRequest

    force_error_message = ""
    request_other_flavor = ""
    request_flavor_code = uuid.UUID(int=0)
    request_other_flavor = ""
    request_some_int_val = Faker('random_int')
    request_some_big_int_val = Faker('random_int')
    request_some_bit_val = Faker('boolean')
    request_is_edit_allowed = Faker('boolean')
    request_is_delete_allowed = Faker('boolean')
    request_some_float_val = Faker(
        'pyfloat',
        positive=True
    )
    request_some_decimal_val = Faker(
        'pydecimal',
        left_digits=5,
        right_digits=2,
        positive=True
    )
    request_some_utc_date_time_val = factory.LazyFunction(
        datetime.utcnow
    )
    request_some_date_val = Faker('date_object')
    request_some_money_val = Faker(
        'pydecimal',
        left_digits=5,
        right_digits=2,
        positive=True
    )
    request_some_n_var_char_val = Faker(
        'sentence',
        nb_words=4
    )
    request_some_var_char_val = Faker(
        'sentence',
        nb_words=4
    )
    request_some_text_val = Faker('text')
    request_some_phone_number = Faker('phone_number')
    request_some_email_address = Faker('email')
    request_sample_image_upload_file = ""
# endset

    @classmethod
    def _build(
        cls, model_class, session=None, *args, **kwargs
    ) -> LandAddPlantPostModelRequest:
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
            An instance of LandAddPlantPostModelRequest.
        """

        if session is None:
            obj2 = model_class(*args, **kwargs)
            return obj2

        request_flavor_code_instance = (  # requestFlavorCode
            FlavorFactory.create(session=session))

# endset

        kwargs["request_flavor_code"] = (  # requestFlavorCode
            request_flavor_code_instance.code)
# endset

        obj = model_class(*args, **kwargs)

        obj.request_flavor_code = (  # requestFlavorCode
            request_flavor_code_instance.code)
# endset

        return obj

    @classmethod
    def _create(
        cls, model_class, session=None, *args, **kwargs
    ) -> LandAddPlantPostModelRequest:
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
            An instance of LandAddPlantPostModelRequest.
        """

        request_flavor_code_instance = (  # requestFlavorCode
            FlavorFactory.create(session=session))
# endset

        kwargs["request_flavor_code"] = (  # requestFlavorCode
            request_flavor_code_instance.code)
# endset

        obj = model_class(*args, **kwargs)

        obj.request_flavor_code = (  # requestFlavorCode
            request_flavor_code_instance.code)
# endset

        return obj

    @classmethod
    async def create_async(
        cls, session: AsyncSession, *args, **kwargs
    ) -> LandAddPlantPostModelRequest:
        """
        Asynchronous create method for the factory. Uses the
        session to create related objects and persists the instance.

        Args:
            session: The asynchronous database session to be
                used for related object creation.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            An instance of LandAddPlantPostModelRequest.
        """

        request_flavor_code_instance = (  # requestFlavorCode
            await FlavorFactory.create_async(session=session))

# endset

        kwargs["request_flavor_code"] = (  # requestFlavorCode
            request_flavor_code_instance.code)
# endset

        obj = LandAddPlantPostModelRequestFactory.build(
            session=None, *args, **kwargs
        )

        obj.request_flavor_code = (  # requestFlavorCode
            request_flavor_code_instance.code)
# endset

        return obj
