# apis/models/factory/error_log_config_resolve_error_log.py
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

from ..error_log_config_resolve_error_log import ErrorLogConfigResolveErrorLogPostModelRequest
class ErrorLogConfigResolveErrorLogPostModelRequestFactory(factory.base.Factory):
    """
    #TODO add comment
    """
    class Meta:
        """
        #TODO add comment
        """
        model = ErrorLogConfigResolveErrorLogPostModelRequest
    force_error_message: str = ""

# endset
    @classmethod
    def _build(cls, model_class, session=None, *args, **kwargs) -> ErrorLogConfigResolveErrorLogPostModelRequest:
        if session is None:
                obj2 = model_class(*args, **kwargs)
                return obj2

# endset

# endset
        obj = model_class(*args, **kwargs)

# endset
        return obj
    @classmethod
    def _create(cls, model_class, session=None, *args, **kwargs) -> ErrorLogConfigResolveErrorLogPostModelRequest:

# endset

# endset
        obj = model_class(*args, **kwargs)

# endset
        return obj
    @classmethod
    async def create_async(cls, session: AsyncSession, *args, **kwargs) -> ErrorLogConfigResolveErrorLogPostModelRequest:
        """
            #TODO add comment
        """

# endset

# endset
        obj = ErrorLogConfigResolveErrorLogPostModelRequestFactory.build(session=None, *args, **kwargs)

# endset
        return obj

