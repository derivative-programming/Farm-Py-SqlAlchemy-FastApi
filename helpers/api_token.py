import jwt
import datetime
import os 
import logging 
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name='API_KEY', auto_error=False)
 
class ApiToken:

    @staticmethod
    def create_token(payload:dict, expires_in_day_count:int): 
        logging.info("create_token Start")

        payload["exp"] = datetime.datetime.utcnow() + datetime.timedelta(days=expires_in_day_count)

        logging.info(str(payload))
        token = ""
        # token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        token = jwt.encode(payload, "xxxxx", algorithm='HS256')
        logging.info("create_token: " + token)
        logging.info("create_token End")
        return token

    @staticmethod
    def validate_token(token:str) -> dict:
        if token is None:
            logging.info("No auth token found") 
            return dict()
        if token == "":
            logging.info("Empty auth token found") 
            return dict()
        try:
            payload = ""
            # Decode the token and verify its validity
            # payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            payload = jwt.decode(token, "xxxxx", algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            logging.info("Auth token expired") 
            return dict()  # The token has expired
        except jwt.InvalidTokenError:
            logging.info("Auth token invalid") 
            return dict()  # The token is invalid