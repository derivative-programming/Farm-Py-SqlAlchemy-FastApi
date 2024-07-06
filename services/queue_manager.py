# services/queue_manager.py  # pylint: disable=duplicate-code
"""
This module contains the QueueManager class which is
responsible for managing the Azure Service Bus queue.
"""

from config import (
    AZURE_SERVICE_BUS_CONNECTION_STRING
)
from azure.servicebus import ServiceBusClient, ServiceBusMessage


class QueueManager:
    """
    The QueueManager class is responsible for managing
    the Azure Service Bus queue.
    """

    def __init__(self):
        """
        Initialize the QueueManager class.
        """
        self._service_bus_client = None
        self._service_bus_client = ServiceBusClient.from_connection_string(
            AZURE_SERVICE_BUS_CONNECTION_STRING)

        if len(AZURE_SERVICE_BUS_CONNECTION_STRING) == 0:
            raise ValueError("Azure Service Bus connection string is not set.")

    async def get_message_count_async(self, queue_name) -> int:
        """
        Get the count of messages in a queue.
        """
        assert self._service_bus_client is not None

        receiver = self._service_bus_client.get_queue_receiver(queue_name)

        count = len(receiver.peek_messages(max_message_count=32))

        return count

    async def read_next_message(self, queue_name) -> str:
        """
        Read the next message from the queue.
        """

        result = ""

        assert self._service_bus_client is not None

        receiver = self._service_bus_client.get_queue_receiver(
            queue_name
        )

        messages = receiver.receive_messages(
            max_message_count=1,
            max_wait_time=5
        )
        if messages:
            result = str(messages[0])

        return result

    async def mark_message_as_completed(self, queue_name, message):
        """
        Mark a message as completed.
        """

        assert self._service_bus_client is not None

        receiver = self._service_bus_client.get_queue_receiver(
            queue_name
        )

        receiver.complete_message(message)

    async def send_message_async(self, queue_name, message):
        """
        Send a message to a queue.
        """

        assert self._service_bus_client is not None

        sender = self._service_bus_client.get_queue_sender(
            queue_name
        )

        sender.send_messages(ServiceBusMessage(message))
