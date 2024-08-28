# apis/models/factory/tests/pac_user_test_async_flow_req_async_test.py
# pylint: disable=unused-import, too-many-public-methods

"""
This module contains test cases for the
PacUserTestAsyncFlowReqPostModelRequestFactoryAsync
class.
"""

import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401

import pytest

from ...pac_user_test_async_flow_req import (
    PacUserTestAsyncFlowReqPostModelRequest)
from ..pac_user_test_async_flow_req import (
    PacUserTestAsyncFlowReqPostModelRequestFactory)


class TestPacUserTestAsyncFlowReqPostModelRequestFactoryAsync:  # pylint: disable=too-few-public-methods
    """
    This class contains test cases for the
    PacUserTestAsyncFlowReqPostModelRequestFactoryAsync
    class.
    """

    @pytest.mark.asyncio
    async def test_create_async(self, session):
        """
        Test the create_async method of
        PacUserTestAsyncFlowReqPostModelRequestFactoryAsync
        class.
        """

        model_instance = await \
            PacUserTestAsyncFlowReqPostModelRequestFactory \
            .create_async(
                session=session)

        assert isinstance(
            model_instance,
            PacUserTestAsyncFlowReqPostModelRequest)
