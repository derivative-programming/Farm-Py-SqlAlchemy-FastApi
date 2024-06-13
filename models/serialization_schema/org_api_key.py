# org_api_key.py
"""
    #TODO add comment
"""
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import OrgApiKey
class OrgApiKeySchema(SQLAlchemyAutoSchema):
    """
    #TODO add comment
    """
    class Meta:
        model = OrgApiKey
        exclude = (
            "_code",
            "_insert_user_id",
            "_last_update_user_id",
            # apiKeyValue,
            # createdBy,
            # createdUTCDateTime
            # expirationUTCDateTime
            # isActive,
            # isTempUserKey,
            # name,
            # OrganizationID
            # orgCustomerID
# endset  # noqa E122
        )
    org_api_key_id = fields.Int()
    code = fields.UUID()
    last_change_code = fields.Int()
    insert_user_id = fields.UUID()
    last_update_user_id = fields.UUID()
    api_key_value = fields.Str()
    created_by = fields.Str()
    created_utc_date_time = fields.DateTime()  # (format="%Y-%m-%dT%H:%M:%S")
    expiration_utc_date_time = fields.DateTime()  # (format="%Y-%m-%dT%H:%M:%S")
    is_active = fields.Bool()
    is_temp_user_key = fields.Bool()
    name = fields.Str()
    organization_id = fields.Int()
    org_customer_id = fields.Int()
    insert_utc_date_time = fields.DateTime()
    last_update_utc_date_time = fields.DateTime()
    organization_code_peek = fields.UUID()  # OrganizationID
    org_customer_code_peek = fields.UUID()   # OrgCustomerID
# endset
