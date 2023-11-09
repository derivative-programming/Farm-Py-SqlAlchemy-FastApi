# api/models/factories.py
import uuid
import factory
from factory import Faker

from ..land_user_plant_multi_select_to_not_editable import LandUserPlantMultiSelectToNotEditablePostModelRequest
from datetime import date, datetime
from decimal import Decimal
from pydantic import Field,UUID4
from sqlalchemy.ext.asyncio import AsyncSession
class LandUserPlantMultiSelectToNotEditablePostModelRequestFactory(factory.base.Factory):
    class Meta:
        model = LandUserPlantMultiSelectToNotEditablePostModelRequest
    force_error_message:str = ""
    plant_code_list_csv:str = ""
    @classmethod
    def _build(cls, model_class, session=None, *args, **kwargs) -> LandUserPlantMultiSelectToNotEditablePostModelRequest:
        if session is None:
                obj2 = model_class(*args, **kwargs)
                return obj2

        obj = model_class(*args, **kwargs)

        return obj
    @classmethod
    def _create(cls, model_class, session=None, *args, **kwargs) -> LandUserPlantMultiSelectToNotEditablePostModelRequest:

        obj = model_class(*args, **kwargs)

        return obj
    @classmethod
    async def create_async(cls, session:AsyncSession, *args, **kwargs) -> LandUserPlantMultiSelectToNotEditablePostModelRequest:

        obj = LandUserPlantMultiSelectToNotEditablePostModelRequestFactory.build(session=None, *args, **kwargs)

        return obj

