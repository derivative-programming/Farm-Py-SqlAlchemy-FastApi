# business/plant.py

"""
This module contains the PlantBusObj class,
which represents the business object for a Plant.
"""

from decimal import Decimal
import random
import uuid
from typing import List
from datetime import datetime, date
from helpers.session_context import SessionContext
from managers import PlantManager
from models import Plant
import models
import managers as managers_and_enums
from .base_bus_obj import BaseBusObj
##GENINCLUDEFILE[GENVALPascalName.top.include.*]

NOT_INITIALIZED_ERROR_MESSAGE = (
    "Plant object is not initialized")


class PlantInvalidInitError(Exception):
    """
    Exception raised when the
    Plant object
    is not initialized properly.
    """


class PlantBusObj(BaseBusObj):
    """
    This class represents the business object for a Plant.
    It requires a valid session context for initialization.
    """

    def __init__(self, session_context: SessionContext):
        """
        Initializes a new instance of the
        PlantBusObj class.

        :param session_context: The session context.
        :raises ValueError: If the session is not provided.
        """

        if not session_context.session:
            raise ValueError("session required")

        self._session_context = session_context
        self.plant = Plant()

    @property
    def plant_id(self) -> int:
        """
        Get the plant ID from the
        Plant object.

        :return: The plant ID.
        :raises AttributeError: If the
            Plant object is not initialized.
        """

        if not self.plant:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.plant.plant_id

    # code
    @property
    def code(self):
        """
        Get the code from the
        Plant object.

        :return: The code.
        :raises AttributeError: If the
            Plant object is not initialized.
        """

        if not self.plant:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.plant.code

    @code.setter
    def code(self, value: uuid.UUID):  # type: ignore
        """
        Set the code for the Plant object.

        :param value: The code value.
        :raises AttributeError: If the
            Plant object is not initialized.
        :raises ValueError: If the code is not a UUID.
        """

        if not self.plant:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, uuid.UUID):
            raise ValueError("code must be a UUID.")

        self.plant.code = value

    # last_change_code
    @property
    def last_change_code(self):
        """
        Get the last change code from the
        Plant object.

        :return: The last change code.
        :raises AttributeError: If the
            Plant object is not initialized.
        """

        if not self.plant:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.plant.last_change_code

    @last_change_code.setter
    def last_change_code(self, value: int):
        """
        Set the last change code for the
        Plant object.

        :param value: The last change code value.
        :raises AttributeError: If the
            Plant object is not initialized.
        :raises ValueError: If the last change code is not an integer.
        """

        if not self.plant:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, int):
            raise ValueError("last_change_code must be an integer.")

        self.plant.last_change_code = value

    # insert_user_id
    @property
    def insert_user_id(self):
        """
        Get the insert user ID from the
        Plant object.

        :return: The insert user ID.
        :raises AttributeError: If the
            Plant object is not initialized.
        """

        if not self.plant:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.plant.insert_user_id

    @insert_user_id.setter
    def insert_user_id(self, value: uuid.UUID):
        """
        Set the insert user ID for the
        Plant object.

        :param value: The insert user ID value.
        :raises AttributeError: If the
            Plant object is not initialized.
        :raises ValueError: If the insert user ID is not a UUID.
        """

        if not self.plant:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, uuid.UUID):
            raise ValueError("insert_user_id must be a UUID.")

        self.plant.insert_user_id = value

    # last_update_user_id
    @property
    def last_update_user_id(self):
        """
        Get the last update user ID from the
        Plant object.

        :return: The last update user ID.
        :raises AttributeError: If the
            Plant object is not initialized.
        """

        if not self.plant:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.plant.last_update_user_id

    @last_update_user_id.setter
    def last_update_user_id(self, value: uuid.UUID):
        """
        Set the last update user ID for the
        Plant object.

        :param value: The last update user ID value.
        :raises AttributeError: If the
            Plant object is not initialized.
        :raises ValueError: If the last update user ID is not a UUID.
        """

        if not self.plant:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, uuid.UUID):
            raise ValueError("last_update_user_id must be a UUID.")

        self.plant.last_update_user_id = value

