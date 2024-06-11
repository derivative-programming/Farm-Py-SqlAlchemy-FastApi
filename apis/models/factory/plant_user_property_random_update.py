# api/models/factories.py
import uuid
import factory
from factory import Faker

from ..plant_user_property_random_update import PlantUserPropertyRandomUpdatePostModelRequest
from datetime import date, datetime
from decimal import Decimal
from pydantic import Field, UUID4
from sqlalchemy.ext.asyncio import AsyncSession
class PlantUserPropertyRandomUpdatePostModelRequestFactory(factory.base.Factory):
    class Meta:
        model = PlantUserPropertyRandomUpdatePostModelRequest
    force_error_message: str = ""

    @classmethod
    def _build(cls, model_class, session = None, *args, **kwargs) -> PlantUserPropertyRandomUpdatePostModelRequest:
        if session is None:
                obj2 = model_class(*args, **kwargs)
                return obj2

        obj = model_class(*args, **kwargs)

        return obj
    @classmethod
    def _create(cls, model_class, session = None, *args, **kwargs) -> PlantUserPropertyRandomUpdatePostModelRequest:

        obj = model_class(*args, **kwargs)

        return obj
    @classmethod
    async def create_async(cls, session: AsyncSession, *args, **kwargs) -> PlantUserPropertyRandomUpdatePostModelRequest:

        obj = PlantUserPropertyRandomUpdatePostModelRequestFactory.build(session = None, *args, **kwargs)

        return obj

