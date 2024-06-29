from prefect import task
import asyncio


@task
async def dyna_flow_task_a():
    """
    This task is for prefect to run the
    dyna_flow_task_a flow.
    """
    print("DynaFlowTaskA is running")
