# farm/models/factories.py
import uuid
import factory
from factory import Faker

from ..pac_user_tac_list import PacUserTacListGetModelRequest
from datetime import date, datetime
from decimal import Decimal
from pydantic import Field,UUID4
from sqlalchemy.ext.asyncio import AsyncSession
class PacUserTacListGetModelRequestFactory(factory.base.Factory):
    class Meta:
        model = PacUserTacListGetModelRequest

    page_number = 1
    item_count_per_page = 1
    @classmethod
    def _build(cls, model_class, session=None, *args, **kwargs) -> PacUserTacListGetModelRequest:
        if session is None:
                obj2 = model_class(*args, **kwargs)
                return obj2

        obj = model_class(*args, **kwargs)

        return obj
    @classmethod
    def _create(cls, model_class, session=None, *args, **kwargs) -> PacUserTacListGetModelRequest:

        obj = model_class(*args, **kwargs)

        return obj
    @classmethod
    async def create_async(cls, session:AsyncSession, *args, **kwargs) -> PacUserTacListGetModelRequest:

        obj = PacUserTacListGetModelRequestFactory.build(session=None, *args, **kwargs)

        return obj
