# models/plant.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import

"""
The Plant model inherits from
the Base model and is mapped to the
'farm_Plant' table in the database.
"""
from decimal import Decimal  # noqa: F401
import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from sqlalchemy_utils import UUIDType
from sqlalchemy import (BigInteger, Boolean,   # noqa: F401
                        Column, Date, DateTime, Float,
                        ForeignKey, Index, Integer, Numeric, String,
                        event, func)
import models.constants.plant as \
    plant_constants
from utils.common_functions import snake_case
from .base import Base, EncryptedType  # noqa: F401


class Plant(Base):
    """
    The Plant model represents a
    plant in the farm.
    It inherits from the Base model and is mapped to the
    'farm_Plant' table in the database.
    """

    __tablename__ = 'farm_' + snake_case('Plant')

    _plant_id = Column(
        'plant_id',
        Integer,
        primary_key=True,
        autoincrement=True)
    _code = Column(
        'code',
        UUIDType(binary=False),
        unique=True,
        default=uuid.uuid4,
        nullable=True)
    _last_change_code = Column(
        'last_change_code',
        Integer,
        nullable=True)
    _insert_user_id = Column(
        'insert_user_id',
        UUIDType(binary=False),
        default=uuid.uuid4,
        nullable=True)
    _last_update_user_id = Column(
        'last_update_user_id',
        UUIDType(binary=False),
        default=uuid.uuid4,
        nullable=True)
    _flvr_foreign_key_id = Column(
        'flvr_foreign_key_id',
        Integer,
        ForeignKey('farm_' + snake_case('Flavor') + '.flavor_id'),
        index=(
            plant_constants.
            flvr_foreign_key_id_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _is_delete_allowed = Column(
        'is_delete_allowed',
        Boolean,
        default=False,
        index=(
            plant_constants.
            is_delete_allowed_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _is_edit_allowed = Column(
        'is_edit_allowed',
        Boolean,
        default=False,
        index=(
            plant_constants.
            is_edit_allowed_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _land_id = Column(
        'land_id',
        Integer,
        ForeignKey('farm_' + snake_case('Land') + '.land_id'),
        index=(
            plant_constants.
            land_id_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _other_flavor = Column(
        'other_flavor',
        ##GENIF[isEncrypted=false]Start
        String,
        ##GENIF[isEncrypted=false]End
        ##GENIF[isEncrypted=true]Start
        ##GENREMOVECOMMENTEncryptedType(),
        ##GENIF[isEncrypted=true]End
        default="",
        index=(
            plant_constants.
            other_flavor_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _some_big_int_val = Column(
        'some_big_int_val',
        BigInteger,
        default=0,
        index=(
            plant_constants.
            some_big_int_val_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _some_bit_val = Column(
        'some_bit_val',
        Boolean,
        default=False,
        index=(
            plant_constants.
            some_bit_val_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _some_date_val = Column(
        'some_date_val',
        Date,
        default=date(1753, 1, 1),
        index=(
            plant_constants.
            some_date_val_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _some_decimal_val = Column(
        'some_decimal_val',
        Numeric(precision=18, scale=6),
        default=0,
        index=(
            plant_constants.
            some_decimal_val_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _some_email_address = Column(
        'some_email_address',
        ##GENIF[isEncrypted=false]Start
        String,
        ##GENIF[isEncrypted=false]End
        ##GENIF[isEncrypted=true]Start
        ##GENREMOVECOMMENTEncryptedType(),
        ##GENIF[isEncrypted=true]End
        default="",
        index=(
            plant_constants.
            some_email_address_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _some_float_val = Column(
        'some_float_val',
        Float,
        default=0.0,
        index=(
            plant_constants.
            some_float_val_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _some_int_val = Column(
        'some_int_val',
        Integer,
        default=0,
        index=(
            plant_constants.
            some_int_val_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _some_money_val = Column(
        'some_money_val',
        Numeric(precision=18, scale=2),
        default=0,
        index=(
            plant_constants.
            some_money_val_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _some_n_var_char_val = Column(
        'some_n_var_char_val',
        ##GENIF[isEncrypted=false]Start
        String,
        ##GENIF[isEncrypted=false]End
        ##GENIF[isEncrypted=true]Start
        ##GENREMOVECOMMENTEncryptedType(),
        ##GENIF[isEncrypted=true]End
        default="",
        index=(
            plant_constants.
            some_n_var_char_val_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _some_phone_number = Column(
        'some_phone_number',
        ##GENIF[isEncrypted=false]Start
        String,
        ##GENIF[isEncrypted=false]End
        ##GENIF[isEncrypted=true]Start
        ##GENREMOVECOMMENTEncryptedType(),
        ##GENIF[isEncrypted=true]End
        default="",
        index=(
            plant_constants.
            some_phone_number_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _some_text_val = Column(
        'some_text_val',
        String,
        default="",
        index=(
            plant_constants.
            some_text_val_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _some_uniqueidentifier_val = Column(
        'some_uniqueidentifier_val',
        UUIDType(binary=False),
        default=uuid.uuid4,
        index=(
            plant_constants.
            some_uniqueidentifier_val_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _some_utc_date_time_val = Column(
        'some_utc_date_time_val',
        DateTime,
        default=datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc),
        index=(
            plant_constants.
            some_utc_date_time_val_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _some_var_char_val = Column(
        'some_var_char_val',
        ##GENIF[isEncrypted=false]Start
        String,
        ##GENIF[isEncrypted=false]End
        ##GENIF[isEncrypted=true]Start
        ##GENREMOVECOMMENTEncryptedType(),
        ##GENIF[isEncrypted=true]End
        default="",
        index=(
            plant_constants.
            some_var_char_val_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    flvr_foreign_key_code_peek: uuid.UUID = uuid.UUID(int=0)  # FlvrForeignKeyID  # noqa: E501
    land_code_peek: uuid.UUID = uuid.UUID(int=0)  # LandID  # noqa: E501
    _insert_utc_date_time = Column(
        'insert_utc_date_time',
        DateTime,
        nullable=True)
    _last_update_utc_date_time = Column(
        'last_update_utc_date_time',
        DateTime,
        nullable=True)

    __mapper_args__ = {
        'version_id_col': _last_change_code
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.code = kwargs.get('code', uuid.uuid4())
        self.last_change_code = kwargs.get(
            'last_change_code', 0)
        self.insert_user_id = kwargs.get(
            'insert_user_id', uuid.UUID(int=0))
        self.last_update_user_id = kwargs.get(
            'last_update_user_id', uuid.UUID(int=0))
        self.flvr_foreign_key_id = kwargs.get(
            'flvr_foreign_key_id', 0)
        self.is_delete_allowed = kwargs.get(
            'is_delete_allowed', False)
        self.is_edit_allowed = kwargs.get(
            'is_edit_allowed', False)
        self.land_id = kwargs.get(
            'land_id', 0)
        self.other_flavor = kwargs.get(
            'other_flavor', "")
        self.some_big_int_val = kwargs.get(
            'some_big_int_val', 0)
        self.some_bit_val = kwargs.get(
            'some_bit_val', False)
        self.some_date_val = kwargs.get(
            'some_date_val', date(1753, 1, 1))
        self.some_decimal_val = kwargs.get(
            'some_decimal_val', 0)
        self.some_email_address = kwargs.get(
            'some_email_address', "")
        self.some_float_val = kwargs.get(
            'some_float_val', 0.0)
        self.some_int_val = kwargs.get(
            'some_int_val', 0)
        self.some_money_val = kwargs.get(
            'some_money_val', 0)
        self.some_n_var_char_val = kwargs.get(
            'some_n_var_char_val', "")
        self.some_phone_number = kwargs.get(
            'some_phone_number', "")
        self.some_text_val = kwargs.get(
            'some_text_val', "")
        self.some_uniqueidentifier_val = kwargs.get(
            'some_uniqueidentifier_val', uuid.uuid4())
        self.some_utc_date_time_val = kwargs.get(
            'some_utc_date_time_val',
            datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc))
        self.some_var_char_val = kwargs.get(
            'some_var_char_val', "")
        self.insert_utc_date_time = kwargs.get(
            'insert_utc_date_time',
            datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc))
        self.last_update_utc_date_time = kwargs.get(
            'last_update_utc_date_time',
            datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc))
# endset
        self.flvr_foreign_key_code_peek = kwargs.get(  # FlvrForeignKeyID
            'flvr_foreign_key_code_peek', uuid.UUID(int=0))
        self.land_code_peek = kwargs.get(  # LandID
            'land_code_peek', uuid.UUID(int=0))
# endset

    @property
    def code(self):
        """
        Get the code of the plant.

        Returns:
            UUID: The code of the plant.
        """
        return uuid.UUID(str(self._code))

    @code.setter
    def code(self, value: uuid.UUID):
        """
        Set the code of the plant.

        Args:
            value (uuid.UUID): The code to set for the
                plant.

        Raises:
            TypeError: If the value is not of type uuid.UUID.

        """
        if isinstance(value, uuid.UUID):
            self._code = value
        else:
            self._code = uuid.UUID(value)
        self.last_update_utc_date_time = datetime.now(timezone.utc)

    @property
    def plant_id(self) -> int:
        """
        Get the ID of the plant.

        Returns:
            int: The ID of the plant.
        """
        return getattr(self, '_plant_id', 0) or 0

    @plant_id.setter
    def plant_id(self, value: int) -> None:
        """
        Set the plant_id.
        """

        self._plant_id = value

    @property
    def last_change_code(self) -> int:
        """
        Returns the last change code of the
        plant.

        :return: The last change code of the
            plant.
        :rtype: int
        """
        return getattr(self, '_last_change_code', 0) or 0

    @last_change_code.setter
    def last_change_code(self, value: int) -> None:
        """
        Set the last_change_code.
        """

        self._last_change_code = value

    @property
    def insert_user_id(self):
        """
        Inserts the user ID into the
        plant object.

        Returns:
            UUID: The UUID of the inserted user ID.
        """
        return uuid.UUID(str(self._insert_user_id))

    @insert_user_id.setter
    def insert_user_id(self, value):
        if isinstance(value, uuid.UUID):
            self._insert_user_id = value
        else:
            self._insert_user_id = uuid.UUID(value)
        self.last_update_utc_date_time = datetime.now(timezone.utc)

    @property
    def last_update_user_id(self):
        """
        Returns the UUID of the last user who updated the
        plant.

        :return: The UUID of the last update user.
        :rtype: UUID
        """
        return uuid.UUID(str(self._last_update_user_id))

    @last_update_user_id.setter
    def last_update_user_id(self, value):
        if isinstance(value, uuid.UUID):
            self._last_update_user_id = value
        else:
            self._last_update_user_id = uuid.UUID(value)
        self.last_update_utc_date_time = datetime.now(timezone.utc)

    @property
    def insert_utc_date_time(self) -> datetime:
        """
        Inserts the UTC date and time for the
        plant.

        Returns:
            datetime: The UTC date and time for the
                plant.
        """
        dt = getattr(
            self,
            '_insert_utc_date_time',
            datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc)
        ) or datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc)
        if dt is not None and dt.tzinfo is None:
            # Make the datetime aware (UTC) if it is naive
            dt = dt.replace(tzinfo=timezone.utc)
        return dt

    @insert_utc_date_time.setter
    def insert_utc_date_time(self, value: datetime) -> None:
        """
        Set the insert_utc_date_time.
        """
        if value is not None and value.tzinfo is None:
            # If the datetime is naive, assume UTC
            value = value.replace(tzinfo=timezone.utc)

        self._insert_utc_date_time = value

    @property
    def last_update_utc_date_time(self) -> datetime:
        """
        Returns the last update UTC date and time of the
        plant.

        :return: A datetime object representing the
            last update UTC date and time.
        """
        dt = getattr(
            self,
            '_last_update_utc_date_time',
            datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc)
        ) or datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc)

        if dt is not None and dt.tzinfo is None:
            # Make the datetime aware (UTC) if it is naive
            dt = dt.replace(tzinfo=timezone.utc)
        return dt

    @last_update_utc_date_time.setter
    def last_update_utc_date_time(self, value: datetime) -> None:
        """
        Set the last_update_utc_date_time.
        """
        if value is not None and value.tzinfo is None:
            # If the datetime is naive, assume UTC
            value = value.replace(tzinfo=timezone.utc)

        self._last_update_utc_date_time = value

    # isDeleteAllowed

    @property
    def is_delete_allowed(self) -> bool:
        """
        Check if the delete operation is allowed for the
        plant.

        Returns:
            bool: True if delete is allowed, False otherwise.
        """
        return getattr(self, '_is_delete_allowed', False) or False

    @is_delete_allowed.setter
    def is_delete_allowed(self, value: bool) -> None:
        """
        Set the is_delete_allowed.
        """

        self._is_delete_allowed = value
    # isEditAllowed

    @property
    def is_edit_allowed(self) -> bool:
        """
        Checks if editing is allowed for the
        plant.

        Returns:
            bool: True if editing is allowed, False otherwise.
        """
        return getattr(self, '_is_edit_allowed', False) or False

    @is_edit_allowed.setter
    def is_edit_allowed(self, value: bool) -> None:
        """
        Set the is_edit_allowed.
        """

        self._is_edit_allowed = value
    # otherFlavor

    @property
    def other_flavor(self) -> str:
        """
        Returns the other flavor of the
        plant.

        :return: The other flavor of the
            plant.
        :rtype: str
        """
        return getattr(self, '_other_flavor', "") or ""

    @other_flavor.setter
    def other_flavor(self, value: str) -> None:
        """
        Set the other_flavor.
        """

        self._other_flavor = value
    # someBigIntVal

    @property
    def some_big_int_val(self) -> int:
        """
        Returns the value of the '_some_big_int_val' attribute.

        If the attribute is not set, it returns 0.

        :return: The value of the '_some_big_int_val' attribute.
        :rtype: int
        """
        return getattr(self, '_some_big_int_val', 0) or 0

    @some_big_int_val.setter
    def some_big_int_val(self, value: int) -> None:
        """
        Set the some_big_int_val.
        """

        self._some_big_int_val = value
    # someBitVal

    @property
    def some_bit_val(self) -> bool:
        """
        Returns the value of the '_some_bit_val' attribute.

        :return: The value of the '_some_bit_val' attribute.
        :rtype: bool
        """
        return getattr(self, '_some_bit_val', False) or False

    @some_bit_val.setter
    def some_bit_val(self, value: bool) -> None:
        """
        Set the some_bit_val.
        """

        self._some_bit_val = value
    # someDecimalVal

    @property
    def some_decimal_val(self) -> Decimal:
        """
        Returns the value of the 'some_decimal_val' attribute.

        If the attribute is not set, it returns 0.

        :return: The value of the 'some_decimal_val' attribute.
        :rtype: Decimal
        """
        return getattr(self, '_some_decimal_val', Decimal(0)) or Decimal(0)

    @some_decimal_val.setter
    def some_decimal_val(self, value: Decimal) -> None:
        """
        Set the some_decimal_val.
        """

        self._some_decimal_val = value
    # someEmailAddress

    @property
    def some_email_address(self) -> str:
        """
        Returns the email address associated with the plant.

        :return: The email address as a string.
        """
        return getattr(self, '_some_email_address', "") or ""

    @some_email_address.setter
    def some_email_address(self, value: str) -> None:
        """
        Set the some_email_address.
        """

        self._some_email_address = value
    # someFloatVal

    @property
    def some_float_val(self) -> float:
        """
        Returns the value of the '_some_float_val' attribute as a float.
        If the attribute is not set, it returns 0.0.

        :return: The value of the '_some_float_val' attribute as a float.
        :rtype: float
        """
        return getattr(self, '_some_float_val', float(0)) or float(0)

    @some_float_val.setter
    def some_float_val(self, value: float) -> None:
        """
        Set the some_float_val.
        """

        self._some_float_val = value
    # someIntVal

    @property
    def some_int_val(self) -> int:
        """
        Returns the value of the '_some_int_val'
            attribute of the object.
        If the attribute is not set, it returns 0.

        :return: The value of the '_some_int_val'
            attribute or 0 if not set.
        :rtype: int
        """
        return getattr(self, '_some_int_val', 0) or 0

    @some_int_val.setter
    def some_int_val(self, value: int) -> None:
        """
        Set the some_int_val.
        """

        self._some_int_val = value
    # someMoneyVal

    @property
    def some_money_val(self) -> Decimal:
        """
        Returns the value of the 'some_money_val'
        attribute for the plant.

        This method retrieves the value of the
        'some_money_val' attribute from
        the plant object.
        If the attribute is not set, it returns 0.

        Returns:
            Decimal: The value of the 'some_money_val' attribute.
        """
        return getattr(self, '_some_money_val', Decimal(0)) or Decimal(0)

    @some_money_val.setter
    def some_money_val(self, value: Decimal) -> None:
        """
        Set the some_money_val.
        """

        self._some_money_val = value
    # someVarCharVal

    @property
    def some_var_char_val(self) -> str:
        """
        Returns the value of the _some_var_char_val attribute.

        :return: The value of _some_var_char_val attribute.
        :rtype: str
        """
        return getattr(self, '_some_var_char_val', "") or ""

    @some_var_char_val.setter
    def some_var_char_val(self, value: str) -> None:
        """
        Set the some_var_char_val.
        """

        self._some_var_char_val = value
    # someDateVal

    @property
    def some_date_val(self) -> date:
        """
        Returns the value of the '_some_date_val' attribute
        if it exists, otherwise returns the default date of January 1, 1753.

        :return: A date object representing the value of
            '_some_date_val'
            attribute or the default date.
        :rtype: date
        """
        return getattr(
            self,
            '_some_date_val',
            date(1753, 1, 1)
        ) or date(1753, 1, 1)

    @some_date_val.setter
    def some_date_val(self, value: date) -> None:
        """
        Set the some_date_val.
        """

        self._some_date_val = value
    # someUTCDateTimeVal

    @property
    def some_utc_date_time_val(self) -> datetime:
        """
        Get the value of some_utc_date_time_val property.

        Returns:
            datetime: The value of some_utc_date_time_val property.
        """
        dt = getattr(
            self,
            '_some_utc_date_time_val',
            datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc)
        ) or datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc)
        if dt is not None and dt.tzinfo is None:
            # Make the datetime aware (UTC) if it is naive
            dt = dt.replace(tzinfo=timezone.utc)
        return dt

    @some_utc_date_time_val.setter
    def some_utc_date_time_val(self, value: datetime) -> None:
        """
        Set the some_utc_date_time_val.
        """
        if value is not None and value.tzinfo is None:
            # If the datetime is naive, assume UTC
            value = value.replace(tzinfo=timezone.utc)
        self._some_utc_date_time_val = value
    # someNVarCharVal

    @property
    def some_n_var_char_val(self) -> str:
        """
        Returns the value of the 'some_n_var_char_val' attribute.

        :return: The value of the 'some_n_var_char_val' attribute.
        :rtype: str
        """
        return getattr(self, '_some_n_var_char_val', "") or ""

    @some_n_var_char_val.setter
    def some_n_var_char_val(self, value: str) -> None:
        """
        Set the some_n_var_char_val.
        """

        self._some_n_var_char_val = value
    # somePhoneNumber

    @property
    def some_phone_number(self) -> str:
        """
        Get the value of the 'some_phone_number' property.

        Returns:
            str: The value of the 'some_phone_number' property.
        """
        return getattr(self, '_some_phone_number', "") or ""

    @some_phone_number.setter
    def some_phone_number(self, value: str) -> None:
        """
        Set the some_phone_number.
        """

        self._some_phone_number = value
    # someUniqueidentifierVal

    @property
    def some_uniqueidentifier_val(self):
        """
        Returns the unique identifier as a UUID object.

        Returns:
            uuid.UUID: The unique identifier value.
        """

        return uuid.UUID(
            str(self._some_uniqueidentifier_val))

    @some_uniqueidentifier_val.setter
    def some_uniqueidentifier_val(self, value):
        """
        Sets the unique identifier value. The input
        can be either a uuid.UUID object or a string
        that can be converted to a uuid.UUID object.
        Updates the last_update_utc_date_time to the
        current naive UTC datetime.

        Args:
            value (uuid.UUID or str): The unique identifier
            value to set.

        Raises:
            ValueError: If the provided value cannot be
            converted to a uuid.UUID.
        """

        if isinstance(value, uuid.UUID):
            self._some_uniqueidentifier_val = value
        else:
            try:
                self._some_uniqueidentifier_val = uuid.UUID(value)
            except ValueError as e:
                raise ValueError(f"Invalid UUID value: {value}") from e
        self.last_update_utc_date_time = datetime.now(timezone.utc)
    # someTextVal

    @property
    def some_text_val(self) -> str:
        """
        Returns the value of the 'some_text_val' attribute.

        :return: The value of the 'some_text_val' attribute.
        :rtype: str
        """
        return getattr(self, '_some_text_val', "") or ""

    @some_text_val.setter
    def some_text_val(self, value: str) -> None:
        """
        Set the some_text_val.
        """

        self._some_text_val = value
    # flvrForeignKeyID
    # LandID
# endset
    # flvrForeignKeyID

    @property
    def flvr_foreign_key_id(self) -> int:
        """
        Get the foreign key ID for the flavor of the
        plant.

        Returns:
            int: The foreign key ID for the flavor of the
                plant.
        """
        return getattr(self, '_flvr_foreign_key_id', 0) or 0

    @flvr_foreign_key_id.setter
    def flvr_foreign_key_id(self, value: int) -> None:
        """
        Set the flvr_foreign_key_id.
        """

        self._flvr_foreign_key_id = value
    # LandID

    @property
    def land_id(self) -> int:
        """
        Get the ID of the land associated with this plant.

        Returns:
            int: The ID of the land.
        """
        return getattr(self, '_land_id', 0) or 0

    @land_id.setter
    def land_id(self, value: int) -> None:
        """
        Set the land_id.
        """

        self._land_id = value
# endset

    @staticmethod
    def property_list():
        """
        Returns a list of property names for
        the Plant model.

        Returns:
            list: A list of property names.
        """

        result = [
            "flvr_foreign_key_id",
            "is_delete_allowed",
            "is_edit_allowed",
            "land_id",
            "other_flavor",
            "some_big_int_val",
            "some_bit_val",
            "some_date_val",
            "some_decimal_val",
            "some_email_address",
            "some_float_val",
            "some_int_val",
            "some_money_val",
            "some_n_var_char_val",
            "some_phone_number",
            "some_text_val",
            "some_uniqueidentifier_val",
            "some_utc_date_time_val",
            "some_var_char_val",
# endset  # noqa: E122
            "code"
        ]
        return result


@event.listens_for(Plant, 'before_insert')
def set_created_on(
    mapper,
    connection,
    target
):  # pylint: disable=unused-argument
    """
    Set the created on and last update timestamps
    for a Plant object.

    Args:
        mapper: The SQLAlchemy mapper.
        connection: The SQLAlchemy connection.
        target: The Plant object
        being inserted.

    Returns:
        None
    """
    target.insert_utc_date_time = datetime.now(timezone.utc)
    target.last_update_utc_date_time = datetime.now(timezone.utc)


@event.listens_for(Plant, 'before_update')
def set_updated_on(
    mapper,
    connection,
    target
):  # pylint: disable=unused-argument
    """
    Sets the 'last_update_utc_date_time'
    attribute of
    the target object to the current UTC date and time.

    :param mapper: The SQLAlchemy mapper object.
    :param connection: The SQLAlchemy connection object.
    :param target: The target object to update.
    """
    target.last_update_utc_date_time = datetime.now(timezone.utc)
