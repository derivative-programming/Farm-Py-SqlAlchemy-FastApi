import pytest
from worker.prefect.tasks.dyna_flow_task_b import dyna_flow_task_b

class TestDynaFlowTaskB:

    def test_run(self, capfd):

        result = dyna_flow_task_b.fn()

        captured = capfd.readouterr()
        assert "DynaFlowTaskB is running" in captured.out
