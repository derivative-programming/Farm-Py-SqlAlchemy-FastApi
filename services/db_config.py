import uuid

db_dialect = None


def generate_uuid():
    return str(uuid.uuid4())