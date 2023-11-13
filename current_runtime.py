from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
import managers
import logging

async def initialize(session: AsyncSession):
    
    await managers.CustomerManager(session).initialize() 
    await managers.CustomerRoleManager(session).initialize()  
    await managers.DateGreaterThanFilterManager(session).initialize()  
    await managers.ErrorLogManager(session).initialize()  
    await managers.FlavorManager(session).initialize()  
    await managers.LandManager(session).initialize()  
    await managers.OrganizationManager(session).initialize()  
    await managers.OrgApiKeyManager(session).initialize()  
    await managers.OrgCustomerManager(session).initialize()  
    await managers.PacManager(session).initialize()  
    await managers.PlantManager(session).initialize()   
    await managers.RoleManager(session).initialize()  
    await managers.TacManager(session).initialize()  
    await managers.TriStateFilterManager(session).initialize()   
#endset