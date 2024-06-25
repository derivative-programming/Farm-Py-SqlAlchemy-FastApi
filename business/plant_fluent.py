# business/plant_fluent.py
# pylint: disable=unused-import

"""
This module contains the
PlantFluentBusObj class,
which adds fluent properties
to the business object for a
Plant.
"""

from decimal import Decimal  # noqa: F401
import uuid  # noqa: F401
from datetime import datetime, date  # noqa: F401
from .plant_base import PlantBaseBusObj


class PlantFluentBusObj(PlantBaseBusObj):
    """
    This class add fluent properties to the
    Base Plant Business Object
    """

# endset
    # FlvrForeignKeyID
    # isDeleteAllowed

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
    # LandID

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
    # somePhoneNumber,
    # someTextVal,
    # someUniqueidentifierVal,
    # someVarCharVal,
# endset
