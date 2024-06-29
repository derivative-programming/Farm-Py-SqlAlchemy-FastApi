# register_flows.py
import os
import prefect
import asyncio
# from prefect import flow
# from prefect.storage import Local
# from prefect.run_configs import LocalRun
from worker.prefect.flows.dyna_flow_a import dyna_flow_a

# Assuming your flows are in worker/prefect/flows directory
# flow_files = os.listdir("/usr/src/app/worker/prefect/flows")

# for file in flow_files:
#     if file.endswith(".py"):
#         flow_name = file[:-3]  # Remove .py extension
#         flow_module = f"worker.prefect.flows.{flow_name}"
#         flow = __import__(flow_module, fromlist=['flow']).flow

#         flow.storage = Local(path=f"/usr/src/app/worker/prefect/flows/{file}")
#         flow.run_config = LocalRun()
#         flow.register(project_name="default")

async def main():

    # Print the PREFECT_API_URL environment variable
    prefect_api_url = os.getenv('PREFECT_API_URL')
    print(f'PREFECT_API_URL: {prefect_api_url}')
    await dyna_flow_a.serve(name="Dyna Flow A Serve")

if __name__ == "__main__":
    dyna_flow_a.serve("Dyna Flow A Serve")
