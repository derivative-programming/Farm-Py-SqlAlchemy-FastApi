# api/models/factories.py
import uuid
import factory
from factory import Faker

from ..land_user_plant_multi_select_to_editable import LandUserPlantMultiSelectToEditablePostModelRequest
from datetime import date, datetime
from decimal import Decimal
from pydantic import Field, UUID4
from sqlalchemy.ext.asyncio import AsyncSession
class LandUserPlantMultiSelectToEditablePostModelRequestFactory(factory.base.Factory):
    class Meta:
        model = LandUserPlantMultiSelectToEditablePostModelRequest
    force_error_message: str = ""
    plant_code_list_csv: str = ""
    @classmethod
    def _build(cls, model_class, session = None, *args, **kwargs) -> LandUserPlantMultiSelectToEditablePostModelRequest:
        if session is None:
                obj2 = model_class(*args, **kwargs)
                return obj2

        obj = model_class(*args, **kwargs)

        return obj
    @classmethod
    def _create(cls, model_class, session = None, *args, **kwargs) -> LandUserPlantMultiSelectToEditablePostModelRequest:

        obj = model_class(*args, **kwargs)

        return obj
    @classmethod
    async def create_async(cls, session: AsyncSession, *args, **kwargs) -> LandUserPlantMultiSelectToEditablePostModelRequest:

        obj = LandUserPlantMultiSelectToEditablePostModelRequestFactory.build(session = None, *args, **kwargs)

        return obj

