# apis/models/factory/tac_register.py
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

from ..tac_register import TacRegisterPostModelRequest
class TacRegisterPostModelRequestFactory(factory.base.Factory):
    """
    #TODO add comment
    """
    class Meta:
        """
        #TODO add comment
        """
        model = TacRegisterPostModelRequest
    force_error_message: str = ""
    email: str = Faker('email')
    password: str = Faker(
         'sentence',
         nb_words=4)
    confirm_password: str = Faker(
         'sentence',
         nb_words=4)
    first_name: str = Faker(
         'sentence',
         nb_words=4)
    last_name: str = Faker(
         'sentence',
         nb_words=4)
    @classmethod
    def _build(cls, model_class, session=None, *args, **kwargs) -> TacRegisterPostModelRequest:
        if session is None:
                obj2 = model_class(*args, **kwargs)
                return obj2

# endset

# endset
        obj = model_class(*args, **kwargs)

# endset
        return obj
    @classmethod
    def _create(cls, model_class, session=None, *args, **kwargs) -> TacRegisterPostModelRequest:

# endset

# endset
        obj = model_class(*args, **kwargs)

# endset
        return obj
    @classmethod
    async def create_async(cls, session: AsyncSession, *args, **kwargs) -> TacRegisterPostModelRequest:

# endset

# endset
        obj = TacRegisterPostModelRequestFactory.build(session=None, *args, **kwargs)

# endset
        return obj

