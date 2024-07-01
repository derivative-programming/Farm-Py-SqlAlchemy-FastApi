# models/serialization_schema/tests/dyna_flow_task_type_test.py
# pylint: disable=redefined-outer-name
# pylint: disable=unused-import

"""
This module contains tests for the
DynaFlowTaskType serialization schema.

The DynaFlowTaskType serialization schema
is responsible for serializing and deserializing
DynaFlowTaskType instances. It ensures that the
data is properly formatted and can be
stored or retrieved from a database or
transmitted over a network.

The tests in this module cover the serialization
and deserialization of DynaFlowTaskType
instances using the DynaFlowTaskTypeSchema
class. They verify
that the serialized data
matches the expected format and that the
deserialized data can be used to
reconstruct a DynaFlowTaskType instance.

The DynaFlowTaskTypeSchema class
is used to define
the serialization and deserialization
rules for DynaFlowTaskType instances. It
specifies how each attribute of a
DynaFlowTaskType instance
should be converted to a serialized
format and how the serialized data should
be converted back to a DynaFlowTaskType
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

import pytest
import pytz

from models import DynaFlowTaskType
from models.factory import DynaFlowTaskTypeFactory
from models.serialization_schema import DynaFlowTaskTypeSchema
from services.logging_config import get_logger

logger = get_logger(__name__)


@pytest.fixture(scope="function")
def new_obj(
    session
) -> DynaFlowTaskType:
    """
    Fixture to create and return a DynaFlowTaskType
    instance using the
    DynaFlowTaskTypeFactory.

    Args:
        session: The database session.

    Returns:
        DynaFlowTaskType: A newly created
            DynaFlowTaskType instance.
    """

    return DynaFlowTaskTypeFactory.create(session=session)


class TestDynaFlowTaskTypeSchema:
    """
    Tests for the DynaFlowTaskType
    serialization schema.
    """

    # Sample data for a DynaFlowTaskType
    # instance
    sample_data = {
        "dyna_flow_task_type_id": 1,
        "code":
            "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
        "last_change_code": 0,
        "insert_user_id":
            "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
        "last_update_user_id":
            "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
# endset  # noqa: E122
        "description": "Vanilla",
        "display_order": 42,
        "is_active": False,
        "lookup_enum_name": "Vanilla",
        "max_retry_count": 42,
        "name": "Vanilla",
        "pac_id": 2,
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

    def test_dyna_flow_task_type_serialization(
        self,
        new_obj: DynaFlowTaskType
    ):
        """
        Test the serialization of a
        DynaFlowTaskType instance using
        DynaFlowTaskTypeSchema.

        Args:
            dyna_flow_task_type (DynaFlowTaskType):
                A DynaFlowTaskType instance to serialize.
        """

        schema = DynaFlowTaskTypeSchema()
        dyna_flow_task_type_data = schema.dump(new_obj)

        assert isinstance(dyna_flow_task_type_data, dict)

        result = dyna_flow_task_type_data

        assert result['code'] == str(new_obj.code)
        assert result['last_change_code'] == (
            new_obj.last_change_code)
        assert result['insert_user_id'] == (
            str(new_obj.insert_user_id))
        assert result['last_update_user_id'] == (
            str(new_obj.last_update_user_id))

        assert result['description'] == (
            new_obj.description)
        assert result['display_order'] == (
            new_obj.display_order)
        assert result['is_active'] == (
            new_obj.is_active)
        assert result['lookup_enum_name'] == (
            new_obj.lookup_enum_name)
        assert result['max_retry_count'] == (
            new_obj.max_retry_count)
        assert result['name'] == (
            new_obj.name)
        assert result['pac_id'] == (
            new_obj.pac_id)
        assert result['insert_utc_date_time'] == (
            new_obj.insert_utc_date_time.isoformat())
        assert result['last_update_utc_date_time'] == (
            new_obj.last_update_utc_date_time.isoformat())
        assert result['pac_code_peek'] == (  # PacID
            str(new_obj.pac_code_peek))

    def test_dyna_flow_task_type_deserialization(
        self,
        new_obj: DynaFlowTaskType
    ):
        """
        Test the deserialization of a
        DynaFlowTaskType object using the
        DynaFlowTaskTypeSchema.

        Args:
            dyna_flow_task_type (DynaFlowTaskType): The
                DynaFlowTaskType object to be deserialized.

        Raises:
            AssertionError: If any of the assertions fail.

        Returns:
            None
        """

        schema = DynaFlowTaskTypeSchema()
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
        assert deserialized_data['description'] == (
            new_obj.description)
        assert deserialized_data['display_order'] == (
            new_obj.display_order)
        assert deserialized_data['is_active'] == (
            new_obj.is_active)
        assert deserialized_data['lookup_enum_name'] == (
            new_obj.lookup_enum_name)
        assert deserialized_data['max_retry_count'] == (
            new_obj.max_retry_count)
        assert deserialized_data['name'] == (
            new_obj.name)
        assert deserialized_data['pac_id'] == (
            new_obj.pac_id)
        assert deserialized_data['insert_utc_date_time'].isoformat() == (
            new_obj.insert_utc_date_time.isoformat())
        assert deserialized_data['last_update_utc_date_time'].isoformat() == (
            new_obj.last_update_utc_date_time.isoformat())
        assert deserialized_data[(  # PacID
            'pac_code_peek')] == (
            new_obj.pac_code_peek)

        obj_from_dict = DynaFlowTaskType(
            **deserialized_data)

        assert isinstance(new_obj,
                          DynaFlowTaskType)

        # Now compare the new_obj attributes with
        # the dyna_flow_task_type attributes
        assert obj_from_dict.code == \
            new_obj.code
        assert obj_from_dict.last_change_code == \
            new_obj.last_change_code
        assert obj_from_dict.insert_user_id == \
            new_obj.insert_user_id
        assert obj_from_dict.last_update_user_id == \
            new_obj.last_update_user_id
        assert obj_from_dict.description == (
            new_obj.description)
        assert obj_from_dict.display_order == (
            new_obj.display_order)
        assert obj_from_dict.is_active == (
            new_obj.is_active)
        assert obj_from_dict.lookup_enum_name == (
            new_obj.lookup_enum_name)
        assert obj_from_dict.max_retry_count == (
            new_obj.max_retry_count)
        assert obj_from_dict.name == (
            new_obj.name)
        assert obj_from_dict.pac_id == (
            new_obj.pac_id)

        assert obj_from_dict.insert_utc_date_time.isoformat() == (
            new_obj.insert_utc_date_time.isoformat())
        assert obj_from_dict.last_update_utc_date_time.isoformat() == (
            new_obj.last_update_utc_date_time.isoformat())
        assert obj_from_dict.pac_code_peek == (  # PacID
            new_obj.pac_code_peek)

    def test_from_json(self):
        """
        Test the `from_json` method of the DynaFlowTaskTypeSchema class.

        This method tests the deserialization of
        a JSON string to a
        DynaFlowTaskType object.
        It converts the sample data to a JSON string,
        deserializes it to a dictionary,
        and then loads the dictionary to a DynaFlowTaskType
        object. Finally, it asserts the
        equality of the deserialized
        DynaFlowTaskType object
        with the sample data.

        Returns:
            None
        """

        dyna_flow_task_type_schema = DynaFlowTaskTypeSchema()

        # Convert sample data to JSON string
        json_str = json.dumps(self.sample_data)

        # Deserialize the JSON string to a dictionary
        json_data = json.loads(json_str)

        # Load the dictionary to an object
        deserialized_data = dyna_flow_task_type_schema.load(json_data)

        assert str(deserialized_data['dyna_flow_task_type_id']) == (
            str(self.sample_data['dyna_flow_task_type_id']))
        assert str(deserialized_data['code']) == (
            str(self.sample_data['code']))
        assert str(deserialized_data['last_change_code']) == (
            str(self.sample_data['last_change_code']))
        assert str(deserialized_data['insert_user_id']) == (
            str(self.sample_data['insert_user_id']))
        assert str(deserialized_data['last_update_user_id']) == (
            str(self.sample_data['last_update_user_id']))
        assert str(deserialized_data['description']) == (
            str(self.sample_data['description']))
        assert str(deserialized_data['display_order']) == (
            str(self.sample_data['display_order']))
        assert str(deserialized_data['is_active']) == (
            str(self.sample_data['is_active']))
        assert str(deserialized_data['lookup_enum_name']) == (
            str(self.sample_data['lookup_enum_name']))
        assert str(deserialized_data['max_retry_count']) == (
            str(self.sample_data['max_retry_count']))
        assert str(deserialized_data['name']) == (
            str(self.sample_data['name']))
        assert str(deserialized_data['pac_id']) == (
            str(self.sample_data['pac_id']))
        assert deserialized_data['insert_utc_date_time'].isoformat() == (
            self.sample_data['insert_utc_date_time'])
        assert str(deserialized_data[(  # PacID
            'pac_code_peek')]) == (
            str(self.sample_data['pac_code_peek']))
        assert deserialized_data['last_update_utc_date_time'].isoformat() == (
            self.sample_data['last_update_utc_date_time'])

        new_dyna_flow_task_type = DynaFlowTaskType(
            **deserialized_data)

        assert isinstance(new_dyna_flow_task_type,
                          DynaFlowTaskType)

    def test_to_json(
        self,
        new_obj: DynaFlowTaskType
    ):
        """
        Test the conversion of a
        DynaFlowTaskType instance to JSON.

        Args:
            dyna_flow_task_type (DynaFlowTaskType): The
            DynaFlowTaskType instance to convert.

        Raises:
            AssertionError: If the conversion fails or the
            converted JSON does not match the expected values.
        """

        # Convert the DynaFlowTaskType instance
        # to JSON using the schema
        dyna_flow_task_type_schema = DynaFlowTaskTypeSchema()
        dyna_flow_task_type_dict = dyna_flow_task_type_schema.dump(
            new_obj)

        # Convert the dyna_flow_task_type_dict to JSON string
        dyna_flow_task_type_json = json.dumps(
            dyna_flow_task_type_dict)

        # Convert the JSON strings back to dictionaries
        dict_from_json = json.loads(
            dyna_flow_task_type_json)
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
        assert dict_from_json['description'] == (
            new_obj.description), (
            "failed on description"
        )
        assert dict_from_json['display_order'] == (
            new_obj.display_order), (
            "failed on display_order"
        )
        assert dict_from_json['is_active'] == (
            new_obj.is_active), (
            "failed on is_active"
        )
        assert dict_from_json['lookup_enum_name'] == (
            new_obj.lookup_enum_name), (
            "failed on lookup_enum_name"
        )
        assert dict_from_json['max_retry_count'] == (
            new_obj.max_retry_count), (
            "failed on max_retry_count"
        )
        assert dict_from_json['name'] == (
            new_obj.name), (
            "failed on name"
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
        assert dict_from_json[(  # PacID
            'pac_code_peek')] == (
            str(new_obj.pac_code_peek)), (
            "failed on pac_code_peek"
        )