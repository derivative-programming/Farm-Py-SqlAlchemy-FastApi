from datetime import date, datetime
from decimal import Decimal
import uuid
from helpers import TypeConversion
from .post_reponse import PostResponse
from flows import FlowErrorLogConfigResolveErrorLogResult
from flows import FlowErrorLogConfigResolveErrorLog
from helpers import SessionContext
from models import ErrorLog
from flows import FlowValidationError
import apis.models as view_models
from helpers.pydantic_serialization import CamelModel,SnakeModel
from pydantic import Field,UUID4
import logging
from models import ErrorLog
class ErrorLogConfigResolveErrorLogPostModelResponse(PostResponse):

    def load_flow_response(self,data:FlowErrorLogConfigResolveErrorLogResult):
        placeholder = "" #to avoid pass line

### request. expect camel case. use marshmallow to validate.
class ErrorLogConfigResolveErrorLogPostModelRequest(SnakeModel):

    def process_request(self,
                        session_context:SessionContext,
                        error_log_code:uuid,
                        response:ErrorLogConfigResolveErrorLogPostModelResponse) -> ErrorLogConfigResolveErrorLogPostModelResponse:
        try:
            logging.debug("loading model...")
            error_log = ErrorLog.objects.get(code=error_log_code)
            flow = FlowErrorLogConfigResolveErrorLog(session_context)
            logging.debug("process flow...")
            flowResponse = flow.process(
                error_log,

            )
            response.load_flow_response(flowResponse);
            response.success = True
            response.message = "Success."
        except FlowValidationError as ve:
            response.success = False
            response.validation_errors = list()
            for key in ve.error_dict:
                response.validation_errors.append(view_models.ValidationError(key,ve.error_dict[key]))
        return response

