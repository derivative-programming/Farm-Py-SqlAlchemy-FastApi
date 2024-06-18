# models/org_customer.py
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
import models.constants.org_customer as org_customer_constants
from utils.common_functions import snake_case
from .base import Base, EncryptedType  # noqa: F401
class OrgCustomer(Base):
    """
    #TODO add comment
    """
    __tablename__ = 'farm_' + snake_case('OrgCustomer')
    _org_customer_id = Column(
        'org_customer_id',
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
    _customer_id = Column(
        'customer_id',
        Integer,
        ForeignKey('farm_' + snake_case('Customer') + '.customer_id'),
        index=(
            org_customer_constants.
            customer_id_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _email = Column(
        'email',

        String,

        default="",
        index=(
            org_customer_constants.
            email_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _organization_id = Column(
        'organization_id',
        Integer,
        ForeignKey('farm_' + snake_case('Organization') + '.organization_id'),
        index=(
            org_customer_constants.
            organization_id_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    customer_code_peek = uuid.UUID  # CustomerID
    organization_code_peek = uuid.UUID  # OrganizationID
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
    # organization = relationship('Organization', back_populates=snake_case('Organization'))
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
        self.customer_id = kwargs.get(
            'customer_id', 0)
        self.email = kwargs.get(
            'email', "")
        self.organization_id = kwargs.get(
            'organization_id', 0)
        self.insert_utc_date_time = kwargs.get(
            'insert_utc_date_time', datetime(1753, 1, 1))
        self.last_update_utc_date_time = kwargs.get(
            'last_update_utc_date_time', datetime(1753, 1, 1))
# endset
        self.customer_code_peek = kwargs.get(  # CustomerID
            'customer_code_peek', uuid.UUID(int=0))
        self.organization_code_peek = kwargs.get(  # OrganizationID
            'organization_code_peek', uuid.UUID(int=0))
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
    def org_customer_id(self) -> int:
        """
            #TODO add comment
        """
        return getattr(self, '_org_customer_id', 0) or 0
    @org_customer_id.setter
    def org_customer_id(self, value: int) -> None:
        """
        Set the org_customer_id.
        """
        self._org_customer_id = value
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
    # customerID
    @property
    def customer_id(self) -> int:
        """
            #TODO add comment
        """
        return getattr(self, '_customer_id', 0) or 0
    @customer_id.setter
    def customer_id(self, value: int) -> None:
        """
        Set the customer_id.
        """
        self._customer_id = value
    # email,
    @property
    def email(self) -> str:
        """
            #TODO add comment
        """
        return getattr(self, '_email', "") or ""
    @email.setter
    def email(self, value: str) -> None:
        """
        Set the email.
        """
        self._email = value
    # OrganizationID
    @property
    def organization_id(self) -> int:
        """
            #TODO add comment
        """
        return getattr(self, '_organization_id', 0) or 0
    @organization_id.setter
    def organization_id(self, value: int) -> None:
        """
        Set the organization_id.
        """
        self._organization_id = value
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
            "customer_id",
            "email",
            "organization_id",
# endset  # noqa: E122
            "code"
        ]
        return result
@event.listens_for(OrgCustomer, 'before_insert')
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
@event.listens_for(OrgCustomer, 'before_update')
def set_updated_on(
    mapper,
    connection,
    target
):  # pylint: disable=unused-argument
    """
        #TODO add comment
    """
    target.last_update_utc_date_time = datetime.utcnow()
