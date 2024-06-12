# services/db_config.py

"""
    #TODO add comment
"""

import uuid
# from sqlalchemy.dialects.postgresql import UUID
# from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
# from sqlalchemy import String

DB_DIALECT = None


def generate_uuid():
    """
    #TODO add comment
    """
    return str(uuid.uuid4())
