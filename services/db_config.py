import uuid
from sqlalchemy.dialects.postgresql import UUID 
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy import String 

db_dialect = None


def generate_uuid():
    return str(uuid.uuid4())


# Conditionally set the UUID column type
if db_dialect == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif db_dialect == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  # This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)


