from prefect import flow
from worker.prefect.tasks import dyna_flow_task_a, dyna_flow_task_b


@flow()
def dyna_flow_a():
    print("DynaFlowA is running")

    dyna_flow_task_a()
    dyna_flow_task_b()