# endset

    # FlvrForeignKeyID

    # isDeleteAllowed
    @property
    def is_delete_allowed(self):
        """
        Get the is delete allowed flag from the
        Plant object.

        :return: The is delete allowed flag.
        :raises AttributeError: If the
            Plant object is not initialized.
        """

        if not self.plant:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.plant.is_delete_allowed

    @is_delete_allowed.setter
    def is_delete_allowed(self, value: bool):
        """
        Set the is delete allowed flag for the
        Plant object.

        :param value: The is delete allowed flag value.
        :raises AttributeError: If the
            Plant object is not initialized.
        :raises ValueError: If the is delete allowed flag is not a boolean.
        """

        if not self.plant:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, bool):
            raise ValueError("is_delete_allowed must be a boolean.")

        self.plant.is_delete_allowed = value

    def set_prop_is_delete_allowed(self, value: bool):
        """
        Set the is delete allowed flag for the
        Plant object.

        :param value: The is delete allowed flag value.
        :return: The updated
            PlantBusObj instance.
        """

        self.is_delete_allowed = value
        return self

    # isEditAllowed
    @property
    def is_edit_allowed(self):
        """
        Get the is edit allowed flag from the
        Plant object.

        :return: The is edit allowed flag.
        :raises AttributeError: If the
            Plant object is not initialized.
        """

        if not self.plant:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.plant.is_edit_allowed

    @is_edit_allowed.setter
    def is_edit_allowed(self, value):
        """
        Set the is edit allowed flag for the
        Plant object.

        :param value: The is edit allowed flag value.
        :raises AttributeError: If the
            Plant object is not initialized.
        :raises AssertionError: If the is edit allowed flag is not a boolean.
        """

        if not self.plant:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, bool), "is_edit_allowed must be a boolean"
        self.plant.is_edit_allowed = value

    def set_prop_is_edit_allowed(self, value: bool):
        """
        Set the is edit allowed flag for the
        Plant object.

        :param value: The is edit allowed flag value.
        :return: The updated
            PlantBusObj instance.
        """

        self.is_edit_allowed = value
        return self

    # otherFlavor
    @property
    def other_flavor(self):
        """
        Get the other flavor from the
        Plant object.

        :return: The other flavor.
        :raises AttributeError: If the
            Plant object is not initialized.
        """

        if not self.plant:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if self.plant.other_flavor is None:
            return ""

        return self.plant.other_flavor

    @other_flavor.setter
    def other_flavor(self, value):
        """
        Set the other flavor for the
        Plant object.

        :param value: The other flavor value.
        :raises AttributeError: If the
            Plant object is not initialized.
        :raises AssertionError: If the other flavor is not a string.
        """

        if not self.plant:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, str), "other_flavor must be a string"
        self.plant.other_flavor = value

    def set_prop_other_flavor(self, value: str):
        """
        Set the other flavor for the
        Plant object.

        :param value: The other flavor value.
        :return: The updated
            PlantBusObj instance.
        """

        self.other_flavor = value
        return self

    # someBigIntVal
    @property
    def some_big_int_val(self):
        """
        Get the some big int value from the
        Plant object.

        :return: The some big int value.
        :raises AttributeError: If the
            Plant object is not initialized.
        """

        if not self.plant:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.plant.some_big_int_val

    @some_big_int_val.setter
    def some_big_int_val(self, value):
        """
        Set the some big int value for the
        Plant object.

        :param value: The some big int value.
        :raises AttributeError: If the
            Plant object is not initialized.
        :raises AssertionError: If the some big int value is not an integer.
        """

        if not self.plant:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, int), "some_big_int_val must be an integer"
        self.plant.some_big_int_val = value

    def set_prop_some_big_int_val(self, value: int):
        """
        Set the some big int value for the
        Plant object.

        :param value: The some big int value.
        :return: The updated
            PlantBusObj instance.
        """

        self.some_big_int_val = value
        return self

    # someBitVal
    @property
    def some_bit_val(self):
        """
        Get the some bit value from the
        Plant object.

        :return: The some bit value.
        :raises AttributeError: If the
            Plant object is not initialized.
        """

        if not self.plant:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.plant.some_bit_val

    @some_bit_val.setter
    def some_bit_val(self, value):
        """
        Set the some bit value for the
        Plant object.

        :param value: The some bit value.
        :raises AttributeError: If the
            Plant object is not initialized.
        :raises AssertionError: If the some bit value is not a boolean.
        """

        if not self.plant:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, bool), "some_bit_val must be a boolean"
        self.plant.some_bit_val = value

    def set_prop_some_bit_val(self, value: bool):
        """
        Set the some bit value for the
        Plant object.

        :param value: The some bit value.
        :return: The updated
            PlantBusObj instance.
        """

        self.some_bit_val = value
        return self

    # someDateVal
    @property
    def some_date_val(self):
        """
        Get the some date value from the
        Plant object.

        :return: The some date value.
        :raises AttributeError: If the
            Plant object is not initialized.
        """

        if not self.plant:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.plant.some_date_val

    @some_date_val.setter
    def some_date_val(self, value):
        """
        Set the some date value for the
        Plant object.

        :param value: The some date value.
        :raises AttributeError: If the
            Plant object is not initialized.
        :raises AssertionError: If the some date value is not a date object.
        """

        if not self.plant:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, date), (
            "some_date_val must be a date object"
        )
        self.plant.some_date_val = value

    def set_prop_some_date_val(self, value: date):
        """
        Set the some date value for the
        Plant object.

        :param value: The some date value.
        :return: The updated
            PlantBusObj instance.
        """

        self.some_date_val = value
        return self

    # someDecimalVal
    @property
    def some_decimal_val(self):
        """
        Get the some decimal value from the
        Plant object.

        :return: The some decimal value.
        :raises AttributeError: If the
            Plant object is not initialized.
        """

        if not self.plant:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.plant.some_decimal_val

    @some_decimal_val.setter
    def some_decimal_val(self, value):
        """
        Set the some decimal value for the
        Plant object.

        :param value: The some decimal value.
        :raises AttributeError: If the
            Plant object is not initialized.
        :raises AssertionError: If the some decimal value is not a number.
        """

        if not self.plant:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, Decimal), (
            "some_decimal_val must be a number"
        )
        self.plant.some_decimal_val = value

    def set_prop_some_decimal_val(self, value: Decimal):
        """
        Set the value of
        some_decimal_val property.

        Args:
            value (Decimal): The value to set for
                some_decimal_val.

        Returns:
            self: Returns the instance of the class with the updated
            some_decimal_val property.
        """
        self.some_decimal_val = value
        return self

    # someEmailAddress
    @property
    def some_email_address(self):
        """
        Returns the some email address
        associated with the plant.

        :return: The some email address
            of the plant.
        :rtype: str
        :raises AttributeError: If the
            plant is not initialized.
        """

        if not self.plant:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if self.plant.some_email_address is None:
            return ""

        return self.plant.some_email_address

    @some_email_address.setter
    def some_email_address(self, value):
        """
        Sets the some email address
        for the plant.

        Args:
            value (str): The some email address
                to be set.

        Raises:
            AttributeError: If the
                plant is not initialized.

        """
        if not self.plant:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, str), (
            "some_email_address must be a string")
        self.plant.some_email_address = value

    def set_prop_some_email_address(self, value: str):
        """
        Set the value of the
        some_email_address property.

        Args:
            value (str): The some email address
                to set.

        Returns:
            self: The current instance of the class.
        """
        self.some_email_address = value
        return self

    # someFloatVal
    @property
    def some_float_val(self):
        """
        Returns the value of the
        'some_float_val' attribute of the plant.

        Raises:
            AttributeError: If the
                plant is not initialized.

        Returns:
            float: The value of the
                'some_float_val' attribute.
        """
        if not self.plant:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.plant.some_float_val

    @some_float_val.setter
    def some_float_val(self, value):
        """
        Sets the value of
        some_float_val for the
        plant.

        Args:
            value (float): The value to set for
                some_float_val.

        Raises:
            AttributeError: If the
                plant is not initialized.

        """
        if not self.plant:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, float), (
            "some_float_val must be a float")
        self.plant.some_float_val = value

    def set_prop_some_float_val(self, value):
        """
        Set the value of the
        'some_float_val' property.

        Args:
            value (float): The value to set for the
                'some_float_val' property.

        Returns:
            self: The current instance of the class.

        """
        self.some_float_val = value
        return self

    # someIntVal
    @property
    def some_int_val(self):
        """
        Returns the value of
        some_int_val attribute of the
        plant.

        Raises:
            AttributeError: If the
                plant is not initialized.

        Returns:
            int: The value of
                some_int_val attribute.
        """
        if not self.plant:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.plant.some_int_val

    @some_int_val.setter
    def some_int_val(self, value):
        """
        Sets the value of
        some_int_val for the
        plant.

        Args:
            value (int): The integer value to set for
                some_int_val.

        Raises:
            AttributeError: If the
                plant is not initialized.

        """
        if not self.plant:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, int), (
            "some_int_val must be an integer")
        self.plant.some_int_val = value

    def set_prop_some_int_val(self, value: int):
        """
        Set the value of
        some_int_val property.

        Args:
            value (int): The value to set for
                some_int_val.

        Returns:
            self: Returns the instance of the class.

        """
        self.some_int_val = value
        return self

    # someMoneyVal
    @property
    def some_money_val(self):
        """
        Returns the value of
        some_money_val for the
        plant.

        Raises:
            AttributeError: If the
                plant is not initialized.

        Returns:
            The value of
            some_money_val for the plant.
        """
        if not self.plant:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.plant.some_money_val

    @some_money_val.setter
    def some_money_val(self, value):
        """
        Sets the value of
        some_money_val for the
        plant.

        Args:
            value (Decimal): The value to set for
                some_money_val.

        Raises:
            AttributeError: If the
                plant is not initialized.

        """
        if not self.plant:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, Decimal), (
            "some_money_val must be a number")
        self.plant.some_money_val = value

    def set_prop_some_money_val(self, value: Decimal):
        """
        Set the value of
        some_money_val property.

        Args:
            value (Decimal): The value to set for
                some_money_val.

        Returns:
            self: Returns the instance of the class.

        """
        self.some_money_val = value
        return self

    # someNVarCharVal
    @property
    def some_n_var_char_val(self):
        """
        Returns the value of the
        'some_n_var_char_val' attribute of the
        plant.

        If the plant is not
        initialized, an AttributeError is raised.

        Returns:
            str: The value of the
                'some_n_var_char_val' attribute,
                or an empty string if it is None.
        """
        if not self.plant:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if self.plant.some_n_var_char_val is None:
            return ""

        return self.plant.some_n_var_char_val

    @some_n_var_char_val.setter
    def some_n_var_char_val(self, value):
        """
        Sets the value of
        some_n_var_char_val attribute for the
        plant.

        Args:
            value (str): The value to be set for
                some_n_var_char_val.

        Raises:
            AttributeError: If the
                plant is not initialized.

        """
        if not self.plant:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, str), (
            "some_n_var_char_val must be a string")
        self.plant.some_n_var_char_val = value

    def set_prop_some_n_var_char_val(self, value: str):
        """
        Set the value of
        some_n_var_char_val property.

        Args:
            value (str): The value to set.

        Returns:
            self: The current instance of the class.
        """
        self.some_n_var_char_val = value
        return self

    # somePhoneNumber
    @property
    def some_phone_number(self):
        """
        Returns the some phone number
        associated with the
        plant.

        If the plant is not initialized,
        an AttributeError is raised.
        If the some phone number is None,
        an empty string is returned.

        Returns:
            str: The some phone number
                associated with the
                plant,
                or an empty string if it is None.

        Raises:
            AttributeError: If the
                plant is not initialized.
        """

        if not self.plant:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if self.plant.some_phone_number is None:
            return ""

        return self.plant.some_phone_number

    @some_phone_number.setter
    def some_phone_number(self, value):
        """
        Sets the some phone number
        for the plant.

        Args:
            value (str): The
                some phone number
                to set.

        Raises:
            AttributeError: If the
            plant is not initialized.

        """
        if not self.plant:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, str), (
            "some_phone_number must be a string")
        self.plant.some_phone_number = value

    def set_prop_some_phone_number(self, value: str):
        """
        Set the value of the
        'some_phone_number' property.

        Args:
            value (str): The
                some phone number to set.

        Returns:
            Plant: The updated
                Plant instance.

        """

        self.some_phone_number = value
        return self

    # someTextVal
    @property
    def some_text_val(self):
        """
        Returns the value of the
        'some_text_val' attribute of the plant.

        If the 'plant'
        attribute is not initialized,
        an AttributeError is raised.
        If the 'some_text_val'
        attribute is None,
        an empty string is returned.
        """

        if not self.plant:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if self.plant.some_text_val is None:
            return ""

        return self.plant.some_text_val

    @some_text_val.setter
    def some_text_val(self, value):
        """
        Sets the value of the
        'some_text_val' attribute for the
        plant.

        Args:
            value (str): The value to be set for
                'some_text_val'.

        Raises:
            AttributeError: If the
            plant is not initialized.

        """
        if not self.plant:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, str), (
            "some_text_val must be a string")
        self.plant.some_text_val = value

    def set_prop_some_text_val(self, value: str):
        """
        Sets the value of the
        'some_text_val' property.

        Args:
            value (str): The value to set for
                'some_text_val'.

        Returns:
            self: The current instance of the class.
        """
        self.some_text_val = value
        return self

    # someUniqueidentifierVal
    @property
    def some_uniqueidentifier_val(self):
        """
        Returns the value of the
        some unique identifier for the
        plant.

        Raises:
            AttributeError: If the
                plant is not initialized.

        Returns:
            The value of the some unique identifier for the
            plant.
        """
        if not self.plant:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.plant.some_uniqueidentifier_val

    @some_uniqueidentifier_val.setter
    def some_uniqueidentifier_val(self, value):
        """
        Sets the value of the
        'some_uniqueidentifier_val'
        attribute for the
        plant.

        Args:
            value (uuid.UUID): The UUID value to set for
                'some_uniqueidentifier_val'.

        Raises:
            AttributeError: If the
                plant is not initialized.

        """
        if not self.plant:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, uuid.UUID), (
            "some_uniqueidentifier_val must be a UUID")
        self.plant.some_uniqueidentifier_val = value

    def set_prop_some_uniqueidentifier_val(self, value: uuid.UUID):
        """
        Set the value of the
        'some_uniqueidentifier_val' property.

        Args:
            value (uuid.UUID): The value to set.

        Returns:
            self: The current instance of the class.
        """
        self.some_uniqueidentifier_val = value
        return self

    # someUTCDateTimeVal
    @property
    def some_utc_date_time_val(self):
        """
        Returns the value of
        some_utc_date_time_val attribute of the
        plant.

        Raises:
            AttributeError: If the
                plant is not initialized.

        Returns:
            The value of
            some_utc_date_time_val
            attribute.
        """
        if not self.plant:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.plant.some_utc_date_time_val

    @some_utc_date_time_val.setter
    def some_utc_date_time_val(self, value):
        """
        Sets the value of
        some_utc_date_time_val attribute
        for the plant.

        Args:
            value (datetime): The datetime value to be set.

        Raises:
            AttributeError: If the
                plant is not initialized.

        """
        if not self.plant:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, datetime), (
            "some_utc_date_time_val must be a datetime object")
        self.plant.some_utc_date_time_val = value

    def set_prop_some_utc_date_time_val(self, value: datetime):
        """
        Sets the value of the
        'some_utc_date_time_val' property.

        Args:
            value (datetime): The datetime value to set.

        Returns:
            self: The current instance of the class.
        """
        self.some_utc_date_time_val = value
        return self

    # someVarCharVal
    @property
    def some_var_char_val(self):
        """
        Returns the value of the
        'some_var_char_val'
        attribute of the
        plant.

        If the plant
        is not initialized, an AttributeError is raised.
        If the 'some_var_char_val'
        attribute is None,
        an empty string is returned.
        """

        if not self.plant:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if self.plant.some_var_char_val is None:
            return ""

        return self.plant.some_var_char_val

    @some_var_char_val.setter
    def some_var_char_val(self, value):
        """
        Sets the value of the
        'some_var_char_val' attribute for the
        plant.

        Args:
            value (str): The value to be set for
                'some_var_char_val'.

        Raises:
            AttributeError: If the
                plant is not initialized.

        """
        if not self.plant:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, str), (
            "some_var_char_val must be a string")
        self.plant.some_var_char_val = value

    def set_prop_some_var_char_val(self, value: str):
        """
        Set the value of some_var_char_val
        property.

        Args:
            value (str): The value to set for
                some_var_char_val.

        Returns:
            self: Returns the instance of the class.

        """
        self.some_var_char_val = value
        return self

    # LandID

