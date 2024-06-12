# current_runtime.py

"""
    #TODO add commment
"""

import managers
from helpers.session_context import SessionContext


async def initialize(session_context: SessionContext):
    """
        #TODO add commment
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
# endset
