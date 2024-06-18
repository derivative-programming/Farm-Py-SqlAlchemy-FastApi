# models/flavor.py
# pylint: disable=unused-import
"""
    #TODO add comment
"""
from decimal import Decimal
import uuid
from datetime import date, datetime
from sqlalchemy_utils import UUIDType
from sqlalchemy import (BigInteger, Boolean,   # noqa: F401
                        Column, Date, DateTime, Float,
                        ForeignKey, Index, Integer, Numeric, String,
                        event, func)
import models.constants.flavor as flavor_constants
from utils.common_functions import snake_case
from .base import Base, EncryptedType  # noqa: F401
class Flavor(Base):
    """
    #TODO add comment
    """
    __tablename__ = 'farm_' + snake_case('Flavor')
    _flavor_id = Column(
        'flavor_id',
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
    _description = Column(
        'description',

        String,

        default="",
        index=(
            flavor_constants.
            description_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _display_order = Column(
        'display_order',
        Integer,
        default=0,
        index=(
            flavor_constants.
            display_order_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _is_active = Column(
        'is_active',
        Boolean,
        default=False,
        index=(
            flavor_constants.
            is_active_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _lookup_enum_name = Column(
        'lookup_enum_name',

        String,

        default="",
        index=(
            flavor_constants.
            lookup_enum_name_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _name = Column(
        'name',

        String,

        default="",
        index=(
            flavor_constants.
            name_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _pac_id = Column(
        'pac_id',
        Integer,
        ForeignKey('farm_' + snake_case('Pac') + '.pac_id'),
        index=(
            flavor_constants.
            pac_id_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    pac_code_peek = uuid.UUID  # PacID
    _insert_utc_date_time = Column(
        'insert_utc_date_time',
        DateTime,
        nullable=True)
    _last_update_utc_date_time = Column(
        'last_update_utc_date_time',
        DateTime,
        nullable=True)
    # no relationsip properties.
    # they are not updated immediately if the id prop is updated directly
    # pac = relationship('Pac', back_populates=snake_case('Pac'))
    # flavor = relationship('Flavor', back_populates=snake_case('Flavor'))
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
        self.description = kwargs.get(
            'description', "")
        self.display_order = kwargs.get(
            'display_order', 0)
        self.is_active = kwargs.get(
            'is_active', False)
        self.lookup_enum_name = kwargs.get(
            'lookup_enum_name', "")
        self.name = kwargs.get(
            'name', "")
        self.pac_id = kwargs.get(
            'pac_id', 0)
        self.insert_utc_date_time = kwargs.get(
            'insert_utc_date_time', datetime(1753, 1, 1))
        self.last_update_utc_date_time = kwargs.get(
            'last_update_utc_date_time', datetime(1753, 1, 1))
# endset
        self.pac_code_peek = kwargs.get(  # PacID
            'pac_code_peek', uuid.UUID(int=0))
# endset
    @property
    def code(self):
        """
            #TODO add comment
        """
        return uuid.UUID(str(self._code))
    @code.setter
    def code(self, value: uuid.UUID):
        """
            #TODO add comment
        """
        if isinstance(value, uuid.UUID):
            self._code = value
        else:
            self._code = uuid.UUID(value)
        self.last_update_utc_date_time = datetime.utcnow()
    @property
    def flavor_id(self) -> int:
        """
            #TODO add comment
        """
        return getattr(self, '_flavor_id', 0) or 0
    @flavor_id.setter
    def flavor_id(self, value: int) -> None:
        """
        Set the flavor_id.
        """
        self._flavor_id = value
    @property
    def last_change_code(self) -> int:
        """
            #TODO add comment
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
            #TODO add comment
        """
        return uuid.UUID(str(self._insert_user_id))
    @insert_user_id.setter
    def insert_user_id(self, value):
        if isinstance(value, uuid.UUID):
            self._insert_user_id = value
        else:
            self._insert_user_id = uuid.UUID(value)
        self.last_update_utc_date_time = datetime.utcnow()
    @property
    def last_update_user_id(self):
        """
            #TODO add comment
        """
        return uuid.UUID(str(self._last_update_user_id))
    @last_update_user_id.setter
    def last_update_user_id(self, value):
        if isinstance(value, uuid.UUID):
            self._last_update_user_id = value
        else:
            self._last_update_user_id = uuid.UUID(value)
        self.last_update_utc_date_time = datetime.utcnow()
    @property
    def insert_utc_date_time(self) -> datetime:
        """
            #TODO add comment
        """
        return getattr(
            self,
            '_insert_utc_date_time',
            datetime(1753, 1, 1)
        ) or datetime(1753, 1, 1)
    @insert_utc_date_time.setter
    def insert_utc_date_time(self, value: datetime) -> None:
        """
        Set the insert_utc_date_time.
        """
        self._insert_utc_date_time = value
    @property
    def last_update_utc_date_time(self) -> datetime:
        """
            #TODO add comment
        """
        return getattr(
            self,
            '_last_update_utc_date_time',
            datetime(1753, 1, 1)
        ) or datetime(1753, 1, 1)
    @last_update_utc_date_time.setter
    def last_update_utc_date_time(self, value: datetime) -> None:
        """
        Set the last_update_utc_date_time.
        """
        self._last_update_utc_date_time = value
    # description,
    @property
    def description(self) -> str:
        """
            #TODO add comment
        """
        return getattr(self, '_description', "") or ""
    @description.setter
    def description(self, value: str) -> None:
        """
        Set the description.
        """
        self._description = value
    # displayOrder,
    @property
    def display_order(self) -> int:
        """
            #TODO add comment
        """
        return getattr(self, '_display_order', 0) or 0
    @display_order.setter
    def display_order(self, value: int) -> None:
        """
        Set the display_order.
        """
        self._display_order = value
    # isActive,
    @property
    def is_active(self) -> bool:
        """
            #TODO add comment
        """
        return getattr(self, '_is_active', False) or False
    @is_active.setter
    def is_active(self, value: bool) -> None:
        """
        Set the is_active.
        """
        self._is_active = value
    # lookupEnumName,
    @property
    def lookup_enum_name(self) -> str:
        """
            #TODO add comment
        """
        return getattr(self, '_lookup_enum_name', "") or ""
    @lookup_enum_name.setter
    def lookup_enum_name(self, value: str) -> None:
        """
        Set the lookup_enum_name.
        """
        self._lookup_enum_name = value
    # name,
    @property
    def name(self) -> str:
        """
            #TODO add comment
        """
        return getattr(self, '_name', "") or ""
    @name.setter
    def name(self, value: str) -> None:
        """
        Set the name.
        """
        self._name = value
    # PacID
    @property
    def pac_id(self) -> int:
        """
            #TODO add comment
        """
        return getattr(self, '_pac_id', 0) or 0
    @pac_id.setter
    def pac_id(self, value: int) -> None:
        """
        Set the pac_id.
        """
        self._pac_id = value
    @property
    def some_text_val(self) -> str:
        """
            #TODO add comment
        """
        return getattr(self, '_some_text_val', "") or ""
    @some_text_val.setter
    def some_text_val(self, value: str) -> None:
        """
        Set the some_text_val.
        """
        self._some_text_val = value
# endset
    @staticmethod
    def property_list():
        """
            #TODO add comment
        """
        result = [
            "description",
            "display_order",
            "is_active",
            "lookup_enum_name",
            "name",
            "pac_id",
# endset  # noqa: E122
            "code"
        ]
        return result
@event.listens_for(Flavor, 'before_insert')
def set_created_on(
    mapper,
    connection,
    target
):  # pylint: disable=unused-argument
    """
        #TODO add comment
    """
    target.insert_utc_date_time = datetime.utcnow()
    target.last_update_utc_date_time = datetime.utcnow()
@event.listens_for(Flavor, 'before_update')
def set_updated_on(
    mapper,
    connection,
    target
):  # pylint: disable=unused-argument
    """
        #TODO add comment
    """
    target.last_update_utc_date_time = datetime.utcnow()