# endset

    # isDeleteAllowed,
    # isEditAllowed,
    # otherFlavor,
    # someBigIntVal,
    # someBitVal,
    # someDecimalVal,
    # someEmailAddress,
    # someFloatVal,
    # someIntVal,
    # someMoneyVal,
    # someNVarCharVal,
    # someDateVal
    # someUTCDateTimeVal
    # FlvrForeignKeyID
    @property
    def flvr_foreign_key_id(self):
        """
        Returns the flvr_foreign_key_id
        of the flavor
        associated with the
        plant.

        Raises:
            AttributeError: If the
            plant is not initialized.

        Returns:
            int: The foreign key ID of the flavor.
        """
        if not self.plant:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.plant.flvr_foreign_key_id

    @flvr_foreign_key_id.setter
    def flvr_foreign_key_id(self, value: int):
        """
        Sets the foreign key ID for the
        flavor of the
        plant.

        Args:
            value (int): The foreign key ID to set.

        Raises:
            AttributeError: If the
                plant is not initialized.
            ValueError: If the value is not an integer.
        """

        if not self.plant:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, int):
            raise ValueError("flvr_foreign_key_id must be an integer.")

        self.plant.flvr_foreign_key_id = value

    def set_prop_flvr_foreign_key_id(self, value: int):
        """
        Sets the value of the
        'flvr_foreign_key_id' property.

        Args:
            value (int): The value to set for the
                'flvr_foreign_key_id' property.

        Returns:
            self: The current instance of the class.

        """
        self.flvr_foreign_key_id = value
        return self

    @property
    def flvr_foreign_key_code_peek(self) -> uuid.UUID:
        """
        Returns the flvr_foreign_key_id code peek
        of the plant.

        Raises:
            AttributeError: If the plant
                is not initialized.

        Returns:
            uuid.UUID: The flvr foreign key code peek
            of the plant.
        """
        if not self.plant:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.plant.flvr_foreign_key_code_peek

    # @flvr_foreign_key_code_peek.setter
    # def flvr_foreign_key_code_peek(self, value):
    #     assert isinstance(
    #       value, uuid.UUID),
    #       "flvr_foreign_key_code_peek must be a UUID"
    #     self.plant.flvr_foreign_key_code_peek = value

    # LandID
    @property
    def land_id(self):
        """
        Returns the land ID
        associated with the
        plant.

        Raises:
            AttributeError: If the
                plant is not initialized.

        Returns:
            int: The land ID of the plant.
        """
        if not self.plant:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.plant.land_id

    @land_id.setter
    def land_id(self, value):
        """
        Sets the land ID
        for the plant.

        Args:
            value (int or None): The
                land ID to be set.
                Must be an integer or None.

        Raises:
            AttributeError: If the
                plant is not initialized.

        """
        if not self.plant:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, int) or value is None, (
            "land_id must be an integer or None")

        self.plant.land_id = value

    def set_prop_land_id(self, value: int):
        """
        Set the land ID for the
        plant.

        Args:
            value (int): The land id value.

        Returns:
            Plant: The updated
                Plant object.
        """

        self.land_id = value
        return self

    @property
    def land_code_peek(self) -> uuid.UUID:
        """
        Returns the land id code peek
        of the plant.

        Raises:
            AttributeError: If the
            plant is not initialized.

        Returns:
            uuid.UUID: The land id code peek
            of the plant.
        """
        if not self.plant:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.plant.land_code_peek

    # @land_code_peek.setter
    # def land_code_peek(self, value):
    #     assert isinstance(value, uuid.UUID),
    #           "land_code_peek must be a UUID"
    #     self.plant.land_code_peek = value

    # somePhoneNumber,
    # someTextVal,
    # someUniqueidentifierVal,
    # someVarCharVal,

