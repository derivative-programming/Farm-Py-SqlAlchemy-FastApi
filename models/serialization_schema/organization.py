# organization.py
"""
    #TODO add comment
"""
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import Organization
class OrganizationSchema(SQLAlchemyAutoSchema):
    """
    #TODO add comment
    """
    class Meta:
        """
            #TODO add comment
        """
        model = Organization
        exclude = (
            "_code",
            "_insert_user_id",
            "_last_update_user_id",
            # name,
            # TacID
# endset  # noqa E122
        )
    organization_id = fields.Int()
    code = fields.UUID()
    last_change_code = fields.Int()
    insert_user_id = fields.UUID()
    last_update_user_id = fields.UUID()
    name = fields.Str()
    tac_id = fields.Int()
    insert_utc_date_time = fields.DateTime()
    last_update_utc_date_time = fields.DateTime()
    tac_code_peek = fields.UUID()  # TacID
# endset
