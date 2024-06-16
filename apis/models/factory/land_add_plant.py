# apis/models/factory/land_add_plant.py

"""
Factory module for creating instances of LandAddPlantPostModelRequest with various field values for testing.
"""

import uuid
from datetime import date, datetime
from decimal import Decimal
from pydantic import UUID4
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

    force_error_message: str = ""
    request_other_flavor: str = ""
    request_flavor_code: UUID4 = uuid.UUID(int=0)
    request_other_flavor: str = ""
    request_some_int_val: int = factory.Faker('random_int')
    request_some_big_int_val: int = Faker('random_int')
    request_some_bit_val: bool = Faker('boolean')
    request_is_edit_allowed: bool = Faker('boolean')
    request_is_delete_allowed: bool = Faker('boolean')
    request_some_float_val: float = Faker(
        'pyfloat',
        positive=True
    )
    request_some_decimal_val: Decimal = Faker(
        'pydecimal',
        left_digits=5,
        right_digits=2,
        positive=True
    )
    request_some_utc_date_time_val: datetime = factory.LazyFunction(
        datetime.utcnow
    )
    request_some_date_val: date = Faker('date_object')
    request_some_money_val: Decimal = Faker(
        'pydecimal',
        left_digits=5,
        right_digits=2,
        positive=True
    )
    request_some_n_var_char_val: str = Faker(
        'sentence',
        nb_words=4
    )
    request_some_var_char_val: str = Faker(
        'sentence',
        nb_words=4
    )
    request_some_text_val: str = Faker('text')
    request_some_phone_number: str = Faker('phone_number')
    request_some_email_address: str = Faker('email')
    request_sample_image_upload_file: str = ""
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

        request_flavor_code_instance = FlavorFactory.create(session=session)  # requestFlavorCode
# endset

        kwargs["request_flavor_code"] = request_flavor_code_instance.code  # requestFlavorCode
# endset

        obj = model_class(*args, **kwargs)

        obj.request_flavor_code = request_flavor_code_instance.code  # requestFlavorCode
# endset

        return obj

    @classmethod
    def _create(
        cls, model_class, session=None, *args, **kwargs
    ) -> LandAddPlantPostModelRequest:

        request_flavor_code_instance = FlavorFactory.create(session=session)  # requestFlavorCode
# endset

        kwargs["request_flavor_code"] = request_flavor_code_instance.code  # requestFlavorCode
# endset

        obj = model_class(*args, **kwargs)

        obj.request_flavor_code = request_flavor_code_instance.code  # requestFlavorCode
# endset
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

        request_flavor_code_instance = await FlavorFactory.create_async(session=session)  # requestFlavorCode
# endset

        kwargs["request_flavor_code"] = request_flavor_code_instance.code  # requestFlavorCode
# endset

        obj = LandAddPlantPostModelRequestFactory.build(
            session=None, *args, **kwargs
        )

        obj.request_flavor_code = request_flavor_code_instance.code  # requestFlavorCode
# endset

        return obj
