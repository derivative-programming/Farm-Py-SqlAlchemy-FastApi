# apis/models/factory/tests/pac_user_test_async_file_download_async_test.py
# pylint: disable=unused-import, too-many-public-methods

"""
This module contains test cases for the
PacUserTestAsyncFileDownloadPostModelRequestFactoryAsync
class.
"""

import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from decimal import Decimal  # noqa: F401

import pytest

from ...pac_user_test_async_file_download import (
    PacUserTestAsyncFileDownloadPostModelRequest)
from ..pac_user_test_async_file_download import (
    PacUserTestAsyncFileDownloadPostModelRequestFactory)


class TestPacUserTestAsyncFileDownloadPostModelRequestFactoryAsync:  # pylint: disable=too-few-public-methods
    """
    This class contains test cases for the
    PacUserTestAsyncFileDownloadPostModelRequestFactoryAsync
    class.
    """

    @pytest.mark.asyncio
    async def test_create_async(self, session):
        """
        Test the create_async method of
        PacUserTestAsyncFileDownloadPostModelRequestFactoryAsync
        class.
        """

        model_instance = await \
            PacUserTestAsyncFileDownloadPostModelRequestFactory \
            .create_async(
                session=session)

        assert isinstance(
            model_instance,
            PacUserTestAsyncFileDownloadPostModelRequest)
