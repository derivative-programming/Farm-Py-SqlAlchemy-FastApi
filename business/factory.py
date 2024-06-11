# business/factory.py

"""
    #TODO add comment
"""

import uuid

from helpers.session_context import SessionContext
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
    async def create(session_context: SessionContext, name, code: uuid.UUID = None, id: int = None):
        if code is not None:
            if name == 'Customer':
                return await CustomerBusObj(session_context=session_context).load(code=code)
            elif name == 'CustomerRole':
                return await CustomerRoleBusObj(session_context).load(code=code)
            elif name == 'DateGreaterThanFilter':
                return await DateGreaterThanFilterBusObj(session_context).load(code=code)
            elif name == 'ErrorLog':
                return await ErrorLogBusObj(session_context).load(code=code)
            elif name == 'Flavor':
                return await FlavorBusObj(session_context).load(code=code)
            elif name == 'Land':
                return await LandBusObj(session_context).load(code=code)
            elif name == 'Organization':
                return await OrganizationBusObj(session_context).load(code=code)
            elif name == 'OrgApiKey':
                return await OrgApiKeyBusObj(session_context).load(code=code)
            elif name == 'OrgCustomer':
                return await OrgCustomerBusObj(session_context).load(code=code)
            elif name == 'Pac':
                return await PacBusObj(session_context).load(code=code)
            elif name == 'Plant':
                return await PlantBusObj(session_context).load(code=code)
            elif name == 'Role':
                return await RoleBusObj(session_context).load(code=code)
            elif name == 'Tac':
                return await TacBusObj(session_context).load(code=code)
            elif name == 'TriStateFilter':
                return await TriStateFilterBusObj(session_context).load(code=code)
    #endset
            else:
                raise ValueError(f"Unknown object type: {name}")
        else:
            if name == 'Customer':
                return await CustomerBusObj(session_context).load(customer_id=id)
            elif name == 'CustomerRole':
                return await CustomerRoleBusObj(session_context).load(customer_role_id=id)
            elif name == 'DateGreaterThanFilter':
                return await DateGreaterThanFilterBusObj(session_context).load(date_greater_than_filter_id=id)
            elif name == 'ErrorLog':
                return await ErrorLogBusObj(session_context).load(error_log_id=id)
            elif name == 'Flavor':
                return await FlavorBusObj(session_context).load(flavor_id=id)
            elif name == 'Land':
                return await LandBusObj(session_context).load(land_id=id)
            elif name == 'Organization':
                return await OrganizationBusObj(session_context).load(organization_id=id)
            elif name == 'OrgApiKey':
                return await OrgApiKeyBusObj(session_context).load(org_api_key_id=id)
            elif name == 'OrgCustomer':
                return await OrgCustomerBusObj(session_context).load(org_customer_id=id)
            elif name == 'Pac':
                return await PacBusObj(session_context).load(pac_id=id)
            elif name == 'Plant':
                return await PlantBusObj(session_context).load(plant_id=id)
            elif name == 'Role':
                return await RoleBusObj(session_context).load(role_id=id)
            elif name == 'Tac':
                return await TacBusObj(session_context).load(tac_id=id)
            elif name == 'TriStateFilter':
                return await TriStateFilterBusObj(session_context).load(tri_state_filter_id=id)
    #endset
            else:
                raise ValueError(f"Unknown object type: {name}")
