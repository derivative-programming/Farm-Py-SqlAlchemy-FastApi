# worker/prefect/flows/dyna_flow_a.py
import asyncio
from prefect import flow
from worker.prefect.tasks import dyna_flow_task_a, dyna_flow_task_b


@flow(name="Dyna Flow A")
async def dyna_flow_a():
    print("DynaFlowA is running")

    await dyna_flow_task_a()
    await dyna_flow_task_b()