# endset

    # insert_utc_date_time
    @property
    def insert_utc_date_time(self):
        """
        Inserts the UTC date and time into
        the plant object.

        Raises:
            AttributeError: If the
                plant object is not initialized.

        Returns:
            The UTC date and time inserted into the
            plant object.
        """
        if not self.plant:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.plant.insert_utc_date_time

    @insert_utc_date_time.setter
    def insert_utc_date_time(self, value):
        """
        Inserts the UTC date and time for the
        plant.

        Args:
            value (datetime): The UTC date and time to be inserted.
                It should be a datetime object or None.

        Raises:
            AttributeError: If the
                plant is not initialized.

        """
        if not self.plant:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, datetime) or value is None, (
            "insert_utc_date_time must be a datetime object or None")

        self.plant.insert_utc_date_time = value

    # update_utc_date_time
    @property
    def last_update_utc_date_time(self):
        """
        Returns the last update UTC date and time
        of the plant.

        Raises:
            AttributeError: If the
                plant is not initialized.

        Returns:
            datetime: The last update UTC date and time
                of the plant.
        """
        if not self.plant:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.plant.last_update_utc_date_time

    @last_update_utc_date_time.setter
    def last_update_utc_date_time(self, value):
        """
        Sets the last update UTC date and time
        for the plant.

        Args:
            value (datetime): The datetime object
                representing the last update UTC date and time.
                Pass None to unset the value.

        Raises:
            AttributeError: If the
                plant is not initialized.

        """
        if not self.plant:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, datetime) or value is None, (
            "last_update_utc_date_time must be a datetime object or None")

        self.plant.last_update_utc_date_time = value

    async def load_from_json(
        self,
        json_data: str
    ):
        """
        Load plant data
        from JSON string.

        :param json_data: JSON string containing
            plant data.
        :raises ValueError: If json_data is not a string
            or if no plant
            data is found.
        """

        if not isinstance(json_data, str):
            raise ValueError("json_data must be a string")

        plant_manager = PlantManager(
            self._session_context)
        self.plant = plant_manager.from_json(json_data)

        return self

    async def load_from_code(
        self,
        code: uuid.UUID
    ):
        """
        Load plant
        data from UUID code.

        :param code: UUID code for loading a specific
            plant.
        :raises ValueError: If code is not a UUID or if no
            plant data is found.
        """
        if not isinstance(code, uuid.UUID):
            raise ValueError("code must be a UUID")

        plant_manager = PlantManager(
            self._session_context)
        plant_obj = await plant_manager.get_by_code(
            code)
        self.plant = plant_obj

        return self

    async def load_from_id(
        self,
        plant_id: int
    ):
        """
        Load plant data from
        plant ID.

        :param plant_id: Integer ID for loading a specific
            plant.
        :raises ValueError: If plant_id
            is not an integer or
            if no plant
            data is found.
        """

        if not isinstance(plant_id, int):
            raise ValueError("plant_id must be an integer")

        plant_manager = PlantManager(
            self._session_context)
        plant_obj = await plant_manager.get_by_id(
            plant_id)
        self.plant = plant_obj

        return self

    async def load_from_obj_instance(
        self,
        plant_obj_instance: Plant
    ):
        """
        Use the provided
        Plant instance.

        :param plant_obj_instance: Instance of the
            Plant class.
        :raises ValueError: If plant_obj_instance
            is not an instance of
            Plant.
        """

        if not isinstance(plant_obj_instance,
                          Plant):
            raise ValueError("plant_obj_instance must be an instance of Plant")

        plant_manager = PlantManager(
            self._session_context)

        plant_obj_instance_plant_id = plant_obj_instance.plant_id

        plant_obj = await plant_manager.get_by_id(
            plant_obj_instance_plant_id
        )
        self.plant = plant_obj

        return self

    async def load_from_dict(
        self,
        plant_dict: dict
    ):
        """
        Load plant data
        from dictionary.

        :param plant_dict: Dictionary containing
            plant data.
        :raises ValueError: If plant_dict
            is not a
            dictionary or if no
            plant data is found.
        """
        if not isinstance(plant_dict, dict):
            raise ValueError("plant_dict must be a dictionary")

        plant_manager = PlantManager(
            self._session_context)

        self.plant = plant_manager.from_dict(
            plant_dict)

        return self

