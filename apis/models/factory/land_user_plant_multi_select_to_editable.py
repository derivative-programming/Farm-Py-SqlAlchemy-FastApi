# apis/models/factory/land_user_plant_multi_select_to_editable.py
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

from ..land_user_plant_multi_select_to_editable import LandUserPlantMultiSelectToEditablePostModelRequest
class LandUserPlantMultiSelectToEditablePostModelRequestFactory(factory.base.Factory):
    """
    #TODO add comment
    """
    class Meta:
        """
        #TODO add comment
        """
        model = LandUserPlantMultiSelectToEditablePostModelRequest
    force_error_message: str = ""
    plant_code_list_csv: str = ""
# endset
    @classmethod
    def _build(cls, model_class, session=None, *args, **kwargs) -> LandUserPlantMultiSelectToEditablePostModelRequest:
        if session is None:
                obj2 = model_class(*args, **kwargs)
                return obj2

# endset

# endset
        obj = model_class(*args, **kwargs)

# endset
        return obj
    @classmethod
    def _create(cls, model_class, session=None, *args, **kwargs) -> LandUserPlantMultiSelectToEditablePostModelRequest:

# endset

# endset
        obj = model_class(*args, **kwargs)

# endset
        return obj
    @classmethod
    async def create_async(cls, session: AsyncSession, *args, **kwargs) -> LandUserPlantMultiSelectToEditablePostModelRequest:
        """
            #TODO add comment
        """

# endset

# endset
        obj = LandUserPlantMultiSelectToEditablePostModelRequestFactory.build(session=None, *args, **kwargs)

# endset
        return obj

