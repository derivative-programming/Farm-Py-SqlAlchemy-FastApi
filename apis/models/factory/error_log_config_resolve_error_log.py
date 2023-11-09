# api/models/factories.py
import uuid
import factory
from factory import Faker

from ..error_log_config_resolve_error_log import ErrorLogConfigResolveErrorLogPostModelRequest
from datetime import date, datetime
from decimal import Decimal
from pydantic import Field,UUID4
from sqlalchemy.ext.asyncio import AsyncSession
class ErrorLogConfigResolveErrorLogPostModelRequestFactory(factory.base.Factory):
    class Meta:
        model = ErrorLogConfigResolveErrorLogPostModelRequest
    force_error_message:str = ""

    @classmethod
    def _build(cls, model_class, session=None, *args, **kwargs) -> ErrorLogConfigResolveErrorLogPostModelRequest:
        if session is None:
                obj2 = model_class(*args, **kwargs)
                return obj2

        obj = model_class(*args, **kwargs)

        return obj
    @classmethod
    def _create(cls, model_class, session=None, *args, **kwargs) -> ErrorLogConfigResolveErrorLogPostModelRequest:

        obj = model_class(*args, **kwargs)

        return obj
    @classmethod
    async def create_async(cls, session:AsyncSession, *args, **kwargs) -> ErrorLogConfigResolveErrorLogPostModelRequest:

        obj = ErrorLogConfigResolveErrorLogPostModelRequestFactory.build(session=None, *args, **kwargs)

        return obj