##GENTrainingBlock[caseLookupEnums]Start
##GENLearn[isLookup=false]Start
##GENLearn[isLookup=false]End
##GENTrainingBlock[caseLookupEnums]End

    def get_session_context(self):
        """
        Returns the session context.

        :return: The session context.
        :rtype: SessionContext
        """
        return self._session_context

    async def refresh(self):
        """
        Refreshes the plant
        object by fetching
        the latest data from the database.

        Returns:
            The updated
            plant object.
        """
        plant_manager = PlantManager(
            self._session_context)
        self.plant = await plant_manager.refresh(
            self.plant)

        return self

    def is_valid(self):
        """
        Check if the plant
        is valid.

        Returns:
            bool: True if the plant
                is valid, False otherwise.
        """
        return self.plant is not None

    def to_dict(self):
        """
        Converts the Plant
        object to a dictionary representation.

        Returns:
            dict: A dictionary representation of the
                Plant object.
        """
        plant_manager = PlantManager(
            self._session_context)
        return plant_manager.to_dict(
            self.plant)

    def to_json(self):
        """
        Converts the plant
        object to a JSON representation.

        Returns:
            str: The JSON representation of the
                plant object.
        """
        plant_manager = PlantManager(
            self._session_context)
        return plant_manager.to_json(
            self.plant)

    async def save(self):
        """
        Saves the plant object
        to the database.

        If the plant object
        is not initialized, an AttributeError is raised.
        If the plant_id
        is greater than 0, the
        plant is
        updated in the database.
        If the plant_id is 0,
        the plant is
        added to the database.

        Returns:
            The updated or added
            plant object.

        Raises:
            AttributeError: If the plant
            object is not initialized.
        """
        if not self.plant:
            raise AttributeError(NOT_INITIALIZED_ERROR_MESSAGE)

        plant_id = self.plant.plant_id

        if plant_id > 0:
            plant_manager = PlantManager(
                self._session_context)
            self.plant = await plant_manager.update(
                self.plant)

        if plant_id == 0:
            plant_manager = PlantManager(
                self._session_context)
            self.plant = await plant_manager.add(
                self.plant)

        return self

    async def delete(self):
        """
        Deletes the plant
        from the database.

        Raises:
            AttributeError: If the plant
                is not initialized.
        """
        if not self.plant:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if self.plant.plant_id > 0:
            plant_manager = PlantManager(
                self._session_context)
            await plant_manager.delete(
                self.plant.plant_id)
            self.plant = None

    async def randomize_properties(self):
        """
        Randomizes the properties of the
        plant object.

        This method generates random values for various
        properties of the plant
        object

        Returns:
            self: The current instance of the
                Plant class.

        Raises:
            AttributeError: If the plant
                object is not initialized.
        """
        if not self.plant:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        self.plant.flvr_foreign_key_id = random.choice(
            await managers_and_enums.FlavorManager(
                self._session_context).get_list()).flavor_id
        self.plant.is_delete_allowed = (
            random.choice([True, False]))
        self.plant.is_edit_allowed = (
            random.choice([True, False]))
        # self.plant.land_id = random.randint(0, 100)
        self.plant.other_flavor = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        self.plant.some_big_int_val = (
            random.randint(0, 1000000))
        self.plant.some_bit_val = (
            random.choice([True, False]))
        self.plant.some_date_val = date(
            random.randint(2000, 2023),
            random.randint(1, 12),
            random.randint(1, 28))
        self.plant.some_decimal_val = (
            Decimal(str(round(random.uniform(0, 100), 2))))
        self.plant.some_email_address = (
            f"user{random.randint(1, 100)}@abc.com")
        self.plant.some_float_val = (
            random.uniform(0, 100))
        self.plant.some_int_val = (
            random.randint(0, 100))
        self.plant.some_money_val = (
            Decimal(str(round(random.uniform(0, 100), 2))))
        self.plant.some_n_var_char_val = "".join(
            random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        self.plant.some_phone_number = (
            f"+1{random.randint(1000000000, 9999999999)}")
        self.plant.some_text_val = "Random text"
        self.plant.some_uniqueidentifier_val = uuid.uuid4()
        self.plant.some_utc_date_time_val = datetime(
            random.randint(2000, 2023),
            random.randint(1, 12),
            random.randint(1, 28))
        self.plant.some_var_char_val = "".join(
            random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=10))
