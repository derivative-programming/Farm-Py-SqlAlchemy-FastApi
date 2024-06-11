# farm/models/factories.py
import uuid
import factory
from factory import Faker

from ..pac_user_flavor_list import PacUserFlavorListGetModelRequest
from datetime import date, datetime
from decimal import Decimal
from pydantic import Field, UUID4
from sqlalchemy.ext.asyncio import AsyncSession
class PacUserFlavorListGetModelRequestFactory(factory.base.Factory):
    class Meta:
        model = PacUserFlavorListGetModelRequest

    page_number = 1
    item_count_per_page = 1
    order_by_column_name: str = ""
    order_by_descending: bool = False
    force_error_message: str = ""
    @classmethod
    def _build(cls, model_class, session = None, *args, **kwargs) -> PacUserFlavorListGetModelRequest:
        if session is None:
                obj2 = model_class(*args, **kwargs)
                return obj2

        obj = model_class(*args, **kwargs)

        return obj
    @classmethod
    def _create(cls, model_class, session = None, *args, **kwargs) -> PacUserFlavorListGetModelRequest:

        obj = model_class(*args, **kwargs)

        return obj
    @classmethod
    async def create_async(cls, session: AsyncSession, *args, **kwargs) -> PacUserFlavorListGetModelRequest:

        obj = PacUserFlavorListGetModelRequestFactory.build(session = None, *args, **kwargs)

        return obj
