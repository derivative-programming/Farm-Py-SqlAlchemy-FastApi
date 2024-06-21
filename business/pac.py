# business/pac.py

"""
This module contains the PacBusObj class,
which represents the business object for a Pac.
"""

from typing import List
from helpers.session_context import SessionContext
from managers import PacManager
from models import Pac
import models
import managers as managers_and_enums
from .pac_fluent import PacFluentBusObj

from business.tri_state_filter import TriStateFilterBusObj

from business.tac import TacBusObj

from business.role import RoleBusObj

from business.land import LandBusObj

from business.flavor import FlavorBusObj

from business.error_log import ErrorLogBusObj

from business.date_greater_than_filter import DateGreaterThanFilterBusObj

class PacBusObj(PacFluentBusObj):
    """
    This class represents the business object for a Pac.
    It requires a valid session context for initialization.
    """

    @staticmethod
    async def to_bus_obj_list(
        session_context: SessionContext,
        obj_list: List[Pac]
    ):
        """
        Convert a list of Pac
        objects to a list of
        PacBusObj objects.

        Args:
            session_context (SessionContext): The session context.
            obj_list (List[Pac]): The
                list of Pac objects to convert.

        Returns:
            List[PacBusObj]: The
                list of converted PacBusObj
                objects.
        """
        result = list()

        for pac in obj_list:
            pac_bus_obj = PacBusObj(session_context)

            await pac_bus_obj.load_from_obj_instance(
                pac)

            result.append(pac_bus_obj)

        return result

    async def build_tri_state_filter(self) -> TriStateFilterBusObj:
        item = TriStateFilterBusObj(self._session_context)

        item.pac_id = self.pac_id
        item.tri_state_filter.pac_code_peek = self.code

        return item

    async def get_all_tri_state_filter(self) -> List[TriStateFilterBusObj]:
        results = list()
        tri_state_filter_manager = managers_and_enums.TriStateFilterManager(self._session_context)
        obj_list = await tri_state_filter_manager.get_by_pac_id(self.pac_id)
        for obj_item in obj_list:
            bus_obj_item = TriStateFilterBusObj(self._session_context)
            await bus_obj_item.load_from_obj_instance(obj_item)
            results.append(bus_obj_item)
        return results

    async def build_tac(self) -> TacBusObj:
        item = TacBusObj(self._session_context)

        item.pac_id = self.pac_id
        item.tac.pac_code_peek = self.code

        return item

    async def get_all_tac(self) -> List[TacBusObj]:
        results = list()
        tac_manager = managers_and_enums.TacManager(self._session_context)
        obj_list = await tac_manager.get_by_pac_id(self.pac_id)
        for obj_item in obj_list:
            bus_obj_item = TacBusObj(self._session_context)
            await bus_obj_item.load_from_obj_instance(obj_item)
            results.append(bus_obj_item)
        return results

    async def build_role(self) -> RoleBusObj:
        item = RoleBusObj(self._session_context)

        item.pac_id = self.pac_id
        item.role.pac_code_peek = self.code

        return item

    async def get_all_role(self) -> List[RoleBusObj]:
        results = list()
        role_manager = managers_and_enums.RoleManager(self._session_context)
        obj_list = await role_manager.get_by_pac_id(self.pac_id)
        for obj_item in obj_list:
            bus_obj_item = RoleBusObj(self._session_context)
            await bus_obj_item.load_from_obj_instance(obj_item)
            results.append(bus_obj_item)
        return results

    async def build_land(self) -> LandBusObj:
        item = LandBusObj(self._session_context)

        item.pac_id = self.pac_id
        item.land.pac_code_peek = self.code

        return item

    async def get_all_land(self) -> List[LandBusObj]:
        results = list()
        land_manager = managers_and_enums.LandManager(self._session_context)
        obj_list = await land_manager.get_by_pac_id(self.pac_id)
        for obj_item in obj_list:
            bus_obj_item = LandBusObj(self._session_context)
            await bus_obj_item.load_from_obj_instance(obj_item)
            results.append(bus_obj_item)
        return results

    async def build_flavor(self) -> FlavorBusObj:
        item = FlavorBusObj(self._session_context)

        item.pac_id = self.pac_id
        item.flavor.pac_code_peek = self.code

        return item

    async def get_all_flavor(self) -> List[FlavorBusObj]:
        results = list()
        flavor_manager = managers_and_enums.FlavorManager(self._session_context)
        obj_list = await flavor_manager.get_by_pac_id(self.pac_id)
        for obj_item in obj_list:
            bus_obj_item = FlavorBusObj(self._session_context)
            await bus_obj_item.load_from_obj_instance(obj_item)
            results.append(bus_obj_item)
        return results

    async def build_error_log(self) -> ErrorLogBusObj:
        item = ErrorLogBusObj(self._session_context)

        item.pac_id = self.pac_id
        item.error_log.pac_code_peek = self.code

        return item

    async def get_all_error_log(self) -> List[ErrorLogBusObj]:
        results = list()
        error_log_manager = managers_and_enums.ErrorLogManager(self._session_context)
        obj_list = await error_log_manager.get_by_pac_id(self.pac_id)
        for obj_item in obj_list:
            bus_obj_item = ErrorLogBusObj(self._session_context)
            await bus_obj_item.load_from_obj_instance(obj_item)
            results.append(bus_obj_item)
        return results

    async def build_date_greater_than_filter(self) -> DateGreaterThanFilterBusObj:
        item = DateGreaterThanFilterBusObj(self._session_context)

        item.pac_id = self.pac_id
        item.date_greater_than_filter.pac_code_peek = self.code

        return item

    async def get_all_date_greater_than_filter(self) -> List[DateGreaterThanFilterBusObj]:
        results = list()
        date_greater_than_filter_manager = managers_and_enums.DateGreaterThanFilterManager(self._session_context)
        obj_list = await date_greater_than_filter_manager.get_by_pac_id(self.pac_id)
        for obj_item in obj_list:
            bus_obj_item = DateGreaterThanFilterBusObj(self._session_context)
            await bus_obj_item.load_from_obj_instance(obj_item)
            results.append(bus_obj_item)
        return results

