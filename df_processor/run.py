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
from datetime import datetime, timedelta
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
from business import PacBusObj
from reports import (
    ReportManagerLandPlantList,
    ReportItemLandPlantList
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

        await self.init_app_async()

        async for session in get_db():

            session_context = SessionContext(dict(), session)

            try:

                pac = PacBusObj(session_context)
                
                await pac.load_from_enum(
                    pac_enum=managers_and_enums.PacEnum.UNKNOWN)
                
                dyna_flow_task_type_list = \
                    await pac.get_all_dyna_flow_task_type()
                
                dyna_flow_type_list = \
                    await pac.get_all_dyna_flow_type()

                await session.commit()

            except Exception as e:
                await session.rollback()
                print(f'Error occurred: {e}')
            finally:
                await session.close()

            build_to_do_count = 0
            run_to_do_count = 0
            result_message_count = 0

            self._custom_temp_folder.clear_temp_folder()

            # dyna_flow_task_type_list = self.  # await self.get_dyna_flow_task_type_list_async(session_context)
            # dyna_flow_type_list = List()  # await self.get_dyna_flow_type_list_async(session_context)

            await self.log_async(
                session_context,
                f"GetInstanceID() : {self.get_instance_id()}")

        # await self.request_scheduled_dyna_flows(session_context, pac)

        # local_run_loop = read_application_setting("localRunLoop", "false")

        # if not self._is_task_queue_used:
        #     await self.cleanup_my_past_dyna_flow_tasks(session_context, pac)
        # else:
        #     if self._is_task_processor:
        #         await self.cleanup_my_past_dyna_flow_tasks(session_context, pac)
        # if self._is_task_master:
        #     await self.cleanup_old_dyna_flow_tasks(session_context, pac)

        # while run_to_do_count > 0 or build_to_do_count > 0 or local_run_loop == "true":
        #     if self._is_task_master:
        #         result_message_count = await self.process_dyna_flow_queue_task_results(session_context)
        #         build_to_do_count = await self.build_dyna_flow_tasks(session_context, pac, dyna_flow_type_list)
        #         if self._is_task_queue_used:
        #             run_to_do_count = await self.run_dyna_flow_tasks(session_context, pac, dyna_flow_task_type_list)
        #             result_message_count = await self.process_dyna_flow_queue_task_results(session_context)

        #     if self._is_task_processor:
        #         if not self._is_task_queue_used:
        #             run_to_do_count = await self.run_dyna_flow_tasks(session_context, pac, dyna_flow_task_type_list)
        #         else:
        #             await self.run_dyna_flow_queue_tasks(session_context, pac, dyna_flow_task_type_list)

        #     if local_run_loop == "true" and run_to_do_count == 0 and build_to_do_count == 0 and result_message_count == 0:
        #         print("Sleeping...")
        #         await asyncio.sleep(15)
 


    async def init_app_async(self):
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

    async def log_async(
            self,
            session_context: SessionContext,
            message: str):
        print(message)

    def get_instance_id(self):
        return self._explicit_instance_id

    # async def cleanup_my_past_dyna_flow_tasks(self, session_context, pac):
    #     past_task_list = await self.generate_dyna_flow_task_search(session_context, pac)
    #     past_task_list = [x for x in past_task_list if x['ProcessorIdentifier'] == self.get_instance_id()]

    #     if past_task_list:
    #         print("cleanup past dataflow task items")
    #         past_task = past_task_list[0]
    #         if not past_task['IsSuccessful'] and not past_task['IsCompleted']:
    #             past_task['IsStarted'] = False
    #             past_task['IsCompleted'] = False
    #             past_task['ProcessorIdentifier'] = ''
    #             await self.save_dyna_flow_task(past_task)

    # async def generate_dyna_flow_task_search(self, session_context, pac):
    #     # Placeholder for actual search generation logic
    #     return []

    # async def save_dyna_flow_task(self, task):
    #     # Placeholder for actual save logic
    #     pass

    # async def cleanup_old_dyna_flow_tasks(self, session_context, pac):
    #     past_task_list = await self.generate_dyna_flow_task_search(session_context, pac)
    #     # Placeholder for actual cleanup logic

    # async def process_dyna_flow_queue_task_results(self, session_context):
    #     message_count = 0
    #     async with self.service_bus_client.get_queue_receiver(self._task_result_queue_name) as receiver:
    #         while True:
    #             messages = await receiver.receive_messages(max_message_count=1, max_wait_time=5)
    #             if not messages:
    #                 break
    #             message = messages[0]
    #             message_count += 1
    #             await self.log_async(session_context, "Message found...")
    #             try:
    #                 dyna_flow_task = self.create_dyna_flow_task_from_message(message)
    #                 await self.save_dyna_flow_task(dyna_flow_task)
    #             except Exception as ex:
    #                 await self.log_async(session_context, "Error reading message")
    #                 await self.send_message_async(self._task_dead_queue_name, message)
    #                 await self.log_async(session_context, str(ex))
    #             await receiver.complete_message(message)
    #     return message_count

    # def create_dyna_flow_task_from_message(self, message):
    #     # Placeholder for actual task creation logic
    #     return {}

    # async def send_message_async(self, queue_name, message):
    #     async with self.service_bus_client.get_queue_sender(queue_name) as sender:
    #         await sender.send_messages(ServiceBusMessage(message))

    # async def run_dyna_flow_queue_tasks(self, session_context, pac, dyna_flow_task_type_list):
    #     async with self.service_bus_client.get_queue_receiver(self._task_processor_queue_name) as receiver:
    #         while True:
    #             messages = await receiver.receive_messages(max_message_count=1, max_wait_time=60)
    #             if not messages:
    #                 break
    #             message = messages[0]
    #             await self.log_async(session_context, "Message found...")
    #             try:
    #                 dyna_flow_task = self.create_dyna_flow_task_from_message(message)
    #                 dyna_flow_task['ProcessorIdentifier'] = self.get_instance_id()
    #                 await self.save_dyna_flow_task(dyna_flow_task)
    #                 await self.run_dyna_flow_task_async(session_context, pac, dyna_flow_task_type_list, dyna_flow_task)
    #             except Exception as ex:
    #                 await self.log_async(session_context, "Error reading message")
    #                 await self.send_message_async(self._task_dead_queue_name, message)
    #                 await self.log_async(session_context, str(ex))
    #             await receiver.complete_message(message)

    # async def run_dyna_flow_tasks(self, session_context, pac, dyna_flow_task_type_list):
    #     run_to_do_list = await self.generate_dyna_flow_task_run_to_do_list(session_context, pac)
    #     run_to_do_count = len(run_to_do_list)

    #     await self.log_async(session_context, f"Found {run_to_do_count} DynaFlowTasks that need to be run")

    #     for i, run_to_do in enumerate(run_to_do_list):
    #         await self.log_async(session_context, f"Checking DynaFlowTask #{i + 1} of {run_to_do_count} : {run_to_do['DynaFlowTaskCode']}")
    #         dyna_flow_task = await self.get_dyna_flow_task_async(session_context, run_to_do['DynaFlowTaskCode'])

    #         if dyna_flow_task['IsStarted']:
    #             await self.log_async(session_context, f"DynaFlowTask already started : {run_to_do['DynaFlowTaskCode']}")
    #             continue

    #         task_ownership = True
    #         try:
    #             await self.log_async(session_context, f"Claiming DynaFlowTask #{i + 1} of {run_to_do_count} : {run_to_do['DynaFlowTaskCode']}")
    #             dyna_flow_task['IsStarted'] = True
    #             dyna_flow_task['StartedUTCDateTime'] = datetime.utcnow()
    #             dyna_flow_task['ProcessorIdentifier'] = self.get_instance_id()
    #             dyna_flow_task['MaxRetryCount'] = next(x['MaxRetryCount'] for x in dyna_flow_task_type_list if x['DynaFlowTaskTypeID'] == dyna_flow_task['DynaFlowTaskTypeID'])
    #             await self.save_dyna_flow_task(dyna_flow_task)
    #         except Exception as ex:
    #             await self.log_async(session_context, f"Error Claiming DynaFlowTask #{i + 1} of {run_to_do_count} : {run_to_do['DynaFlowTaskCode']}")
    #             task_ownership = False
    #             await self.log_async(session_context, str(ex))

    #         if not task_ownership:
    #             continue

    #         if self._is_task_queue_used:
    #             await self.log_async(session_context, f"Sending Queue Message dft {dyna_flow_task['Code']}")
    #             await self.send_message_async(self._task_processor_queue_name, dyna_flow_task)
    #         else:
    #             await self.run_dyna_flow_task_async(session_context, pac, dyna_flow_task_type_list, dyna_flow_task)

    #     return run_to_do_count

    # async def generate_dyna_flow_task_run_to_do_list(self, session_context, pac):
    #     # Placeholder for actual to-do list generation logic
    #     return []

    # async def get_dyna_flow_task_async(self, session_context, task_code):
    #     # Placeholder for actual task retrieval logic
    #     return {}

    # async def run_dyna_flow_task_async(self, session_context, pac, dyna_flow_task_type_list, claimed_dyna_flow_task):
    #     run_session_context = self.create_session_context(True)
    #     run_session_context['session_code'] = session_context['session_code']
    #     try:
    #         await self.remove_temp_files_async(session_context)
    #         dyna_flow_task = await self.get_dyna_flow_task_async(run_session_context, claimed_dyna_flow_task['Code'])
    #         dyna_flow_task_type = next(x for x in dyna_flow_task_type_list if x['DynaFlowTaskTypeID'] == dyna_flow_task['DynaFlowTaskTypeID'])

    #         if self._force_task_error:
    #             raise Exception("forced error")

    #         print(f"run dataflow task {dyna_flow_task_type['LookupEnumName']}")
    #         await self.run_task(dyna_flow_task)
    #         run_session_context['commit']()
    #     except Exception as ex:
    #         await self.log_async(session_context, str(ex))
    #         run_session_context['rollback']()

    #         dyna_flow_task = await self.get_dyna_flow_task_async(session_context, claimed_dyna_flow_task['Code'])
    #         if dyna_flow_task['RetryCount'] >= dyna_flow_task['MaxRetryCount']:
    #             if dyna_flow_task['MaxRetryCount'] > 0:
    #                 await self.log_async(session_context, str(ex))
    #                 await self.log_async(session_context, "Max Retry count completed. Not Successful.")
    #             dyna_flow_task['IsCompleted'] = True
    #             dyna_flow_task['IsSuccessful'] = False
    #             dyna_flow_task['CompletedUTCDateTime'] = datetime.utcnow()
    #         else:
    #             dyna_flow_task['RetryCount'] += 1
    #             dyna_flow_task['MinStartUTCDateTime'] = datetime.utcnow() + timedelta(minutes=3)
    #             dyna_flow_task['IsStarted'] = False
    #             dyna_flow_task['IsCompleted'] = False
    #             await self.log_async(session_context, f"Request Retry Attempt {dyna_flow_task['RetryCount']}")
    #         await self.save_dyna_flow_task(dyna_flow_task)

    #     if self._is_task_queue_used:
    #         await self.log_async(session_context, f"sending to result queue dft {dyna_flow_task['Code']}")
    #         await self.send_message_async(self._task_result_queue_name, dyna_flow_task)

    # async def run_task(self, dyna_flow_task):
    #     # Placeholder for actual task run logic
    #     pass

    # async def build_dyna_flow_tasks(self, session_context, pac, dyna_flow_type_list):
    #     build_to_do_list = await self.generate_dyna_flow_dft_build_to_do_list(session_context, pac)
    #     build_to_do_count = len(build_to_do_list)

    #     await self.log_async(session_context, f"Found {build_to_do_count} DynaFlows that need tasks built")
    #     for i, build_to_do in enumerate(build_to_do_list):
    #         dyna_flow = await self.get_dyna_flow_async(session_context, build_to_do['DynaFlowCode'])

    #         if dyna_flow['IsTaskCreationStarted']:
    #             continue

    #         task_ownership = True
    #         try:
    #             dyna_flow['IsTaskCreationStarted'] = True
    #             dyna_flow['TaskCreationProcessorIdentifier'] = self.get_instance_id()
    #             dyna_flow['PriorityLevel'] = next(x['PriorityLevel'] for x in dyna_flow_type_list if x['DynaFlowTypeID'] == dyna_flow['DynaFlowTypeID'])
    #             await self.save_dyna_flow(dyna_flow)
    #         except Exception:
    #             task_ownership = False

    #         if not task_ownership:
    #             continue

    #         await self.log_async(session_context, f"Building tasks for DynaFlow {build_to_do['DynaFlowCode']}")
    #         build_session_context = self.create_session_context(True)
    #         build_session_context['session_code'] = session_context['session_code']
    #         try:
    #             dyna_flow = await self.get_dyna_flow_async(build_session_context, build_to_do['DynaFlowCode'])
    #             print(f"build dataflow task...{next(x['LookupEnumName'] for x in dyna_flow_type_list if x['DynaFlowTypeID'] == dyna_flow['DynaFlowTypeID'])}")
    #             await self.build_tasks(dyna_flow)
    #             build_session_context['commit']()
    #         except Exception as ex:
    #             await self.log_async(session_context, str(ex))
    #             build_session_context['rollback']()
    #             dyna_flow = await self.get_dyna_flow_async(session_context, build_to_do['DynaFlowCode'])
    #             dyna_flow['IsCompleted'] = True
    #             dyna_flow['IsSuccessful'] = False
    #             dyna_flow['CompletedUTCDateTime'] = datetime.utcnow()
    #             await self.save_dyna_flow(dyna_flow)

    #     return build_to_do_count

    # async def generate_dyna_flow_dft_build_to_do_list(self, session_context, pac):
    #     # Placeholder for actual to-do list generation logic
    #     return []

    # async def get_dyna_flow_async(self, session_context, dyna_flow_code):
    #     # Placeholder for actual dyna flow retrieval logic
    #     return {}

    # async def save_dyna_flow(self, dyna_flow):
    #     # Placeholder for actual save logic
    #     pass

    # async def build_tasks(self, dyna_flow):
    #     # Placeholder for actual task building logic
    #     pass

    # async def request_scheduled_dyna_flows(self, session_context, pac):
    #     dFMaintenance = await self.get_dFMaintenance(session_context, pac)

    #     if dFMaintenance['IsPaused']:
    #         await asyncio.sleep(10)
    #         return

    #     await dFMaintenance['refresh']()
    #     if dFMaintenance['NextScheduledDFProcessRequestUTCDateTime'] < datetime.utcnow() and (
    #             not dFMaintenance['IsScheduledDFProcessRequestStarted'] or
    #             dFMaintenance['NextScheduledDFProcessRequestUTCDateTime'] < datetime.utcnow() - timedelta(days=1)):
    #         print("request any scheduled dataflows")
    #         task_ownership = True
    #         try:
    #             dFMaintenance['IsScheduledDFProcessRequestStarted'] = True
    #             dFMaintenance['IsScheduledDFProcessRequestCompleted'] = True
    #             dFMaintenance['ScheduledDFProcessRequestProcessorIdentifier'] = self.get_instance_id()
    #             await self.save_dFMaintenance(dFMaintenance)
    #         except Exception:
    #             task_ownership = False

    #         if task_ownership:
    #             await pac['PacProcessAllDynaFlowTypeScheduleFlow_ViaDynaFlow']("Process all scheduled data flows")

    #             rebuild_items = await self.generate_dyna_flow_retry_task_build_list(session_context, pac)
    #             for item in rebuild_items:
    #                 dyna_flow = await self.get_dyna_flow_async(session_context, item['DynaFlowCode'])
    #                 dyna_flow['IsTaskCreationStarted'] = False
    #                 dyna_flow['TaskCreationProcessorIdentifier'] = ''
    #                 dyna_flow['IsStarted'] = False
    #                 await self.save_dyna_flow(dyna_flow)

    #             rerun_items = await self.generate_dyna_flow_task_retry_run_list(session_context, pac)
    #             for item in rerun_items:
    #                 dyna_flow_task = await self.get_dyna_flow_task_async(session_context, item['DynaFlowTaskCode'])
    #                 dyna_flow_task['ProcessorIdentifier'] = ''
    #                 dyna_flow_task['IsStarted'] = False
    #                 await self.save_dyna_flow_task(dyna_flow_task)

    #             dFMaintenance['IsScheduledDFProcessRequestCompleted'] = True
    #             dFMaintenance['IsScheduledDFProcessRequestStarted'] = False
    #             dFMaintenance['LastScheduledDFProcessRequestUTCDateTime'] = datetime.utcnow()
    #             dFMaintenance['NextScheduledDFProcessRequestUTCDateTime'] = datetime.utcnow() + timedelta(minutes=30)
    #             await self.save_dFMaintenance(dFMaintenance)

    # async def get_dFMaintenance(self, session_context, pac):
    #     # Placeholder for actual retrieval logic
    #     return {}

    # async def save_dFMaintenance(self, dFMaintenance):
    #     # Placeholder for actual save logic
    #     pass

    # async def generate_dyna_flow_retry_task_build_list(self, session_context, pac):
    #     # Placeholder for actual to-do list generation logic
    #     return []

    # async def generate_dyna_flow_task_retry_run_list(self, session_context, pac):
    #     # Placeholder for actual to-do list generation logic
    #     return []

    # def create_session_context(self, use_transaction):
    #     # Placeholder for actual session context creation logic
    #     return {}


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
