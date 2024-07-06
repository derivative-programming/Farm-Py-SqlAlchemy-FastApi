# current_runtime.py  # pylint: disable=duplicate-code

"""
This module contains the code for initializing various
managers in the application.
"""

import managers
from helpers.session_context import SessionContext


async def initialize(session_context: SessionContext):
    """
    Initializes various managers in the application.

    Args:
        session_context (SessionContext): The session context object.

    Returns:
        None
    """
    await managers.PacManager(session_context).initialize()
# endset

    await managers.CustomerManager(session_context).initialize()
    await managers.CustomerRoleManager(session_context).initialize()
    await managers.DateGreaterThanFilterManager(session_context).initialize()
    await managers.ErrorLogManager(session_context).initialize()
    await managers.FlavorManager(session_context).initialize()
    await managers.LandManager(session_context).initialize()
    await managers.OrganizationManager(session_context).initialize()
    await managers.OrgApiKeyManager(session_context).initialize()
    await managers.OrgCustomerManager(session_context).initialize()
    await managers.PacManager(session_context).initialize()
    await managers.PlantManager(session_context).initialize()
    await managers.RoleManager(session_context).initialize()
    await managers.TacManager(session_context).initialize()
    await managers.TriStateFilterManager(session_context).initialize()
    await managers.DynaFlowManager(session_context).initialize()
    await managers.DynaFlowTaskManager(session_context).initialize()
    await managers.DynaFlowTypeManager(session_context).initialize()
    await managers.DynaFlowTaskTypeManager(session_context).initialize()
    await managers.DynaFlowTypeManager(session_context).initialize()
    await managers.DFTDependencyManager(session_context).initialize()
    await managers.DFMaintenanceManager(session_context).initialize()
# endset
