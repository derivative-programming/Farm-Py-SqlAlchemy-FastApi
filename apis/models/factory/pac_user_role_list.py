# apis/models/factory/pac_user_role_list.py
"""
    #TODO add comment
"""
import uuid
from datetime import date, datetime
from decimal import Decimal
import factory
from factory import Faker
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from ..pac_user_role_list import PacUserRoleListGetModelRequest
class PacUserRoleListGetModelRequestFactory(factory.base.Factory):
    """
    #TODO add comment
    """
    class Meta:
        """
        #TODO add comment
        """
        model = PacUserRoleListGetModelRequest

    page_number = 1
    item_count_per_page = 1
    order_by_column_name: str = ""
    order_by_descending: bool = False
    force_error_message: str = ""
# endset
    @classmethod
    def _build(cls, model_class, session=None, *args, **kwargs) -> PacUserRoleListGetModelRequest:
        if session is None:
                obj2 = model_class(*args, **kwargs)
                return obj2

# endset

# endset
        obj = model_class(*args, **kwargs)

# endset
        return obj
    @classmethod
    def _create(cls, model_class, session=None, *args, **kwargs) -> PacUserRoleListGetModelRequest:

# endset

# endset
        obj = model_class(*args, **kwargs)

# endset
        return obj
    @classmethod
    async def create_async(cls, session: AsyncSession, *args, **kwargs) -> PacUserRoleListGetModelRequest:
        """
            #TODO add comment
        """

# endset

# endset
        obj = PacUserRoleListGetModelRequestFactory.build(session = None, *args, **kwargs)

# endset
        return obj
