# models/serialization_schema/dft_dependency.py  # pylint: disable=duplicate-code
# pylint: disable=unused-import

"""
This module contains the
DFTDependencySchema
class, which is responsible
for serializing and deserializing
DFTDependency objects.
"""

from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from models import DFTDependency


class DFTDependencySchema(SQLAlchemyAutoSchema):
    """
    Schema class for serializing and deserializing
    DFTDependency objects.
    """

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Meta class for defining the schema's metadata.
        """

        model = DFTDependency
        exclude = (
            "_dft_dependency_id",
            "_code",
            "_insert_user_id",
            "_last_update_user_id",
            "_last_change_code",
            "_insert_utc_date_time",
            "_last_update_utc_date_time",
            "_dependency_df_task_id",  # dependencyDFTaskID
            "_dyna_flow_task_id",  # DynaFlowTaskID
            "_is_placeholder",  # isPlaceholder
# endset  # noqa E122
        )

    dft_dependency_id = fields.Int()
    code = fields.UUID()
    last_change_code = fields.Int()
    insert_user_id = fields.UUID()
    last_update_user_id = fields.UUID()
    dependency_df_task_id = fields.Int()
    dyna_flow_task_id = fields.Int()
    is_placeholder = fields.Bool()
    insert_utc_date_time = fields.DateTime()
    last_update_utc_date_time = fields.DateTime()
    dyna_flow_task_code_peek = fields.UUID()  # DynaFlowTaskID
