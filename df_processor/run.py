import os
import sys
import uuid
import asyncio
import tempfile
import os
from typing import List

from config import (
    IS_DYNAFLOW_TASK_QUEUE_USED,
    IS_DYNAFLOW_TASK_MASTER,
    IS_DYNAFLOW_TASK_PROCESSOR,
    DYNAFLOW_TASK_RESULT_QUEUE_NAME,
    DYNAFLOW_TASK_DEAD_QUEUE_NAME,
    DYNAFLOW_TASK_PROCESSOR_QUEUE_NAME,
    AZURE_SERVICE_BUS_CONNECTION_STRING
)
from azure.servicebus import ServiceBusClient, ServiceBusMessage
from datetime import datetime, timedelta, timezone
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from database import get_db, engine
from helpers.session_context import SessionContext
from services.custom_temp_folder import CustomTempFolder
from services.machine_identifier import MachineIdentifier
import current_runtime
from models import Base
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


class DynaFlowProcessor:
    def __init__(self):
        self._task_result_queue_name = DYNAFLOW_TASK_RESULT_QUEUE_NAME
        self._task_dead_queue_name = DYNAFLOW_TASK_DEAD_QUEUE_NAME
        self._task_processor_queue_name = DYNAFLOW_TASK_PROCESSOR_QUEUE_NAME
        self._is_task_queue_used = bool(IS_DYNAFLOW_TASK_QUEUE_USED)
        self._is_dyna_flow_task_master = bool(IS_DYNAFLOW_TASK_MASTER)
        self._is_dyna_flow_task_processor = bool(IS_DYNAFLOW_TASK_PROCESSOR)

        machine_identifier = MachineIdentifier()
        
        self._explicit_instance_id = machine_identifier.get_id()
        self._force_task_error = False
        self._service_bus_client = None
        if self._is_task_queue_used:
            self._service_bus_client = ServiceBusClient.from_connection_string(
                AZURE_SERVICE_BUS_CONNECTION_STRING)
        self._processor_queue_count = 0
        self._dead_queue_count = 0
        self._result_queue_count = 0

        self._custom_temp_folder = CustomTempFolder(
            "dyna_flow_processor_temp_files")
        
        self._pac_code = uuid.UUID('00000000-0000-0000-0000-000000000000')

    async def run(self):
        """
        Run the DynaFlowProcessor.
        """

        await self.init_app()

        print(f"GetInstanceID() : {self.get_instance_id()}")

        self._custom_temp_folder.clear_temp_folder()

        await self.request_scheduled_dyna_flows()

        await self.cleanup_my_past_dyna_flow_tasks()

        # local_run_loop = read_application_setting("localRunLoop", "false")

        run_to_do_count = 0
        build_to_do_count = 0
        result_message_count = 0

        while (run_to_do_count > 0 or 
                build_to_do_count > 0 or 
                result_message_count > 0):

            if self._is_dyna_flow_task_master:

                result_message_count = await \
                    self.process_dyna_flow_queue_task_results()

                build_to_do_count = await self.build_dyna_flow_tasks()
    
                if self._is_task_queue_used:

                    run_to_do_count = await self.serve_dyna_flow_tasks()

                    result_message_count = await \
                        self.process_dyna_flow_queue_task_results()

            if self._is_dyna_flow_task_processor:
                if not self._is_task_queue_used:
                    run_to_do_count = await self.run_dyna_flow_db_tasks()
                else:
                    await self.run_dyna_flow_queue_tasks()

    async def init_app(self):
        """
        Initialize the application.
        """

        if not self._is_dyna_flow_task_master and \
                not self._is_dyna_flow_task_processor:
            print("No task master or processor")
            sys.exit(1)

        if self._is_task_queue_used:

            if len(self._task_dead_queue_name.strip()) == 0:
                print("No dead queue name")
                sys.exit(1)

            if len(self._task_result_queue_name.strip()) == 0:
                print("No task result queue name")
                sys.exit(1)

            if len(self._task_processor_queue_name.strip()) == 0:
                print("No processor queue name")
                sys.exit(1)

        if self._is_dyna_flow_task_master:
            print("Starting Task Master")

        if self._is_dyna_flow_task_processor:
            print("Starting Task Processor")

        if self._is_task_queue_used:
            self._processor_queue_count = await \
                self.get_message_count_async(self._task_processor_queue_name)
            self._dead_queue_count = await \
                self.get_message_count_async(self._task_dead_queue_name)
            self._result_queue_count = await \
                self.get_message_count_async(self._task_result_queue_name)

    async def get_message_count_async(self, queue_name) -> int:
        """
        Get the count of messages in a queue.
        """
        assert self._service_bus_client is not None

        receiver = self._service_bus_client.get_queue_receiver(queue_name)

        count = len(receiver.peek_messages(max_message_count=32))

        return count

    def get_instance_id(self):
        return self._explicit_instance_id

    async def request_scheduled_dyna_flows(self):

        ownership = await self.claim_dyna_flow_maintenace_for_processing()

        if ownership is not True:
            return

        async for session in get_db():

            session_context = SessionContext(dict(), session)

            try:

                pac = PacBusObj(session_context)

                await pac.load_from_enum(
                    pac_enum=managers_and_enums.PacEnum.UNKNOWN)

                df_mainenance_bus_obj = await self.get_dFMaintenance(
                    session_context)

                print("request any scheduled dataflows")

                # await pac['PacProcessAllDynaFlowTypeScheduleFlow_ViaDynaFlow']("Process all scheduled data flows")

                rebuild_items_manager = \
                    ReportManagerPacConfigDynaFlowRetryTaskBuildList(
                        session_context)

                rebuild_items = await rebuild_items_manager. \
                    generate(
                        pac.code,
                        1,
                        100,
                        "",
                        False
                    )
                for item in rebuild_items:

                    dyna_flow = DynaFlowBusObj(session_context)

                    await dyna_flow.load_from_code(item.dyna_flow_code)

                    dyna_flow \
                        .set_prop_is_task_creation_started(False) \
                        .set_prop_task_creation_processor_identifier("") \
                        .set_prop_is_started(False)

                    await dyna_flow.save()

                rerun_items_manager = \
                    ReportManagerPacConfigDynaFlowTaskRetryRunList(
                        session_context)

                rerun_items = await rerun_items_manager. \
                    generate(
                        pac.code,
                        1,
                        100,
                        "",
                        False
                    )
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

    async def claim_dyna_flow_maintenace_for_processing(
        self
    ) -> bool:

        ownership = True

        async for session in get_db():

            session_context = SessionContext(dict(), session)

            try:

                pac = PacBusObj(session_context)

                await pac.load_from_enum(
                    pac_enum=managers_and_enums.PacEnum.UNKNOWN)

                df_mainenance_bus_obj = await self.get_dFMaintenance(
                    session_context)

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
            except Exception:
                await session.rollback()
                ownership = False
            finally:
                await session.close()

        return ownership

    async def get_dFMaintenance(self, session_context) -> DFMaintenanceBusObj:

        pac = PacBusObj(session_context)

        await pac.load_from_enum(
            pac_enum=managers_and_enums.PacEnum.UNKNOWN)

        df_maintenance_list = await pac.get_all_df_maintenance()

        if len(df_maintenance_list) == 0:
            df_maintenance = await pac.build_df_maintenance()
            await df_maintenance.save()
        else:
            df_maintenance = df_maintenance_list[0]

        return df_maintenance

    async def cleanup_my_past_dyna_flow_tasks(self):

        async for session in get_db():

            session_context = SessionContext(dict(), session)

            try:

                pac = PacBusObj(session_context)

                await pac.load_from_enum(
                    pac_enum=managers_and_enums.PacEnum.UNKNOWN)

                print("cleanup past dataflow task items")

                past_task_list_manager = \
                    ReportManagerPacConfigDynaFlowTaskSearch(
                        session_context)
                
                tri_state_yes = TriStateFilterBusObj(session_context)
                await tri_state_yes.load_from_enum(
                    tri_state_filter_enum=
                    managers_and_enums.TriStateFilterEnum.YES
                )

                tri_state_no = TriStateFilterBusObj(session_context)
                await tri_state_no.load_from_enum(
                    tri_state_filter_enum=
                    managers_and_enums.TriStateFilterEnum.NO
                )

                past_task_list = await past_task_list_manager.generate(
                    pac.code,
                    processor_identifier=self.get_instance_id(),
                    is_started_tri_state_filter_code=tri_state_yes.code,
                    is_completed_tri_state_filter_code=tri_state_no.code,
                    is_successful_tri_state_filter_code=tri_state_no.code,
                    item_count_per_page=100,
                )

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

    async def process_dyna_flow_queue_task_results(self):

        message_count = 0

        assert self._service_bus_client is not None

        receiver = self._service_bus_client.get_queue_receiver(
            self._task_result_queue_name
        )

        while True:
            messages = receiver.receive_messages(
                max_message_count=1,
                max_wait_time=5
            )
            if not messages:
                break
            message = messages[0]
            message_count += 1
            print("Message found...")
            # not necessary. worker is saving it currently
            # try:
            #     dyna_flow_task = self.create_dyna_flow_task_from_message(message)
            #     await self.save_dyna_flow_task(dyna_flow_task)
            # except Exception as ex:
            #     print("Error reading message")
            #     await self.send_message_async(
            #         self._task_dead_queue_name,
            #         message)
            #     print(str(ex))
            receiver.complete_message(message)

        return message_count

    async def send_message_async(self, queue_name, message):

        assert self._service_bus_client is not None

        sender = self._service_bus_client.get_queue_sender(
            queue_name
        )

        sender.send_messages(ServiceBusMessage(message))

    async def build_dyna_flow_tasks(self):

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

        return build_to_do_count

    async def get_task_build_todo_list(
        self
    ) -> List[ReportItemPacConfigDynaFlowDFTBuildToDoList]:

        build_to_do_list = list()

        async for session in get_db():

            session_context = SessionContext(dict(), session)

            try:

                pac = PacBusObj(session_context)

                await pac.load_from_enum(
                    pac_enum=managers_and_enums.PacEnum.UNKNOWN)

                report_manager = \
                    ReportManagerPacConfigDynaFlowDFTBuildToDoList(
                        session_context
                    )

                tri_state_no = TriStateFilterBusObj(session_context)
                await tri_state_no.load_from_enum(
                    tri_state_filter_enum=managers_and_enums.TriStateFilterEnum.NO
                )

                build_to_do_list = await report_manager.generate(
                    pac.code,
                    order_by_column_name="RequestedUTCDateTime",
                    order_by_descending=False,
                    is_build_task_debug_required_tri_state_filter_code=tri_state_no.code,
                    item_count_per_page=100
                )

                await session.commit()
            except Exception as e:
                await session.rollback()
                print(f'Error occurred: {e}')
            finally:
                await session.close()

        return build_to_do_list

    async def get_dyna_flow_type_list(
        self
    ) -> List[DynaFlowTypeBusObj]:

        dyna_flow_type_list = list()

        async for session in get_db():

            session_context = SessionContext(dict(), session)

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

        return dyna_flow_type_list

    async def get_dyna_flow_task_type_list(
        self
    ) -> List[DynaFlowTaskTypeBusObj]:

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

    async def build_tasks_for_dyna_flow(
        self,
        dyna_flow_code: uuid.UUID,
        dyna_flow_type_list: List[DynaFlowTypeBusObj]
    ):
        # get ownership of the dyna flow

        task_ownership = self.claim_dyna_flow_for_task_build(
            dyna_flow_code,
            dyna_flow_type_list
        )

        if task_ownership is not True:
            return

        async for session in get_db():

            session_context = SessionContext(dict(), session)

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
                        # TODO build tasks
                        # build_task_class = dyna_flow.dyna_flow_type
                        # dyna_flow_build_tasks_processor = \
                        #     self.build_tasks_processor_factory.build(
                        #         build_task_class
                        #     )
                        # await dyna_flow_build_tasks_processor.build_task(
                        #     dyna_flow
                        # )
                        # await dyna_flow.refresh()
                        dyna_flow.is_tasks_created = True
                        await dyna_flow.save()
                    except Exception:
                        dyna_flow.is_completed = True
                        dyna_flow.is_successful = False
                        dyna_flow.completed_utc_date_time = \
                            datetime.now(timezone.utc)
                        await dyna_flow.save()
                else:
                    if dyna_flow.is_cancel_requested:
                        dyna_flow.is_canceled = True
                        await dyna_flow.save()

                await session.commit()
            except Exception as e:
                await session.rollback()
                print(f'Error occurred: {e}')
            finally:
                await session.close()

    async def claim_dyna_flow_for_task_build(
        self,
        dyna_flow_code: uuid.UUID,
        dyna_flow_type_list: List[DynaFlowTypeBusObj]
    ) -> bool:

        task_ownership = True

        async for session in get_db():

            session_context = SessionContext(dict(), session)

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
                        if x.code == dyna_flow.dyna_flow_type_id
                    ),
                    None
                )

                assert dyna_flow_type is not None
                
                dyna_flow.priority_level = \
                    dyna_flow_type.priority_level

                await dyna_flow.save()

                await session.commit()
            except Exception:
                await session.rollback()
                task_ownership = False
            finally:
                await session.close()

        return task_ownership

    async def get_task_run_todo_list(
        self
    ) -> List[ReportItemPacConfigDynaFlowTaskRunToDoList]:

        run_to_do_list = list()

        async for session in get_db():

            session_context = SessionContext(dict(), session)

            try:

                pac = PacBusObj(session_context)

                await pac.load_from_enum(
                    pac_enum=managers_and_enums.PacEnum.UNKNOWN)

                report_manager = \
                    ReportManagerPacConfigDynaFlowTaskRunToDoList(
                        session_context
                    )

                tri_state_no = TriStateFilterBusObj(session_context)
                await tri_state_no.load_from_enum(
                    tri_state_filter_enum=managers_and_enums.TriStateFilterEnum.NO
                )

                run_to_do_list = await report_manager.generate(
                    pac.code,
                    order_by_column_name="DynaFlowPriorityLevel",
                    order_by_descending=True,
                    is_run_task_debug_required_tri_state_filter_code==tri_state_no.code,
                    item_count_per_page=100
                )

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
    
    
    async def get_dyna_flow_task_json(
        self,
        dyna_flow_task_code: uuid.UUID
    ) -> str:
        
        json = ""
        async for session in get_db():

            session_context = SessionContext(dict(), session)

            try:

                dyna_flow_task = DynaFlowTaskBusObj(session_context)

                await dyna_flow_task.load_from_code(dyna_flow_task_code)

                json = dyna_flow_task.to_json()

                await session.commit()
            except Exception:
                await session.rollback()
                task_ownership = False
            finally:
                await session.close()

        return json

    async def serve_dyna_flow_task(
        self,
        dyna_flow_task_code: uuid.UUID,
        dyna_flow_task_type_list: List[DynaFlowTaskTypeBusObj]
    ):
        if self._is_task_queue_used is not True:
            return
        
        task_ownership = self.claim_dyna_flow_task_for_task_run(
            dyna_flow_task_code,
            dyna_flow_task_type_list
        )

        if task_ownership is not True:
            return

        print(f"Sending Queue Message dft {str(dyna_flow_task_code)}")

        json = self.get_dyna_flow_task_json(dyna_flow_task_code)

        await self.send_message_async(
            self._task_processor_queue_name,
            json)
        
    async def serve_dyna_flow_tasks(self):

        if self._is_task_queue_used is not True:
            return

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
            await self.serve_dyna_flow_task(
                item.dyna_flow_task_code,
                dyna_flow_task_type_list)

        return run_to_do_count
        
    async def run_dyna_flow_db_tasks(self):
        
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
        
        print("Checking for message...")

        assert self._service_bus_client is not None

        receiver = self._service_bus_client.get_queue_receiver(
            self._task_processor_queue_name
        )

        while True:
            messages = receiver.receive_messages(
                max_message_count=1,
                max_wait_time=5
            )
            if not messages:
                break
            message = messages[0]
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
            receiver.complete_message(message)

    async def run_dyna_flow_task(
            self,
            dyna_flow_task_code: uuid.UUID):
        
        success = False
        
        async for session in get_db():

            session_context = SessionContext(dict(), session)

            try:

                dyna_flow_task = DynaFlowTaskBusObj(session_context)

                await dyna_flow_task.load_from_code(dyna_flow_task_code)

                self._custom_temp_folder.clear_temp_folder()
                # TODO run tasks

                await session.commit()

                success = True

            except Exception:
                await session.rollback()
                task_ownership = False
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
                            print(str(ex))
                            print("Max Retry count completed. Not Successful.")
                        dyna_flow_task.is_completed = True
                        dyna_flow_task.is_successful = False
                        dyna_flow_task.completed_utc_date_time = datetime.utcnow()
                    else:
                        dyna_flow_task.retry_count +=1
                        dyna_flow_task.min_start_utc_date_time = \
                            datetime.utcnow() + timedelta(minutes=3)
                        dyna_flow_task.is_started = False
                        dyna_flow_task.is_completed = False
                        print(f"Request Retry Attempt "
                              f"{str(dyna_flow_task.retry_count)}")
                    await dyna_flow_task.save()

                    await session.commit()
                except Exception:
                    await session.rollback()
                    task_ownership = False
                finally:
                    await session.close()
                
        if self._is_task_queue_used:
            
            print(f"sending to result queue dft "
                  f"{str(dyna_flow_task.code)}")
            
            await self.send_message_async(
                self._task_result_queue_name,
                dyna_flow_task.to_json())
            

async def init_db():
    # Create the database tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async for session in get_db():
        session_context = SessionContext(dict(), session)
        await current_runtime.initialize(session_context)
        await session.commit()
        break


async def main():

    # Initialize the database
    await init_db()

    processor = DynaFlowProcessor()
    await processor.run()


if __name__ == '__main__':
    asyncio.run(main())
