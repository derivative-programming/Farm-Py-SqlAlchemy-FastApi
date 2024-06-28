# worker/prefect/register_flows.py
import os
import prefect
from prefect import Flow
from prefect.storage import Local
from prefect.run_configs import LocalRun

# Assuming your flows are in worker/prefect/flows directory
flow_files = os.listdir("/usr/src/app/worker/prefect/flows")

for file in flow_files:
    if file.endswith(".py"):
        flow_name = file[:-3]  # Remove .py extension
        flow_module = f"worker.prefect.flows.{flow_name}"
        flow = __import__(flow_module, fromlist=['flow']).flow

        flow.storage = Local(path=f"/usr/src/app/worker/prefect/flows/{file}")
        flow.run_config = LocalRun()
        flow.register(project_name="default")
