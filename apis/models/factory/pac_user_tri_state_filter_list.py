# farm/models/factories.py
import uuid
import factory
from factory import Faker

from ..pac_user_tri_state_filter_list import PacUserTriStateFilterListGetModelRequest
from datetime import date, datetime
from decimal import Decimal
from pydantic import Field,UUID4
from sqlalchemy.ext.asyncio import AsyncSession
class PacUserTriStateFilterListGetModelRequestFactory(factory.base.Factory):
    class Meta:
        model = PacUserTriStateFilterListGetModelRequest

    page_number = 1
    item_count_per_page = 1
    order_by_column_name:str = ""
    order_by_descending:bool = False
    force_error_message:str = ""
    @classmethod
    def _build(cls, model_class, session=None, *args, **kwargs) -> PacUserTriStateFilterListGetModelRequest:
        if session is None:
                obj2 = model_class(*args, **kwargs)
                return obj2

        obj = model_class(*args, **kwargs)

        return obj
    @classmethod
    def _create(cls, model_class, session=None, *args, **kwargs) -> PacUserTriStateFilterListGetModelRequest:

        obj = model_class(*args, **kwargs)

        return obj
    @classmethod
    async def create_async(cls, session:AsyncSession, *args, **kwargs) -> PacUserTriStateFilterListGetModelRequest:

        obj = PacUserTriStateFilterListGetModelRequestFactory.build(session=None, *args, **kwargs)

        return obj
