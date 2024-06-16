# apis/models/factory/tac_login.py
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

from ..tac_login import TacLoginPostModelRequest
class TacLoginPostModelRequestFactory(factory.base.Factory):
    """
    #TODO add comment
    """
    class Meta:
        """
        #TODO add comment
        """
        model = TacLoginPostModelRequest
    force_error_message: str = ""
    email: str = Faker('email')
    password: str = Faker(
        'sentence',
        nb_words=4
    )
# endset
    @classmethod
    def _build(
        cls, model_class, session=None, *args, **kwargs
    ) -> TacLoginPostModelRequest:
        if session is None:
            obj2 = model_class(*args, **kwargs)
            return obj2

# endset

# endset
        obj = model_class(*args, **kwargs)

# endset
        return obj
    @classmethod
    def _create(
        cls, model_class, session=None, *args, **kwargs
    ) -> TacLoginPostModelRequest:

# endset

# endset
        obj = model_class(*args, **kwargs)

# endset
        return obj
    @classmethod
    async def create_async(
        cls, session: AsyncSession, *args, **kwargs
    ) -> TacLoginPostModelRequest:
        """
            #TODO add comment
        """

# endset

# endset
        obj = TacLoginPostModelRequestFactory.build(
            session=None, *args, **kwargs
        )

# endset
        return obj

