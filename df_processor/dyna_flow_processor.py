# df_processor/dyna_flow_processor.py  # pylint: disable=duplicate-code
"""
This module contains the `DynaFlowProcessor` class, which is
responsible for running the DynaFlowProcessor application. The
`DynaFlowProcessor` class initializes the application, processes
scheduled DynaFlows, and manages the task queues for DynaFlow tasks.

The `DynaFlowProcessor` class has the following attributes:
- `_task_result_queue_name`: The name of the task result queue.
- `_task_dead_queue_name`: The name of the dead queue.
- `_task_processor_queue_name`: The name of the processor queue.
- `_is_task_queue_used`: A boolean indicating whether the task queue is used.
- `_is_dyna_flow_task_master`: A boolean indicating whether the DynaFlow
    task master is enabled.
- `_is_dyna_flow_task_processor`: A boolean indicating whether the DynaFlow
    task processor is enabled.
- `_queue_manager`: An instance of the `QueueManager` class for managing the
    task queues.
- `_explicit_instance_id`: The explicit instance ID of the DynaFlowProcessor.
- `_force_task_error`: A boolean indicating whether to force task errors.
- `_processor_queue_count`: The count of messages in the processor queue.
- `_dead_queue_count`: The count of messages in the dead queue.
- `_result_queue_count`: The count of messages in the result queue.
- `_custom_temp_folder`: An instance of the `CustomTempFolder` class for
    managing temporary files.
- `_pac_code`: The UUID of the PAC (Process Automation Control) code.

The `DynaFlowProcessor` class has the following methods:
- `run()`: Runs the DynaFlowProcessor application.
- `init_app()`: Initializes the application.
- `get_message_count_async(queue_name)`: Gets the count of messages in a queue.
- `get_instance_id()`: Gets the explicit instance ID of the DynaFlowProcessor.
- `request_scheduled_dyna_flows()`: Requests scheduled DynaFlows for
    processing.
- `claim_dyna_flow_maintenace_for_processing()`: Claims DynaFlow
    maintenance for processing.
"""
import sys
import uuid
from datetime import datetime, timedelta, timezone
from typing import List

import managers as managers_and_enums  # noqa: F401
from business import (DFMaintenanceBusObj, DynaFlowBusObj, DynaFlowTaskBusObj,
                      DynaFlowTaskTypeBusObj, DynaFlowTypeBusObj, PacBusObj,
                      TriStateFilterBusObj)
from config import (DYNAFLOW_TASK_DEAD_QUEUE_NAME,
                    DYNAFLOW_TASK_PROCESSOR_QUEUE_NAME,
                    DYNAFLOW_TASK_RESULT_QUEUE_NAME, IS_DYNAFLOW_TASK_MASTER,
                    IS_DYNAFLOW_TASK_PROCESSOR, IS_DYNAFLOW_TASK_QUEUE_USED)
from database import engine, get_db
from dyna_flows.dyna_flow_factory import DynaFlowFactory  # noqa: F401
from flows.flow_factory import FlowFactory  # noqa: F401
from helpers.session_context import SessionContext
from reports import (ReportItemPacConfigDynaFlowDFTBuildToDoList,
                     ReportItemPacConfigDynaFlowRetryTaskBuildList,
                     ReportItemPacConfigDynaFlowTaskRetryRunList,
                     ReportItemPacConfigDynaFlowTaskRunToDoList,
                     ReportItemPacConfigDynaFlowTaskSearch,
                     ReportManagerPacConfigDynaFlowDFTBuildToDoList,
                     ReportManagerPacConfigDynaFlowRetryTaskBuildList,
                     ReportManagerPacConfigDynaFlowTaskRetryRunList,
                     ReportManagerPacConfigDynaFlowTaskRunToDoList,
                     ReportManagerPacConfigDynaFlowTaskSearch)
from services.custom_temp_folder import CustomTempFolder
from services.machine_identifier import MachineIdentifier
from services.queue_manager import QueueManager


