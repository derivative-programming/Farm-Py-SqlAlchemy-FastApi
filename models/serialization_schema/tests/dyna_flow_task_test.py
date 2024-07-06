# models/serialization_schema/tests/dyna_flow_task_test.py  # pylint: disable=duplicate-code
# pylint: disable=redefined-outer-name, too-many-public-methods
# pylint: disable=unused-import

"""
This module contains tests for the
DynaFlowTask serialization schema.

The DynaFlowTask serialization schema
is responsible for serializing and deserializing
DynaFlowTask instances. It ensures that the
data is properly formatted and can be
stored or retrieved from a database or
transmitted over a network.

The tests in this module cover the serialization
and deserialization of DynaFlowTask
instances using the DynaFlowTaskSchema
class. They verify
that the serialized data
matches the expected format and that the
deserialized data can be used to
reconstruct a DynaFlowTask instance.

The DynaFlowTaskSchema class
is used to define
the serialization and deserialization
rules for DynaFlowTask instances. It
specifies how each attribute of a
DynaFlowTask instance
should be converted to a serialized
format and how the serialized data should
be converted back to a DynaFlowTask
instance.

The tests in this module use the pytest
framework to define test cases and
assertions. They ensure that the serialization
and deserialization process
works correctly and produces the expected results.

"""

import json
import logging
from datetime import datetime  # noqa: F401
from decimal import Decimal  # noqa: F401

import pytz

import pytest
from models import DynaFlowTask
from models.factory import DynaFlowTaskFactory
from models.serialization_schema import DynaFlowTaskSchema
from services.logging_config import get_logger

logger = get_logger(__name__)


@pytest.fixture(scope="function")
def new_obj(
    session
) -> DynaFlowTask:
    """
    Fixture to create and return a DynaFlowTask
    instance using the
    DynaFlowTaskFactory.

    Args:
        session: The database session.

    Returns:
        DynaFlowTask: A newly created
            DynaFlowTask instance.
    """

    return DynaFlowTaskFactory.create(session=session)


