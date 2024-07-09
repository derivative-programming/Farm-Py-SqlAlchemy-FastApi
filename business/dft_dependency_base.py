# business/dft_dependency_base.py  # pylint: disable=duplicate-code # noqa: E501
# pylint: disable=unused-import

"""
This module contains the
DFTDependencyBaseBusObj class,
which represents the base
business object for a
DFTDependency.
"""

from decimal import Decimal  # noqa: F401
import random
from typing import Optional
import uuid  # noqa: F401
from datetime import datetime, date  # noqa: F401
from helpers.session_context import SessionContext
from managers import DFTDependencyManager
from models import DFTDependency
import models
import managers as managers_and_enums
from .base_bus_obj import BaseBusObj

NOT_INITIALIZED_ERROR_MESSAGE = (
    "DFTDependency object is not initialized")


class DFTDependencyInvalidInitError(Exception):
    """
    Exception raised when the
    DFTDependency object
    is not initialized properly.
    """


class DFTDependencyBaseBusObj(BaseBusObj):
    """
    This class represents the base business object
    for a DFTDependency.
    It requires a valid session context for initialization.
    """

    def __init__(
        self,
        session_context: SessionContext,
        dft_dependency: Optional[DFTDependency] = None
    ):
        """
        Initializes a new instance of the
        DFTDependencyBusObj class.

        :param session_context: The session context.
        :raises ValueError: If the session is not provided.
        """

        if not session_context.session:
            raise ValueError("session required")

        if dft_dependency is None:
            dft_dependency = DFTDependency()

        self._session_context = session_context

        self.dft_dependency = dft_dependency

    @property
    def dft_dependency_id(self) -> int:
        """
        Get the dft_dependency ID from the
        DFTDependency object.

        :return: The dft_dependency ID.
        :raises AttributeError: If the
            DFTDependency object is not initialized.
        """

        if not self.dft_dependency:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dft_dependency.dft_dependency_id
    # code

    @property
    def code(self):
        """
        Get the code from the
        DFTDependency object.

        :return: The code.
        :raises AttributeError: If the
            DFTDependency object is not initialized.
        """

        if not self.dft_dependency:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dft_dependency.code

    @code.setter
    def code(self, value: uuid.UUID):  # type: ignore
        """
        Set the code for the DFTDependency object.

        :param value: The code value.
        :raises AttributeError: If the
            DFTDependency object is not initialized.
        :raises ValueError: If the code is not a UUID.
        """

        if not self.dft_dependency:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, uuid.UUID):
            raise ValueError("code must be a UUID.")

        self.dft_dependency.code = value
    # last_change_code

    @property
    def last_change_code(self):
        """
        Get the last change code from the
        DFTDependency object.

        :return: The last change code.
        :raises AttributeError: If the
            DFTDependency object is not initialized.
        """

        if not self.dft_dependency:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dft_dependency.last_change_code

    @last_change_code.setter
    def last_change_code(self, value: int):
        """
        Set the last change code for the
        DFTDependency object.

        :param value: The last change code value.
        :raises AttributeError: If the
            DFTDependency object is not initialized.
        :raises ValueError: If the last change code is not an integer.
        """

        if not self.dft_dependency:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, int):
            raise ValueError("last_change_code must be an integer.")

        self.dft_dependency.last_change_code = value
    # insert_user_id

    @property
    def insert_user_id(self):
        """
        Get the insert user ID from the
        DFTDependency object.

        :return: The insert user ID.
        :raises AttributeError: If the
            DFTDependency object is not initialized.
        """

        if not self.dft_dependency:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dft_dependency.insert_user_id

    @insert_user_id.setter
    def insert_user_id(self, value: uuid.UUID):
        """
        Set the insert user ID for the
        DFTDependency object.

        :param value: The insert user ID value.
        :raises AttributeError: If the
            DFTDependency object is not initialized.
        :raises ValueError: If the insert user ID is not a UUID.
        """

        if not self.dft_dependency:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, uuid.UUID):
            raise ValueError(
                "insert_user_id must be a UUID.")

        self.dft_dependency.insert_user_id = value
    # last_update_user_id

    @property
    def last_update_user_id(self):
        """
        Get the last update user ID from the
        DFTDependency object.

        :return: The last update user ID.
        :raises AttributeError: If the
            DFTDependency object is not initialized.
        """

        if not self.dft_dependency:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dft_dependency.last_update_user_id

    @last_update_user_id.setter
    def last_update_user_id(self, value: uuid.UUID):
        """
        Set the last update user ID for the
        DFTDependency object.

        :param value: The last update user ID value.
        :raises AttributeError: If the
            DFTDependency object is not initialized.
        :raises ValueError: If the last update user ID is not a UUID.
        """

        if not self.dft_dependency:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, uuid.UUID):
            raise ValueError(
                "last_update_user_id must be a UUID.")

        self.dft_dependency.last_update_user_id = value

    # dependencyDFTaskID

    @property
    def dependency_df_task_id(self):
        """
        Returns the value of
        dependency_df_task_id attribute of the
        dft_dependency.

        Raises:
            AttributeError: If the
                dft_dependency is not initialized.

        Returns:
            int: The value of
                dependency_df_task_id attribute.
        """
        if not self.dft_dependency:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dft_dependency.dependency_df_task_id

    @dependency_df_task_id.setter
    def dependency_df_task_id(self, value):
        """
        Sets the value of
        dependency_df_task_id for the
        dft_dependency.

        Args:
            value (int): The integer value to set for
                dependency_df_task_id.

        Raises:
            AttributeError: If the
                dft_dependency is not initialized.

        """
        if not self.dft_dependency:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, int), (
            "dependency_df_task_id must be an integer")
        self.dft_dependency.dependency_df_task_id = value
    # DynaFlowTaskID
    # isPlaceholder

    @property
    def is_placeholder(self):
        """
        Get the Is Placeholder flag from the
        DFTDependency object.

        :return: The Is Placeholder flag.
        :raises AttributeError: If the
            DFTDependency object is not initialized.
        """

        if not self.dft_dependency:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dft_dependency.is_placeholder

    @is_placeholder.setter
    def is_placeholder(self, value: bool):
        """
        Set the Is Placeholder flag for the
        DFTDependency object.

        :param value: The Is Placeholder flag value.
        :raises AttributeError: If the
            DFTDependency object is not initialized.
        :raises ValueError: If the Is Placeholder flag is not a boolean.
        """

        if not self.dft_dependency:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if not isinstance(value, bool):
            raise ValueError(
                "is_placeholder must be a boolean.")

        self.dft_dependency.is_placeholder = value
    # dependencyDFTaskID
    # DynaFlowTaskID

    @property
    def dyna_flow_task_id(self):
        """
        Returns the dyna_flow_task ID
        associated with the
        dft_dependency.

        Raises:
            AttributeError: If the
                dft_dependency is not initialized.

        Returns:
            int: The dyna_flow_task ID of the dft_dependency.
        """
        if not self.dft_dependency:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dft_dependency.dyna_flow_task_id

    @dyna_flow_task_id.setter
    def dyna_flow_task_id(self, value):
        """
        Sets the dyna_flow_task ID
        for the dft_dependency.

        Args:
            value (int or None): The
                dyna_flow_task ID to be set.
                Must be an integer or None.

        Raises:
            AttributeError: If the
                dft_dependency is not initialized.

        """
        if not self.dft_dependency:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, int) or value is None, (
            "dyna_flow_task_id must be an integer or None")

        self.dft_dependency.dyna_flow_task_id = value

    @property
    def dyna_flow_task_code_peek(self) -> uuid.UUID:
        """
        Returns the dyna_flow_task id code peek
        of the dft_dependency.

        Raises:
            AttributeError: If the
            dft_dependency is not initialized.

        Returns:
            uuid.UUID: The dyna_flow_task id code peek
            of the dft_dependency.
        """
        if not self.dft_dependency:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dft_dependency.dyna_flow_task_code_peek
    # isPlaceholder
    # insert_utc_date_time

    @property
    def insert_utc_date_time(self):
        """
        Inserts the UTC date and time into
        the dft_dependency object.

        Raises:
            AttributeError: If the
                dft_dependency object is not initialized.

        Returns:
            The UTC date and time inserted into the
            dft_dependency object.
        """
        if not self.dft_dependency:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dft_dependency.insert_utc_date_time

    @insert_utc_date_time.setter
    def insert_utc_date_time(self, value):
        """
        Inserts the UTC date and time for the
        dft_dependency.

        Args:
            value (datetime): The UTC date and time to be inserted.
                It should be a datetime object or None.

        Raises:
            AttributeError: If the
                dft_dependency is not initialized.

        """
        if not self.dft_dependency:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, datetime) or value is None, (
            "insert_utc_date_time must be "
            "a datetime object or None")

        self.dft_dependency.insert_utc_date_time = value

    # update_utc_date_time
    @property
    def last_update_utc_date_time(self):
        """
        Returns the last update UTC date and time
        of the dft_dependency.

        Raises:
            AttributeError: If the
                dft_dependency is not initialized.

        Returns:
            datetime: The last update UTC date and time
                of the dft_dependency.
        """
        if not self.dft_dependency:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dft_dependency.last_update_utc_date_time

    @last_update_utc_date_time.setter
    def last_update_utc_date_time(self, value):
        """
        Sets the last update UTC date and time
        for the dft_dependency.

        Args:
            value (datetime): The datetime object
                representing the last update UTC date and time.
                Pass None to unset the value.

        Raises:
            AttributeError: If the
                dft_dependency is not initialized.

        """
        if not self.dft_dependency:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        assert isinstance(value, datetime) or value is None, (
            "last_update_utc_date_time "
            "must be a datetime object or None")

        self.dft_dependency.last_update_utc_date_time = value

    async def load_from_json(
        self,
        json_data: str
    ):
        """
        Load dft_dependency data
        from JSON string.

        :param json_data: JSON string containing
            dft_dependency data.
        :raises ValueError: If json_data is not a string
            or if no dft_dependency
            data is found.
        """

        if not isinstance(json_data, str):
            raise ValueError(
                "json_data must be a string")

        dft_dependency_manager = DFTDependencyManager(
            self._session_context)
        self.dft_dependency = await \
            dft_dependency_manager.from_json(json_data)

        return self

    async def load_from_code(
        self,
        code: uuid.UUID
    ):
        """
        Load dft_dependency
        data from UUID code.

        :param code: UUID code for loading a specific
            dft_dependency.
        :raises ValueError: If code is not a UUID or if no
            dft_dependency data is found.
        """
        if not isinstance(code, uuid.UUID):
            raise ValueError(
                "code must be a UUID")

        dft_dependency_manager = DFTDependencyManager(
            self._session_context)
        dft_dependency_obj = await dft_dependency_manager.get_by_code(
            code)
        self.dft_dependency = dft_dependency_obj

        return self

    async def load_from_id(
        self,
        dft_dependency_id: int
    ):
        """
        Load dft_dependency data from
        dft_dependency ID.

        :param dft_dependency_id: Integer ID for loading a specific
            dft_dependency.
        :raises ValueError: If dft_dependency_id
            is not an integer or
            if no dft_dependency
            data is found.
        """

        if not isinstance(dft_dependency_id, int):
            raise ValueError(
                "dft_dependency_id must be an integer")

        dft_dependency_manager = DFTDependencyManager(
            self._session_context)
        dft_dependency_obj = await dft_dependency_manager.get_by_id(
            dft_dependency_id)
        self.dft_dependency = dft_dependency_obj

        return self

    def load_from_obj_instance(
        self,
        dft_dependency_obj_instance: DFTDependency
    ):
        """
        Use the provided
        DFTDependency instance.

        :param dft_dependency_obj_instance: Instance of the
            DFTDependency class.
        :raises ValueError: If dft_dependency_obj_instance
            is not an instance of
            DFTDependency.
        """

        if not isinstance(dft_dependency_obj_instance,
                          DFTDependency):
            raise ValueError(
                "dft_dependency_obj_instance must be an "
                "instance of DFTDependency")

        self.dft_dependency = dft_dependency_obj_instance

        return self

    async def load_from_dict(
        self,
        dft_dependency_dict: dict
    ):
        """
        Load dft_dependency data
        from dictionary.

        :param dft_dependency_dict: Dictionary containing
            dft_dependency data.
        :raises ValueError: If dft_dependency_dict
            is not a
            dictionary or if no
            dft_dependency data is found.
        """
        if not isinstance(dft_dependency_dict, dict):
            raise ValueError(
                "dft_dependency_dict must be a dictionary")

        dft_dependency_manager = DFTDependencyManager(
            self._session_context)

        self.dft_dependency = await \
            dft_dependency_manager.from_dict(
                dft_dependency_dict)

        return self

    def get_session_context(self):
        """
        Returns the session context.

        :return: The session context.
        :rtype: SessionContext
        """
        return self._session_context

    async def refresh(self):
        """
        Refreshes the dft_dependency
        object by fetching
        the latest data from the database.

        Returns:
            The updated
            dft_dependency object.
        """
        dft_dependency_manager = DFTDependencyManager(
            self._session_context)
        self.dft_dependency = await \
            dft_dependency_manager.refresh(
                self.dft_dependency)

        return self

    def is_valid(self):
        """
        Check if the dft_dependency
        is valid.

        Returns:
            bool: True if the dft_dependency
                is valid, False otherwise.
        """
        return self.dft_dependency is not None

    def to_dict(self):
        """
        Converts the DFTDependency
        object to a dictionary representation.

        Returns:
            dict: A dictionary representation of the
                DFTDependency object.
        """
        dft_dependency_manager = DFTDependencyManager(
            self._session_context)
        return dft_dependency_manager.to_dict(
            self.dft_dependency)

    def to_json(self):
        """
        Converts the dft_dependency
        object to a JSON representation.

        Returns:
            str: The JSON representation of the
                dft_dependency object.
        """
        dft_dependency_manager = DFTDependencyManager(
            self._session_context)
        return dft_dependency_manager.to_json(
            self.dft_dependency)

    async def save(self):
        """
        Saves the dft_dependency object
        to the database.

        If the dft_dependency object
        is not initialized, an AttributeError is raised.
        If the dft_dependency_id
        is greater than 0, the
        dft_dependency is
        updated in the database.
        If the dft_dependency_id is 0,
        the dft_dependency is
        added to the database.

        Returns:
            The updated or added
            dft_dependency object.

        Raises:
            AttributeError: If the dft_dependency
            object is not initialized.
        """
        if not self.dft_dependency:
            raise AttributeError(NOT_INITIALIZED_ERROR_MESSAGE)

        dft_dependency_id = self.dft_dependency.dft_dependency_id

        if dft_dependency_id > 0:
            dft_dependency_manager = DFTDependencyManager(
                self._session_context)
            self.dft_dependency = await \
                dft_dependency_manager.update(
                    self.dft_dependency)

        if dft_dependency_id == 0:
            dft_dependency_manager = DFTDependencyManager(
                self._session_context)
            self.dft_dependency = await \
                dft_dependency_manager.add(
                    self.dft_dependency)

        return self

    async def delete(self):
        """
        Deletes the dft_dependency
        from the database.

        Raises:
            AttributeError: If the dft_dependency
                is not initialized.
        """
        if not self.dft_dependency:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        if self.dft_dependency.dft_dependency_id > 0:
            dft_dependency_manager = DFTDependencyManager(
                self._session_context)
            await dft_dependency_manager.delete(
                self.dft_dependency.dft_dependency_id)
            self.dft_dependency = None

    async def randomize_properties(self):
        """
        Randomizes the properties of the
        dft_dependency object.

        This method generates random values for various
        properties of the dft_dependency
        object

        Returns:
            self: The current instance of the
                DFTDependency class.

        Raises:
            AttributeError: If the dft_dependency
                object is not initialized.
        """
        if not self.dft_dependency:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        self.dft_dependency.dependency_df_task_id = (
            random.randint(0, 100))
        # dyna_flow_task_id
        self.dft_dependency.is_placeholder = (
            random.choice([True, False]))

        return self

    def get_dft_dependency_obj(self) -> DFTDependency:
        """
        Returns the dft_dependency
        object.

        Raises:
            AttributeError: If the dft_dependency
                object is not initialized.

        Returns:
            DFTDependency: The dft_dependency
                object.
        """
        if not self.dft_dependency:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )

        return self.dft_dependency

    def is_equal(
        self,
        dft_dependency: DFTDependency
    ) -> bool:
        """
        Checks if the current dft_dependency
        is equal to the given dft_dependency.

        Args:
            dft_dependency (DFTDependency): The
                dft_dependency to compare with.

        Returns:
            bool: True if the dft_dependencys
                are equal, False otherwise.
        """
        dft_dependency_manager = DFTDependencyManager(
            self._session_context)
        my_dft_dependency = self.get_dft_dependency_obj()
        return dft_dependency_manager.is_equal(
            dft_dependency, my_dft_dependency)

    def get_obj(self) -> DFTDependency:
        """
        Returns the DFTDependency object.

        :return: The DFTDependency object.
        :rtype: DFTDependency
        """

        return self.dft_dependency

    def get_object_name(self) -> str:
        """
        Returns the name of the object.

        :return: The name of the object.
        :rtype: str
        """
        return "dft_dependency"

    def get_id(self) -> int:
        """
        Returns the ID of the dft_dependency.

        :return: The ID of the dft_dependency.
        :rtype: int
        """
        return self.dft_dependency_id
    # dependencyDFTaskID
    # DynaFlowTaskID

    async def get_parent_name(self) -> str:
        """
        Get the name of the parent dft_dependency.

        Returns:
            str: The name of the parent dft_dependency.
        """
        return 'DynaFlowTask'

    async def get_parent_code(self) -> uuid.UUID:
        """
        Get the parent code of the dft_dependency.

        Returns:
            The parent code of the dft_dependency
            as a UUID.
        """
        return self.dyna_flow_task_code_peek

    async def get_parent_obj(self) -> models.DynaFlowTask:
        """
        Get the parent object of the current
        dft_dependency.

        Returns:
            The parent object of the current
            dft_dependency,
            which is an instance of the
            DynaFlowTask model.
        """
        dyna_flow_task_manager = managers_and_enums.DynaFlowTaskManager(
            self._session_context)
        dyna_flow_task_obj = await dyna_flow_task_manager.get_by_id(
            self.dyna_flow_task_id)
        return dyna_flow_task_obj
    # isPlaceholder
