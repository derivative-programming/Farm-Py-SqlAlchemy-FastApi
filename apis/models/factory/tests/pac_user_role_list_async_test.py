# apis/models/factory/tests/pac_user_role_list_async_test.py
# pylint: disable=unused-import

"""
This module contains test cases for the
PacUserRoleListGetModelRequestFactoryAsync
class.
"""

import uuid  # noqa: F401
from datetime import date, datetime  # noqa: F401
from decimal import Decimal  # noqa: F401

import pytest

from ...pac_user_role_list import (
    PacUserRoleListGetModelRequest)
from ..pac_user_role_list import (
    PacUserRoleListGetModelRequestFactory)


class TestPacUserRoleListGetModelRequestFactoryAsync:
    """
    This class contains test cases for the
    PacUserRoleListGetModelRequestFactoryAsync
    class.
    """

    @pytest.mark.asyncio
    async def test_create_async(self, session):
        """
        Test the create_async method of
        PacUserRoleListGetModelRequestFactoryAsync
        class.
        """

        model_instance = await (
            PacUserRoleListGetModelRequestFactory
            .create_async(
                session=session
            )
        )
        assert isinstance(model_instance,
                          PacUserRoleListGetModelRequest)

