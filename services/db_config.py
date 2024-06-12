# services/db_config.py

"""
    #TODO add comment
"""

import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy import String

DB_DIALECT = None


def get_uuid_type(db_dialect: str):
    """
    #TODO add comment
    """

    # Conditionally set the UUID column type
    if db_dialect == 'postgresql':
        uuid_type = UUID(as_uuid=True)
    elif db_dialect == 'mssql':
        uuid_type = UNIQUEIDENTIFIER
    else:  # This will cover SQLite, MySQL, and other databases
        uuid_type = String(36)

    return uuid_type


def generate_uuid():
    """
    #TODO add comment
    """

    return str(uuid.uuid4())
