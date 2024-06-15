# customer.py
"""
    #TODO add comment
"""
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import Customer
class CustomerSchema(SQLAlchemyAutoSchema):
    """
    #TODO add comment
    """
    class Meta:
        """
            #TODO add comment
        """
        model = Customer
        exclude = (
            "_code",
            "_insert_user_id",
            "_last_update_user_id",
            # activeOrganizationID,
            # email,
            # emailConfirmedUTCDateTime
            # firstName,
            # forgotPasswordKeyExpirationUTCDateTime
            # forgotPasswordKeyValue,
            # fSUserCodeValue,
            "_fs_user_code_value",
            # isActive,
            # isEmailAllowed,
            # isEmailConfirmed,
            # isEmailMarketingAllowed,
            # isLocked,
            # isMultipleOrganizationsAllowed,
            # isVerboseLoggingForced,
            # lastLoginUTCDateTime
            # lastName,
            # password,
            # phone,
            # province,
            # registrationUTCDateTime
            # TacID
            # uTCOffsetInMinutes,
            # zip,
# endset  # noqa E122
        )
    customer_id = fields.Int()
    code = fields.UUID()
    last_change_code = fields.Int()
    insert_user_id = fields.UUID()
    last_update_user_id = fields.UUID()
    active_organization_id = fields.Int()
    email = fields.Str()
    email_confirmed_utc_date_time = fields.DateTime()  # (format="%Y-%m-%dT%H:%M:%S")
    first_name = fields.Str()
    forgot_password_key_expiration_utc_date_time = fields.DateTime()  # (format="%Y-%m-%dT%H:%M:%S")
    forgot_password_key_value = fields.Str()
    fs_user_code_value = fields.UUID()
    is_active = fields.Bool()
    is_email_allowed = fields.Bool()
    is_email_confirmed = fields.Bool()
    is_email_marketing_allowed = fields.Bool()
    is_locked = fields.Bool()
    is_multiple_organizations_allowed = fields.Bool()
    is_verbose_logging_forced = fields.Bool()
    last_login_utc_date_time = fields.DateTime()  # (format="%Y-%m-%dT%H:%M:%S")
    last_name = fields.Str()
    password = fields.Str()
    phone = fields.Str()
    province = fields.Str()
    registration_utc_date_time = fields.DateTime()  # (format="%Y-%m-%dT%H:%M:%S")
    tac_id = fields.Int()
    utc_offset_in_minutes = fields.Int()
    zip = fields.Str()
    insert_utc_date_time = fields.DateTime()
    last_update_utc_date_time = fields.DateTime()
    tac_code_peek = fields.UUID()  # TacID
# endset
