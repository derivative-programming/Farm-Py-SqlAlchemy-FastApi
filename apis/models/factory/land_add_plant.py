# apis/models/factory/land_add_plant.py

"""
    #TODO add comment
"""

import uuid
from datetime import date, datetime
from decimal import Decimal
from pydantic import Field, UUID4
from sqlalchemy.ext.asyncio import AsyncSession
import factory
from factory import Faker
from models.factory import FlavorFactory  # requestFlavorCode
from ..land_add_plant import LandAddPlantPostModelRequest


class LandAddPlantPostModelRequestFactory(factory.base.Factory):
    """
    #TODO add comment
    """

    class Meta:
        """
        #TODO add comment
        """
        model = LandAddPlantPostModelRequest

    force_error_message: str = ""
    request_other_flavor: str = ""
    request_flavor_code: UUID4 = uuid.UUID(int=0)
    request_other_flavor: str = ""
    request_some_int_val: int = Faker('random_int')
    request_some_big_int_val: int = Faker('random_int')
    request_some_bit_val: bool = Faker('boolean')
    request_is_edit_allowed: bool = Faker('boolean')
    request_is_delete_allowed: bool = Faker('boolean')
    request_some_float_val: float = Faker(
         'pyfloat',
         positive=True)
    request_some_decimal_val: Decimal = Faker(
         'pydecimal',
         left_digits=5,
         right_digits=2,
         positive=True)
    request_some_utc_date_time_val: datetime = factory.LazyFunction(
         datetime.utcnow)
    request_some_date_val: date = Faker('date_object')
    request_some_money_val: Decimal = Faker(
         'pydecimal',
         left_digits=5,
         right_digits=2,
         positive=True)
    request_some_n_var_char_val: str = Faker(
         'sentence',
         nb_words=4)
    request_some_var_char_val: str = Faker(
         'sentence',
         nb_words=4)
    request_some_text_val: str = Faker('text')
    request_some_phone_number: str = Faker('phone_number')
    request_some_email_address: str = Faker('email')
    request_sample_image_upload_file: str = ""

    @classmethod
    def _build(cls, model_class, session=None, *args, **kwargs) -> LandAddPlantPostModelRequest:

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
    def _create(cls, model_class, session=None, *args, **kwargs) -> LandAddPlantPostModelRequest:

        request_flavor_code_instance = FlavorFactory.create(session=session)  # requestFlavorCode
# endset

        kwargs["request_flavor_code"] = request_flavor_code_instance.code  # requestFlavorCode
# endset

        obj = model_class(*args, **kwargs)

        obj.request_flavor_code = request_flavor_code_instance.code  # requestFlavorCode
# endset

        return obj

    @classmethod
    async def create_async(cls, session: AsyncSession, *args, **kwargs) -> LandAddPlantPostModelRequest:

        request_flavor_code_instance = await FlavorFactory.create_async(session=session)  # requestFlavorCode
# endset

        kwargs["request_flavor_code"] = request_flavor_code_instance.code  # requestFlavorCode
# endset

        obj = LandAddPlantPostModelRequestFactory.build(session=None, *args, **kwargs)

        obj.request_flavor_code = request_flavor_code_instance.code  # requestFlavorCode
# endset

        return obj
