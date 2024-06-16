# apis/models/factory/plant_user_property_random_update.py
"""
    #TODO add comment
"""
import uuid
from datetime import date, datetime
from decimal import Decimal
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession
import factory
from factory import Faker

from ..plant_user_property_random_update import PlantUserPropertyRandomUpdatePostModelRequest
class PlantUserPropertyRandomUpdatePostModelRequestFactory(factory.base.Factory):
    """
    #TODO add comment
    """
    class Meta:
        """
        #TODO add comment
        """
        model = PlantUserPropertyRandomUpdatePostModelRequest
    force_error_message: str = ""

# endset
    @classmethod
    def _build(
        cls, model_class, session=None, *args, **kwargs
    ) -> PlantUserPropertyRandomUpdatePostModelRequest:
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
    ) -> PlantUserPropertyRandomUpdatePostModelRequest:

# endset

# endset
        obj = model_class(*args, **kwargs)

# endset
        return obj
    @classmethod
    async def create_async(
        cls, session: AsyncSession, *args, **kwargs
    ) -> PlantUserPropertyRandomUpdatePostModelRequest:
        """
            #TODO add comment
        """

# endset

# endset
        obj = PlantUserPropertyRandomUpdatePostModelRequestFactory.build(
            session=None, *args, **kwargs
        )

# endset
        return obj

