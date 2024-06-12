# apis/models/factory/plant_user_delete.py
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

from ..plant_user_delete import PlantUserDeletePostModelRequest
class PlantUserDeletePostModelRequestFactory(factory.base.Factory):
    """
    #TODO add comment
    """
    class Meta:
        """
        #TODO add comment
        """
        model = PlantUserDeletePostModelRequest
    force_error_message: str = ""

    @classmethod
    def _build(cls, model_class, session=None, *args, **kwargs) -> PlantUserDeletePostModelRequest:
        if session is None:
                obj2 = model_class(*args, **kwargs)
                return obj2

# endset

# endset
        obj = model_class(*args, **kwargs)

# endset
        return obj
    @classmethod
    def _create(cls, model_class, session=None, *args, **kwargs) -> PlantUserDeletePostModelRequest:

# endset

# endset
        obj = model_class(*args, **kwargs)

# endset
        return obj
    @classmethod
    async def create_async(cls, session: AsyncSession, *args, **kwargs) -> PlantUserDeletePostModelRequest:

# endset

# endset
        obj = PlantUserDeletePostModelRequestFactory.build(session=None, *args, **kwargs)

# endset
        return obj

