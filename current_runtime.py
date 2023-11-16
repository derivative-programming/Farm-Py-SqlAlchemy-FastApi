from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from helpers.session_context import SessionContext
import managers
import logging

async def initialize(session_context: SessionContext):
    
    await managers.PacManager(session_context).initialize()  
#endset
    
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
#endset