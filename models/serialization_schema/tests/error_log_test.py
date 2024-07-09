# models/serialization_schema/tests/error_log_test.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=redefined-outer-name, too-many-public-methods
# pylint: disable=unused-import

"""
This module contains tests for the
ErrorLog serialization schema.

The ErrorLog serialization schema
is responsible for serializing and deserializing
ErrorLog instances. It ensures that the
data is properly formatted and can be
stored or retrieved from a database or
transmitted over a network.

The tests in this module cover the serialization
and deserialization of ErrorLog
instances using the ErrorLogSchema
class. They verify
that the serialized data
matches the expected format and that the
deserialized data can be used to
reconstruct a ErrorLog instance.

The ErrorLogSchema class
is used to define
the serialization and deserialization
rules for ErrorLog instances. It
specifies how each attribute of a
ErrorLog instance
should be converted to a serialized
format and how the serialized data should
be converted back to a ErrorLog
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
from models import ErrorLog
from models.factory import ErrorLogFactory
from models.serialization_schema import ErrorLogSchema
from services.logging_config import get_logger

logger = get_logger(__name__)


@pytest.fixture(scope="function")
def new_obj(
    session
) -> ErrorLog:
    """
    Fixture to create and return a ErrorLog
    instance using the
    ErrorLogFactory.

    Args:
        session: The database session.

    Returns:
        ErrorLog: A newly created
            ErrorLog instance.
    """

    return ErrorLogFactory.create(session=session)


class TestErrorLogSchema:
    """
    Tests for the ErrorLog
    serialization schema.
    """

    # Sample data for a ErrorLog
    # instance
    sample_data = {
        "error_log_id": 1,
        "code":
            "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
        "last_change_code": 0,
        "insert_user_id":
            "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
        "last_update_user_id":
            "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
# endset  # noqa: E122
        "browser_code":
            "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
        "context_code":
            "a1b2c3d4-e5f6-7a8b-9c0d-123456789012",
        "created_utc_date_time": datetime(
            2023, 1, 1, 12, 0, 0, tzinfo=pytz.utc
        ).isoformat(),
        "description": "Vanilla",
        "is_client_side_error": False,
        "is_resolved": False,
        "pac_id": 2,
        "url": "Vanilla",
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

    def test_error_log_serialization(
        self,
        new_obj: ErrorLog
    ):
        """
        Test the serialization of a
        ErrorLog instance using
        ErrorLogSchema.

        Args:
            error_log (ErrorLog):
                A ErrorLog instance to serialize.
        """

        schema = ErrorLogSchema()
        error_log_data = schema.dump(new_obj)

        assert isinstance(error_log_data, dict)

        result = error_log_data

        assert result['code'] == str(new_obj.code)
        assert result['last_change_code'] == (
            new_obj.last_change_code)
        assert result['insert_user_id'] == (
            str(new_obj.insert_user_id))
        assert result['last_update_user_id'] == (
            str(new_obj.last_update_user_id))

        assert result['browser_code'] == (
            str(new_obj.browser_code))
        assert result['context_code'] == (
            str(new_obj.context_code))
        assert result['created_utc_date_time'] == (
            new_obj.created_utc_date_time.isoformat())
        assert result['description'] == (
            new_obj.description)
        assert result['is_client_side_error'] == (
            new_obj.is_client_side_error)
        assert result['is_resolved'] == (
            new_obj.is_resolved)
        assert result['pac_id'] == (
            new_obj.pac_id)
        assert result['url'] == (
            new_obj.url)
        assert result['insert_utc_date_time'] == (
            new_obj.insert_utc_date_time.isoformat())
        assert result['last_update_utc_date_time'] == (
            new_obj.last_update_utc_date_time.isoformat())
        assert result['pac_code_peek'] == (  # PacID
            str(new_obj.pac_code_peek))

    def test_error_log_deserialization(
        self,
        new_obj: ErrorLog
    ):
        """
        Test the deserialization of a
        ErrorLog object using the
        ErrorLogSchema.

        Args:
            error_log (ErrorLog): The
                ErrorLog object to be deserialized.

        Raises:
            AssertionError: If any of the assertions fail.

        Returns:
            None
        """

        schema = ErrorLogSchema()
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
        assert deserialized_data['browser_code'] == (
            new_obj.browser_code)
        assert deserialized_data['context_code'] == (
            new_obj.context_code)
        assert deserialized_data['created_utc_date_time'].isoformat() == (
            new_obj.created_utc_date_time.isoformat())
        assert deserialized_data['description'] == (
            new_obj.description)
        assert deserialized_data['is_client_side_error'] == (
            new_obj.is_client_side_error)
        assert deserialized_data['is_resolved'] == (
            new_obj.is_resolved)
        assert deserialized_data['pac_id'] == (
            new_obj.pac_id)
        assert deserialized_data['url'] == (
            new_obj.url)
        assert deserialized_data['insert_utc_date_time'].isoformat() == (
            new_obj.insert_utc_date_time.isoformat())
        assert deserialized_data['last_update_utc_date_time'].isoformat() == (
            new_obj.last_update_utc_date_time.isoformat())
        assert deserialized_data[(  # PacID
            'pac_code_peek')] == (
            new_obj.pac_code_peek)

        obj_from_dict = ErrorLog(
            **deserialized_data)

        assert isinstance(new_obj,
                          ErrorLog)

        # Now compare the new_obj attributes with
        # the error_log attributes
        assert obj_from_dict.code == \
            new_obj.code
        assert obj_from_dict.last_change_code == \
            new_obj.last_change_code
        assert obj_from_dict.insert_user_id == \
            new_obj.insert_user_id
        assert obj_from_dict.last_update_user_id == \
            new_obj.last_update_user_id
        assert obj_from_dict.browser_code == (
            new_obj.browser_code)
        assert obj_from_dict.context_code == (
            new_obj.context_code)
        assert obj_from_dict.created_utc_date_time.isoformat() == (
            new_obj.created_utc_date_time.isoformat())
        assert obj_from_dict.description == (
            new_obj.description)
        assert obj_from_dict.is_client_side_error == (
            new_obj.is_client_side_error)
        assert obj_from_dict.is_resolved == (
            new_obj.is_resolved)
        assert obj_from_dict.pac_id == (
            new_obj.pac_id)
        assert obj_from_dict.url == (
            new_obj.url)

        assert obj_from_dict.insert_utc_date_time.isoformat() == (
            new_obj.insert_utc_date_time.isoformat())
        assert obj_from_dict.last_update_utc_date_time.isoformat() == (
            new_obj.last_update_utc_date_time.isoformat())
        assert obj_from_dict.pac_code_peek == (  # PacID
            new_obj.pac_code_peek)

    def test_from_json(self):
        """
        Test the `from_json` method of the ErrorLogSchema class.

        This method tests the deserialization of
        a JSON string to a
        ErrorLog object.
        It converts the sample data to a JSON string,
        deserializes it to a dictionary,
        and then loads the dictionary to a ErrorLog
        object. Finally, it asserts the
        equality of the deserialized
        ErrorLog object
        with the sample data.

        Returns:
            None
        """

        error_log_schema = ErrorLogSchema()

        # Convert sample data to JSON string
        json_str = json.dumps(self.sample_data)

        # Deserialize the JSON string to a dictionary
        json_data = json.loads(json_str)

        # Load the dictionary to an object
        deserialized_data = error_log_schema.load(json_data)

        assert str(deserialized_data['error_log_id']) == (
            str(self.sample_data['error_log_id']))
        assert str(deserialized_data['code']) == (
            str(self.sample_data['code']))
        assert str(deserialized_data['last_change_code']) == (
            str(self.sample_data['last_change_code']))
        assert str(deserialized_data['insert_user_id']) == (
            str(self.sample_data['insert_user_id']))
        assert str(deserialized_data['last_update_user_id']) == (
            str(self.sample_data['last_update_user_id']))
        assert str(deserialized_data['browser_code']) == (
            str(self.sample_data['browser_code']))
        assert str(deserialized_data['context_code']) == (
            str(self.sample_data['context_code']))
        assert deserialized_data['created_utc_date_time'].isoformat() == (
            self.sample_data['created_utc_date_time'])
        assert str(deserialized_data['description']) == (
            str(self.sample_data['description']))
        assert str(deserialized_data['is_client_side_error']) == (
            str(self.sample_data['is_client_side_error']))
        assert str(deserialized_data['is_resolved']) == (
            str(self.sample_data['is_resolved']))
        assert str(deserialized_data['pac_id']) == (
            str(self.sample_data['pac_id']))
        assert str(deserialized_data['url']) == (
            str(self.sample_data['url']))
        assert deserialized_data['insert_utc_date_time'].isoformat() == (
            self.sample_data['insert_utc_date_time'])
        assert str(deserialized_data[(  # PacID
            'pac_code_peek')]) == (
            str(self.sample_data['pac_code_peek']))
        assert deserialized_data['last_update_utc_date_time'].isoformat() == (
            self.sample_data['last_update_utc_date_time'])

        new_error_log = ErrorLog(
            **deserialized_data)

        assert isinstance(new_error_log,
                          ErrorLog)

    def test_to_json(
        self,
        new_obj: ErrorLog
    ):
        """
        Test the conversion of a
        ErrorLog instance to JSON.

        Args:
            error_log (ErrorLog): The
            ErrorLog instance to convert.

        Raises:
            AssertionError: If the conversion fails or the
            converted JSON does not match the expected values.
        """

        # Convert the ErrorLog instance
        # to JSON using the schema
        error_log_schema = ErrorLogSchema()
        error_log_dict = error_log_schema.dump(
            new_obj)

        # Convert the error_log_dict to JSON string
        error_log_json = json.dumps(
            error_log_dict)

        # Convert the JSON strings back to dictionaries
        dict_from_json = json.loads(
            error_log_json)

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
        assert dict_from_json['browser_code'] == (
            str(new_obj.browser_code)), (
            "failed on browser_code"
        )
        assert dict_from_json['context_code'] == (
            str(new_obj.context_code)), (
            "failed on context_code"
        )
        assert dict_from_json['created_utc_date_time'] == (
            new_obj.created_utc_date_time.isoformat()), (
            "failed on created_utc_date_time"
        )
        assert dict_from_json['description'] == (
            new_obj.description), (
            "failed on description"
        )
        assert dict_from_json['is_client_side_error'] == (
            new_obj.is_client_side_error), (
            "failed on is_client_side_error"
        )
        assert dict_from_json['is_resolved'] == (
            new_obj.is_resolved), (
            "failed on is_resolved"
        )
        assert dict_from_json['pac_id'] == (
            new_obj.pac_id), (
            "failed on pac_id"
        )
        assert dict_from_json['url'] == (
            new_obj.url), (
            "failed on url"
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
