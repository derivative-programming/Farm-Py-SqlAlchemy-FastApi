# models/tac.py
# pylint: disable=unused-import
"""
    #TODO add comment
"""
import uuid
from datetime import date, datetime
from sqlalchemy_utils import UUIDType
from sqlalchemy import (BigInteger, Boolean,   # noqa: F401
                        Column, Date, DateTime, Float,
                        ForeignKey, Index, Integer, Numeric, String,
                        event, func)
import models.constants.tac as tac_constants
from utils.common_functions import snake_case
from .base import Base, EncryptedType  # noqa: F401
class Tac(Base):
    """
    #TODO add comment
    """
    __tablename__ = 'farm_' + snake_case('Tac')
    _tac_id = Column(
        'tac_id',
        Integer,
        primary_key=True,
        autoincrement=True)
    _code = Column(
        'code',
        UUIDType(binary=False),
        unique=True,
        default=uuid.uuid4,
        nullable=True)
    last_change_code = Column(
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
    description = Column(
        'description',

        String,

        default="",
        index=(
            tac_constants.
            description_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    display_order = Column(
        'display_order',
        Integer,
        default=0,
        index=(
            tac_constants.
            display_order_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    is_active = Column(
        'is_active',
        Boolean,
        default=False,
        index=(
            tac_constants.
            is_active_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    lookup_enum_name = Column(
        'lookup_enum_name',

        String,

        default="",
        index=(
            tac_constants.
            lookup_enum_name_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    name = Column(
        'name',

        String,

        default="",
        index=(
            tac_constants.
            name_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    pac_id = Column(
        'pac_id',
        Integer,
        ForeignKey('farm_' + snake_case('Pac') + '.pac_id'),
        index=(
            tac_constants.
            pac_id_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    pac_code_peek = uuid.UUID  # PacID
    insert_utc_date_time = Column(
        'insert_utc_date_time',
        DateTime,
        nullable=True)
    last_update_utc_date_time = Column(
        'last_update_utc_date_time',
        DateTime,
        nullable=True)
    # no relationsip properties.
    # they are not updated immediately if the id prop is updated directly
    # pac = relationship('Pac', back_populates=snake_case('Pac'))
    # flavor = relationship('Flavor', back_populates=snake_case('Flavor'))
    __mapper_args__ = {
        'version_id_col': last_change_code
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
    def code(self, value):
        """
            #TODO add comment
        """
        if isinstance(value, uuid.UUID):
            self._code = value
        else:
            self._code = uuid.UUID(value)
        self.last_update_utc_date_time = datetime.utcnow()
    @property
    def tac_id(self) -> int:
        """
            #TODO add comment
        """
        return getattr(self, '_tac_id', 0) or 0
    @tac_id.setter
    def tac_id(self, value: int) -> None:
        """
        Set the tac_id.
        """
        self._tac_id = value
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
    # description,
    # displayOrder,
    # isActive,
    # lookupEnumName,
    # name,
    # PacID
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
@event.listens_for(Tac, 'before_insert')
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
@event.listens_for(Tac, 'before_update')
def set_updated_on(
    mapper,
    connection,
    target
):  # pylint: disable=unused-argument
    """
        #TODO add comment
    """
    target.last_update_utc_date_time = datetime.utcnow()
