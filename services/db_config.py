import uuid
from sqlalchemy.dialects.postgresql import UUID 
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy import String 

db_dialect = None


def generate_uuid():
    return str(uuid.uuid4())

 


