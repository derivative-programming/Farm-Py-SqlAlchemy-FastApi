# business/dyna_flow_task_type.py  # pylint: disable=duplicate-code
# pylint: disable=unused-import
"""
This module contains the
DynaFlowTaskTypeBusObj class,
which represents the
business object for a
DynaFlowTaskType.
"""

from typing import List

import managers as managers_and_enums  # noqa: F401
import models
from helpers.session_context import SessionContext
from models import DynaFlowTaskType

from .dyna_flow_task_type_dyna_flows import DynaFlowTaskTypeDynaFlowsBusObj


NOT_INITIALIZED_ERROR_MESSAGE = (
    "DynaFlowTaskType object is not initialized")


class DynaFlowTaskTypeBusObj(DynaFlowTaskTypeDynaFlowsBusObj):
    """
    This class represents the business object for a DynaFlowTaskType.
    It requires a valid session context for initialization.
    """

    @staticmethod
    async def to_bus_obj_list(
        session_context: SessionContext,
        obj_list: List[DynaFlowTaskType]
    ):
        """
        Convert a list of DynaFlowTaskType
        objects to a list of
        DynaFlowTaskTypeBusObj objects.

        Args:
            session_context (SessionContext): The session context.
            obj_list (List[DynaFlowTaskType]): The
                list of DynaFlowTaskType objects to convert.

        Returns:
            List[DynaFlowTaskTypeBusObj]: The
                list of converted DynaFlowTaskTypeBusObj
                objects.
        """
        result = []

        for dyna_flow_task_type in obj_list:
            dyna_flow_task_type_bus_obj = DynaFlowTaskTypeBusObj(
                session_context)

            dyna_flow_task_type_bus_obj.load_from_obj_instance(
                dyna_flow_task_type)

            result.append(dyna_flow_task_type_bus_obj)

        return result
    # description,
    # displayOrder,
    # isActive,
    # lookupEnumName,
    # maxRetryCount,
    # name,
    # PacID

    async def get_pac_id_obj(self) -> models.Pac:
        """
        Retrieves the related Pac object based
        on the pac_id.

        Returns:
            An instance of the Pac model
            representing the related pac.

        """
        pac_manager = managers_and_enums.PacManager(
            self._session_context)
        pac_obj = await pac_manager.get_by_id(
            self.pac_id)
        return pac_obj

    async def get_pac_id_bus_obj(self):
        """
        Retrieves the related Pac
        business object based
        on the pac_id.

        Returns:
            An instance of the Pac
            business object
            representing the related pac.

        """
        from business.pac import \
            PacBusObj  # pylint: disable=import-outside-toplevel
        bus_obj = PacBusObj(self._session_context)
        await bus_obj.load_from_id(self.pac_id)
        return bus_obj


    @property
    def lookup_enum(self) -> managers_and_enums.DynaFlowTaskTypeEnum:
        """
        Returns the corresponding DynaFlowTaskTypeEnum
        value based on the lookup_enum_name.
        Raises:
            AttributeError: If the dyna_flow_task_type
                attribute is not initialized.
        Returns:
            managers_and_enums.DynaFlowTaskTypeEnum:
                The corresponding DynaFlowTaskTypeEnum value.
        """
        if not self.dyna_flow_task_type:
            raise AttributeError(
                NOT_INITIALIZED_ERROR_MESSAGE
            )
        return (
            managers_and_enums.DynaFlowTaskTypeEnum[
                self.dyna_flow_task_type.lookup_enum_name
            ]
        )

    async def load_from_enum(
        self,
        dyna_flow_task_type_enum:
            managers_and_enums.DynaFlowTaskTypeEnum
    ):
        """
        Load dyna_flow_task_type data from dictionary.
        :param dyna_flow_task_type_dict: Dictionary
            containing dyna_flow_task_type data.
        :raises ValueError: If dyna_flow_task_type_dict
            is not a dictionary or if no
            dyna_flow_task_type data is found.
        """
        if not isinstance(
            dyna_flow_task_type_enum,
            managers_and_enums.DynaFlowTaskTypeEnum
        ):
            raise ValueError("dyna_flow_task_type_enum must be a enum")
        dyna_flow_task_type_manager =  \
            managers_and_enums.DynaFlowTaskTypeManager(
                self._session_context
            )
        self.dyna_flow_task_type = await (
            dyna_flow_task_type_manager.
            from_enum(dyna_flow_task_type_enum)
        )
