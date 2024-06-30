# models/serialization_schema/tests/dft_dependency_test.py
# pylint: disable=redefined-outer-name
# pylint: disable=unused-import

"""
This module contains tests for the
DFTDependency serialization schema.

The DFTDependency serialization schema
is responsible for serializing and deserializing
DFTDependency instances. It ensures that the
data is properly formatted and can be
stored or retrieved from a database or
transmitted over a network.

The tests in this module cover the serialization
and deserialization of DFTDependency
instances using the DFTDependencySchema
class. They verify
that the serialized data
matches the expected format and that the
deserialized data can be used to
reconstruct a DFTDependency instance.

The DFTDependencySchema class
is used to define
the serialization and deserialization
rules for DFTDependency instances. It
specifies how each attribute of a
DFTDependency instance
should be converted to a serialized
format and how the serialized data should
be converted back to a DFTDependency
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

from models import DFTDependency
from models.factory import DFTDependencyFactory
from models.serialization_schema import DFTDependencySchema
from services.logging_config import get_logger

logger = get_logger(__name__)


@pytest.fixture(scope="function")
def new_obj(
    session
) -> DFTDependency:
    """
    Fixture to create and return a DFTDependency
    instance using the
    DFTDependencyFactory.

    Args:
        session: The database session.

    Returns:
        DFTDependency: A newly created
            DFTDependency instance.
    """

    return DFTDependencyFactory.create(session=session)


class TestDFTDependencySchema:
    """
    Tests for the DFTDependency
    serialization schema.
    """

    # Sample data for a DFTDependency
    # instance
    sample_data = {
        "dft_dependency_id": 1,
        "code":
            "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
        "last_change_code": 0,
        "insert_user_id":
            "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
        "last_update_user_id":
            "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
# endset  # noqa: E122
        "dependency_df_task_id": 42,
        "dyna_flow_task_id": 2,
        "is_placeholder": False,
        "insert_utc_date_time": datetime(
            2024, 1, 1, 12, 0, 0, tzinfo=pytz.utc
        ).isoformat(),
        "last_update_utc_date_time": datetime(
            2025, 1, 1, 12, 0, 0, tzinfo=pytz.utc
        ).isoformat(),
# endset  # noqa: E122
        "dyna_flow_task_code_peek":  # DynaFlowTaskID
            "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
# endset  # noqa: E122
    }

    def test_dft_dependency_serialization(
        self,
        new_obj: DFTDependency
    ):
        """
        Test the serialization of a
        DFTDependency instance using
        DFTDependencySchema.

        Args:
            dft_dependency (DFTDependency):
                A DFTDependency instance to serialize.
        """

        schema = DFTDependencySchema()
        dft_dependency_data = schema.dump(new_obj)

        assert isinstance(dft_dependency_data, dict)

        result = dft_dependency_data

        assert result['code'] == str(new_obj.code)
        assert result['last_change_code'] == (
            new_obj.last_change_code)
        assert result['insert_user_id'] == (
            str(new_obj.insert_user_id))
        assert result['last_update_user_id'] == (
            str(new_obj.last_update_user_id))

        assert result['dependency_df_task_id'] == (
            new_obj.dependency_df_task_id)
        assert result['dyna_flow_task_id'] == (
            new_obj.dyna_flow_task_id)
        assert result['is_placeholder'] == (
            new_obj.is_placeholder)
        assert result['insert_utc_date_time'] == (
            new_obj.insert_utc_date_time.isoformat())
        assert result['last_update_utc_date_time'] == (
            new_obj.last_update_utc_date_time.isoformat())
        assert result['dyna_flow_task_code_peek'] == (  # DynaFlowTaskID
            str(new_obj.dyna_flow_task_code_peek))

    def test_dft_dependency_deserialization(
        self,
        new_obj: DFTDependency
    ):
        """
        Test the deserialization of a
        DFTDependency object using the
        DFTDependencySchema.

        Args:
            dft_dependency (DFTDependency): The
                DFTDependency object to be deserialized.

        Raises:
            AssertionError: If any of the assertions fail.

        Returns:
            None
        """

        schema = DFTDependencySchema()
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
        assert deserialized_data['dependency_df_task_id'] == (
            new_obj.dependency_df_task_id)
        assert deserialized_data['dyna_flow_task_id'] == (
            new_obj.dyna_flow_task_id)
        assert deserialized_data['is_placeholder'] == (
            new_obj.is_placeholder)
        assert deserialized_data['insert_utc_date_time'].isoformat() == (
            new_obj.insert_utc_date_time.isoformat())
        assert deserialized_data['last_update_utc_date_time'].isoformat() == (
            new_obj.last_update_utc_date_time.isoformat())
        assert deserialized_data[(  # DynaFlowTaskID
            'dyna_flow_task_code_peek')] == (
            new_obj.dyna_flow_task_code_peek)

        obj_from_dict = DFTDependency(
            **deserialized_data)

        assert isinstance(new_obj,
                          DFTDependency)

        # Now compare the new_obj attributes with
        # the dft_dependency attributes
        assert obj_from_dict.code == \
            new_obj.code
        assert obj_from_dict.last_change_code == \
            new_obj.last_change_code
        assert obj_from_dict.insert_user_id == \
            new_obj.insert_user_id
        assert obj_from_dict.last_update_user_id == \
            new_obj.last_update_user_id
        assert obj_from_dict.dependency_df_task_id == (
            new_obj.dependency_df_task_id)
        assert obj_from_dict.dyna_flow_task_id == (
            new_obj.dyna_flow_task_id)
        assert obj_from_dict.is_placeholder == (
            new_obj.is_placeholder)

        assert obj_from_dict.insert_utc_date_time.isoformat() == (
            new_obj.insert_utc_date_time.isoformat())
        assert obj_from_dict.last_update_utc_date_time.isoformat() == (
            new_obj.last_update_utc_date_time.isoformat())
        assert obj_from_dict.dyna_flow_task_code_peek == (  # DynaFlowTaskID
            new_obj.dyna_flow_task_code_peek)

    def test_from_json(self):
        """
        Test the `from_json` method of the DFTDependencySchema class.

        This method tests the deserialization of
        a JSON string to a
        DFTDependency object.
        It converts the sample data to a JSON string,
        deserializes it to a dictionary,
        and then loads the dictionary to a DFTDependency
        object. Finally, it asserts the
        equality of the deserialized
        DFTDependency object
        with the sample data.

        Returns:
            None
        """

        dft_dependency_schema = DFTDependencySchema()

        # Convert sample data to JSON string
        json_str = json.dumps(self.sample_data)

        # Deserialize the JSON string to a dictionary
        json_data = json.loads(json_str)

        # Load the dictionary to an object
        deserialized_data = dft_dependency_schema.load(json_data)

        assert str(deserialized_data['dft_dependency_id']) == (
            str(self.sample_data['dft_dependency_id']))
        assert str(deserialized_data['code']) == (
            str(self.sample_data['code']))
        assert str(deserialized_data['last_change_code']) == (
            str(self.sample_data['last_change_code']))
        assert str(deserialized_data['insert_user_id']) == (
            str(self.sample_data['insert_user_id']))
        assert str(deserialized_data['last_update_user_id']) == (
            str(self.sample_data['last_update_user_id']))
        assert str(deserialized_data['dependency_df_task_id']) == (
            str(self.sample_data['dependency_df_task_id']))
        assert str(deserialized_data['dyna_flow_task_id']) == (
            str(self.sample_data['dyna_flow_task_id']))
        assert str(deserialized_data['is_placeholder']) == (
            str(self.sample_data['is_placeholder']))
        assert deserialized_data['insert_utc_date_time'].isoformat() == (
            self.sample_data['insert_utc_date_time'])
        assert str(deserialized_data[(  # DynaFlowTaskID
            'dyna_flow_task_code_peek')]) == (
            str(self.sample_data['dyna_flow_task_code_peek']))
        assert deserialized_data['last_update_utc_date_time'].isoformat() == (
            self.sample_data['last_update_utc_date_time'])

        new_dft_dependency = DFTDependency(
            **deserialized_data)

        assert isinstance(new_dft_dependency,
                          DFTDependency)

    def test_to_json(
        self,
        new_obj: DFTDependency
    ):
        """
        Test the conversion of a
        DFTDependency instance to JSON.

        Args:
            dft_dependency (DFTDependency): The
            DFTDependency instance to convert.

        Raises:
            AssertionError: If the conversion fails or the
            converted JSON does not match the expected values.
        """

        # Convert the DFTDependency instance
        # to JSON using the schema
        dft_dependency_schema = DFTDependencySchema()
        dft_dependency_dict = dft_dependency_schema.dump(
            new_obj)

        # Convert the dft_dependency_dict to JSON string
        dft_dependency_json = json.dumps(
            dft_dependency_dict)

        # Convert the JSON strings back to dictionaries
        dict_from_json = json.loads(
            dft_dependency_json)
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
        assert dict_from_json['dependency_df_task_id'] == (
            new_obj.dependency_df_task_id), (
            "failed on dependency_df_task_id"
        )
        assert dict_from_json['dyna_flow_task_id'] == (
            new_obj.dyna_flow_task_id), (
            "failed on dyna_flow_task_id"
        )
        assert dict_from_json['is_placeholder'] == (
            new_obj.is_placeholder), (
            "failed on is_placeholder"
        )
        assert dict_from_json['insert_utc_date_time'] == (
            new_obj.insert_utc_date_time.isoformat()), (
            "failed on insert_utc_date_time"
        )
        assert dict_from_json['last_update_utc_date_time'] == (
            new_obj.last_update_utc_date_time.isoformat()), (
            "failed on last_update_utc_date_time"
        )
        assert dict_from_json[(  # DynaFlowTaskID
            'dyna_flow_task_code_peek')] == (
            str(new_obj.dyna_flow_task_code_peek)), (
            "failed on dyna_flow_task_code_peek"
        )
