# models/dft_dependency.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import

"""
The DFTDependency model inherits from
the Base model and is mapped to the
'farm_DFTDependency' table in the database.
"""
from decimal import Decimal  # noqa: F401
import uuid  # noqa: F401
from datetime import date, datetime, timezone  # noqa: F401
from sqlalchemy_utils import UUIDType
from sqlalchemy import (BigInteger, Boolean,   # noqa: F401
                        Column, Date, DateTime, Float,
                        ForeignKey, Index, Integer, Numeric, String,
                        event, func)
import models.constants.dft_dependency as \
    dft_dependency_constants
from utils.common_functions import snake_case
from .base import Base, EncryptedType  # noqa: F401


class DFTDependency(Base):
    """
    The DFTDependency model represents a
    dft_dependency in the farm.
    It inherits from the Base model and is mapped to the
    'farm_DFTDependency' table in the database.
    """

    __tablename__ = 'farm_' + snake_case('DFTDependency')

    _dft_dependency_id = Column(
        'dft_dependency_id',
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
    _dependency_df_task_id = Column(
        'dependency_df_task_id',
        Integer,
        default=0,
        index=(
            dft_dependency_constants.
            dependency_df_task_id_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _dyna_flow_task_id = Column(
        'dyna_flow_task_id',
        Integer,
        ForeignKey('farm_' + snake_case('DynaFlowTask') + '.dyna_flow_task_id'),
        index=(
            dft_dependency_constants.
            dyna_flow_task_id_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    _is_placeholder = Column(
        'is_placeholder',
        Boolean,
        default=False,
        index=(
            dft_dependency_constants.
            is_placeholder_calculatedIsDBColumnIndexed
        ),
        nullable=True)
    dyna_flow_task_code_peek: uuid.UUID = uuid.UUID(int=0)  # DynaFlowTaskID  # noqa: E501
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
        self.dependency_df_task_id = kwargs.get(
            'dependency_df_task_id', 0)
        self.dyna_flow_task_id = kwargs.get(
            'dyna_flow_task_id', 0)
        self.is_placeholder = kwargs.get(
            'is_placeholder', False)
        self.insert_utc_date_time = kwargs.get(
            'insert_utc_date_time',
            datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc))
        self.last_update_utc_date_time = kwargs.get(
            'last_update_utc_date_time',
            datetime(1753, 1, 1, 0, 0, tzinfo=timezone.utc))
        self.dyna_flow_task_code_peek = kwargs.get(  # DynaFlowTaskID
            'dyna_flow_task_code_peek', uuid.UUID(int=0))

    @property
    def code(self):
        """
        Get the code of the dft_dependency.

        Returns:
            UUID: The code of the dft_dependency.
        """
        return uuid.UUID(str(self._code))

    @code.setter
    def code(self, value: uuid.UUID):
        """
        Set the code of the dft_dependency.

        Args:
            value (uuid.UUID): The code to set for the
                dft_dependency.

        Raises:
            TypeError: If the value is not of type uuid.UUID.

        """
        if isinstance(value, uuid.UUID):
            self._code = value
        else:
            self._code = uuid.UUID(value)
        self.last_update_utc_date_time = datetime.now(timezone.utc)

    @property
    def dft_dependency_id(self) -> int:
        """
        Get the ID of the dft_dependency.

        Returns:
            int: The ID of the dft_dependency.
        """
        return getattr(self, '_dft_dependency_id', 0) or 0

    @dft_dependency_id.setter
    def dft_dependency_id(self, value: int) -> None:
        """
        Set the dft_dependency_id.
        """

        self._dft_dependency_id = value

    @property
    def last_change_code(self) -> int:
        """
        Returns the last change code of the
        dft_dependency.

        :return: The last change code of the
            dft_dependency.
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
        dft_dependency object.

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
        dft_dependency.

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
        dft_dependency.

        Returns:
            datetime: The UTC date and time for the
                dft_dependency.
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
        dft_dependency.

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
    # dependencyDFTaskID

    @property
    def dependency_df_task_id(self) -> int:
        """
        Returns the value of the '_dependency_df_task_id'
            attribute of the object.
        If the attribute is not set, it returns 0.

        :return: The value of the '_dependency_df_task_id'
            attribute or 0 if not set.
        :rtype: int
        """
        return getattr(self, '_dependency_df_task_id', 0) or 0

    @dependency_df_task_id.setter
    def dependency_df_task_id(self, value: int) -> None:
        """
        Set the dependency_df_task_id.
        """

        self._dependency_df_task_id = value
    # DynaFlowTaskID
    # isPlaceholder

    @property
    def is_placeholder(self) -> bool:
        """
        Check if the delete operation is allowed for the
        dft_dependency.

        Returns:
            bool: True if delete is allowed, False otherwise.
        """
        return getattr(self, '_is_placeholder', False) or False

    @is_placeholder.setter
    def is_placeholder(self, value: bool) -> None:
        """
        Set the is_placeholder.
        """

        self._is_placeholder = value
    # DynaFlowTaskID
    @property
    def dyna_flow_task_id(self) -> int:
        """
        Get the ID of the dyna_flow_task associated with this dft_dependency.

        Returns:
            int: The ID of the dyna_flow_task.
        """
        return getattr(self, '_dyna_flow_task_id', 0) or 0

    @dyna_flow_task_id.setter
    def dyna_flow_task_id(self, value: int) -> None:
        """
        Set the dyna_flow_task_id.
        """

        self._dyna_flow_task_id = value

    @staticmethod
    def property_list():
        """
        Returns a list of property names for
        the DFTDependency model.

        Returns:
            list: A list of property names.
        """

        result = [
            "dependency_df_task_id",
            "dyna_flow_task_id",
            "is_placeholder",
# endset  # noqa: E122
            "code"
        ]
        return result


@event.listens_for(DFTDependency, 'before_insert')
def set_created_on(
    mapper,
    connection,
    target
):  # pylint: disable=unused-argument
    """
    Set the created on and last update timestamps
    for a DFTDependency object.

    Args:
        mapper: The SQLAlchemy mapper.
        connection: The SQLAlchemy connection.
        target: The DFTDependency object
        being inserted.

    Returns:
        None
    """
    target.insert_utc_date_time = datetime.now(timezone.utc)
    target.last_update_utc_date_time = datetime.now(timezone.utc)


@event.listens_for(DFTDependency, 'before_update')
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
