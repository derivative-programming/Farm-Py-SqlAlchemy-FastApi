# business/pac.py
# pylint: disable=unused-import
"""
This module contains the PacBusObj class,
which represents the business object for a Pac.
"""

from typing import List
from helpers.session_context import SessionContext
from models import Pac
import managers as managers_and_enums  # noqa: F401
from .pac_fluent import PacFluentBusObj


from business.tri_state_filter import TriStateFilterBusObj


from business.tac import TacBusObj


from business.role import RoleBusObj


from business.land import LandBusObj


from business.flavor import FlavorBusObj


from business.error_log import ErrorLogBusObj


from business.date_greater_than_filter import DateGreaterThanFilterBusObj


NOT_INITIALIZED_ERROR_MESSAGE = (
    "Pac object is not initialized")


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

            pac_bus_obj.load_from_obj_instance(
                pac)

            result.append(pac_bus_obj)

        return result


    async def build_tri_state_filter(
        self) -> TriStateFilterBusObj:
        """
        build tri_state_filter
        instance (not saved yet)
        """
        item = TriStateFilterBusObj(self._session_context)

        assert item.tri_state_filter is not None


        item.pac_id = self.pac_id
        item.tri_state_filter.pac_code_peek = self.code

        return item

    async def get_all_tri_state_filter(
        self) -> List[TriStateFilterBusObj]:
        """
        get all tri_state_filter
        """
        results = list()
        tri_state_filter_manager = managers_and_enums.TriStateFilterManager(
            self._session_context)
        obj_list = await tri_state_filter_manager.get_by_pac_id(
            self.pac_id)
        for obj_item in obj_list:
            bus_obj_item = TriStateFilterBusObj(
                self._session_context)
            bus_obj_item.load_from_obj_instance(obj_item)
            results.append(bus_obj_item)
        return results


    async def build_tac(
        self) -> TacBusObj:
        """
        build tac
        instance (not saved yet)
        """
        item = TacBusObj(self._session_context)

        assert item.tac is not None


        item.pac_id = self.pac_id
        item.tac.pac_code_peek = self.code

        return item

    async def get_all_tac(
        self) -> List[TacBusObj]:
        """
        get all tac
        """
        results = list()
        tac_manager = managers_and_enums.TacManager(
            self._session_context)
        obj_list = await tac_manager.get_by_pac_id(
            self.pac_id)
        for obj_item in obj_list:
            bus_obj_item = TacBusObj(
                self._session_context)
            bus_obj_item.load_from_obj_instance(obj_item)
            results.append(bus_obj_item)
        return results


    async def build_role(
        self) -> RoleBusObj:
        """
        build role
        instance (not saved yet)
        """
        item = RoleBusObj(self._session_context)

        assert item.role is not None


        item.pac_id = self.pac_id
        item.role.pac_code_peek = self.code

        return item

    async def get_all_role(
        self) -> List[RoleBusObj]:
        """
        get all role
        """
        results = list()
        role_manager = managers_and_enums.RoleManager(
            self._session_context)
        obj_list = await role_manager.get_by_pac_id(
            self.pac_id)
        for obj_item in obj_list:
            bus_obj_item = RoleBusObj(
                self._session_context)
            bus_obj_item.load_from_obj_instance(obj_item)
            results.append(bus_obj_item)
        return results


    async def build_land(
        self) -> LandBusObj:
        """
        build land
        instance (not saved yet)
        """
        item = LandBusObj(self._session_context)

        assert item.land is not None


        item.pac_id = self.pac_id
        item.land.pac_code_peek = self.code

        return item

    async def get_all_land(
        self) -> List[LandBusObj]:
        """
        get all land
        """
        results = list()
        land_manager = managers_and_enums.LandManager(
            self._session_context)
        obj_list = await land_manager.get_by_pac_id(
            self.pac_id)
        for obj_item in obj_list:
            bus_obj_item = LandBusObj(
                self._session_context)
            bus_obj_item.load_from_obj_instance(obj_item)
            results.append(bus_obj_item)
        return results


    async def build_flavor(
        self) -> FlavorBusObj:
        """
        build flavor
        instance (not saved yet)
        """
        item = FlavorBusObj(self._session_context)

        assert item.flavor is not None


        item.pac_id = self.pac_id
        item.flavor.pac_code_peek = self.code

        return item

    async def get_all_flavor(
        self) -> List[FlavorBusObj]:
        """
        get all flavor
        """
        results = list()
        flavor_manager = managers_and_enums.FlavorManager(
            self._session_context)
        obj_list = await flavor_manager.get_by_pac_id(
            self.pac_id)
        for obj_item in obj_list:
            bus_obj_item = FlavorBusObj(
                self._session_context)
            bus_obj_item.load_from_obj_instance(obj_item)
            results.append(bus_obj_item)
        return results


    async def build_error_log(
        self) -> ErrorLogBusObj:
        """
        build error_log
        instance (not saved yet)
        """
        item = ErrorLogBusObj(self._session_context)

        assert item.error_log is not None


        item.pac_id = self.pac_id
        item.error_log.pac_code_peek = self.code

        return item

    async def get_all_error_log(
        self) -> List[ErrorLogBusObj]:
        """
        get all error_log
        """
        results = list()
        error_log_manager = managers_and_enums.ErrorLogManager(
            self._session_context)
        obj_list = await error_log_manager.get_by_pac_id(
            self.pac_id)
        for obj_item in obj_list:
            bus_obj_item = ErrorLogBusObj(
                self._session_context)
            bus_obj_item.load_from_obj_instance(obj_item)
            results.append(bus_obj_item)
        return results


    async def build_date_greater_than_filter(
        self) -> DateGreaterThanFilterBusObj:
        """
        build date_greater_than_filter
        instance (not saved yet)
        """
        item = DateGreaterThanFilterBusObj(self._session_context)

        assert item.date_greater_than_filter is not None


        item.pac_id = self.pac_id
        item.date_greater_than_filter.pac_code_peek = self.code

        return item

    async def get_all_date_greater_than_filter(
        self) -> List[DateGreaterThanFilterBusObj]:
        """
        get all date_greater_than_filter
        """
        results = list()
        date_greater_than_filter_manager = managers_and_enums.DateGreaterThanFilterManager(
            self._session_context)
        obj_list = await date_greater_than_filter_manager.get_by_pac_id(
            self.pac_id)
        for obj_item in obj_list:
            bus_obj_item = DateGreaterThanFilterBusObj(
                self._session_context)
            bus_obj_item.load_from_obj_instance(obj_item)
            results.append(bus_obj_item)
        return results

