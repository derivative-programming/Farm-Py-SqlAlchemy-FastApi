import pytest
from worker.prefect.tasks.dyna_flow_task_a import dyna_flow_task_a

class TestDynaFlowTaskA:

    def test_run(self, capfd):

        result = dyna_flow_task_a.fn()

        captured = capfd.readouterr()
        assert "DynaFlowTaskA is running" in captured.out
