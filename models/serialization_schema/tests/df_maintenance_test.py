# models/serialization_schema/tests/df_maintenance_test.py  # pylint: disable=duplicate-code
# pylint: disable=redefined-outer-name, too-many-public-methods
# pylint: disable=unused-import

"""
This module contains tests for the
DFMaintenance serialization schema.

The DFMaintenance serialization schema
is responsible for serializing and deserializing
DFMaintenance instances. It ensures that the
data is properly formatted and can be
stored or retrieved from a database or
transmitted over a network.

The tests in this module cover the serialization
and deserialization of DFMaintenance
instances using the DFMaintenanceSchema
class. They verify
that the serialized data
matches the expected format and that the
deserialized data can be used to
reconstruct a DFMaintenance instance.

The DFMaintenanceSchema class
is used to define
the serialization and deserialization
rules for DFMaintenance instances. It
specifies how each attribute of a
DFMaintenance instance
should be converted to a serialized
format and how the serialized data should
be converted back to a DFMaintenance
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
from models import DFMaintenance
from models.factory import DFMaintenanceFactory
from models.serialization_schema import DFMaintenanceSchema
from services.logging_config import get_logger

logger = get_logger(__name__)


@pytest.fixture(scope="function")
def new_obj(
    session
) -> DFMaintenance:
    """
    Fixture to create and return a DFMaintenance
    instance using the
    DFMaintenanceFactory.

    Args:
        session: The database session.

    Returns:
        DFMaintenance: A newly created
            DFMaintenance instance.
    """

    return DFMaintenanceFactory.create(session=session)


class TestDFMaintenanceSchema:
    """
    Tests for the DFMaintenance
    serialization schema.
    """

    # Sample data for a DFMaintenance
    # instance
    sample_data = {
        "df_maintenance_id": 1,
        "code":
            "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
        "last_change_code": 0,
        "insert_user_id":
            "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
        "last_update_user_id":
            "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
# endset  # noqa: E122
        "is_paused": False,
        "is_scheduled_df_process_request_completed": False,
        "is_scheduled_df_process_request_started": False,
        "last_scheduled_df_process_request_utc_date_time": datetime(
            2023, 1, 1, 12, 0, 0, tzinfo=pytz.utc
        ).isoformat(),
        "next_scheduled_df_process_request_utc_date_time": datetime(
            2023, 1, 1, 12, 0, 0, tzinfo=pytz.utc
        ).isoformat(),
        "pac_id": 2,
        "paused_by_username": "Vanilla",
        "paused_utc_date_time": datetime(
            2023, 1, 1, 12, 0, 0, tzinfo=pytz.utc
        ).isoformat(),
        "scheduled_df_process_request_processor_identifier": "Vanilla",
        "insert_utc_date_time": datetime(
            2024, 1, 1, 12, 0, 0, tzinfo=pytz.utc
        ).isoformat(),
        "last_update_utc_date_time": datetime(
            2025, 1, 1, 12, 0, 0, tzinfo=pytz.utc
        ).isoformat(),
# endset  # noqa: E122
        "pac_code_peek":  # PacID
            "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
# endset  # noqa: E122
    }

    def test_df_maintenance_serialization(
        self,
        new_obj: DFMaintenance
    ):
        """
        Test the serialization of a
        DFMaintenance instance using
        DFMaintenanceSchema.

        Args:
            df_maintenance (DFMaintenance):
                A DFMaintenance instance to serialize.
        """

        schema = DFMaintenanceSchema()
        df_maintenance_data = schema.dump(new_obj)

        assert isinstance(df_maintenance_data, dict)

        result = df_maintenance_data

        assert result['code'] == str(new_obj.code)
        assert result['last_change_code'] == (
            new_obj.last_change_code)
        assert result['insert_user_id'] == (
            str(new_obj.insert_user_id))
        assert result['last_update_user_id'] == (
            str(new_obj.last_update_user_id))

        assert result['is_paused'] == (
            new_obj.is_paused)
        assert result['is_scheduled_df_process_request_completed'] == (
            new_obj.is_scheduled_df_process_request_completed)
        assert result['is_scheduled_df_process_request_started'] == (
            new_obj.is_scheduled_df_process_request_started)
        assert result['last_scheduled_df_process_request_utc_date_time'] == (
            new_obj.last_scheduled_df_process_request_utc_date_time.isoformat())
        assert result['next_scheduled_df_process_request_utc_date_time'] == (
            new_obj.next_scheduled_df_process_request_utc_date_time.isoformat())
        assert result['pac_id'] == (
            new_obj.pac_id)
        assert result['paused_by_username'] == (
            new_obj.paused_by_username)
        assert result['paused_utc_date_time'] == (
            new_obj.paused_utc_date_time.isoformat())
        assert result['scheduled_df_process_request_processor_identifier'] == (
            new_obj.scheduled_df_process_request_processor_identifier)
        assert result['insert_utc_date_time'] == (
            new_obj.insert_utc_date_time.isoformat())
        assert result['last_update_utc_date_time'] == (
            new_obj.last_update_utc_date_time.isoformat())
        assert result['pac_code_peek'] == (  # PacID
            str(new_obj.pac_code_peek))

    def test_df_maintenance_deserialization(
        self,
        new_obj: DFMaintenance
    ):
        """
        Test the deserialization of a
        DFMaintenance object using the
        DFMaintenanceSchema.

        Args:
            df_maintenance (DFMaintenance): The
                DFMaintenance object to be deserialized.

        Raises:
            AssertionError: If any of the assertions fail.

        Returns:
            None
        """

        schema = DFMaintenanceSchema()
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
        assert deserialized_data['is_paused'] == (
            new_obj.is_paused)
        assert deserialized_data['is_scheduled_df_process_request_completed'] == (
            new_obj.is_scheduled_df_process_request_completed)
        assert deserialized_data['is_scheduled_df_process_request_started'] == (
            new_obj.is_scheduled_df_process_request_started)
        assert deserialized_data['last_scheduled_df_process_request_utc_date_time'].isoformat() == (
            new_obj.last_scheduled_df_process_request_utc_date_time.isoformat())
        assert deserialized_data['next_scheduled_df_process_request_utc_date_time'].isoformat() == (
            new_obj.next_scheduled_df_process_request_utc_date_time.isoformat())
        assert deserialized_data['pac_id'] == (
            new_obj.pac_id)
        assert deserialized_data['paused_by_username'] == (
            new_obj.paused_by_username)
        assert deserialized_data['paused_utc_date_time'].isoformat() == (
            new_obj.paused_utc_date_time.isoformat())
        assert deserialized_data['scheduled_df_process_request_processor_identifier'] == (
            new_obj.scheduled_df_process_request_processor_identifier)
        assert deserialized_data['insert_utc_date_time'].isoformat() == (
            new_obj.insert_utc_date_time.isoformat())
        assert deserialized_data['last_update_utc_date_time'].isoformat() == (
            new_obj.last_update_utc_date_time.isoformat())
        assert deserialized_data[(  # PacID
            'pac_code_peek')] == (
            new_obj.pac_code_peek)

        obj_from_dict = DFMaintenance(
            **deserialized_data)

        assert isinstance(new_obj,
                          DFMaintenance)

        # Now compare the new_obj attributes with
        # the df_maintenance attributes
        assert obj_from_dict.code == \
            new_obj.code
        assert obj_from_dict.last_change_code == \
            new_obj.last_change_code
        assert obj_from_dict.insert_user_id == \
            new_obj.insert_user_id
        assert obj_from_dict.last_update_user_id == \
            new_obj.last_update_user_id
        assert obj_from_dict.is_paused == (
            new_obj.is_paused)
        assert obj_from_dict.is_scheduled_df_process_request_completed == (
            new_obj.is_scheduled_df_process_request_completed)
        assert obj_from_dict.is_scheduled_df_process_request_started == (
            new_obj.is_scheduled_df_process_request_started)
        assert obj_from_dict.last_scheduled_df_process_request_utc_date_time.isoformat() == (
            new_obj.last_scheduled_df_process_request_utc_date_time.isoformat())
        assert obj_from_dict.next_scheduled_df_process_request_utc_date_time.isoformat() == (
            new_obj.next_scheduled_df_process_request_utc_date_time.isoformat())
        assert obj_from_dict.pac_id == (
            new_obj.pac_id)
        assert obj_from_dict.paused_by_username == (
            new_obj.paused_by_username)
        assert obj_from_dict.paused_utc_date_time.isoformat() == (
            new_obj.paused_utc_date_time.isoformat())
        assert obj_from_dict.scheduled_df_process_request_processor_identifier == (
            new_obj.scheduled_df_process_request_processor_identifier)

        assert obj_from_dict.insert_utc_date_time.isoformat() == (
            new_obj.insert_utc_date_time.isoformat())
        assert obj_from_dict.last_update_utc_date_time.isoformat() == (
            new_obj.last_update_utc_date_time.isoformat())
        assert obj_from_dict.pac_code_peek == (  # PacID
            new_obj.pac_code_peek)

    def test_from_json(self):
        """
        Test the `from_json` method of the DFMaintenanceSchema class.

        This method tests the deserialization of
        a JSON string to a
        DFMaintenance object.
        It converts the sample data to a JSON string,
        deserializes it to a dictionary,
        and then loads the dictionary to a DFMaintenance
        object. Finally, it asserts the
        equality of the deserialized
        DFMaintenance object
        with the sample data.

        Returns:
            None
        """

        df_maintenance_schema = DFMaintenanceSchema()

        # Convert sample data to JSON string
        json_str = json.dumps(self.sample_data)

        # Deserialize the JSON string to a dictionary
        json_data = json.loads(json_str)

        # Load the dictionary to an object
        deserialized_data = df_maintenance_schema.load(json_data)

        assert str(deserialized_data['df_maintenance_id']) == (
            str(self.sample_data['df_maintenance_id']))
        assert str(deserialized_data['code']) == (
            str(self.sample_data['code']))
        assert str(deserialized_data['last_change_code']) == (
            str(self.sample_data['last_change_code']))
        assert str(deserialized_data['insert_user_id']) == (
            str(self.sample_data['insert_user_id']))
        assert str(deserialized_data['last_update_user_id']) == (
            str(self.sample_data['last_update_user_id']))
        assert str(deserialized_data['is_paused']) == (
            str(self.sample_data['is_paused']))
        assert str(deserialized_data['is_scheduled_df_process_request_completed']) == (
            str(self.sample_data['is_scheduled_df_process_request_completed']))
        assert str(deserialized_data['is_scheduled_df_process_request_started']) == (
            str(self.sample_data['is_scheduled_df_process_request_started']))
        assert deserialized_data['last_scheduled_df_process_request_utc_date_time'].isoformat() == (
            self.sample_data['last_scheduled_df_process_request_utc_date_time'])
        assert deserialized_data['next_scheduled_df_process_request_utc_date_time'].isoformat() == (
            self.sample_data['next_scheduled_df_process_request_utc_date_time'])
        assert str(deserialized_data['pac_id']) == (
            str(self.sample_data['pac_id']))
        assert str(deserialized_data['paused_by_username']) == (
            str(self.sample_data['paused_by_username']))
        assert deserialized_data['paused_utc_date_time'].isoformat() == (
            self.sample_data['paused_utc_date_time'])
        assert str(deserialized_data['scheduled_df_process_request_processor_identifier']) == (
            str(self.sample_data['scheduled_df_process_request_processor_identifier']))
        assert deserialized_data['insert_utc_date_time'].isoformat() == (
            self.sample_data['insert_utc_date_time'])
        assert str(deserialized_data[(  # PacID
            'pac_code_peek')]) == (
            str(self.sample_data['pac_code_peek']))
        assert deserialized_data['last_update_utc_date_time'].isoformat() == (
            self.sample_data['last_update_utc_date_time'])

        new_df_maintenance = DFMaintenance(
            **deserialized_data)

        assert isinstance(new_df_maintenance,
                          DFMaintenance)

    def test_to_json(
        self,
        new_obj: DFMaintenance
    ):
        """
        Test the conversion of a
        DFMaintenance instance to JSON.

        Args:
            df_maintenance (DFMaintenance): The
            DFMaintenance instance to convert.

        Raises:
            AssertionError: If the conversion fails or the
            converted JSON does not match the expected values.
        """

        # Convert the DFMaintenance instance
        # to JSON using the schema
        df_maintenance_schema = DFMaintenanceSchema()
        df_maintenance_dict = df_maintenance_schema.dump(
            new_obj)

        # Convert the df_maintenance_dict to JSON string
        df_maintenance_json = json.dumps(
            df_maintenance_dict)

        # Convert the JSON strings back to dictionaries
        dict_from_json = json.loads(
            df_maintenance_json)

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
        assert dict_from_json['is_paused'] == (
            new_obj.is_paused), (
            "failed on is_paused"
        )
        assert dict_from_json['is_scheduled_df_process_request_completed'] == (
            new_obj.is_scheduled_df_process_request_completed), (
            "failed on is_scheduled_df_process_request_completed"
        )
        assert dict_from_json['is_scheduled_df_process_request_started'] == (
            new_obj.is_scheduled_df_process_request_started), (
            "failed on is_scheduled_df_process_request_started"
        )
        assert dict_from_json['last_scheduled_df_process_request_utc_date_time'] == (
            new_obj.last_scheduled_df_process_request_utc_date_time.isoformat()), (
            "failed on last_scheduled_df_process_request_utc_date_time"
        )
        assert dict_from_json['next_scheduled_df_process_request_utc_date_time'] == (
            new_obj.next_scheduled_df_process_request_utc_date_time.isoformat()), (
            "failed on next_scheduled_df_process_request_utc_date_time"
        )
        assert dict_from_json['pac_id'] == (
            new_obj.pac_id), (
            "failed on pac_id"
        )
        assert dict_from_json['paused_by_username'] == (
            new_obj.paused_by_username), (
            "failed on paused_by_username"
        )
        assert dict_from_json['paused_utc_date_time'] == (
            new_obj.paused_utc_date_time.isoformat()), (
            "failed on paused_utc_date_time"
        )
        assert dict_from_json['scheduled_df_process_request_processor_identifier'] == (
            new_obj.scheduled_df_process_request_processor_identifier), (
            "failed on scheduled_df_process_request_processor_identifier"
        )
        assert dict_from_json['insert_utc_date_time'] == (
            new_obj.insert_utc_date_time.isoformat()), (
            "failed on insert_utc_date_time"
        )
        assert dict_from_json['last_update_utc_date_time'] == (
            new_obj.last_update_utc_date_time.isoformat()), (
            "failed on last_update_utc_date_time"
        )
        assert dict_from_json[(  # PacID
            'pac_code_peek')] == (
            str(new_obj.pac_code_peek)), (
            "failed on pac_code_peek"
        )
