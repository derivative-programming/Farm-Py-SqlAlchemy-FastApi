# models/serialization_schema/tests/dyna_flow_type_schedule_test.py  # pylint: disable=duplicate-code
# pylint: disable=redefined-outer-name, too-many-public-methods
# pylint: disable=unused-import

"""
This module contains tests for the
DynaFlowTypeSchedule serialization schema.

The DynaFlowTypeSchedule serialization schema
is responsible for serializing and deserializing
DynaFlowTypeSchedule instances. It ensures that the
data is properly formatted and can be
stored or retrieved from a database or
transmitted over a network.

The tests in this module cover the serialization
and deserialization of DynaFlowTypeSchedule
instances using the DynaFlowTypeScheduleSchema
class. They verify
that the serialized data
matches the expected format and that the
deserialized data can be used to
reconstruct a DynaFlowTypeSchedule instance.

The DynaFlowTypeScheduleSchema class
is used to define
the serialization and deserialization
rules for DynaFlowTypeSchedule instances. It
specifies how each attribute of a
DynaFlowTypeSchedule instance
should be converted to a serialized
format and how the serialized data should
be converted back to a DynaFlowTypeSchedule
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
from models import DynaFlowTypeSchedule
from models.factory import DynaFlowTypeScheduleFactory
from models.serialization_schema import DynaFlowTypeScheduleSchema
from services.logging_config import get_logger

logger = get_logger(__name__)


@pytest.fixture(scope="function")
def new_obj(
    session
) -> DynaFlowTypeSchedule:
    """
    Fixture to create and return a DynaFlowTypeSchedule
    instance using the
    DynaFlowTypeScheduleFactory.

    Args:
        session: The database session.

    Returns:
        DynaFlowTypeSchedule: A newly created
            DynaFlowTypeSchedule instance.
    """

    return DynaFlowTypeScheduleFactory.create(session=session)


class TestDynaFlowTypeScheduleSchema:
    """
    Tests for the DynaFlowTypeSchedule
    serialization schema.
    """

    # Sample data for a DynaFlowTypeSchedule
    # instance
    sample_data = {
        "dyna_flow_type_schedule_id": 1,
        "code":
            "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
        "last_change_code": 0,
        "insert_user_id":
            "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
        "last_update_user_id":
            "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
# endset  # noqa: E122
        "dyna_flow_type_id": 1,
        "frequency_in_hours": 42,
        "is_active": False,
        "last_utc_date_time": datetime(
            2023, 1, 1, 12, 0, 0, tzinfo=pytz.utc
        ).isoformat(),
        "next_utc_date_time": datetime(
            2023, 1, 1, 12, 0, 0, tzinfo=pytz.utc
        ).isoformat(),
        "pac_id": 2,
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

    def test_dyna_flow_type_schedule_serialization(
        self,
        new_obj: DynaFlowTypeSchedule
    ):
        """
        Test the serialization of a
        DynaFlowTypeSchedule instance using
        DynaFlowTypeScheduleSchema.

        Args:
            dyna_flow_type_schedule (DynaFlowTypeSchedule):
                A DynaFlowTypeSchedule instance to serialize.
        """

        schema = DynaFlowTypeScheduleSchema()
        dyna_flow_type_schedule_data = schema.dump(new_obj)

        assert isinstance(dyna_flow_type_schedule_data, dict)

        result = dyna_flow_type_schedule_data

        assert result['code'] == str(new_obj.code)
        assert result['last_change_code'] == (
            new_obj.last_change_code)
        assert result['insert_user_id'] == (
            str(new_obj.insert_user_id))
        assert result['last_update_user_id'] == (
            str(new_obj.last_update_user_id))

        assert result['dyna_flow_type_id'] == (
            new_obj.dyna_flow_type_id)
        assert result['frequency_in_hours'] == (
            new_obj.frequency_in_hours)
        assert result['is_active'] == (
            new_obj.is_active)
        assert result['last_utc_date_time'] == (
            new_obj.last_utc_date_time.isoformat())
        assert result['next_utc_date_time'] == (
            new_obj.next_utc_date_time.isoformat())
        assert result['pac_id'] == (
            new_obj.pac_id)
        assert result['insert_utc_date_time'] == (
            new_obj.insert_utc_date_time.isoformat())
        assert result['last_update_utc_date_time'] == (
            new_obj.last_update_utc_date_time.isoformat())
        assert result['dyna_flow_type_code_peek'] == (  # DynaFlowTypeID
            str(new_obj.dyna_flow_type_code_peek))
        assert result['pac_code_peek'] == (  # PacID
            str(new_obj.pac_code_peek))

    def test_dyna_flow_type_schedule_deserialization(
        self,
        new_obj: DynaFlowTypeSchedule
    ):
        """
        Test the deserialization of a
        DynaFlowTypeSchedule object using the
        DynaFlowTypeScheduleSchema.

        Args:
            dyna_flow_type_schedule (DynaFlowTypeSchedule): The
                DynaFlowTypeSchedule object to be deserialized.

        Raises:
            AssertionError: If any of the assertions fail.

        Returns:
            None
        """

        schema = DynaFlowTypeScheduleSchema()
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
        assert deserialized_data['dyna_flow_type_id'] == (
            new_obj.dyna_flow_type_id)
        assert deserialized_data['frequency_in_hours'] == (
            new_obj.frequency_in_hours)
        assert deserialized_data['is_active'] == (
            new_obj.is_active)
        assert deserialized_data['last_utc_date_time'].isoformat() == (
            new_obj.last_utc_date_time.isoformat())
        assert deserialized_data['next_utc_date_time'].isoformat() == (
            new_obj.next_utc_date_time.isoformat())
        assert deserialized_data['pac_id'] == (
            new_obj.pac_id)
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

        obj_from_dict = DynaFlowTypeSchedule(
            **deserialized_data)

        assert isinstance(new_obj,
                          DynaFlowTypeSchedule)

        # Now compare the new_obj attributes with
        # the dyna_flow_type_schedule attributes
        assert obj_from_dict.code == \
            new_obj.code
        assert obj_from_dict.last_change_code == \
            new_obj.last_change_code
        assert obj_from_dict.insert_user_id == \
            new_obj.insert_user_id
        assert obj_from_dict.last_update_user_id == \
            new_obj.last_update_user_id
        assert obj_from_dict.dyna_flow_type_id == (
            new_obj.dyna_flow_type_id)
        assert obj_from_dict.frequency_in_hours == (
            new_obj.frequency_in_hours)
        assert obj_from_dict.is_active == (
            new_obj.is_active)
        assert obj_from_dict.last_utc_date_time.isoformat() == (
            new_obj.last_utc_date_time.isoformat())
        assert obj_from_dict.next_utc_date_time.isoformat() == (
            new_obj.next_utc_date_time.isoformat())
        assert obj_from_dict.pac_id == (
            new_obj.pac_id)

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
        Test the `from_json` method of the DynaFlowTypeScheduleSchema class.

        This method tests the deserialization of
        a JSON string to a
        DynaFlowTypeSchedule object.
        It converts the sample data to a JSON string,
        deserializes it to a dictionary,
        and then loads the dictionary to a DynaFlowTypeSchedule
        object. Finally, it asserts the
        equality of the deserialized
        DynaFlowTypeSchedule object
        with the sample data.

        Returns:
            None
        """

        dyna_flow_type_schedule_schema = DynaFlowTypeScheduleSchema()

        # Convert sample data to JSON string
        json_str = json.dumps(self.sample_data)

        # Deserialize the JSON string to a dictionary
        json_data = json.loads(json_str)

        # Load the dictionary to an object
        deserialized_data = dyna_flow_type_schedule_schema.load(json_data)

        assert str(deserialized_data['dyna_flow_type_schedule_id']) == (
            str(self.sample_data['dyna_flow_type_schedule_id']))
        assert str(deserialized_data['code']) == (
            str(self.sample_data['code']))
        assert str(deserialized_data['last_change_code']) == (
            str(self.sample_data['last_change_code']))
        assert str(deserialized_data['insert_user_id']) == (
            str(self.sample_data['insert_user_id']))
        assert str(deserialized_data['last_update_user_id']) == (
            str(self.sample_data['last_update_user_id']))
        assert str(deserialized_data['dyna_flow_type_id']) == (
            str(self.sample_data['dyna_flow_type_id']))
        assert str(deserialized_data['frequency_in_hours']) == (
            str(self.sample_data['frequency_in_hours']))
        assert str(deserialized_data['is_active']) == (
            str(self.sample_data['is_active']))
        assert deserialized_data['last_utc_date_time'].isoformat() == (
            self.sample_data['last_utc_date_time'])
        assert deserialized_data['next_utc_date_time'].isoformat() == (
            self.sample_data['next_utc_date_time'])
        assert str(deserialized_data['pac_id']) == (
            str(self.sample_data['pac_id']))
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

        new_dyna_flow_type_schedule = DynaFlowTypeSchedule(
            **deserialized_data)

        assert isinstance(new_dyna_flow_type_schedule,
                          DynaFlowTypeSchedule)

    def test_to_json(
        self,
        new_obj: DynaFlowTypeSchedule
    ):
        """
        Test the conversion of a
        DynaFlowTypeSchedule instance to JSON.

        Args:
            dyna_flow_type_schedule (DynaFlowTypeSchedule): The
            DynaFlowTypeSchedule instance to convert.

        Raises:
            AssertionError: If the conversion fails or the
            converted JSON does not match the expected values.
        """

        # Convert the DynaFlowTypeSchedule instance
        # to JSON using the schema
        dyna_flow_type_schedule_schema = DynaFlowTypeScheduleSchema()
        dyna_flow_type_schedule_dict = dyna_flow_type_schedule_schema.dump(
            new_obj)

        # Convert the dyna_flow_type_schedule_dict to JSON string
        dyna_flow_type_schedule_json = json.dumps(
            dyna_flow_type_schedule_dict)

        # Convert the JSON strings back to dictionaries
        dict_from_json = json.loads(
            dyna_flow_type_schedule_json)
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
        assert dict_from_json['dyna_flow_type_id'] == (
            new_obj.dyna_flow_type_id), (
            "failed on dyna_flow_type_id"
        )
        assert dict_from_json['frequency_in_hours'] == (
            new_obj.frequency_in_hours), (
            "failed on frequency_in_hours"
        )
        assert dict_from_json['is_active'] == (
            new_obj.is_active), (
            "failed on is_active"
        )
        assert dict_from_json['last_utc_date_time'] == (
            new_obj.last_utc_date_time.isoformat()), (
            "failed on last_utc_date_time"
        )
        assert dict_from_json['next_utc_date_time'] == (
            new_obj.next_utc_date_time.isoformat()), (
            "failed on next_utc_date_time"
        )
        assert dict_from_json['pac_id'] == (
            new_obj.pac_id), (
            "failed on pac_id"
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
