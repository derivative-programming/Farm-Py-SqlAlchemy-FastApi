# apis/models/factory/__init__.py

"""
This module contains the factory functions for creating model request
objects used in the API.

The factory functions in this module are responsible for creating
model request objects for various operations and workflows related
to the Land object and its associated workflows. It also includes
model request objects for other operations and reports.

The factory functions are imported from their respective modules
and are used to create instances of the model request objects when needed.

Example usage:

    from .land_add_plant import LandAddPlantPostModelRequestFactory
    request_factory = LandAddPlantPostModelRequestFactory()
    request = request_factory.create_model_request(data)

    The `create_model_request` method of the factory object is used
    to create a model request object with the provided data.

Note: This module contains generated code and should not be modified manually.
"""

##GENLOOPObjectStart
##GENTrainingBlock[a]Start
##GENLearn[modelType=object,name=Land]Start
##GENLOOPObjectWorkflowStart
##GENTrainingBlock[b]Start
##GENLearn[modelType=objectWorkflow,name=LandAddPlant,calculatedIsInitObjWF=false]Start
from .land_add_plant import LandAddPlantPostModelRequestFactory  # noqa: F401
##GENLearn[modelType=objectWorkflow,name=LandAddPlant,calculatedIsInitObjWF=false]End
##GENTrainingBlock[b]End
##GENLOOPObjectWorkflowEnd
##GENLOOPReportStart
##GENTrainingBlock[b2]Start
##GENLearn[modelType=report,name=LandPlantList]Start
from .land_plant_list import LandPlantListGetModelRequestFactory  # noqa: F401
##GENLearn[modelType=report,name=LandPlantList]End
##GENTrainingBlock[b2]End
##GENLOOPReportEnd
##GENLearn[modelType=object,name=Land]End
from .tac_login import (  # noqa: F401
    TacLoginPostModelRequestFactory)
from .tac_register import (  # noqa: F401
    TacRegisterPostModelRequestFactory)
from .tac_farm_dashboard import (  # noqa: F401
    TacFarmDashboardGetModelRequestFactory)
from .customer_build_temp_api_key import (  # noqa: F401
    CustomerBuildTempApiKeyPostModelRequestFactory)
from .customer_user_log_out import (  # noqa: F401
    CustomerUserLogOutPostModelRequestFactory)
from .error_log_config_resolve_error_log import (  # noqa: F401
    ErrorLogConfigResolveErrorLogPostModelRequestFactory)
from .land_user_plant_multi_select_to_editable import (  # noqa: F401
    LandUserPlantMultiSelectToEditablePostModelRequestFactory)
from .land_user_plant_multi_select_to_not_editable import (  # noqa: F401
    LandUserPlantMultiSelectToNotEditablePostModelRequestFactory)
from .pac_user_date_greater_than_filter_list import (  # noqa: F401
    PacUserDateGreaterThanFilterListGetModelRequestFactory)
from .pac_user_flavor_list import (  # noqa: F401
    PacUserFlavorListGetModelRequestFactory)
from .pac_user_land_list import (  # noqa: F401
    PacUserLandListGetModelRequestFactory)
from .pac_user_role_list import (  # noqa: F401
    PacUserRoleListGetModelRequestFactory)
from .pac_user_tac_list import (  # noqa: F401
    PacUserTacListGetModelRequestFactory)
from .pac_user_tri_state_filter_list import (  # noqa: F401
    PacUserTriStateFilterListGetModelRequestFactory)
from .plant_user_delete import (  # noqa: F401
    PlantUserDeletePostModelRequestFactory)
from .plant_user_details import (  # noqa: F401
    PlantUserDetailsGetModelRequestFactory)
from .plant_user_property_random_update import (  # noqa: F401
    PlantUserPropertyRandomUpdatePostModelRequestFactory)
##GENTrainingBlock[a]End
##GENLOOPObjectEnd
