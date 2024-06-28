import pytest
from prefect import flow, Flow
from worker.prefect.flows.dyna_flow_a import dyna_flow_a


def test_dyna_flow_a(capfd):

    # Run the flow
    dyna_flow_a()

    captured = capfd.readouterr()

    assert "DynaFlowA is running" in captured.out
    assert "DynaFlowTaskA is running" in captured.out
    assert "DynaFlowTaskB is running" in captured.out
    
