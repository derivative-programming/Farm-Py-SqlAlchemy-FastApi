# models/serialization_schema/org_api_key.py
# pylint: disable=unused-import

"""
This module contains the
OrgApiKeySchema
class, which is responsible
for serializing and deserializing
OrgApiKey objects.
"""

from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import OrgApiKey


class OrgApiKeySchema(SQLAlchemyAutoSchema):
    """
    Schema class for serializing and deserializing
    OrgApiKey objects.
    """

    class Meta:
        """
        Meta class for defining the schema's metadata.
        """

        model = OrgApiKey
        exclude = (
            "_org_api_key_id",
            "_code",
            "_insert_user_id",
            "_last_update_user_id",
            "_last_change_code",
            "_insert_utc_date_time",
            "_last_update_utc_date_time",
            "_api_key_value",  # apiKeyValue
            "_created_by",  # createdBy
            "_created_utc_date_time",  # createdUTCDateTime
            "_expiration_utc_date_time",  # expirationUTCDateTime
            "_is_active",  # isActive
            "_is_temp_user_key",  # isTempUserKey
            "_name",  # name
            "_organization_id",  # OrganizationID
            "_org_customer_id",  # orgCustomerID
# endset  # noqa E122
        )

    org_api_key_id = fields.Int()
    code = fields.UUID()
    last_change_code = fields.Int()
    insert_user_id = fields.UUID()
    last_update_user_id = fields.UUID()
    api_key_value = fields.Str()
    created_by = fields.Str()
    created_utc_date_time = \
        fields.DateTime()  # (format="%Y-%m-%dT%H:%M:%S")
    expiration_utc_date_time = \
        fields.DateTime()  # (format="%Y-%m-%dT%H:%M:%S")
    is_active = fields.Bool()
    is_temp_user_key = fields.Bool()
    name = fields.Str()
    organization_id = fields.Int()
    org_customer_id = fields.Int()
    insert_utc_date_time = fields.DateTime()
    last_update_utc_date_time = fields.DateTime()
    organization_code_peek = fields.UUID()  # OrganizationID
    org_customer_code_peek = fields.UUID()   # OrgCustomerID

