# apis/models/factory/tests/tac_register_async_test.py
# pylint: disable=unused-import, too-many-public-methods

"""
This module contains test cases for the
TacRegisterPostModelRequestFactoryAsync
class.
"""

import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401

import pytest

from ...tac_register import (
    TacRegisterPostModelRequest)
from ..tac_register import (
    TacRegisterPostModelRequestFactory)


class TestTacRegisterPostModelRequestFactoryAsync:  # pylint: disable=too-few-public-methods
    """
    This class contains test cases for the
    TacRegisterPostModelRequestFactoryAsync
    class.
    """

    @pytest.mark.asyncio
    async def test_create_async(self, session):
        """
        Test the create_async method of
        TacRegisterPostModelRequestFactoryAsync
        class.
        """

        model_instance = await \
            TacRegisterPostModelRequestFactory \
            .create_async(
                session=session)

        assert isinstance(
            model_instance,
            TacRegisterPostModelRequest)
        assert isinstance(model_instance.email,
                          str)
        assert isinstance(model_instance.password,
                          str)
        assert isinstance(model_instance.confirm_password,
                          str)
        assert isinstance(model_instance.first_name,
                          str)
        assert isinstance(model_instance.last_name,
                          str)
