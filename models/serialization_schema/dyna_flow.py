# models/serialization_schema/dyna_flow.py  # pylint: disable=duplicate-code
# pylint: disable=unused-import

"""
This module contains the
DynaFlowSchema
class, which is responsible
for serializing and deserializing
DynaFlow objects.
"""

from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from models import DynaFlow


class DynaFlowSchema(SQLAlchemyAutoSchema):
    """
    Schema class for serializing and deserializing
    DynaFlow objects.
    """

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Meta class for defining the schema's metadata.
        """

        model = DynaFlow
        exclude = (
            "_dyna_flow_id",
            "_code",
            "_insert_user_id",
            "_last_update_user_id",
            "_last_change_code",
            "_insert_utc_date_time",
            "_last_update_utc_date_time",
            "_completed_utc_date_time",  # completedUTCDateTime
            "_dependency_dyna_flow_id",  # dependencyDynaFlowID
            "_description",  # description
            "_dyna_flow_type_id",  # dynaFlowTypeID
            "_is_build_task_debug_required",  # isBuildTaskDebugRequired
            "_is_canceled",  # isCanceled
            "_is_cancel_requested",  # isCancelRequested
            "_is_completed",  # isCompleted
            "_is_paused",  # isPaused
            "_is_resubmitted",  # isResubmitted
            "_is_run_task_debug_required",  # isRunTaskDebugRequired
            "_is_started",  # isStarted
            "_is_successful",  # isSuccessful
            "_is_task_creation_started",  # isTaskCreationStarted
            "_is_tasks_created",  # isTasksCreated
            "_min_start_utc_date_time",  # minStartUTCDateTime
            "_pac_id",  # PacID
            "_param_1",  # param1
            "_parent_dyna_flow_id",  # parentDynaFlowID
            "_priority_level",  # priorityLevel
            "_requested_utc_date_time",  # requestedUTCDateTime
            "_result_value",  # resultValue
            "_root_dyna_flow_id",  # rootDynaFlowID
            "_started_utc_date_time",  # startedUTCDateTime
            "_subject_code",  # subjectCode
            "_task_creation_processor_identifier",  # taskCreationProcessorIdentifier
# endset  # noqa E122
        )

    dyna_flow_id = fields.Int()
    code = fields.UUID()
    last_change_code = fields.Int()
    insert_user_id = fields.UUID()
    last_update_user_id = fields.UUID()
    completed_utc_date_time = \
        fields.DateTime()  # (format="%Y-%m-%dT%H:%M:%S")
    dependency_dyna_flow_id = fields.Int()
    description = fields.Str()
    dyna_flow_type_id = fields.Int()
    is_build_task_debug_required = fields.Bool()
    is_canceled = fields.Bool()
    is_cancel_requested = fields.Bool()
    is_completed = fields.Bool()
    is_paused = fields.Bool()
    is_resubmitted = fields.Bool()
    is_run_task_debug_required = fields.Bool()
    is_started = fields.Bool()
    is_successful = fields.Bool()
    is_task_creation_started = fields.Bool()
    is_tasks_created = fields.Bool()
    min_start_utc_date_time = \
        fields.DateTime()  # (format="%Y-%m-%dT%H:%M:%S")
    pac_id = fields.Int()
    param_1 = fields.Str()
    parent_dyna_flow_id = fields.Int()
    priority_level = fields.Int()
    requested_utc_date_time = \
        fields.DateTime()  # (format="%Y-%m-%dT%H:%M:%S")
    result_value = fields.Str()
    root_dyna_flow_id = fields.Int()
    started_utc_date_time = \
        fields.DateTime()  # (format="%Y-%m-%dT%H:%M:%S")
    subject_code = fields.UUID()
    task_creation_processor_identifier = fields.Str()
    insert_utc_date_time = fields.DateTime()
    last_update_utc_date_time = fields.DateTime()
    dyna_flow_type_code_peek = fields.UUID()   # DynaFlowTypeID
    pac_code_peek = fields.UUID()  # PacID