class TestDynaFlowTaskSchema:
    """
    Tests for the DynaFlowTask
    serialization schema.
    """

    # Sample data for a DynaFlowTask
    # instance
    sample_data = {
        "dyna_flow_task_id": 1,
        "code":
            "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
        "last_change_code": 0,
        "insert_user_id":
            "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
        "last_update_user_id":
            "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
# endset  # noqa: E122
        "completed_utc_date_time": datetime(
            2023, 1, 1, 12, 0, 0, tzinfo=pytz.utc
        ).isoformat(),
        "dependency_dyna_flow_task_id": 42,
        "description": "Vanilla",
        "dyna_flow_id": 2,
        "dyna_flow_subject_code":
            "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
        "dyna_flow_task_type_id": 1,
        "is_canceled": False,
        "is_cancel_requested": False,
        "is_completed": False,
        "is_parallel_run_allowed": False,
        "is_run_task_debug_required": False,
        "is_started": False,
        "is_successful": False,
        "max_retry_count": 42,
        "min_start_utc_date_time": datetime(
            2023, 1, 1, 12, 0, 0, tzinfo=pytz.utc
        ).isoformat(),
        "param_1": "Vanilla",
        "param_2": "Vanilla",
        "processor_identifier": "Vanilla",
        "requested_utc_date_time": datetime(
            2023, 1, 1, 12, 0, 0, tzinfo=pytz.utc
        ).isoformat(),
        "result_value": "Vanilla",
        "retry_count": 42,
        "started_utc_date_time": datetime(
            2023, 1, 1, 12, 0, 0, tzinfo=pytz.utc
        ).isoformat(),
        "insert_utc_date_time": datetime(
            2024, 1, 1, 12, 0, 0, tzinfo=pytz.utc
        ).isoformat(),
        "last_update_utc_date_time": datetime(
            2025, 1, 1, 12, 0, 0, tzinfo=pytz.utc
        ).isoformat(),
# endset  # noqa: E122
        "dyna_flow_code_peek":  # DynaFlowID
            "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
        "dyna_flow_task_type_code_peek":  # DynaFlowTaskTypeID
            "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
# endset  # noqa: E122
    }

    def test_dyna_flow_task_serialization(
        self,
        new_obj: DynaFlowTask
    ):
        """
        Test the serialization of a
        DynaFlowTask instance using
        DynaFlowTaskSchema.

        Args:
            dyna_flow_task (DynaFlowTask):
                A DynaFlowTask instance to serialize.
        """

        schema = DynaFlowTaskSchema()
        dyna_flow_task_data = schema.dump(new_obj)

        assert isinstance(dyna_flow_task_data, dict)

        result = dyna_flow_task_data

        assert result['code'] == str(new_obj.code)
        assert result['last_change_code'] == (
            new_obj.last_change_code)
        assert result['insert_user_id'] == (
            str(new_obj.insert_user_id))
        assert result['last_update_user_id'] == (
            str(new_obj.last_update_user_id))

        assert result['completed_utc_date_time'] == (
            new_obj.completed_utc_date_time.isoformat())
        assert result['dependency_dyna_flow_task_id'] == (
            new_obj.dependency_dyna_flow_task_id)
        assert result['description'] == (
            new_obj.description)
        assert result['dyna_flow_id'] == (
            new_obj.dyna_flow_id)
        assert result['dyna_flow_subject_code'] == (
            str(new_obj.dyna_flow_subject_code))
        assert result['dyna_flow_task_type_id'] == (
            new_obj.dyna_flow_task_type_id)
        assert result['is_canceled'] == (
            new_obj.is_canceled)
        assert result['is_cancel_requested'] == (
            new_obj.is_cancel_requested)
        assert result['is_completed'] == (
            new_obj.is_completed)
        assert result['is_parallel_run_allowed'] == (
            new_obj.is_parallel_run_allowed)
        assert result['is_run_task_debug_required'] == (
            new_obj.is_run_task_debug_required)
        assert result['is_started'] == (
            new_obj.is_started)
        assert result['is_successful'] == (
            new_obj.is_successful)
        assert result['max_retry_count'] == (
            new_obj.max_retry_count)
        assert result['min_start_utc_date_time'] == (
            new_obj.min_start_utc_date_time.isoformat())
        assert result['param_1'] == (
            new_obj.param_1)
        assert result['param_2'] == (
            new_obj.param_2)
        assert result['processor_identifier'] == (
            new_obj.processor_identifier)
        assert result['requested_utc_date_time'] == (
            new_obj.requested_utc_date_time.isoformat())
        assert result['result_value'] == (
            new_obj.result_value)
        assert result['retry_count'] == (
            new_obj.retry_count)
        assert result['started_utc_date_time'] == (
            new_obj.started_utc_date_time.isoformat())
        assert result['insert_utc_date_time'] == (
            new_obj.insert_utc_date_time.isoformat())
        assert result['last_update_utc_date_time'] == (
            new_obj.last_update_utc_date_time.isoformat())
        assert result['dyna_flow_code_peek'] == (  # DynaFlowID
            str(new_obj.dyna_flow_code_peek))
        assert result['dyna_flow_task_type_code_peek'] == (  # DynaFlowTaskTypeID
            str(new_obj.dyna_flow_task_type_code_peek))

    def test_dyna_flow_task_deserialization(
        self,
        new_obj: DynaFlowTask
    ):
        """
        Test the deserialization of a
        DynaFlowTask object using the
        DynaFlowTaskSchema.

        Args:
            dyna_flow_task (DynaFlowTask): The
                DynaFlowTask object to be deserialized.

        Raises:
            AssertionError: If any of the assertions fail.

        Returns:
            None
        """

        schema = DynaFlowTaskSchema()
        serialized_data = schema.dump(new_obj)
        deserialized_data = schema.load(serialized_data)

        assert deserialized_data['code'] == \
            new_obj.code
        assert deserialized_data['last_change_code'] == (
            new_obj.last_change_code)
        assert deserialized_data['insert_user_id'] == (
            new_obj.insert_user_id)
        assert deserialized_data['last_update_user_id'] == (
            new_obj.last_update_user_id)
        assert deserialized_data['completed_utc_date_time'].isoformat() == (
            new_obj.completed_utc_date_time.isoformat())
        assert deserialized_data['dependency_dyna_flow_task_id'] == (
            new_obj.dependency_dyna_flow_task_id)
        assert deserialized_data['description'] == (
            new_obj.description)
        assert deserialized_data['dyna_flow_id'] == (
            new_obj.dyna_flow_id)
        assert deserialized_data['dyna_flow_subject_code'] == (
            new_obj.dyna_flow_subject_code)
        assert deserialized_data['dyna_flow_task_type_id'] == (
            new_obj.dyna_flow_task_type_id)
        assert deserialized_data['is_canceled'] == (
            new_obj.is_canceled)
        assert deserialized_data['is_cancel_requested'] == (
            new_obj.is_cancel_requested)
        assert deserialized_data['is_completed'] == (
            new_obj.is_completed)
        assert deserialized_data['is_parallel_run_allowed'] == (
            new_obj.is_parallel_run_allowed)
        assert deserialized_data['is_run_task_debug_required'] == (
            new_obj.is_run_task_debug_required)
        assert deserialized_data['is_started'] == (
            new_obj.is_started)
        assert deserialized_data['is_successful'] == (
            new_obj.is_successful)
        assert deserialized_data['max_retry_count'] == (
            new_obj.max_retry_count)
        assert deserialized_data['min_start_utc_date_time'].isoformat() == (
            new_obj.min_start_utc_date_time.isoformat())
        assert deserialized_data['param_1'] == (
            new_obj.param_1)
        assert deserialized_data['param_2'] == (
            new_obj.param_2)
        assert deserialized_data['processor_identifier'] == (
            new_obj.processor_identifier)
        assert deserialized_data['requested_utc_date_time'].isoformat() == (
            new_obj.requested_utc_date_time.isoformat())
        assert deserialized_data['result_value'] == (
            new_obj.result_value)
        assert deserialized_data['retry_count'] == (
            new_obj.retry_count)
        assert deserialized_data['started_utc_date_time'].isoformat() == (
            new_obj.started_utc_date_time.isoformat())
        assert deserialized_data['insert_utc_date_time'].isoformat() == (
            new_obj.insert_utc_date_time.isoformat())
        assert deserialized_data['last_update_utc_date_time'].isoformat() == (
            new_obj.last_update_utc_date_time.isoformat())
        assert deserialized_data[(  # DynaFlowID
            'dyna_flow_code_peek')] == (
            new_obj.dyna_flow_code_peek)
        assert deserialized_data[(  # DynaFlowTaskTypeID
            'dyna_flow_task_type_code_peek')] == (
            new_obj.dyna_flow_task_type_code_peek)

        obj_from_dict = DynaFlowTask(
            **deserialized_data)

        assert isinstance(new_obj,
                          DynaFlowTask)

        # Now compare the new_obj attributes with
        # the dyna_flow_task attributes
        assert obj_from_dict.code == \
            new_obj.code
        assert obj_from_dict.last_change_code == \
            new_obj.last_change_code
        assert obj_from_dict.insert_user_id == \
            new_obj.insert_user_id
        assert obj_from_dict.last_update_user_id == \
            new_obj.last_update_user_id
        assert obj_from_dict.completed_utc_date_time.isoformat() == (
            new_obj.completed_utc_date_time.isoformat())
        assert obj_from_dict.dependency_dyna_flow_task_id == (
            new_obj.dependency_dyna_flow_task_id)
        assert obj_from_dict.description == (
            new_obj.description)
        assert obj_from_dict.dyna_flow_id == (
            new_obj.dyna_flow_id)
        assert obj_from_dict.dyna_flow_subject_code == (
            new_obj.dyna_flow_subject_code)
        assert obj_from_dict.dyna_flow_task_type_id == (
            new_obj.dyna_flow_task_type_id)
        assert obj_from_dict.is_canceled == (
            new_obj.is_canceled)
        assert obj_from_dict.is_cancel_requested == (
            new_obj.is_cancel_requested)
        assert obj_from_dict.is_completed == (
            new_obj.is_completed)
        assert obj_from_dict.is_parallel_run_allowed == (
            new_obj.is_parallel_run_allowed)
        assert obj_from_dict.is_run_task_debug_required == (
            new_obj.is_run_task_debug_required)
        assert obj_from_dict.is_started == (
            new_obj.is_started)
        assert obj_from_dict.is_successful == (
            new_obj.is_successful)
        assert obj_from_dict.max_retry_count == (
            new_obj.max_retry_count)
        assert obj_from_dict.min_start_utc_date_time.isoformat() == (
            new_obj.min_start_utc_date_time.isoformat())
        assert obj_from_dict.param_1 == (
            new_obj.param_1)
        assert obj_from_dict.param_2 == (
            new_obj.param_2)
        assert obj_from_dict.processor_identifier == (
            new_obj.processor_identifier)
        assert obj_from_dict.requested_utc_date_time.isoformat() == (
            new_obj.requested_utc_date_time.isoformat())
        assert obj_from_dict.result_value == (
            new_obj.result_value)
        assert obj_from_dict.retry_count == (
            new_obj.retry_count)
        assert obj_from_dict.started_utc_date_time.isoformat() == (
            new_obj.started_utc_date_time.isoformat())

        assert obj_from_dict.insert_utc_date_time.isoformat() == (
            new_obj.insert_utc_date_time.isoformat())
        assert obj_from_dict.last_update_utc_date_time.isoformat() == (
            new_obj.last_update_utc_date_time.isoformat())
        assert obj_from_dict.dyna_flow_code_peek == (  # DynaFlowID
            new_obj.dyna_flow_code_peek)
        assert obj_from_dict.dyna_flow_task_type_code_peek == (  # DynaFlowTaskTypeID
            new_obj.dyna_flow_task_type_code_peek)

    def test_from_json(self):
        """
        Test the `from_json` method of the DynaFlowTaskSchema class.

        This method tests the deserialization of
        a JSON string to a
        DynaFlowTask object.
        It converts the sample data to a JSON string,
        deserializes it to a dictionary,
        and then loads the dictionary to a DynaFlowTask
        object. Finally, it asserts the
        equality of the deserialized
        DynaFlowTask object
        with the sample data.

        Returns:
            None
        """

        dyna_flow_task_schema = DynaFlowTaskSchema()

        # Convert sample data to JSON string
        json_str = json.dumps(self.sample_data)

        # Deserialize the JSON string to a dictionary
        json_data = json.loads(json_str)

        # Load the dictionary to an object
        deserialized_data = dyna_flow_task_schema.load(json_data)

        assert str(deserialized_data['dyna_flow_task_id']) == (
            str(self.sample_data['dyna_flow_task_id']))
        assert str(deserialized_data['code']) == (
            str(self.sample_data['code']))
        assert str(deserialized_data['last_change_code']) == (
            str(self.sample_data['last_change_code']))
        assert str(deserialized_data['insert_user_id']) == (
            str(self.sample_data['insert_user_id']))
        assert str(deserialized_data['last_update_user_id']) == (
            str(self.sample_data['last_update_user_id']))
        assert deserialized_data['completed_utc_date_time'].isoformat() == (
            self.sample_data['completed_utc_date_time'])
        assert str(deserialized_data['dependency_dyna_flow_task_id']) == (
            str(self.sample_data['dependency_dyna_flow_task_id']))
        assert str(deserialized_data['description']) == (
            str(self.sample_data['description']))
        assert str(deserialized_data['dyna_flow_id']) == (
            str(self.sample_data['dyna_flow_id']))
        assert str(deserialized_data['dyna_flow_subject_code']) == (
            str(self.sample_data['dyna_flow_subject_code']))
        assert str(deserialized_data['dyna_flow_task_type_id']) == (
            str(self.sample_data['dyna_flow_task_type_id']))
        assert str(deserialized_data['is_canceled']) == (
            str(self.sample_data['is_canceled']))
        assert str(deserialized_data['is_cancel_requested']) == (
            str(self.sample_data['is_cancel_requested']))
        assert str(deserialized_data['is_completed']) == (
            str(self.sample_data['is_completed']))
        assert str(deserialized_data['is_parallel_run_allowed']) == (
            str(self.sample_data['is_parallel_run_allowed']))
        assert str(deserialized_data['is_run_task_debug_required']) == (
            str(self.sample_data['is_run_task_debug_required']))
        assert str(deserialized_data['is_started']) == (
            str(self.sample_data['is_started']))
        assert str(deserialized_data['is_successful']) == (
            str(self.sample_data['is_successful']))
        assert str(deserialized_data['max_retry_count']) == (
            str(self.sample_data['max_retry_count']))
        assert deserialized_data['min_start_utc_date_time'].isoformat() == (
            self.sample_data['min_start_utc_date_time'])
        assert str(deserialized_data['param_1']) == (
            str(self.sample_data['param_1']))
        assert str(deserialized_data['param_2']) == (
            str(self.sample_data['param_2']))
        assert str(deserialized_data['processor_identifier']) == (
            str(self.sample_data['processor_identifier']))
        assert deserialized_data['requested_utc_date_time'].isoformat() == (
            self.sample_data['requested_utc_date_time'])
        assert str(deserialized_data['result_value']) == (
            str(self.sample_data['result_value']))
        assert str(deserialized_data['retry_count']) == (
            str(self.sample_data['retry_count']))
        assert deserialized_data['started_utc_date_time'].isoformat() == (
            self.sample_data['started_utc_date_time'])
        assert deserialized_data['insert_utc_date_time'].isoformat() == (
            self.sample_data['insert_utc_date_time'])
        assert str(deserialized_data[(  # DynaFlowID
            'dyna_flow_code_peek')]) == (
            str(self.sample_data['dyna_flow_code_peek']))
        assert str(deserialized_data[(  # DynaFlowTaskTypeID
            'dyna_flow_task_type_code_peek')]) == (
            str(self.sample_data['dyna_flow_task_type_code_peek']))
        assert deserialized_data['last_update_utc_date_time'].isoformat() == (
            self.sample_data['last_update_utc_date_time'])

        new_dyna_flow_task = DynaFlowTask(
            **deserialized_data)

        assert isinstance(new_dyna_flow_task,
                          DynaFlowTask)

    def test_to_json(
        self,
        new_obj: DynaFlowTask
    ):
        """
        Test the conversion of a
        DynaFlowTask instance to JSON.

        Args:
            dyna_flow_task (DynaFlowTask): The
            DynaFlowTask instance to convert.

        Raises:
            AssertionError: If the conversion fails or the
            converted JSON does not match the expected values.
        """

        # Convert the DynaFlowTask instance
        # to JSON using the schema
        dyna_flow_task_schema = DynaFlowTaskSchema()
        dyna_flow_task_dict = dyna_flow_task_schema.dump(
            new_obj)

        # Convert the dyna_flow_task_dict to JSON string
        dyna_flow_task_json = json.dumps(
            dyna_flow_task_dict)

        # Convert the JSON strings back to dictionaries
        dict_from_json = json.loads(
            dyna_flow_task_json)
        # sample_dict_from_json = json.loads(self.sample_data)

        logging.info(
            "dict_from_json.keys() %s",
            dict_from_json.keys())

        logging.info("self.sample_data.keys() %s", self.sample_data.keys())

        # Verify the keys in both dictionaries match
        assert set(dict_from_json.keys()) == (
            set(self.sample_data.keys())), (
            f"Expected keys: {set(self.sample_data.keys())}, "
            f"Got: {set(dict_from_json.keys())}"
        )

        assert dict_from_json['code'] == \
            str(new_obj.code), (
            "failed on code"
        )
        assert dict_from_json['last_change_code'] == (
            new_obj.last_change_code), (
            "failed on last_change_code"
        )
        assert dict_from_json['insert_user_id'] == (
            str(new_obj.insert_user_id)), (
            "failed on insert_user_id"
        )
        assert dict_from_json['last_update_user_id'] == (
            str(new_obj.last_update_user_id)), (
            "failed on last_update_user_id"
        )
        assert dict_from_json['completed_utc_date_time'] == (
            new_obj.completed_utc_date_time.isoformat()), (
            "failed on completed_utc_date_time"
        )
        assert dict_from_json['dependency_dyna_flow_task_id'] == (
            new_obj.dependency_dyna_flow_task_id), (
            "failed on dependency_dyna_flow_task_id"
        )
        assert dict_from_json['description'] == (
            new_obj.description), (
            "failed on description"
        )
        assert dict_from_json['dyna_flow_id'] == (
            new_obj.dyna_flow_id), (
            "failed on dyna_flow_id"
        )
        assert dict_from_json['dyna_flow_subject_code'] == (
            str(new_obj.dyna_flow_subject_code)), (
            "failed on dyna_flow_subject_code"
        )
        assert dict_from_json['dyna_flow_task_type_id'] == (
            new_obj.dyna_flow_task_type_id), (
            "failed on dyna_flow_task_type_id"
        )
        assert dict_from_json['is_canceled'] == (
            new_obj.is_canceled), (
            "failed on is_canceled"
        )
        assert dict_from_json['is_cancel_requested'] == (
            new_obj.is_cancel_requested), (
            "failed on is_cancel_requested"
        )
        assert dict_from_json['is_completed'] == (
            new_obj.is_completed), (
            "failed on is_completed"
        )
        assert dict_from_json['is_parallel_run_allowed'] == (
            new_obj.is_parallel_run_allowed), (
            "failed on is_parallel_run_allowed"
        )
        assert dict_from_json['is_run_task_debug_required'] == (
            new_obj.is_run_task_debug_required), (
            "failed on is_run_task_debug_required"
        )
        assert dict_from_json['is_started'] == (
            new_obj.is_started), (
            "failed on is_started"
        )
        assert dict_from_json['is_successful'] == (
            new_obj.is_successful), (
            "failed on is_successful"
        )
        assert dict_from_json['max_retry_count'] == (
            new_obj.max_retry_count), (
            "failed on max_retry_count"
        )
        assert dict_from_json['min_start_utc_date_time'] == (
            new_obj.min_start_utc_date_time.isoformat()), (
            "failed on min_start_utc_date_time"
        )
        assert dict_from_json['param_1'] == (
            new_obj.param_1), (
            "failed on param_1"
        )
        assert dict_from_json['param_2'] == (
            new_obj.param_2), (
            "failed on param_2"
        )
        assert dict_from_json['processor_identifier'] == (
            new_obj.processor_identifier), (
            "failed on processor_identifier"
        )
        assert dict_from_json['requested_utc_date_time'] == (
            new_obj.requested_utc_date_time.isoformat()), (
            "failed on requested_utc_date_time"
        )
        assert dict_from_json['result_value'] == (
            new_obj.result_value), (
            "failed on result_value"
        )
        assert dict_from_json['retry_count'] == (
            new_obj.retry_count), (
            "failed on retry_count"
        )
        assert dict_from_json['started_utc_date_time'] == (
            new_obj.started_utc_date_time.isoformat()), (
            "failed on started_utc_date_time"
        )
        assert dict_from_json['insert_utc_date_time'] == (
            new_obj.insert_utc_date_time.isoformat()), (
            "failed on insert_utc_date_time"
        )
        assert dict_from_json['last_update_utc_date_time'] == (
            new_obj.last_update_utc_date_time.isoformat()), (
            "failed on last_update_utc_date_time"
        )
        assert dict_from_json[(  # DynaFlowID
            'dyna_flow_code_peek')] == (
            str(new_obj.dyna_flow_code_peek)), (
            "failed on dyna_flow_code_peek"
        )
        assert dict_from_json[(  # DynaFlowTaskTypeID
            'dyna_flow_task_type_code_peek')] == (
            str(new_obj.dyna_flow_task_type_code_peek)), (
            "failed on dyna_flow_task_type_code_peek"
        )
