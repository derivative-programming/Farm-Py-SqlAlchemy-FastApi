# api/models/factories.py
import uuid
import factory
from factory import Faker

from ..customer_user_log_out import CustomerUserLogOutPostModelRequest
from datetime import date, datetime
from decimal import Decimal
from pydantic import Field,UUID4
from sqlalchemy.ext.asyncio import AsyncSession
class CustomerUserLogOutPostModelRequestFactory(factory.base.Factory):
    class Meta:
        model = CustomerUserLogOutPostModelRequest
    force_error_message:str = ""

    @classmethod
    def _build(cls, model_class, session=None, *args, **kwargs) -> CustomerUserLogOutPostModelRequest:
        if session is None:
                obj2 = model_class(*args, **kwargs)
                return obj2

        obj = model_class(*args, **kwargs)

        return obj
    @classmethod
    def _create(cls, model_class, session=None, *args, **kwargs) -> CustomerUserLogOutPostModelRequest:

        obj = model_class(*args, **kwargs)

        return obj
    @classmethod
    async def create_async(cls, session:AsyncSession, *args, **kwargs) -> CustomerUserLogOutPostModelRequest:

        obj = CustomerUserLogOutPostModelRequestFactory.build(session=None, *args, **kwargs)

        return obj

