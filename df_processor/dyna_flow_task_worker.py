# df_processor/dyna_flow_task_worker.py
"""
not ready. do not use. logic is still in dyna_flow_processor.py
"""
import sys
import uuid
from typing import List

from config import (
    IS_DYNAFLOW_TASK_QUEUE_USED,
    IS_DYNAFLOW_TASK_MASTER,
    IS_DYNAFLOW_TASK_PROCESSOR,
    DYNAFLOW_TASK_RESULT_QUEUE_NAME,
    DYNAFLOW_TASK_DEAD_QUEUE_NAME,
    DYNAFLOW_TASK_PROCESSOR_QUEUE_NAME
)
from datetime import datetime, timedelta, timezone
from database import get_db, engine
from helpers.session_context import SessionContext
from services.custom_temp_folder import CustomTempFolder
from services.machine_identifier import MachineIdentifier
from services.queue_manager import QueueManager
from business import (
    PacBusObj, DFMaintenanceBusObj,
    DynaFlowBusObj, DynaFlowTaskBusObj,
    TriStateFilterBusObj,
    DynaFlowTypeBusObj,
    DynaFlowTaskTypeBusObj
)
from reports import (
    ReportItemPacConfigDynaFlowRetryTaskBuildList,
    ReportManagerPacConfigDynaFlowRetryTaskBuildList,
    ReportItemPacConfigDynaFlowTaskRetryRunList,
    ReportManagerPacConfigDynaFlowTaskRetryRunList,
    ReportItemPacConfigDynaFlowTaskSearch,
    ReportManagerPacConfigDynaFlowTaskSearch,
    ReportManagerPacConfigDynaFlowDFTBuildToDoList,
    ReportItemPacConfigDynaFlowDFTBuildToDoList,
    ReportItemPacConfigDynaFlowTaskRunToDoList,
    ReportManagerPacConfigDynaFlowTaskRunToDoList
    
)
import managers as managers_and_enums  # noqa: F401
from flows.flow_factory import FlowFactory  # noqa: F401
from dyna_flows.dyna_flow_factory import DynaFlowFactory  # noqa: F401