class DynaFlowProcessor:
    """
    The DynaFlowProcessor class is responsible for running the
    DynaFlowProcessor application. The DynaFlowProcessor initializes
    the application, processes scheduled DynaFlows, and manages the
    task queues for DynaFlow tasks.
    """
    def __init__(self):
        print(f"DYNAFLOW_TASK_RESULT_QUEUE_NAME: {DYNAFLOW_TASK_RESULT_QUEUE_NAME}")
        print(f"DYNAFLOW_TASK_DEAD_QUEUE_NAME: {DYNAFLOW_TASK_DEAD_QUEUE_NAME}")
        print(f"DYNAFLOW_TASK_PROCESSOR_QUEUE_NAME: {DYNAFLOW_TASK_PROCESSOR_QUEUE_NAME}")
        print(f"IS_DYNAFLOW_TASK_QUEUE_USED: {IS_DYNAFLOW_TASK_QUEUE_USED}")
        print(f"IS_DYNAFLOW_TASK_MASTER: {IS_DYNAFLOW_TASK_MASTER}")
        print(f"IS_DYNAFLOW_TASK_PROCESSOR: {IS_DYNAFLOW_TASK_PROCESSOR}")

        self._task_result_queue_name = DYNAFLOW_TASK_RESULT_QUEUE_NAME
        self._task_dead_queue_name = DYNAFLOW_TASK_DEAD_QUEUE_NAME
        self._task_processor_queue_name = DYNAFLOW_TASK_PROCESSOR_QUEUE_NAME
        self._is_task_queue_used = IS_DYNAFLOW_TASK_QUEUE_USED
        self._is_dyna_flow_task_master = IS_DYNAFLOW_TASK_MASTER
        self._is_dyna_flow_task_processor = IS_DYNAFLOW_TASK_PROCESSOR

        print(f"self._is_task_queue_used: {self._is_task_queue_used}")
        print(f"self._is_dyna_flow_task_master: {self._is_dyna_flow_task_master}")
        print(f"self._is_dyna_flow_task_processor: {self._is_dyna_flow_task_processor}")

        assert isinstance(self._is_dyna_flow_task_master, bool)
        assert isinstance(self._is_dyna_flow_task_processor, bool)
        assert isinstance(self._is_task_queue_used, bool)

        if self._is_task_queue_used is True:
            self._queue_manager = QueueManager()

        machine_identifier = MachineIdentifier()

        self._explicit_instance_id = machine_identifier.get_id()
        self._force_task_error = False
        self._processor_queue_count = 0
        self._dead_queue_count = 0
        self._result_queue_count = 0

        self._custom_temp_folder = CustomTempFolder(
            "dyna_flow_processor_temp_files")

    def build_session_context(self, session) -> SessionContext:
        """
        Build a session context.
        """

        session_context = SessionContext({}, session)
        session_context.role_name_csv = "Config"
        session_context.user_name = "System"
        session_context.session_code = uuid.uuid4()
        return session_context

    async def run(self):
        """
        Run the DynaFlowProcessor.
        """
        print("Starting DynaFlowProcessor")

        await self.init_app()

        print(f"GetInstanceID() : {self.get_instance_id()}")

        self._custom_temp_folder.clear_temp_folder()

        await self.request_scheduled_dyna_flows()

        await self.cleanup_my_past_dyna_flow_tasks()

        # local_run_loop = read_application_setting("localRunLoop", "false")

        run_to_do_count = 0
        build_to_do_count = 0
        result_message_count = 0
        first_run = True

        while (run_to_do_count > 0 or
                build_to_do_count > 0 or
                result_message_count > 0 or
                first_run is True):

            run_to_do_count = 0
            build_to_do_count = 0
            result_message_count = 0

            first_run = False

            if self._is_dyna_flow_task_master is True:

                if self._is_task_queue_used is True:
                    result_message_count = await \
                        self.process_dyna_flow_queue_task_results()

                build_to_do_count = await self.build_dyna_flow_tasks()

                if self._is_task_queue_used is True:

                    run_to_do_count = await self.serve_dyna_flow_tasks()

                    result_message_count = await \
                        self.process_dyna_flow_queue_task_results()

            if self._is_dyna_flow_task_processor is True:
                if self._is_task_queue_used is True:
                    await self.run_dyna_flow_queue_tasks()
                else:
                    run_to_do_count = await self.run_dyna_flow_db_tasks()
        print("DynaFlowProcessor completed")

    async def init_app(self):
        """
        Initialize the application.
        """
        print("Initializing DynaFlowProcessor")

        print(f"self._is_dyna_flow_task_master: {self._is_dyna_flow_task_master}")
        print(f"self._is_dyna_flow_task_processor: {self._is_dyna_flow_task_processor}")
        if self._is_dyna_flow_task_master is not True and \
                self._is_dyna_flow_task_processor is not True:
            print("No task master or processor")
            sys.exit(1)

        if self._is_task_queue_used is True:

            if len(self._task_dead_queue_name.strip()) == 0:
                print("No dead queue name")
                sys.exit(1)

            if len(self._task_result_queue_name.strip()) == 0:
                print("No task result queue name")
                sys.exit(1)

            if len(self._task_processor_queue_name.strip()) == 0:
                print("No processor queue name")
                sys.exit(1)

        if self._is_dyna_flow_task_master is True:
            print("Starting Task Master")

        if self._is_dyna_flow_task_processor is True:
            print("Starting Task Processor")

        if self._is_task_queue_used is True:
            self._processor_queue_count = await \
                self.get_message_count_async(self._task_processor_queue_name)
            self._dead_queue_count = await \
                self.get_message_count_async(self._task_dead_queue_name)
            self._result_queue_count = await \
                self.get_message_count_async(self._task_result_queue_name)
        print("DynaFlowProcessor initialized")

    async def get_message_count_async(self, queue_name) -> int:
        """
        Get the count of messages in a queue.
        """
        print(f"Getting message count for {queue_name}")
        count = await self._queue_manager.get_message_count_async(queue_name)
        print(f"Message count for {queue_name}: {count}")
        return count

    def get_instance_id(self):
        """
        Get the explicit instance ID of the DynaFlowProcessor.
        """
        print(f"Returning instance ID: {self._explicit_instance_id}")
        return self._explicit_instance_id

    async def request_scheduled_dyna_flows(self):
        """
        Request scheduled DynaFlows for processing.
        """
        print("Requesting scheduled DynaFlows for processing")
        ownership = await self.claim_dyna_flow_maintenace_for_processing()

        if ownership is not True:
            return

        async for session in get_db():

            session_context = self.build_session_context(session)

            try:

                pac = PacBusObj(session_context)

                await pac.load_from_enum(
                    pac_enum=managers_and_enums.PacEnum.UNKNOWN)

                df_mainenance_bus_obj = await self.get_dFMaintenance(
                    session_context)

                print("request any scheduled dataflows")

                await pac.request_dyna_flow_pac_process_all_dyna_flow_type_schedule_flow(  # noqa: E501
                    description="Process all scheduled data flows"
                )

                rebuild_items = await pac. \
                    generate_report_pac_config_dyna_flow_retry_task_build_list(
                        1,
                        100,
                        "",
                        False
                    )

                print("rebuild_items: ", rebuild_items)

                for item in rebuild_items:

                    dyna_flow = DynaFlowBusObj(session_context)

                    await dyna_flow.load_from_code(item.dyna_flow_code)

                    dyna_flow \
                        .set_prop_is_task_creation_started(False) \
                        .set_prop_task_creation_processor_identifier("") \
                        .set_prop_is_started(False)

                    await dyna_flow.save()

                rerun_items = await pac. \
                    generate_report_pac_config_dyna_flow_task_retry_run_list(
                        1,
                        100,
                        "",
                        False
                    )

                print("rerun_items: ", rerun_items)

                for item in rerun_items:

                    dyna_flow_task = DynaFlowTaskBusObj(session_context)

                    await dyna_flow_task.load_from_code(
                        item.dyna_flow_task_code)

                    dyna_flow_task \
                        .set_prop_processor_identifier("") \
                        .set_prop_is_started(False)

                    await dyna_flow_task.save()

                df_mainenance_bus_obj \
                    .set_prop_is_scheduled_df_process_request_started(False) \
                    .set_prop_is_scheduled_df_process_request_completed(True) \
                    .set_prop_last_scheduled_df_process_request_utc_date_time(
                        datetime.now(timezone.utc)) \
                    .set_prop_next_scheduled_df_process_request_utc_date_time(
                        datetime.now(timezone.utc) + timedelta(minutes=30))

                await df_mainenance_bus_obj.save()

                await session.commit()

            except Exception as e:
                await session.rollback()
                print(f'Error occurred: {e}')
            finally:
                await session.close()
        print("Scheduled DynaFlows requested")

    async def claim_dyna_flow_maintenace_for_processing(
        self
    ) -> bool:
        """
        Claim DynaFlow maintenance for processing.
        """
        print("Claiming DynaFlow maintenance for processing")
        ownership = True

        async for session in get_db():

            session_context = self.build_session_context(session)

            try:

                pac = PacBusObj(session_context)

                await pac.load_from_enum(
                    pac_enum=managers_and_enums.PacEnum.UNKNOWN)

                df_mainenance_bus_obj = await self.get_dFMaintenance(
                    session_context)

                if df_mainenance_bus_obj. \
                        scheduled_df_process_request_processor_identifier == \
                        self.get_instance_id() and \
                        df_mainenance_bus_obj. \
                        is_scheduled_df_process_request_started is True:
                    # This is a retry. it errored out on this machine
                    # force it to try again
                    df_mainenance_bus_obj. \
                        is_scheduled_df_process_request_started = False
                    df_mainenance_bus_obj. \
                        is_scheduled_df_process_request_completed = True
                    df_mainenance_bus_obj. \
                        next_scheduled_df_process_request_utc_date_time = \
                        datetime.now(timezone.utc) - timedelta(days=100)

                if df_mainenance_bus_obj. \
                        is_scheduled_df_process_request_started is True:
                    # if attempting now, it may have errored out
                    # give it a day to try again
                    if df_mainenance_bus_obj. \
                        next_scheduled_df_process_request_utc_date_time >= \
                            datetime.now(timezone.utc) - timedelta(days=1):
                        ownership = False
                        return ownership

                else:
                    # if not attempted already, check if it is time to run
                    if df_mainenance_bus_obj. \
                        next_scheduled_df_process_request_utc_date_time >= \
                            datetime.now(timezone.utc):
                        ownership = False
                        return ownership

                df_mainenance_bus_obj. \
                    is_scheduled_df_process_request_started = True

                df_mainenance_bus_obj. \
                    is_scheduled_df_process_request_completed = False

                df_mainenance_bus_obj. \
                    scheduled_df_process_request_processor_identifier = \
                    self.get_instance_id()

                await df_mainenance_bus_obj.save()

                await session.commit()
            except Exception as e:
                await session.rollback()
                print(f'Error occurred: {e}')
                ownership = False
            finally:
                await session.close()
        print("DynaFlow maintenance claimed for processing")
        return ownership

    async def get_dFMaintenance(self, session_context) -> DFMaintenanceBusObj:
        """
        Get the DynaFlow maintenance object.
        """
        print("Getting DynaFlow maintenance object")
        pac = PacBusObj(session_context)

        await pac.load_from_enum(
            pac_enum=managers_and_enums.PacEnum.UNKNOWN)

        df_maintenance_list = await pac.get_all_df_maintenance()

        if len(df_maintenance_list) == 0:
            df_maintenance = await pac.build_df_maintenance()
            await df_maintenance.save()
        else:
            df_maintenance = df_maintenance_list[0]
        print(f"DynaFlow maintenance object retrieved {df_maintenance.df_maintenance_id}")
        return df_maintenance

    async def cleanup_my_past_dyna_flow_tasks(self):
        """
        Cleanup past DynaFlow tasks.
        """
        print("Cleaning up past DynaFlow tasks")
        async for session in get_db():

            session_context = self.build_session_context(session)

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

                print("past_task_list: ", past_task_list)

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
        print("Past DynaFlow tasks cleaned up")

    async def process_dyna_flow_queue_task_results(self):
        """
        Process DynaFlow queue task results.
        """
        print("Processing DynaFlow queue task results")
        message_count = 0

        while True:
            message = await self._queue_manager.read_next_message(
                self._task_result_queue_name
            )
            if len(message) == 0:
                break
            message_count += 1
            print("Message found...")
            # not necessary. worker is saving it currently
            # try:
            #     dyna_flow_task =
            #   self.create_dyna_flow_task_from_message(message)
            #     await self.save_dyna_flow_task(dyna_flow_task)
            # except Exception as ex:
            #     print("Error reading message")
            #     await self.send_message_async(
            #         self._task_dead_queue_name,
            #         message)
            #     print(str(ex))
            await self._queue_manager.mark_message_as_completed(
                self._task_result_queue_name, message)

        print("DynaFlow queue task results processed")

        return message_count

    async def send_message_async(self, queue_name, message):
        """
        Send a message to a queue.
        """
        print(f"Sending message to {queue_name}")
        await self._queue_manager.send_message_async(queue_name, message)

    async def build_dyna_flow_tasks(self):
        """
        Build DynaFlow tasks.
        """
        print("Building DynaFlow tasks")
        build_to_do_count = 0

        build_to_do_list = await self.get_task_build_todo_list()

        dyna_flow_type_list = await self.get_dyna_flow_type_list()

        build_to_do_count = len(build_to_do_list)

        print(
            f"Found {build_to_do_count} "
            "DynaFlows that need tasks built"
        )

        for item in build_to_do_list:
            await self.build_tasks_for_dyna_flow(
                item.dyna_flow_code,
                dyna_flow_type_list
            )
        print("DynaFlow tasks built")
        return build_to_do_count

    async def get_task_build_todo_list(
        self
    ) -> List[ReportItemPacConfigDynaFlowDFTBuildToDoList]:
        """
        Get the task build to-do list.
        """
        print("Getting task build to-do list")
        build_to_do_list = []

        async for session in get_db():

            session_context = self.build_session_context(session)

            try:

                pac = PacBusObj(session_context)

                await pac.load_from_enum(
                    pac_enum=managers_and_enums.PacEnum.UNKNOWN)

                tri_state_no = TriStateFilterBusObj(session_context)
                await tri_state_no.load_from_enum(
                    tri_state_filter_enum=(
                        managers_and_enums.TriStateFilterEnum.NO)
                )

                build_to_do_list = await pac. \
                    generate_report_pac_config_dyna_flow_dft_build_to_do_list(
                        order_by_column_name="RequestedUTCDateTime",
                        order_by_descending=False,
                        is_build_task_debug_required_tri_state_filter_code=(
                            tri_state_no.code),
                        item_count_per_page=100)

                await session.commit()
            except Exception as e:
                await session.rollback()
                print(f'Error occurred: {e}')
            finally:
                await session.close()
        print("Task build to-do list retrieved")
        return build_to_do_list

    async def get_dyna_flow_type_list(
        self
    ) -> List[DynaFlowTypeBusObj]:
        """
        Get the DynaFlow type list.
        """
        print("Getting DynaFlow type list")
        dyna_flow_type_list = []

        async for session in get_db():

            session_context = self.build_session_context(session)

            try:

                pac = PacBusObj(session_context)

                await pac.load_from_enum(
                    pac_enum=managers_and_enums.PacEnum.UNKNOWN)

                dyna_flow_type_list = await pac.get_all_dyna_flow_type()

                await session.commit()
            except Exception as e:
                await session.rollback()
                print(f'Error occurred: {e}')
            finally:
                await session.close()
        print("DynaFlow type list retrieved")
        return dyna_flow_type_list

    async def get_dyna_flow_task_type_list(
        self
    ) -> List[DynaFlowTaskTypeBusObj]:
        """
        Get the DynaFlow task type list.
        """
        print("Getting DynaFlow task type list")
        dyna_flow_task_type_list = []

        async for session in get_db():

            session_context = self.build_session_context(session)

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
        print("DynaFlow task type list retrieved")
        return dyna_flow_task_type_list

    async def build_tasks_for_dyna_flow(
        self,
        dyna_flow_code: uuid.UUID,
        dyna_flow_type_list: List[DynaFlowTypeBusObj]
    ):
        """
        Build tasks for a DynaFlow.
        """
        print(f"Building tasks for DynaFlow {dyna_flow_code}")
        task_ownership = await self.claim_dyna_flow_for_task_build(
            dyna_flow_code,
            dyna_flow_type_list
        )

        if task_ownership is not True:
            return

        async for session in get_db():

            session_context = self.build_session_context(session)

            try:

                dyna_flow = DynaFlowBusObj(session_context)
                await dyna_flow.load_from_code(dyna_flow_code)

                print(
                    "Building tasks for DynaFlow "
                    f"{dyna_flow.code}")

                if dyna_flow.is_completed is True:
                    print("DynaFlow Tasks already completed.  "
                          "Skipping buildtasks.")
                elif dyna_flow.is_tasks_created is True:
                    print("DynaFlow Tasks already built.  "
                          "Skipping buildtasks.")
                elif dyna_flow.is_cancel_requested is not True:
                    try:

                        dyna_flow_type = await \
                            dyna_flow.get_dyna_flow_type_id_obj()

                        build_task_processor = DynaFlowFactory.create_instance(
                            dyna_flow_type.lookup_enum_name
                        )
                        await build_task_processor.build_dyna_flow_tasks(
                            dyna_flow)

                        dyna_flow.is_tasks_created = True
                        await dyna_flow.save()
                    except Exception as e:
                        print(f'Error occurred: {e}')
                        dyna_flow.is_completed = True
                        dyna_flow.is_successful = False
                        dyna_flow.completed_utc_date_time = \
                            datetime.now(timezone.utc)
                        await dyna_flow.save()
                else:
                    if dyna_flow.is_cancel_requested is True:
                        dyna_flow.is_canceled = True
                        await dyna_flow.save()

                await session.commit()
            except Exception as e:
                await session.rollback()
                print(f'Error occurred: {e}')
            finally:
                await session.close()
        print("Tasks built for DynaFlow")

    async def claim_dyna_flow_for_task_build(
        self,
        dyna_flow_code: uuid.UUID,
        dyna_flow_type_list: List[DynaFlowTypeBusObj]
    ) -> bool:
        """
        Claim a DynaFlow for task build
        """
        print(f"Claiming DynaFlow for task build {dyna_flow_code}")
        task_ownership = True

        async for session in get_db():

            session_context = self.build_session_context(session)

            try:

                dyna_flow = DynaFlowBusObj(session_context)
                await dyna_flow.load_from_code(dyna_flow_code)

                if dyna_flow.is_task_creation_started is True:
                    task_ownership = False
                    return task_ownership

                dyna_flow.is_task_creation_started = True

                dyna_flow.task_creation_processor_identifier = \
                    self.get_instance_id()

                dyna_flow_type = next(
                    (
                        x
                        for x in dyna_flow_type_list
                        if x.dyna_flow_type_id == dyna_flow.dyna_flow_type_id
                    ),
                    None
                )

                assert dyna_flow_type is not None

                dyna_flow.priority_level = \
                    dyna_flow_type.priority_level

                await dyna_flow.save()

                await session.commit()
            except Exception as e:
                print(f'Error occurred: {e}')
                await session.rollback()
                task_ownership = False
            finally:
                await session.close()
        print("DynaFlow claimed for task build")
        return task_ownership

    async def get_task_run_todo_list(
        self
    ) -> List[ReportItemPacConfigDynaFlowTaskRunToDoList]:
        """
        Get the task run to-do list
        """
        print("Getting task run to-do list")
        run_to_do_list = []

        async for session in get_db():

            session_context = self.build_session_context(session)

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
        print("Task run to-do list retrieved")
        return run_to_do_list

    async def claim_dyna_flow_task_for_task_run(
        self,
        dyna_flow_task_code: uuid.UUID,
        dyna_flow_task_type_list: List[DynaFlowTaskTypeBusObj]
    ) -> bool:
        """
        Claim a DynaFlow task for task run
        """
        print(f"Claiming DynaFlow task for task run {dyna_flow_task_code}")
        task_ownership = True

        async for session in get_db():

            session_context = self.build_session_context(session)

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
                        if x.dyna_flow_task_type_id == dyna_flow_task.dyna_flow_task_type_id
                    ),
                    None
                )

                assert dyna_flow_task_type is not None

                dyna_flow_task.max_retry_count = \
                    dyna_flow_task_type.max_retry_count

                await dyna_flow_task.save()

                await session.commit()
            except Exception as e:
                print(f'Error occurred: {e}')
                await session.rollback()
                task_ownership = False
            finally:
                await session.close()
        print("DynaFlow task claimed for task run")
        return task_ownership

    async def get_dyna_flow_task_json(
        self,
        dyna_flow_task_code: uuid.UUID
    ) -> str:
        """
        Get the JSON representation of a DynaFlow task
        """
        print(f"Getting JSON representation of DynaFlow task {dyna_flow_task_code}")
        json = ""
        async for session in get_db():

            session_context = self.build_session_context(session)

            try:

                dyna_flow_task = DynaFlowTaskBusObj(session_context)

                await dyna_flow_task.load_from_code(dyna_flow_task_code)

                json = dyna_flow_task.to_json()

                await session.commit()
            except Exception as e:
                print(f'Error occurred: {e}')
                await session.rollback()
                task_ownership = False
            finally:
                await session.close()
        print("JSON representation of DynaFlow task retrieved")
        return json

    async def serve_dyna_flow_task(
        self,
        dyna_flow_task_code: uuid.UUID,
        dyna_flow_task_type_list: List[DynaFlowTaskTypeBusObj]
    ):
        """
        Serve a DynaFlow task
        """
        print(f"Serving DynaFlow task {dyna_flow_task_code}")
        if self._is_task_queue_used is not True:
            return

        task_ownership = await self.claim_dyna_flow_task_for_task_run(
            dyna_flow_task_code,
            dyna_flow_task_type_list
        )

        if task_ownership is not True:
            return

        print(f"Sending Queue Message dft {str(dyna_flow_task_code)}")

        json = await self.get_dyna_flow_task_json(dyna_flow_task_code)

        await self.send_message_async(
            self._task_processor_queue_name,
            json)
        print("DynaFlow task served")

    async def serve_dyna_flow_tasks(self):
        """
        Serve DynaFlow tasks
        """
        print("Serving DynaFlow tasks")
        if self._is_task_queue_used is not True:
            return

        run_to_do_list = await self.get_task_run_todo_list()

        dyna_flow_task_type_list = await self.get_dyna_flow_task_type_list()

        run_to_do_count = len(run_to_do_list)

        print(f"Found {run_to_do_count} "
              "DynaFlowTasks that need to be run")

        count = 0

        for item in run_to_do_list:
            count += 1

            print(f"Checking DynaFlowTask #{str(count)} of {run_to_do_count}"
                  f" : {str(item.dyna_flow_task_code)}")
            await self.serve_dyna_flow_task(
                item.dyna_flow_task_code,
                dyna_flow_task_type_list)
        print("DynaFlow tasks served")
        return run_to_do_count

    async def run_dyna_flow_db_tasks(self):
        """
        Run DynaFlow tasks from the
        database
        """
        print("Running DynaFlow tasks from the database")
        run_to_do_list = await self.get_task_run_todo_list()

        dyna_flow_task_type_list = await self.get_dyna_flow_task_type_list()

        run_to_do_count = len(run_to_do_list)

        print(f"Found {run_to_do_count} "
              "DynaFlowTasks that need to be run")

        count = 0

        for item in run_to_do_list:
            count += 1

            print(f"Checking DynaFlowTask #{str(count)} of {run_to_do_count}"
                  f" : {str(item.dyna_flow_task_code)}")
            await self.run_dyna_flow_db_task(
                item.dyna_flow_task_code,
                dyna_flow_task_type_list)
        print("DynaFlow tasks run from the database")
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
        print(f"Running DynaFlow task from the database {dyna_flow_task_code}")
        if self._is_dyna_flow_task_processor is not True:
            return

        task_ownership = await self.claim_dyna_flow_task_for_task_run(
            dyna_flow_task_code,
            dyna_flow_task_type_list
        )

        if task_ownership is not True:
            return

        await self.run_dyna_flow_task(dyna_flow_task_code)

        print("DynaFlow task run from the database")

    async def run_dyna_flow_queue_tasks(self):
        """
        Run DynaFlow tasks from the
        queue
        """
        print("Running DynaFlow tasks from the queue")
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

                    session_context = self.build_session_context(session)

                    try:

                        dyna_flow_task = DynaFlowTaskBusObj(session_context)

                        await dyna_flow_task.load_from_json(
                            str(message))

                        dyna_flow_task.processor_identifier = \
                            self.get_instance_id()

                        await dyna_flow_task.save()

                        task_code = dyna_flow_task.code

                        await session.commit()
                    except Exception as e:
                        print(f'Error occurred: {e}')
                        await session.rollback()
                    finally:
                        await session.close()

                    if success is not True:
                        raise Exception(
                            "error resetting processor id in task")

                    await self.run_dyna_flow_task(task_code)

            except Exception as ex:
                print("Error reading message...")
                print(f'Error occurred: {e}')
                await self.send_message_async(
                    self._task_dead_queue_name,
                    message)
                print(str(ex))
            await self._queue_manager.mark_message_as_completed(
                self._task_processor_queue_name, message)
        print("DynaFlow tasks run from the queue")

    async def run_dyna_flow_task(
            self,
            dyna_flow_task_code: uuid.UUID):
        """
        Run a DynaFlow task.
        """
        print(f"Running DynaFlow task {dyna_flow_task_code}")
        success = False

        async for session in get_db():

            session_context = self.build_session_context(session)

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

                if dyna_flow.is_completed is True:
                    print("DynaFlowTask already completed.  Skipping Run.")

                elif dyna_flow.is_cancel_requested is True:
                    print("DynaFlowTask cancel requested.")
                    dyna_flow_task.is_canceled = True
                    await dyna_flow_task.save()
                    if dyna_flow.is_cancel_requested is True:

                        dyna_flow_task_list = await \
                            dyna_flow.get_all_dyna_flow_task()

                        dyna_flow_task_list = [
                            x
                            for x in dyna_flow_task_list
                            if x.is_completed is not True and x.is_canceled is not True
                        ]

                        if len(dyna_flow_task_list) == 0:
                            dyna_flow.is_canceled = True
                            await dyna_flow.save()
                else:
                    # get dyna flow task type of dyna flow task
                    dyna_flow_task_type = await \
                        dyna_flow_task.get_dyna_flow_task_type_id_bus_obj()

                    print(
                        "run dataflow task "
                        f"{dyna_flow_task_type.lookup_enum_name}"
                    )

                    # create flow of requested dynaflowtask using factory
                    flow = FlowFactory.create_instance(
                        f"Flow{dyna_flow_task_type.lookup_enum_name}",
                        session_context
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

            except Exception as e:
                print(f'Error occurred: {e}')
                await session.rollback()
            finally:
                await session.close()

        if success is not True:
            async for session in get_db():

                session_context = self.build_session_context(session)

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
                        dyna_flow_task.retry_count += 1
                        dyna_flow_task.min_start_utc_date_time = \
                            datetime.now(timezone.utc) + timedelta(minutes=3)
                        dyna_flow_task.is_started = False
                        dyna_flow_task.is_completed = False
                        print(f"Request Retry Attempt "
                              f"{str(dyna_flow_task.retry_count)}")
                    await dyna_flow_task.save()

                    await session.commit()
                except Exception as e:
                    print(f'Error occurred: {e}')
                    await session.rollback()
                finally:
                    await session.close()

        if self._is_task_queue_used is True:

            print(f"sending to result queue dft "
                  f"{str(dyna_flow_task.code)}")

            await self.send_message_async(
                self._task_result_queue_name,
                dyna_flow_task.to_json())
        print("DynaFlow task run")
