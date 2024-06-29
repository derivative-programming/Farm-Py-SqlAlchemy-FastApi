from prefect import task
import asyncio


@task
async def dyna_flow_task_b():
    """
    This task is for prefect to run the
    dyna_flow_task_a flow.
    """
    print("DynaFlowTaskB is running")
