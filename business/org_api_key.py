# business/org_api_key.py

"""
This module contains the OrgApiKeyBusObj class,
which represents the business object for a OrgApiKey.
"""

from typing import List
from helpers.session_context import SessionContext
from managers import OrgApiKeyManager
from models import OrgApiKey
import models
import managers as managers_and_enums
from .org_api_key_fluent import OrgApiKeyFluentBusObj

class OrgApiKeyBusObj(OrgApiKeyFluentBusObj):
    """
    This class represents the business object for a OrgApiKey.
    It requires a valid session context for initialization.
    """

    @staticmethod
    async def to_bus_obj_list(
        session_context: SessionContext,
        obj_list: List[OrgApiKey]
    ):
        """
        Convert a list of OrgApiKey
        objects to a list of
        OrgApiKeyBusObj objects.

        Args:
            session_context (SessionContext): The session context.
            obj_list (List[OrgApiKey]): The
                list of OrgApiKey objects to convert.

        Returns:
            List[OrgApiKeyBusObj]: The
                list of converted OrgApiKeyBusObj
                objects.
        """
        result = list()

        for org_api_key in obj_list:
            org_api_key_bus_obj = OrgApiKeyBusObj(session_context)

            await org_api_key_bus_obj.load_from_obj_instance(
                org_api_key)

            result.append(org_api_key_bus_obj)

        return result

