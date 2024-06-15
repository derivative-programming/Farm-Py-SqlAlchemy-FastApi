# apis/models/tests/tac_login_test.py
"""
    #TODO add comment
"""
import uuid
from datetime import date, datetime
from decimal import Decimal
from unittest.mock import AsyncMock, patch
import pytest
from business.tac import TacBusObj
from flows.tac_login import FlowTacLogin, FlowTacLoginResult
from helpers.session_context import SessionContext
from helpers.type_conversion import TypeConversion
from models.factory.tac import TacFactory
from ...models.tac_login import (TacLoginPostModelResponse)
from ..factory.tac_login import TacLoginPostModelRequestFactory
class TestTacLoginPostModelResponse:
    """
    #TODO add comment
    """
    @pytest.mark.asyncio
    async def test_flow_process_request(self, session):
        """
            #TODO add comment
        """
        async def mock_process(
            tac_bus_obj: TacBusObj,  # pylint: disable=unused-argument
            email: str = "",  # pylint: disable=unused-argument
            password: str = "",  # pylint: disable=unused-argument
        ):
            return FlowTacLoginResult()
        with patch.object(FlowTacLogin, 'process', new_callable=AsyncMock) as mock_method:
            mock_method.side_effect = mock_process
            request_instance = await TacLoginPostModelRequestFactory.create_async(session=session)
            response_instance = TacLoginPostModelResponse()
            session_context = SessionContext(dict(), session)
            tac = await TacFactory.create_async(session)
            await response_instance.process_request(
                session_context=session_context,
                tac_code=tac.code,
                request=request_instance
            )
            assert response_instance.success is True
            mock_method.assert_awaited()

