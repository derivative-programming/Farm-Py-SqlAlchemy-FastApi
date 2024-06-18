# customer_role.py
"""
    #TODO add comment
"""
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import CustomerRole
class CustomerRoleSchema(SQLAlchemyAutoSchema):
    """
    #TODO add comment
    """
    class Meta:
        """
            #TODO add comment
        """
        model = CustomerRole
        exclude = (
            "_customer_role_id",
            "_code",
            "_insert_user_id",
            "_last_update_user_id",
            "_last_change_code",
            "_customer_id",  # CustomerID
            "_is_placeholder",  # isPlaceholder
            "_placeholder",  # placeholder
            "_role_id",  # roleID
# endset  # noqa E122
        )
    customer_role_id = fields.Int()
    code = fields.UUID()
    last_change_code = fields.Int()
    insert_user_id = fields.UUID()
    last_update_user_id = fields.UUID()
    customer_id = fields.Int()
    is_placeholder = fields.Bool()
    placeholder = fields.Bool()
    role_id = fields.Int()
    insert_utc_date_time = fields.DateTime()
    last_update_utc_date_time = fields.DateTime()
    customer_code_peek = fields.UUID()  # CustomerID
    role_code_peek = fields.UUID()   # RoleID
# endset
