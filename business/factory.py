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
            elif name == 'CustomerRoleBusObj':
                return await CustomerRoleBusObj(session=session).load(code=code)
            elif name == 'DateGreaterThanFilterBusObj':
                return await DateGreaterThanFilterBusObj(session=session).load(code=code)
            elif name == 'ErrorLogBusObj':
                return await ErrorLogBusObj(session=session).load(code=code)
            elif name == 'FlavorBusObj':
                return await FlavorBusObj(session=session).load(code=code)
            elif name == 'LandBusObj':
                return await LandBusObj(session=session).load(code=code)
            elif name == 'OrganizationBusObj':
                return await OrganizationBusObj(session=session).load(code=code)
            elif name == 'OrgApiKeyBusObj':
                return await OrgApiKeyBusObj(session=session).load(code=code)
            elif name == 'OrgCustomerBusObj':
                return await OrgCustomerBusObj(session=session).load(code=code)
            elif name == 'PacBusObj':
                return await PacBusObj(session=session).load(code=code)
            elif name == 'PlantBusObj':
                return await PlantBusObj(session=session).load(code=code)
            elif name == 'RoleBusObj':
                return await RoleBusObj(session=session).load(code=code)
            elif name == 'TacBusObj':
                return await TacBusObj(session=session).load(code=code)
            elif name == 'TriStateFilterBusObj':
                return await TriStateFilterBusObj(session=session).load(code=code) 
    #endset
            else:
                raise ValueError(f"Unknown object type: {name}")
        else:
            if name == 'Customer':
                return await CustomerBusObj(session=session).load(customer_id=id)
            elif name == 'CustomerRoleBusObj':
                return await CustomerRoleBusObj(session=session).load(customer_role_id=id)
            elif name == 'DateGreaterThanFilterBusObj':
                return await DateGreaterThanFilterBusObj(session=session).load(date_greater_than_filter_id=id)
            elif name == 'ErrorLogBusObj':
                return await ErrorLogBusObj(session=session).load(error_log_id=id)
            elif name == 'FlavorBusObj':
                return await FlavorBusObj(session=session).load(flavor_id=id)
            elif name == 'LandBusObj':
                return await LandBusObj(session=session).load(land_id=id)
            elif name == 'OrganizationBusObj':
                return await OrganizationBusObj(session=session).load(organization_id=id)
            elif name == 'OrgApiKeyBusObj':
                return await OrgApiKeyBusObj(session=session).load(org_api_key_id=id)
            elif name == 'OrgCustomerBusObj':
                return await OrgCustomerBusObj(session=session).load(org_customer_id=id)
            elif name == 'PacBusObj':
                return await PacBusObj(session=session).load(pac_id=id)
            elif name == 'PlantBusObj':
                return await PlantBusObj(session=session).load(plant_id=id)
            elif name == 'RoleBusObj':
                return await RoleBusObj(session=session).load(role_id=id)
            elif name == 'TacBusObj':
                return await TacBusObj(session=session).load(tac_id=id)
            elif name == 'TriStateFilterBusObj':
                return await TriStateFilterBusObj(session=session).load(tri_state_filter_id=id) 
    #endset
            else:
                raise ValueError(f"Unknown object type: {name}")