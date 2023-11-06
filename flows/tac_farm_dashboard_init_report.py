
from dataclasses import dataclass
from dataclasses_json import dataclass_json,LetterCase 
import uuid
import flows.base
from flows.base import BaseFlowTacFarmDashboardInitReport 
from models import Tac 
from flows.base import LogSeverity
from helpers import SessionContext
import models as farm_models 
import managers as farm_managers

@dataclass_json
@dataclass
class FlowTacFarmDashboardInitReportResult():
    context_object_code:uuid = uuid.UUID(int=0)
    customer_code:uuid = uuid.UUID(int=0)

    def __init__(self): 
        pass

class FlowTacFarmDashboardInitReport(BaseFlowTacFarmDashboardInitReport):  
    def __init__(self, session_context:SessionContext):  
        super(FlowTacFarmDashboardInitReport, self).__init__(session_context) 

    def process(self, 
        tac: Tac,
        ) -> FlowTacFarmDashboardInitReportResult:
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Start")
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Code::" + str(tac.code))

        super()._process_validation_rules(
            tac,
        )

        super()._throw_queued_validation_errors()
        
        # customer_code_output = uuid.UUID(int=0)

        customer_code_output = self._session_context.customer_code
    
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Building result")
        result = FlowTacFarmDashboardInitReportResult()
        result.context_object_code = tac.code
        result.customer_code = customer_code_output
        result.context_object_code = tac.code
        super()._log_message_and_severity(LogSeverity.information_high_detail, "Result:" + result.to_json())
        
        super()._log_message_and_severity(LogSeverity.information_high_detail, "End")
        return result


    