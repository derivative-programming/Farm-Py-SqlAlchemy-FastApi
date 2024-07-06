# models/serialization_schema/dyna_flow_task.py  # pylint: disable=duplicate-code
# pylint: disable=unused-import

"""
This module contains the
DynaFlowTaskSchema
class, which is responsible
for serializing and deserializing
DynaFlowTask objects.
"""

from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from models import DynaFlowTask


class DynaFlowTaskSchema(SQLAlchemyAutoSchema):
    """
    Schema class for serializing and deserializing
    DynaFlowTask objects.
    """

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Meta class for defining the schema's metadata.
        """

        model = DynaFlowTask
        exclude = (
            "_dyna_flow_task_id",
            "_code",
            "_insert_user_id",
            "_last_update_user_id",
            "_last_change_code",
            "_insert_utc_date_time",
            "_last_update_utc_date_time",
            "_completed_utc_date_time",  # completedUTCDateTime
            "_dependency_dyna_flow_task_id",  # dependencyDynaFlowTaskID
            "_description",  # description
            "_dyna_flow_id",  # DynaFlowID
            "_dyna_flow_subject_code",  # dynaFlowSubjectCode
            "_dyna_flow_task_type_id",  # dynaFlowTaskTypeID
            "_is_canceled",  # isCanceled
            "_is_cancel_requested",  # isCancelRequested
            "_is_completed",  # isCompleted
            "_is_parallel_run_allowed",  # isParallelRunAllowed
            "_is_run_task_debug_required",  # isRunTaskDebugRequired
            "_is_started",  # isStarted
            "_is_successful",  # isSuccessful
            "_max_retry_count",  # maxRetryCount
            "_min_start_utc_date_time",  # minStartUTCDateTime
            "_param_1",  # param1
            "_param_2",  # param2
            "_processor_identifier",  # processorIdentifier
            "_requested_utc_date_time",  # requestedUTCDateTime
            "_result_value",  # resultValue
            "_retry_count",  # retryCount
            "_started_utc_date_time",  # startedUTCDateTime
# endset  # noqa E122
        )

    dyna_flow_task_id = fields.Int()
    code = fields.UUID()
    last_change_code = fields.Int()
    insert_user_id = fields.UUID()
    last_update_user_id = fields.UUID()
    completed_utc_date_time = \
        fields.DateTime()  # (format="%Y-%m-%dT%H:%M:%S")
    dependency_dyna_flow_task_id = fields.Int()
    description = fields.Str()
    dyna_flow_id = fields.Int()
    dyna_flow_subject_code = fields.UUID()
    dyna_flow_task_type_id = fields.Int()
    is_canceled = fields.Bool()
    is_cancel_requested = fields.Bool()
    is_completed = fields.Bool()
    is_parallel_run_allowed = fields.Bool()
    is_run_task_debug_required = fields.Bool()
    is_started = fields.Bool()
    is_successful = fields.Bool()
    max_retry_count = fields.Int()
    min_start_utc_date_time = \
        fields.DateTime()  # (format="%Y-%m-%dT%H:%M:%S")
    param_1 = fields.Str()
    param_2 = fields.Str()
    processor_identifier = fields.Str()
    requested_utc_date_time = \
        fields.DateTime()  # (format="%Y-%m-%dT%H:%M:%S")
    result_value = fields.Str()
    retry_count = fields.Int()
    started_utc_date_time = \
        fields.DateTime()  # (format="%Y-%m-%dT%H:%M:%S")
    insert_utc_date_time = fields.DateTime()
    last_update_utc_date_time = fields.DateTime()
    dyna_flow_code_peek = fields.UUID()  # DynaFlowID
    dyna_flow_task_type_code_peek = fields.UUID()   # DynaFlowTaskTypeID