# endset

        return self

    def get_plant_obj(self) -> Plant:
        """
        Returns the plant
        object.

        Raises:
            AttributeError: If the plant
                object is not initialized.

        Returns:
            Plant: The plant
                object.
        """
        if not self.plant:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.plant

    def is_equal(
        self,
        plant: Plant
    ) -> bool:
        """
        Checks if the current plant
        is equal to the given plant.

        Args:
            plant (Plant): The
                plant to compare with.

        Returns:
            bool: True if the plants
                are equal, False otherwise.
        """
        plant_manager = PlantManager(
            self._session_context)
        my_plant = self.get_plant_obj()
        return plant_manager.is_equal(
            plant, my_plant)
# endset

    # isDeleteAllowed,
    # isEditAllowed,
    # otherFlavor,
    # someBigIntVal,
    # someBitVal,
    # someDecimalVal,
    # someEmailAddress,
    # someFloatVal,
    # someIntVal,
    # someMoneyVal,
    # someNVarCharVal,
    # someDateVal
    # someUTCDateTimeVal
    # LandID
    async def get_land_id_rel_obj(self) -> models.Land:
        """
        Retrieves the related Land object based
        on the land_id.

        Returns:
            An instance of the Land model
            representing the related land.

        """
        land_manager = managers_and_enums.LandManager(self._session_context)
        land_obj = await land_manager.get_by_id(self.land_id)
        return land_obj

    # FlvrForeignKeyID
    async def get_flvr_foreign_key_id_rel_obj(self) -> models.Flavor:
        """
        Retrieves the related Flavor object based on the
        flvr_foreign_key_id.

        Returns:
            The related Flavor object.

        """
        flavor_manager = managers_and_enums.FlavorManager(
            self._session_context)
        flavor_obj = await flavor_manager.get_by_id(
            self.flvr_foreign_key_id
        )
        return flavor_obj
    # somePhoneNumber,
    # someTextVal,
    # someUniqueidentifierVal,
    # someVarCharVal,

