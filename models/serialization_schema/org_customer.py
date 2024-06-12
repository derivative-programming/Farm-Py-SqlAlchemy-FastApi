# org_customer.py
"""
    #TODO add comment
"""
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from models import OrgCustomer
from services.db_config import DB_DIALECT
# Conditionally set the UUID column type
if DB_DIALECT == 'postgresql':
    schema_UUIDType = fields.UUID()
elif DB_DIALECT == 'mssql':
    schema_UUIDType = UNIQUEIDENTIFIER
else:  # This will cover SQLite, MySQL, and other databases
    schema_UUIDType = fields.Str()
class OrgCustomerSchema(SQLAlchemyAutoSchema):
    """
    #TODO add comment
    """
    class Meta:
        model = OrgCustomer
    org_customer_id = fields.Int()
    code = schema_UUIDType
    last_change_code = fields.Int()
    insert_user_id = schema_UUIDType
    last_update_user_id = schema_UUIDType
    customer_id = fields.Int()
    email = fields.Str()
    organization_id = fields.Int()
    insert_utc_date_time = fields.DateTime()
    last_update_utc_date_time = fields.DateTime()
    customer_code_peek = schema_UUIDType   # CustomerID
    organization_code_peek = schema_UUIDType  # OrganizationID
# endset
