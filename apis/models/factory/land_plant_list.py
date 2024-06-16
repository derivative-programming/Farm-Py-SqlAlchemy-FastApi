# apis/models/factory/land_plant_list.py
# pylint: disable=unused-import
"""
    #TODO add comment
"""

import uuid
from datetime import datetime

import factory
from factory import Faker
from sqlalchemy.ext.asyncio import AsyncSession

from models.factory import FlavorFactory  # requestFlavorCode

from ..land_plant_list import (
    LandPlantListGetModelRequest)


class LandPlantListGetModelRequestFactory(
    factory.base.Factory
):
    """
    #TODO add comment
    """

    class Meta:
        """
        #TODO add comment
        """
        model = LandPlantListGetModelRequest
    flavor_code = uuid.uuid4()
    some_int_val = Faker('random_int')
    some_big_int_val = Faker('random_int')
    some_float_val = Faker('pyfloat', positive=True)
    some_bit_val = Faker('boolean')
    is_edit_allowed = Faker('boolean')
    is_delete_allowed = Faker('boolean')
    some_decimal_val = Faker(
        'pydecimal',
        left_digits=5,
        right_digits=2,
        positive=True
    )
    some_min_utc_date_time_val = factory.LazyFunction(
        datetime.utcnow
    )
    some_min_date_val = Faker('date_object')
    some_money_val = Faker(
        'pydecimal',
        left_digits=5,
        right_digits=2,
        positive=True
    )
    some_n_var_char_val = Faker('sentence', nb_words=4)
    some_var_char_val = Faker('sentence', nb_words=4)
    some_text_val = Faker('text')
    some_phone_number = Faker('sentence', nb_words=4)
    some_email_address = Faker('sentence', nb_words=4)
    page_number = 1
    item_count_per_page = 1
    order_by_column_name = ""
    order_by_descending = False
    force_error_message = ""
# endset

    @classmethod
    def _build(
        cls,
        model_class,
        session=None,
        *args, **kwargs
    ) -> LandPlantListGetModelRequest:

        if session is None:
            obj2 = model_class(*args, **kwargs)
            return obj2

        flavor_code_instance = FlavorFactory.create(  # FlavorCode
            session=session)
# endset

        kwargs["flavor_code"] = flavor_code_instance.code  # FlavorCode
# endset

        obj = model_class(*args, **kwargs)

        obj.flavor_code = flavor_code_instance.code  # FlavorCode
# endset

        return obj

    @classmethod
    def _create(
        cls,
        model_class,
        session=None,
        *args, **kwargs
    ) -> LandPlantListGetModelRequest:

        flavor_code_instance = FlavorFactory.create(  # requestFlavorCode
            session=session)

# endset

        kwargs["flavor_code"] = flavor_code_instance.code  # requestFlavorCode
# endset

        obj = model_class(*args, **kwargs)

        obj.flavor_code = flavor_code_instance.code  # requestFlavorCode
# endset

        return obj

    @classmethod
    async def create_async(
        cls,
        session: AsyncSession,
        *args, **kwargs
    ) -> LandPlantListGetModelRequest:
        """
            #TODO add comment
        """

        flavor_code_instance = await FlavorFactory.create_async(  # requestFlavorCode
            session=session)
# endset

        kwargs["flavor_code"] = flavor_code_instance.code  # requestFlavorCode
# endset

        obj = LandPlantListGetModelRequestFactory.build(
            session=None,
            *args, **kwargs
        )

        obj.flavor_code = flavor_code_instance.code  # requestFlavorCode
# endset

        return obj
