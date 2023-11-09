# api/models/factories.py
import uuid
import factory
from factory import Faker

from ..tac_login import TacLoginPostModelRequest
from datetime import date, datetime
from decimal import Decimal
from pydantic import Field,UUID4
from sqlalchemy.ext.asyncio import AsyncSession
class TacLoginPostModelRequestFactory(factory.base.Factory):
    class Meta:
        model = TacLoginPostModelRequest
    force_error_message:str = ""
    email:str = Faker('email')
    password:str = Faker('sentence', nb_words=4)
    @classmethod
    def _build(cls, model_class, session=None, *args, **kwargs) -> TacLoginPostModelRequest:
        if session is None:
                obj2 = model_class(*args, **kwargs)
                return obj2

        obj = model_class(*args, **kwargs)

        return obj
    @classmethod
    def _create(cls, model_class, session=None, *args, **kwargs) -> TacLoginPostModelRequest:

        obj = model_class(*args, **kwargs)

        return obj
    @classmethod
    async def create_async(cls, session:AsyncSession, *args, **kwargs) -> TacLoginPostModelRequest:

        obj = TacLoginPostModelRequestFactory.build(session=None, *args, **kwargs)

        return obj

