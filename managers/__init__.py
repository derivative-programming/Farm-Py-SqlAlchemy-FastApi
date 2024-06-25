# models/managers/__init__.py
# pylint: disable=line-too-long
"""
This module contains the manager classes for various models.
The manager classes provide an interface for interacting with
the database tables corresponding to the models.
They encapsulate the logic for querying, creating,
updating, and deleting records in the database.
The following manager classes are defined in this module:
- CustomerManager: Manages customer records.
- CustomerRoleManager: Manages customer_role records.
- DateGreaterThanFilterManager: Manages Date Greater Than Filter records.
- ErrorLogManager: Manages error_log records.
- FlavorManager: Manages Flavor records.
- LandManager: Manages Land records.
- OrganizationManager: Manages organization records.
- OrgApiKeyManager: Manages org_api_key records.
- OrgCustomerManager: Manages org_customer records.
- PacManager: Manages Pac records.
- PlantManager: Manages plant records.
- RoleManager: Manages Role records.
- TacManager: Manages Tac records.
- TriStateFilterManager: Manages Tri State Filter records.
Note: The `noqa` comments are used to disable linting warnings for
unused imports.
"""
from .customer import (CustomerManager)  # noqa: F401,E501
from .customer_role import (CustomerRoleManager)  # noqa: F401,E501
from .date_greater_than_filter import (DateGreaterThanFilterManager, DateGreaterThanFilterEnum)  # noqa: F401,E501
from .error_log import (ErrorLogManager)  # noqa: F401,E501
from .flavor import (FlavorManager, FlavorEnum)  # noqa: F401,E501
from .land import (LandManager, LandEnum)  # noqa: F401,E501
from .organization import (OrganizationManager)  # noqa: F401,E501
from .org_api_key import (OrgApiKeyManager)  # noqa: F401,E501
from .org_customer import (OrgCustomerManager)  # noqa: F401,E501
from .pac import (PacManager, PacEnum)  # noqa: F401,E501
from .plant import (PlantManager)  # noqa: F401,E501
from .role import (RoleManager, RoleEnum)  # noqa: F401,E501
from .tac import (TacManager, TacEnum)  # noqa: F401,E501
from .tri_state_filter import (TriStateFilterManager, TriStateFilterEnum)  # noqa: F401,E501

