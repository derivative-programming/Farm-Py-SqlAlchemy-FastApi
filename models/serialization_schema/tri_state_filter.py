# tri_state_filter.py
"""
    #TODO add comment
"""
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import TriStateFilter
class TriStateFilterSchema(SQLAlchemyAutoSchema):
    """
    #TODO add comment
    """
    class Meta:
        model = TriStateFilter
        exclude = (
            "_code",
            "_insert_user_id",
            "_last_update_user_id",
            # description,
            # displayOrder,
            # isActive,
            # lookupEnumName,
            # name,
            # PacID
            # stateIntValue,
# endset  # noqa E122
        )
    tri_state_filter_id = fields.Int()
    code = fields.UUID()
    last_change_code = fields.Int()
    insert_user_id = fields.UUID()
    last_update_user_id = fields.UUID()
    description = fields.Str()
    display_order = fields.Int()
    is_active = fields.Bool()
    lookup_enum_name = fields.Str()
    name = fields.Str()
    pac_id = fields.Int()
    state_int_value = fields.Int()
    insert_utc_date_time = fields.DateTime()
    last_update_utc_date_time = fields.DateTime()
    pac_code_peek = fields.UUID()  # PacID
# endset
