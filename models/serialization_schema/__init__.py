# models/serialization_schema/__init__.py  # pylint: disable=duplicate-code
"""
This module contains the serialization schemas for the
models in the Farm-Py-SqlAlchemy-FastApi project.
The serialization schemas define how the data should be
serialized and deserialized when interacting with the API.
"""
from .customer import CustomerSchema  # noqa: F401
from .customer_role import CustomerRoleSchema  # noqa: F401
from .date_greater_than_filter import DateGreaterThanFilterSchema  # noqa: F401
from .df_maintenance import DFMaintenanceSchema  # noqa: F401
from .dft_dependency import DFTDependencySchema  # noqa: F401
from .dyna_flow import DynaFlowSchema  # noqa: F401
from .dyna_flow_task import DynaFlowTaskSchema  # noqa: F401
from .dyna_flow_task_type import DynaFlowTaskTypeSchema  # noqa: F401
from .dyna_flow_type import DynaFlowTypeSchema  # noqa: F401
from .dyna_flow_type_schedule import DynaFlowTypeScheduleSchema  # noqa: F401
from .error_log import ErrorLogSchema  # noqa: F401
from .flavor import FlavorSchema  # noqa: F401
from .land import LandSchema  # noqa: F401
from .organization import OrganizationSchema  # noqa: F401
from .org_api_key import OrgApiKeySchema  # noqa: F401
from .org_customer import OrgCustomerSchema  # noqa: F401
from .pac import PacSchema  # noqa: F401
from .plant import PlantSchema  # noqa: F401
from .role import RoleSchema  # noqa: F401
from .tac import TacSchema  # noqa: F401
from .tri_state_filter import TriStateFilterSchema  # noqa: F401
