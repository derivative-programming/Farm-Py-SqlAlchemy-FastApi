# org_customer.py
"""
    #TODO add comment
"""
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import OrgCustomer
class OrgCustomerSchema(SQLAlchemyAutoSchema):
    """
    #TODO add comment
    """
    class Meta:
        """
            #TODO add comment
        """
        model = OrgCustomer
        exclude = (
            "_org_customer_id",
            "_code",
            "_insert_user_id",
            "_last_update_user_id",
            # customerID
            # email,
            # OrganizationID
# endset  # noqa E122
        )
    org_customer_id = fields.Int()
    code = fields.UUID()
    last_change_code = fields.Int()
    insert_user_id = fields.UUID()
    last_update_user_id = fields.UUID()
    customer_id = fields.Int()
    email = fields.Str()
    organization_id = fields.Int()
    insert_utc_date_time = fields.DateTime()
    last_update_utc_date_time = fields.DateTime()
    customer_code_peek = fields.UUID()   # CustomerID
    organization_code_peek = fields.UUID()  # OrganizationID
# endset