class DynaFlowTaskWorker:
    """
    The DynaFlowProcessor class is responsible for running the
    DynaFlowProcessor application. The DynaFlowProcessor initializes
    the application, processes scheduled DynaFlows, and manages the
    task queues for DynaFlow tasks.
    """
    def __init__(self):
        self._task_result_queue_name = DYNAFLOW_TASK_RESULT_QUEUE_NAME
        self._task_dead_queue_name = DYNAFLOW_TASK_DEAD_QUEUE_NAME
        self._task_processor_queue_name = DYNAFLOW_TASK_PROCESSOR_QUEUE_NAME
        self._is_task_queue_used = bool(IS_DYNAFLOW_TASK_QUEUE_USED)
        self._is_dyna_flow_task_master = bool(IS_DYNAFLOW_TASK_MASTER)
        self._is_dyna_flow_task_processor = bool(IS_DYNAFLOW_TASK_PROCESSOR)

        self._queue_manager = QueueManager()

        machine_identifier = MachineIdentifier()

        self._explicit_instance_id = machine_identifier.get_id()
        self._force_task_error = False
        self._processor_queue_count = 0
        self._dead_queue_count = 0
        self._result_queue_count = 0

        self._custom_temp_folder = CustomTempFolder(
            "dyna_flow_processor_temp_files")

        self._pac_code = uuid.UUID('00000000-0000-0000-0000-000000000000')

    async def run(self):
        """
        Run the DynaFlowTaskWorker.
        """

        print(f"GetInstanceID() : {self.get_instance_id()}")

        self._custom_temp_folder.clear_temp_folder()

        await self.cleanup_my_past_dyna_flow_tasks()

        run_to_do_count = 0
        build_to_do_count = 0
        result_message_count = 0

        while (run_to_do_count > 0 or 
                build_to_do_count > 0 or 
                result_message_count > 0):

            if self._is_task_queue_used is True:
                await self.run_dyna_flow_queue_tasks()
            else:
                run_to_do_count = await self.run_dyna_flow_db_tasks()

    async def get_message_count_async(self, queue_name) -> int:
        """
        Get the count of messages in a queue.
        """

        count = await self._queue_manager.get_message_count_async(queue_name)

        return count

    def get_instance_id(self):
        """
        Get the explicit instance ID of the DynaFlowProcessor.
        """
        return self._explicit_instance_id

    async def cleanup_my_past_dyna_flow_tasks(self):
        """
        Cleanup past DynaFlow tasks.
        """
        async for session in get_db():

            session_context = SessionContext(dict(), session)

            try:

                pac = PacBusObj(session_context)

                await pac.load_from_enum(
                    pac_enum=managers_and_enums.PacEnum.UNKNOWN)

                print("cleanup past dataflow task items")

                tri_state_yes = TriStateFilterBusObj(session_context)
                await tri_state_yes.load_from_enum(
                    tri_state_filter_enum=(
                        managers_and_enums.TriStateFilterEnum.YES)
                )

                tri_state_no = TriStateFilterBusObj(session_context)
                await tri_state_no.load_from_enum(
                    tri_state_filter_enum=(
                        managers_and_enums.TriStateFilterEnum.NO)
                )

                past_task_list = await pac. \
                    generate_report_pac_config_dyna_flow_task_search(
                        processor_identifier=self.get_instance_id(),
                        is_started_tri_state_filter_code=tri_state_yes.code,
                        is_completed_tri_state_filter_code=tri_state_no.code,
                        is_successful_tri_state_filter_code=tri_state_no.code,
                        item_count_per_page=100)

                for item in past_task_list:
                    dyna_flow_task = DynaFlowTaskBusObj(
                        session_context)
                    await dyna_flow_task.load_from_code(
                        item.dyna_flow_task_code)

                    if dyna_flow_task.is_successful is not True and \
                            dyna_flow_task.is_completed is not True:

                        dyna_flow_task.processor_identifier = ""
                        dyna_flow_task.is_started = False
                        dyna_flow_task.is_completed = False

                        await dyna_flow_task.save()

                await session.commit()

            except Exception as e:
                await session.rollback()
                print(f'Error occurred: {e}')
            finally:
                await session.close()

    async def send_message_async(self, queue_name, message):
        """
        Send a message to a queue.
        """

        await self._queue_manager.send_message_async(queue_name, message)

    async def get_dyna_flow_task_type_list(
        self
    ) -> List[DynaFlowTaskTypeBusObj]:
        """
        Get the DynaFlow task type list.
        """
        dyna_flow_task_type_list = list()

        async for session in get_db():

            session_context = SessionContext(dict(), session)

            try:

                pac = PacBusObj(session_context)

                await pac.load_from_enum(
                    pac_enum=managers_and_enums.PacEnum.UNKNOWN)

                dyna_flow_task_type_list = \
                    await pac.get_all_dyna_flow_task_type()

                await session.commit()
            except Exception as e:
                await session.rollback()
                print(f'Error occurred: {e}')
            finally:
                await session.close()

        return dyna_flow_task_type_list

    async def get_task_run_todo_list(
        self
    ) -> List[ReportItemPacConfigDynaFlowTaskRunToDoList]:
        """
        Get the task run to-do list
        """
        run_to_do_list = list()

        async for session in get_db():

            session_context = SessionContext(dict(), session)

            try:

                pac = PacBusObj(session_context)

                await pac.load_from_enum(
                    pac_enum=managers_and_enums.PacEnum.UNKNOWN)

                tri_state_no = TriStateFilterBusObj(session_context)
                await tri_state_no.load_from_enum(
                    tri_state_filter_enum=(
                        managers_and_enums.TriStateFilterEnum.NO)
                )

                run_to_do_list = await pac. \
                    generate_report_pac_config_dyna_flow_task_run_to_do_list(
                        order_by_column_name="DynaFlowPriorityLevel",
                        order_by_descending=True,
                        is_run_task_debug_required_tri_state_filter_code=(
                            tri_state_no.code),
                        item_count_per_page=100)

                await session.commit()
            except Exception as e:
                await session.rollback()
                print(f'Error occurred: {e}')
            finally:
                await session.close()

        return run_to_do_list

    async def claim_dyna_flow_task_for_task_run(
        self,
        dyna_flow_task_code: uuid.UUID,
        dyna_flow_task_type_list: List[DynaFlowTaskTypeBusObj]
    ) -> bool:
        """
        Claim a DynaFlow task for task run
        """
        task_ownership = True

        async for session in get_db():

            session_context = SessionContext(dict(), session)

            try:

                dyna_flow_task = DynaFlowTaskBusObj(session_context)
                await dyna_flow_task.load_from_code(dyna_flow_task_code)

                if dyna_flow_task.is_started is True:
                    task_ownership = False
                    return task_ownership

                dyna_flow_task.is_started = True
                dyna_flow_task.started_utc_date_time = datetime.now(timezone.utc)
                dyna_flow_task.processor_identifier = self.get_instance_id()
                
                dyna_flow_task_type = next(
                    (
                        x
                        for x in dyna_flow_task_type_list
                        if x.code == dyna_flow_task.dyna_flow_task_type_id
                    ),
                    None
                )

                assert dyna_flow_task_type is not None

                dyna_flow_task.max_retry_count = \
                    dyna_flow_task_type.max_retry_count

                await dyna_flow_task.save()

                await session.commit()
            except Exception:
                await session.rollback()
                task_ownership = False
            finally:
                await session.close()

        return task_ownership

    async def run_dyna_flow_db_tasks(self):
        """
        Run DynaFlow tasks from the
        database
        """
        run_to_do_list = await self.get_task_run_todo_list()

        dyna_flow_task_type_list = await self.get_dyna_flow_task_type_list()

        run_to_do_count = len(run_to_do_list)

        print(f"Found {run_to_do_count} "
              "DynaFlowTasks that need to be run")
        
        count = 1

        for item in run_to_do_list:
            count += 1

            print(f"Checking DynaFlowTask #{str(count)} of {run_to_do_count}"
                  f" : {str(item.dyna_flow_task_code)}")
            await self.run_dyna_flow_db_task(
                item.dyna_flow_task_code,
                dyna_flow_task_type_list)

        return run_to_do_count

    async def run_dyna_flow_db_task(
        self,
        dyna_flow_task_code: uuid.UUID,
        dyna_flow_task_type_list: List[DynaFlowTaskTypeBusObj]
    ):
        """
        Run a DynaFlow task from the
        database
        """
        if self._is_dyna_flow_task_processor is not True:
            return
        
        task_ownership = self.claim_dyna_flow_task_for_task_run(
            dyna_flow_task_code,
            dyna_flow_task_type_list
        )

        if task_ownership is not True:
            return

        await self.run_dyna_flow_task(dyna_flow_task_code)

    async def run_dyna_flow_queue_tasks(self):
        """
        Run DynaFlow tasks from the
        queue
        """
        print("Checking for message...")

        while True:
            message = await self._queue_manager.read_next_message(
                self._task_processor_queue_name
            )
            if len(message) == 0:
                break
            print("Message found...")
            try:
                print("Building DynaFlowTask busobj using json data")

                task_code = uuid.UUID(int=0)

                success = False
                
                async for session in get_db():

                    session_context = SessionContext(dict(), session)

                    try:

                        dyna_flow_task = DynaFlowTaskBusObj(session_context)

                        await dyna_flow_task.load_from_json(
                            str(message))

                        dyna_flow_task.processor_identifier = \
                            self.get_instance_id()
                        
                        await dyna_flow_task.save()

                        task_code = dyna_flow_task.code

                        await session.commit()
                    except Exception:
                        await session.rollback()
                    finally:
                        await session.close()

                    if success is not True:
                        raise Exception(
                            "error resetting processor id in task")

                    await self.run_dyna_flow_task(task_code)
            
            except Exception as ex:
                print("Error reading message")
                await self.send_message_async(
                    self._task_dead_queue_name,
                    message)
                print(str(ex))
            await self._queue_manager.mark_message_as_completed(
                self._task_processor_queue_name, message)

    async def run_dyna_flow_task(
            self,
            dyna_flow_task_code: uuid.UUID):
        """
        Run a DynaFlow task.
        """
        success = False

        async for session in get_db():

            session_context = SessionContext(dict(), session)

            try:

                dyna_flow_task = DynaFlowTaskBusObj(session_context)

                await dyna_flow_task.load_from_code(dyna_flow_task_code)

                self._custom_temp_folder.clear_temp_folder()

                dyna_flow_task.started_utc_date_time = datetime.now(timezone.utc)
                dyna_flow_task.is_started = True
                await dyna_flow_task.save()

                dyna_flow = await dyna_flow_task.get_dyna_flow_id_bus_obj()
                if dyna_flow.is_started is not True:
                    dyna_flow.is_started = True
                    dyna_flow.started_utc_date_time = datetime.now(timezone.utc)
                    await dyna_flow.save()  

                if dyna_flow.is_completed:
                    print("DynaFlowTask already completed.  Skipping Run.")

                elif dyna_flow.is_cancel_requested is True: 
                    print("DynaFlowTask cancel requested.")
                    dyna_flow_task.is_canceled = True
                    await dyna_flow_task.save()
                    if dyna_flow.is_cancel_requested:

                        dyna_flow_task_list = await \
                            dyna_flow.get_all_dyna_flow_task()

                        dyna_flow_task_list = [
                            x
                            for x in dyna_flow_task_list
                            if x.is_completed is not True and 
                            not x.is_canceled is not True
                        ]

                        if len(dyna_flow_task_list) == 0:
                            dyna_flow.is_canceled = True
                            await dyna_flow.save()
                else:
                    print(
                        "run dataflow task "
                        f"{dyna_flow_task_type.lookup_enum_name}"
                    )
                    
                    # get dyna flow task type of dyna flow task
                    dyna_flow_task_type = await \
                        dyna_flow_task.get_dyna_flow_task_type_id_bus_obj()

                    # create flow of requested dynaflowtask using factory
                    flow = FlowFactory.create_instance(
                        f"Flow{dyna_flow_task_type.lookup_enum_name}"
                    )

                    # run process fn
                    try:
                        await flow.process(dyna_flow_task)
                        dyna_flow_task.is_successful = True
                        success = True
                    except Exception:
                        # if ((dynaFlowTask.MaxRetryCount > 0 && dynaFlowTask.RetryCount >= dynaFlowTask.MaxRetryCount) ||
                        #     dynaFlowTask.MaxRetryCount == 0)
                        # {
                        #     await DR.Core.Flows.Emails.SendEmailToConfigManagerAsync(new SessionContext(false),
                        #         "Error Running Data Flow Task",
                        #         "Error Running Data Flow Task",
                        #         "Data Flow Task ID: " + dynaFlowTask.DynaFlowTaskID.ToString() + ", Flow Type: " + dynaFlow.GetDynaFlowType().Name + ", Task Type: " + dynaFlowTask.GetDynaFlowTaskType().Name,
                        #         "View",
                        #         "/Report/DynaFlowTaskConfigDetails/" + dynaFlowTask.Code.ToString(),
                        #         EmailTypeManager.LookupEnum.DynaFlowTask_Error_ToConfig,
                        #         dynaFlowTask.Code);
                        # }
                        # throw;
                        pass
                    finally:
                        dyna_flow_task.completed_utc_date_time = \
                            datetime.now(timezone.utc)
                        dyna_flow_task.is_completed = True
                        await dyna_flow_task.save()

                await session.commit()

            except Exception:
                await session.rollback()
            finally:
                await session.close()

        if success is not True:
            async for session in get_db():

                session_context = SessionContext(dict(), session)

                try:

                    dyna_flow_task = DynaFlowTaskBusObj(session_context)

                    await dyna_flow_task.load_from_code(dyna_flow_task_code)

                    if dyna_flow_task.retry_count >= \
                    dyna_flow_task.max_retry_count:
                        if dyna_flow_task.max_retry_count > 0:
                            print("Max Retry count completed. Not Successful.")
                        dyna_flow_task.is_completed = True
                        dyna_flow_task.is_successful = False
                        dyna_flow_task.completed_utc_date_time = \
                            datetime.now(timezone.utc)
                    else:
                        dyna_flow_task.retry_count +=1
                        dyna_flow_task.min_start_utc_date_time = \
                            datetime.now(timezone.utc) + timedelta(minutes=3)
                        dyna_flow_task.is_started = False
                        dyna_flow_task.is_completed = False
                        print(f"Request Retry Attempt "
                              f"{str(dyna_flow_task.retry_count)}")
                    await dyna_flow_task.save()

                    await session.commit()
                except Exception:
                    await session.rollback()
                finally:
                    await session.close()

        if self._is_task_queue_used:

            print(f"sending to result queue dft "
                  f"{str(dyna_flow_task.code)}")

            await self.send_message_async(
                self._task_result_queue_name,
                dyna_flow_task.to_json())
