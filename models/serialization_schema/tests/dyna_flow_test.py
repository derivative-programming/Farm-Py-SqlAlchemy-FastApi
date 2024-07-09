# models/serialization_schema/tests/dyna_flow_test.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=redefined-outer-name, too-many-public-methods
# pylint: disable=unused-import

"""
This module contains tests for the
DynaFlow serialization schema.

The DynaFlow serialization schema
is responsible for serializing and deserializing
DynaFlow instances. It ensures that the
data is properly formatted and can be
stored or retrieved from a database or
transmitted over a network.

The tests in this module cover the serialization
and deserialization of DynaFlow
instances using the DynaFlowSchema
class. They verify
that the serialized data
matches the expected format and that the
deserialized data can be used to
reconstruct a DynaFlow instance.

The DynaFlowSchema class
is used to define
the serialization and deserialization
rules for DynaFlow instances. It
specifies how each attribute of a
DynaFlow instance
should be converted to a serialized
format and how the serialized data should
be converted back to a DynaFlow
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
from models import DynaFlow
from models.factory import DynaFlowFactory
from models.serialization_schema import DynaFlowSchema
from services.logging_config import get_logger

logger = get_logger(__name__)


@pytest.fixture(scope="function")
def new_obj(
    session
) -> DynaFlow:
    """
    Fixture to create and return a DynaFlow
    instance using the
    DynaFlowFactory.

    Args:
        session: The database session.

    Returns:
        DynaFlow: A newly created
            DynaFlow instance.
    """

    return DynaFlowFactory.create(session=session)


class TestDynaFlowSchema:
    """
    Tests for the DynaFlow
    serialization schema.
    """

    # Sample data for a DynaFlow
    # instance
    sample_data = {
        "dyna_flow_id": 1,
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
        "dependency_dyna_flow_id": 42,
        "description": "Vanilla",
        "dyna_flow_type_id": 1,
        "is_build_task_debug_required": False,
        "is_canceled": False,
        "is_cancel_requested": False,
        "is_completed": False,
        "is_paused": False,
        "is_resubmitted": False,
        "is_run_task_debug_required": False,
        "is_started": False,
        "is_successful": False,
        "is_task_creation_started": False,
        "is_tasks_created": False,
        "min_start_utc_date_time": datetime(
            2023, 1, 1, 12, 0, 0, tzinfo=pytz.utc
        ).isoformat(),
        "pac_id": 2,
        "param_1": "Vanilla",
        "parent_dyna_flow_id": 42,
        "priority_level": 42,
        "requested_utc_date_time": datetime(
            2023, 1, 1, 12, 0, 0, tzinfo=pytz.utc
        ).isoformat(),
        "result_value": "Vanilla",
        "root_dyna_flow_id": 42,
        "started_utc_date_time": datetime(
            2023, 1, 1, 12, 0, 0, tzinfo=pytz.utc
        ).isoformat(),
        "subject_code":
            "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
        "task_creation_processor_identifier": "Vanilla",
        "insert_utc_date_time": datetime(
            2024, 1, 1, 12, 0, 0, tzinfo=pytz.utc
        ).isoformat(),
        "last_update_utc_date_time": datetime(
            2025, 1, 1, 12, 0, 0, tzinfo=pytz.utc
        ).isoformat(),
# endset  # noqa: E122
        "dyna_flow_type_code_peek":  # DynaFlowTypeID
            "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
        "pac_code_peek":  # PacID
            "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
# endset  # noqa: E122
    }

    def test_dyna_flow_serialization(
        self,
        new_obj: DynaFlow
    ):
        """
        Test the serialization of a
        DynaFlow instance using
        DynaFlowSchema.

        Args:
            dyna_flow (DynaFlow):
                A DynaFlow instance to serialize.
        """

        schema = DynaFlowSchema()
        dyna_flow_data = schema.dump(new_obj)

        assert isinstance(dyna_flow_data, dict)

        result = dyna_flow_data

        assert result['code'] == str(new_obj.code)
        assert result['last_change_code'] == (
            new_obj.last_change_code)
        assert result['insert_user_id'] == (
            str(new_obj.insert_user_id))
        assert result['last_update_user_id'] == (
            str(new_obj.last_update_user_id))

        assert result['completed_utc_date_time'] == (
            new_obj.completed_utc_date_time.isoformat())
        assert result['dependency_dyna_flow_id'] == (
            new_obj.dependency_dyna_flow_id)
        assert result['description'] == (
            new_obj.description)
        assert result['dyna_flow_type_id'] == (
            new_obj.dyna_flow_type_id)
        assert result['is_build_task_debug_required'] == (
            new_obj.is_build_task_debug_required)
        assert result['is_canceled'] == (
            new_obj.is_canceled)
        assert result['is_cancel_requested'] == (
            new_obj.is_cancel_requested)
        assert result['is_completed'] == (
            new_obj.is_completed)
        assert result['is_paused'] == (
            new_obj.is_paused)
        assert result['is_resubmitted'] == (
            new_obj.is_resubmitted)
        assert result['is_run_task_debug_required'] == (
            new_obj.is_run_task_debug_required)
        assert result['is_started'] == (
            new_obj.is_started)
        assert result['is_successful'] == (
            new_obj.is_successful)
        assert result['is_task_creation_started'] == (
            new_obj.is_task_creation_started)
        assert result['is_tasks_created'] == (
            new_obj.is_tasks_created)
        assert result['min_start_utc_date_time'] == (
            new_obj.min_start_utc_date_time.isoformat())
        assert result['pac_id'] == (
            new_obj.pac_id)
        assert result['param_1'] == (
            new_obj.param_1)
        assert result['parent_dyna_flow_id'] == (
            new_obj.parent_dyna_flow_id)
        assert result['priority_level'] == (
            new_obj.priority_level)
        assert result['requested_utc_date_time'] == (
            new_obj.requested_utc_date_time.isoformat())
        assert result['result_value'] == (
            new_obj.result_value)
        assert result['root_dyna_flow_id'] == (
            new_obj.root_dyna_flow_id)
        assert result['started_utc_date_time'] == (
            new_obj.started_utc_date_time.isoformat())
        assert result['subject_code'] == (
            str(new_obj.subject_code))
        assert result['task_creation_processor_identifier'] == (
            new_obj.task_creation_processor_identifier)
        assert result['insert_utc_date_time'] == (
            new_obj.insert_utc_date_time.isoformat())
        assert result['last_update_utc_date_time'] == (
            new_obj.last_update_utc_date_time.isoformat())
        assert result['dyna_flow_type_code_peek'] == (  # DynaFlowTypeID
            str(new_obj.dyna_flow_type_code_peek))
        assert result['pac_code_peek'] == (  # PacID
            str(new_obj.pac_code_peek))

    def test_dyna_flow_deserialization(
        self,
        new_obj: DynaFlow
    ):
        """
        Test the deserialization of a
        DynaFlow object using the
        DynaFlowSchema.

        Args:
            dyna_flow (DynaFlow): The
                DynaFlow object to be deserialized.

        Raises:
            AssertionError: If any of the assertions fail.

        Returns:
            None
        """

        schema = DynaFlowSchema()
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
        assert deserialized_data['dependency_dyna_flow_id'] == (
            new_obj.dependency_dyna_flow_id)
        assert deserialized_data['description'] == (
            new_obj.description)
        assert deserialized_data['dyna_flow_type_id'] == (
            new_obj.dyna_flow_type_id)
        assert deserialized_data['is_build_task_debug_required'] == (
            new_obj.is_build_task_debug_required)
        assert deserialized_data['is_canceled'] == (
            new_obj.is_canceled)
        assert deserialized_data['is_cancel_requested'] == (
            new_obj.is_cancel_requested)
        assert deserialized_data['is_completed'] == (
            new_obj.is_completed)
        assert deserialized_data['is_paused'] == (
            new_obj.is_paused)
        assert deserialized_data['is_resubmitted'] == (
            new_obj.is_resubmitted)
        assert deserialized_data['is_run_task_debug_required'] == (
            new_obj.is_run_task_debug_required)
        assert deserialized_data['is_started'] == (
            new_obj.is_started)
        assert deserialized_data['is_successful'] == (
            new_obj.is_successful)
        assert deserialized_data['is_task_creation_started'] == (
            new_obj.is_task_creation_started)
        assert deserialized_data['is_tasks_created'] == (
            new_obj.is_tasks_created)
        assert deserialized_data['min_start_utc_date_time'].isoformat() == (
            new_obj.min_start_utc_date_time.isoformat())
        assert deserialized_data['pac_id'] == (
            new_obj.pac_id)
        assert deserialized_data['param_1'] == (
            new_obj.param_1)
        assert deserialized_data['parent_dyna_flow_id'] == (
            new_obj.parent_dyna_flow_id)
        assert deserialized_data['priority_level'] == (
            new_obj.priority_level)
        assert deserialized_data['requested_utc_date_time'].isoformat() == (
            new_obj.requested_utc_date_time.isoformat())
        assert deserialized_data['result_value'] == (
            new_obj.result_value)
        assert deserialized_data['root_dyna_flow_id'] == (
            new_obj.root_dyna_flow_id)
        assert deserialized_data['started_utc_date_time'].isoformat() == (
            new_obj.started_utc_date_time.isoformat())
        assert deserialized_data['subject_code'] == (
            new_obj.subject_code)
        assert deserialized_data['task_creation_processor_identifier'] == (
            new_obj.task_creation_processor_identifier)
        assert deserialized_data['insert_utc_date_time'].isoformat() == (
            new_obj.insert_utc_date_time.isoformat())
        assert deserialized_data['last_update_utc_date_time'].isoformat() == (
            new_obj.last_update_utc_date_time.isoformat())
        assert deserialized_data[(  # DynaFlowTypeID
            'dyna_flow_type_code_peek')] == (
            new_obj.dyna_flow_type_code_peek)
        assert deserialized_data[(  # PacID
            'pac_code_peek')] == (
            new_obj.pac_code_peek)

        obj_from_dict = DynaFlow(
            **deserialized_data)

        assert isinstance(new_obj,
                          DynaFlow)

        # Now compare the new_obj attributes with
        # the dyna_flow attributes
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
        assert obj_from_dict.dependency_dyna_flow_id == (
            new_obj.dependency_dyna_flow_id)
        assert obj_from_dict.description == (
            new_obj.description)
        assert obj_from_dict.dyna_flow_type_id == (
            new_obj.dyna_flow_type_id)
        assert obj_from_dict.is_build_task_debug_required == (
            new_obj.is_build_task_debug_required)
        assert obj_from_dict.is_canceled == (
            new_obj.is_canceled)
        assert obj_from_dict.is_cancel_requested == (
            new_obj.is_cancel_requested)
        assert obj_from_dict.is_completed == (
            new_obj.is_completed)
        assert obj_from_dict.is_paused == (
            new_obj.is_paused)
        assert obj_from_dict.is_resubmitted == (
            new_obj.is_resubmitted)
        assert obj_from_dict.is_run_task_debug_required == (
            new_obj.is_run_task_debug_required)
        assert obj_from_dict.is_started == (
            new_obj.is_started)
        assert obj_from_dict.is_successful == (
            new_obj.is_successful)
        assert obj_from_dict.is_task_creation_started == (
            new_obj.is_task_creation_started)
        assert obj_from_dict.is_tasks_created == (
            new_obj.is_tasks_created)
        assert obj_from_dict.min_start_utc_date_time.isoformat() == (
            new_obj.min_start_utc_date_time.isoformat())
        assert obj_from_dict.pac_id == (
            new_obj.pac_id)
        assert obj_from_dict.param_1 == (
            new_obj.param_1)
        assert obj_from_dict.parent_dyna_flow_id == (
            new_obj.parent_dyna_flow_id)
        assert obj_from_dict.priority_level == (
            new_obj.priority_level)
        assert obj_from_dict.requested_utc_date_time.isoformat() == (
            new_obj.requested_utc_date_time.isoformat())
        assert obj_from_dict.result_value == (
            new_obj.result_value)
        assert obj_from_dict.root_dyna_flow_id == (
            new_obj.root_dyna_flow_id)
        assert obj_from_dict.started_utc_date_time.isoformat() == (
            new_obj.started_utc_date_time.isoformat())
        assert obj_from_dict.subject_code == (
            new_obj.subject_code)
        assert obj_from_dict.task_creation_processor_identifier == (
            new_obj.task_creation_processor_identifier)

        assert obj_from_dict.insert_utc_date_time.isoformat() == (
            new_obj.insert_utc_date_time.isoformat())
        assert obj_from_dict.last_update_utc_date_time.isoformat() == (
            new_obj.last_update_utc_date_time.isoformat())
        assert obj_from_dict.dyna_flow_type_code_peek == (  # DynaFlowTypeID
            new_obj.dyna_flow_type_code_peek)
        assert obj_from_dict.pac_code_peek == (  # PacID
            new_obj.pac_code_peek)

    def test_from_json(self):
        """
        Test the `from_json` method of the DynaFlowSchema class.

        This method tests the deserialization of
        a JSON string to a
        DynaFlow object.
        It converts the sample data to a JSON string,
        deserializes it to a dictionary,
        and then loads the dictionary to a DynaFlow
        object. Finally, it asserts the
        equality of the deserialized
        DynaFlow object
        with the sample data.

        Returns:
            None
        """

        dyna_flow_schema = DynaFlowSchema()

        # Convert sample data to JSON string
        json_str = json.dumps(self.sample_data)

        # Deserialize the JSON string to a dictionary
        json_data = json.loads(json_str)

        # Load the dictionary to an object
        deserialized_data = dyna_flow_schema.load(json_data)

        assert str(deserialized_data['dyna_flow_id']) == (
            str(self.sample_data['dyna_flow_id']))
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
        assert str(deserialized_data['dependency_dyna_flow_id']) == (
            str(self.sample_data['dependency_dyna_flow_id']))
        assert str(deserialized_data['description']) == (
            str(self.sample_data['description']))
        assert str(deserialized_data['dyna_flow_type_id']) == (
            str(self.sample_data['dyna_flow_type_id']))
        assert str(deserialized_data['is_build_task_debug_required']) == (
            str(self.sample_data['is_build_task_debug_required']))
        assert str(deserialized_data['is_canceled']) == (
            str(self.sample_data['is_canceled']))
        assert str(deserialized_data['is_cancel_requested']) == (
            str(self.sample_data['is_cancel_requested']))
        assert str(deserialized_data['is_completed']) == (
            str(self.sample_data['is_completed']))
        assert str(deserialized_data['is_paused']) == (
            str(self.sample_data['is_paused']))
        assert str(deserialized_data['is_resubmitted']) == (
            str(self.sample_data['is_resubmitted']))
        assert str(deserialized_data['is_run_task_debug_required']) == (
            str(self.sample_data['is_run_task_debug_required']))
        assert str(deserialized_data['is_started']) == (
            str(self.sample_data['is_started']))
        assert str(deserialized_data['is_successful']) == (
            str(self.sample_data['is_successful']))
        assert str(deserialized_data['is_task_creation_started']) == (
            str(self.sample_data['is_task_creation_started']))
        assert str(deserialized_data['is_tasks_created']) == (
            str(self.sample_data['is_tasks_created']))
        assert deserialized_data['min_start_utc_date_time'].isoformat() == (
            self.sample_data['min_start_utc_date_time'])
        assert str(deserialized_data['pac_id']) == (
            str(self.sample_data['pac_id']))
        assert str(deserialized_data['param_1']) == (
            str(self.sample_data['param_1']))
        assert str(deserialized_data['parent_dyna_flow_id']) == (
            str(self.sample_data['parent_dyna_flow_id']))
        assert str(deserialized_data['priority_level']) == (
            str(self.sample_data['priority_level']))
        assert deserialized_data['requested_utc_date_time'].isoformat() == (
            self.sample_data['requested_utc_date_time'])
        assert str(deserialized_data['result_value']) == (
            str(self.sample_data['result_value']))
        assert str(deserialized_data['root_dyna_flow_id']) == (
            str(self.sample_data['root_dyna_flow_id']))
        assert deserialized_data['started_utc_date_time'].isoformat() == (
            self.sample_data['started_utc_date_time'])
        assert str(deserialized_data['subject_code']) == (
            str(self.sample_data['subject_code']))
        assert str(deserialized_data['task_creation_processor_identifier']) == (
            str(self.sample_data['task_creation_processor_identifier']))
        assert deserialized_data['insert_utc_date_time'].isoformat() == (
            self.sample_data['insert_utc_date_time'])
        assert str(deserialized_data[(  # DynaFlowTypeID
            'dyna_flow_type_code_peek')]) == (
            str(self.sample_data['dyna_flow_type_code_peek']))
        assert str(deserialized_data[(  # PacID
            'pac_code_peek')]) == (
            str(self.sample_data['pac_code_peek']))
        assert deserialized_data['last_update_utc_date_time'].isoformat() == (
            self.sample_data['last_update_utc_date_time'])

        new_dyna_flow = DynaFlow(
            **deserialized_data)

        assert isinstance(new_dyna_flow,
                          DynaFlow)

    def test_to_json(
        self,
        new_obj: DynaFlow
    ):
        """
        Test the conversion of a
        DynaFlow instance to JSON.

        Args:
            dyna_flow (DynaFlow): The
            DynaFlow instance to convert.

        Raises:
            AssertionError: If the conversion fails or the
            converted JSON does not match the expected values.
        """

        # Convert the DynaFlow instance
        # to JSON using the schema
        dyna_flow_schema = DynaFlowSchema()
        dyna_flow_dict = dyna_flow_schema.dump(
            new_obj)

        # Convert the dyna_flow_dict to JSON string
        dyna_flow_json = json.dumps(
            dyna_flow_dict)

        # Convert the JSON strings back to dictionaries
        dict_from_json = json.loads(
            dyna_flow_json)

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
        assert dict_from_json['dependency_dyna_flow_id'] == (
            new_obj.dependency_dyna_flow_id), (
            "failed on dependency_dyna_flow_id"
        )
        assert dict_from_json['description'] == (
            new_obj.description), (
            "failed on description"
        )
        assert dict_from_json['dyna_flow_type_id'] == (
            new_obj.dyna_flow_type_id), (
            "failed on dyna_flow_type_id"
        )
        assert dict_from_json['is_build_task_debug_required'] == (
            new_obj.is_build_task_debug_required), (
            "failed on is_build_task_debug_required"
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
        assert dict_from_json['is_paused'] == (
            new_obj.is_paused), (
            "failed on is_paused"
        )
        assert dict_from_json['is_resubmitted'] == (
            new_obj.is_resubmitted), (
            "failed on is_resubmitted"
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
        assert dict_from_json['is_task_creation_started'] == (
            new_obj.is_task_creation_started), (
            "failed on is_task_creation_started"
        )
        assert dict_from_json['is_tasks_created'] == (
            new_obj.is_tasks_created), (
            "failed on is_tasks_created"
        )
        assert dict_from_json['min_start_utc_date_time'] == (
            new_obj.min_start_utc_date_time.isoformat()), (
            "failed on min_start_utc_date_time"
        )
        assert dict_from_json['pac_id'] == (
            new_obj.pac_id), (
            "failed on pac_id"
        )
        assert dict_from_json['param_1'] == (
            new_obj.param_1), (
            "failed on param_1"
        )
        assert dict_from_json['parent_dyna_flow_id'] == (
            new_obj.parent_dyna_flow_id), (
            "failed on parent_dyna_flow_id"
        )
        assert dict_from_json['priority_level'] == (
            new_obj.priority_level), (
            "failed on priority_level"
        )
        assert dict_from_json['requested_utc_date_time'] == (
            new_obj.requested_utc_date_time.isoformat()), (
            "failed on requested_utc_date_time"
        )
        assert dict_from_json['result_value'] == (
            new_obj.result_value), (
            "failed on result_value"
        )
        assert dict_from_json['root_dyna_flow_id'] == (
            new_obj.root_dyna_flow_id), (
            "failed on root_dyna_flow_id"
        )
        assert dict_from_json['started_utc_date_time'] == (
            new_obj.started_utc_date_time.isoformat()), (
            "failed on started_utc_date_time"
        )
        assert dict_from_json['subject_code'] == (
            str(new_obj.subject_code)), (
            "failed on subject_code"
        )
        assert dict_from_json['task_creation_processor_identifier'] == (
            new_obj.task_creation_processor_identifier), (
            "failed on task_creation_processor_identifier"
        )
        assert dict_from_json['insert_utc_date_time'] == (
            new_obj.insert_utc_date_time.isoformat()), (
            "failed on insert_utc_date_time"
        )
        assert dict_from_json['last_update_utc_date_time'] == (
            new_obj.last_update_utc_date_time.isoformat()), (
            "failed on last_update_utc_date_time"
        )
        assert dict_from_json[(  # DynaFlowTypeID
            'dyna_flow_type_code_peek')] == (
            str(new_obj.dyna_flow_type_code_peek)), (
            "failed on dyna_flow_type_code_peek"
        )
        assert dict_from_json[(  # PacID
            'pac_code_peek')] == (
            str(new_obj.pac_code_peek)), (
            "failed on pac_code_peek"
        )
