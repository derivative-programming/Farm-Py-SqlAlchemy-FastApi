import uuid
from .customer import CustomerBusObj
from .customer_role import CustomerRoleBusObj
from .date_greater_than_filter import DateGreaterThanFilterBusObj
from .error_log import ErrorLogBusObj
from .flavor import FlavorBusObj
from .land import LandBusObj
from .organization import OrganizationBusObj
from .org_api_key import OrgApiKeyBusObj
from .org_customer import OrgCustomerBusObj
from .pac import PacBusObj
from .plant import PlantBusObj
from .role import RoleBusObj
from .tac import TacBusObj
from .tri_state_filter import TriStateFilterBusObj
from sqlalchemy.ext.asyncio import AsyncSession
#endset

class BusObjFactory: 
    @staticmethod
    async def create(session:AsyncSession, name, code:uuid.UUID=None, id:int=None):
        if code is not None:
            if name == 'Customer':
                return await CustomerBusObj(session=session).load(code=code)
            elif name == 'CustomerRole':
                return await CustomerRoleBusObj(session=session).load(code=code)
            elif name == 'DateGreaterThanFilter':
                return await DateGreaterThanFilterBusObj(session=session).load(code=code)
            elif name == 'ErrorLog':
                return await ErrorLogBusObj(session=session).load(code=code)
            elif name == 'Flavor':
                return await FlavorBusObj(session=session).load(code=code)
            elif name == 'Land':
                return await LandBusObj(session=session).load(code=code)
            elif name == 'Organization':
                return await OrganizationBusObj(session=session).load(code=code)
            elif name == 'OrgApiKey':
                return await OrgApiKeyBusObj(session=session).load(code=code)
            elif name == 'OrgCustomer':
                return await OrgCustomerBusObj(session=session).load(code=code)
            elif name == 'Pac':
                return await PacBusObj(session=session).load(code=code)
            elif name == 'Plant':
                return await PlantBusObj(session=session).load(code=code)
            elif name == 'Role':
                return await RoleBusObj(session=session).load(code=code)
            elif name == 'Tac':
                return await TacBusObj(session=session).load(code=code)
            elif name == 'TriStateFilter':
                return await TriStateFilterBusObj(session=session).load(code=code) 
    #endset
            else:
                raise ValueError(f"Unknown object type: {name}")
        else:
            if name == 'Customer':
                return await CustomerBusObj(session=session).load(customer_id=id)
            elif name == 'CustomerRole':
                return await CustomerRoleBusObj(session=session).load(customer_role_id=id)
            elif name == 'DateGreaterThanFilter':
                return await DateGreaterThanFilterBusObj(session=session).load(date_greater_than_filter_id=id)
            elif name == 'ErrorLog':
                return await ErrorLogBusObj(session=session).load(error_log_id=id)
            elif name == 'Flavor':
                return await FlavorBusObj(session=session).load(flavor_id=id)
            elif name == 'Land':
                return await LandBusObj(session=session).load(land_id=id)
            elif name == 'Organization':
                return await OrganizationBusObj(session=session).load(organization_id=id)
            elif name == 'OrgApiKey':
                return await OrgApiKeyBusObj(session=session).load(org_api_key_id=id)
            elif name == 'OrgCustomer':
                return await OrgCustomerBusObj(session=session).load(org_customer_id=id)
            elif name == 'Pac':
                return await PacBusObj(session=session).load(pac_id=id)
            elif name == 'Plant':
                return await PlantBusObj(session=session).load(plant_id=id)
            elif name == 'Role':
                return await RoleBusObj(session=session).load(role_id=id)
            elif name == 'Tac':
                return await TacBusObj(session=session).load(tac_id=id)
            elif name == 'TriStateFilter':
                return await TriStateFilterBusObj(session=session).load(tri_state_filter_id=id) 
    #endset
            else:
                raise ValueError(f"Unknown object type: {name}")