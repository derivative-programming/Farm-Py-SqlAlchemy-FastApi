# apis/models/factory/pac_user_land_list.py
"""
    #TODO add comment
"""
import uuid
from datetime import date, datetime
from decimal import Decimal
import factory
from factory import Faker
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ..pac_user_land_list import PacUserLandListGetModelRequest
class PacUserLandListGetModelRequestFactory(factory.base.Factory):
    """
    #TODO add comment
    """
    class Meta:
        """
        #TODO add comment
        """
        model = PacUserLandListGetModelRequest

# endset
    @classmethod
    def _build(
        cls,
        model_class,
        session=None,
        *args, **kwargs
    ) -> PacUserLandListGetModelRequest:
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
        cls,
        model_class,
        session=None,
        *args, **kwargs
    ) -> PacUserLandListGetModelRequest:

# endset

# endset
        obj = model_class(*args, **kwargs)

# endset
        return obj
    @classmethod
    async def create_async(
        cls,
        session: AsyncSession,
        *args, **kwargs
    ) -> PacUserLandListGetModelRequest:
        """
            #TODO add comment
        """

# endset

# endset
        obj = PacUserLandListGetModelRequestFactory.build(
            session=None,
            *args, **kwargs
        )

# endset
        return obj
