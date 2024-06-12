# apis/models/factory/customer_build_temp_api_key.py
"""
    #TODO add comment
"""
import uuid
from datetime import date, datetime
from decimal import Decimal
from pydantic import Field, UUID4
from sqlalchemy.ext.asyncio import AsyncSession
import factory
from factory import Faker

from ..customer_build_temp_api_key import CustomerBuildTempApiKeyPostModelRequest
class CustomerBuildTempApiKeyPostModelRequestFactory(factory.base.Factory):
    """
    #TODO add comment
    """
    class Meta:
        """
        #TODO add comment
        """
        model = CustomerBuildTempApiKeyPostModelRequest
    force_error_message: str = ""

    @classmethod
    def _build(cls, model_class, session=None, *args, **kwargs) -> CustomerBuildTempApiKeyPostModelRequest:
        if session is None:
                obj2 = model_class(*args, **kwargs)
                return obj2

# endset

# endset
        obj = model_class(*args, **kwargs)

# endset
        return obj
    @classmethod
    def _create(cls, model_class, session=None, *args, **kwargs) -> CustomerBuildTempApiKeyPostModelRequest:

# endset

# endset
        obj = model_class(*args, **kwargs)

# endset
        return obj
    @classmethod
    async def create_async(cls, session: AsyncSession, *args, **kwargs) -> CustomerBuildTempApiKeyPostModelRequest:

# endset

# endset
        obj = CustomerBuildTempApiKeyPostModelRequestFactory.build(session=None, *args, **kwargs)

# endset
        return obj