# endset

    def get_obj(self) -> Plant:
        """
        Returns the Plant object.

        :return: The Plant object.
        :rtype: Plant
        """

        return self.plant

    def get_object_name(self) -> str:
        """
        Returns the name of the object.

        :return: The name of the object.
        :rtype: str
        """
        return "plant"

    def get_id(self) -> int:
        """
        Returns the ID of the plant.

        :return: The ID of the plant.
        :rtype: int
        """
        return self.plant_id

    # isDeleteAllowed,
    # isEditAllowed,
    # otherFlavor,
    # someBigIntVal,
    # someBitVal,
    # someDecimalVal,
    # someEmailAddress,
    # someFloatVal,
    # someIntVal,
    # someMoneyVal,
    # someNVarCharVal,
    # someDateVal
    # someUTCDateTimeVal
    # FlvrForeignKeyID
    # LandID

    async def get_parent_name(self) -> str:
        """
        Get the name of the parent plant.

        Returns:
            str: The name of the parent plant.
        """
        return 'Land'

    async def get_parent_code(self) -> uuid.UUID:
        """
        Get the parent code of the plant.

        Returns:
            The parent code of the plant
            as a UUID.
        """
        return self.land_code_peek

    async def get_parent_obj(self) -> models.Land:
        """
        Get the parent object of the current
        plant.

        Returns:
            The parent object of the current
            plant,
            which is an instance of the
            Land model.
        """
        land = await self.get_land_id_rel_obj()

        return land
    # somePhoneNumber,
    # someTextVal,
    # someUniqueidentifierVal,
    # someVarCharVal,
# endset

    @staticmethod
    async def to_bus_obj_list(
        session_context: SessionContext,
        obj_list: List[Plant]
    ):
        """
        Convert a list of Plant
        objects to a list of
        PlantBusObj objects.

        Args:
            session_context (SessionContext): The session context.
            obj_list (List[Plant]): The
                list of Plant objects to convert.

        Returns:
            List[PlantBusObj]: The
                list of converted PlantBusObj
                objects.
        """
        result = list()

        for plant in obj_list:
            plant_bus_obj = PlantBusObj(session_context)

            await plant_bus_obj.load_from_obj_instance(
                plant)

            result.append(plant_bus_obj)

        return result

    ##GENINCLUDEFILE[GENVALPascalName.bottom.include.*]
