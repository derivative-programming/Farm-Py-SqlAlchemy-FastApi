import json 
import traceback 
from django.db import transaction
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet 
from rest_framework import status 
import marshmallow_dataclass
import logging
import marshmallow.exceptions  
from helpers import SessionContext, ApiToken
import apis.models as view_models
import apis.models.init as view_init_models 
class LandPlantListViewSet(ViewSet):  
    isGetAvailable:bool = False
    isGetWithIdAvailable:bool = True
    isGetInitAvailable:bool = True
    isGetToCsvAvailable:bool = True
    isPostAvailable:bool = False
    isPostWithIdAvailable:bool = False
    isPutAvailable:bool = False 
    isDeleteAvailable:bool = False  
    isPublic: bool = False

    def get_token(self, request):
        token = request.META.get('HTTP_API_KEY')
        return token
    
    @action(detail=False, methods=['get'],url_path=r'(?P<landCode>[0-9a-f-]{36})/init')
    def request_get_init(self, request, landCode=None, *args, **kwargs):
        logging.debug('LandPlantListViewSet.request_get_init start. landCode:' + landCode)
        if self.isGetInitAvailable == False:
            return Response(status=status.HTTP_501_NOT_IMPLEMENTED) 
##GENTrainingBlock[caseisGetInitAvailable]Start
##GENLearn[isGetInitAvailable=true]Start
        response = view_init_models.LandPlantListInitReportGetInitModelResponse() 

        auth_dict = dict()
        if self.isPublic == False:
            token = self.get_token(request)
            auth_dict = ApiToken.validate_token(token)
            if auth_dict == None or len(auth_dict) == 0:
                return Response(json.loads(response.to_json()),status=status.HTTP_401_UNAUTHORIZED)   
            
        sid = transaction.savepoint()
        try: 
            logging.debug("Start session...")
            session_context = SessionContext(auth_dict)
            land_code = session_context.check_context_code("LandCode", landCode)
            init_request = view_init_models.LandPlantListInitReportGetInitModelRequest() 
            response = init_request.process_request(
                session_context,
                landCode,
                response
            )  
        except TypeError as te: 
            response.success = False
            traceback_string = "".join(traceback.format_tb(te.__traceback__))
            response.message = str(te) + " traceback:" + traceback_string 
        except Exception as e:
            response.success = False
            traceback_string = "".join(traceback.format_tb(e.__traceback__))
            response.message = str(e) + " traceback:" + traceback_string
        finally:
            if response.success == True:
                transaction.savepoint_commit(sid)
            else:
                transaction.savepoint_rollback(sid)
        logging.debug('LandPlantListViewSet.init get result:' + response.to_json())
        responseDict = json.loads(response.to_json())
        return Response(responseDict,status=status.HTTP_200_OK) 
##GENLearn[isGetInitAvailable=true]End
##GENTrainingBlock[caseisGetInitAvailable]End 
    def list(self, request, *args, **kwargs):
        logging.debug('LandPlantListViewSet.request_get start.')
        if self.isGetAvailable == False:
            return Response(status=status.HTTP_501_NOT_IMPLEMENTED) 
##GENTrainingBlock[caseisGetAvailable]Start
##GENLearn[isGetAvailable=false]Start
##GENLearn[isGetAvailable=false]End
##GENTrainingBlock[caseisGetAvailable]End
    @action(detail=False, methods=['get'],url_path=r'(?P<landCode>[0-9a-f-]{36})')
    def request_get_with_id(self, request, landCode=None, *args, **kwargs): 
        logging.debug('LandPlantListViewSet.request_get_with_id start. landCode:' + landCode)
        if self.isGetWithIdAvailable == False:
            return Response(status=status.HTTP_501_NOT_IMPLEMENTED)  
##GENTrainingBlock[caseisGetWithIdAvailable]Start
##GENLearn[isGetWithIdAvailable=true]Start
        response = view_models.LandPlantListGetModelResponse()

        auth_dict = dict()
        if self.isPublic == False:
            token = self.get_token(request)
            auth_dict = ApiToken.validate_token(token)
            if auth_dict == None or len(auth_dict) == 0:
                return Response(json.loads(response.to_json()),status=status.HTTP_401_UNAUTHORIZED)   
            
        sid = transaction.savepoint()
        try:
            session_context = SessionContext(auth_dict)
            land_code = session_context.check_context_code("LandCode", landCode)
            logging.debug("Request:" + json.dumps(request.query_params))
            logging.debug("get schema")
            schema = marshmallow_dataclass.class_schema(view_models.LandPlantListGetModelRequest)()
            logging.debug("validating request...")
            request = schema.load(request.query_params)  
            response.request = request
            logging.debug("process request...") 
            response.process_request(
                session_context,
                landCode,
                request
            )  
        except marshmallow.exceptions.ValidationError as se:
            response.success = False
            response.message = "Schema validation error. Invalid Request"  
        except Exception as e:
            response.success = False
            traceback_string = "".join(traceback.format_tb(e.__traceback__))
            response.message = str(e) + " traceback:" + traceback_string
        finally:
            if response.success == True:
                transaction.savepoint_commit(sid)
            else:
                transaction.savepoint_rollback(sid)
        logging.debug('LandPlantListViewSet.submit get result:' + response.to_json())
        responseDict = json.loads(response.to_json())
        return Response(responseDict,status=status.HTTP_200_OK) 
##GENLearn[isGetWithIdAvailable=true]End
##GENTrainingBlock[caseisGetWithIdAvailable]End
    @action(detail=False, methods=['get'],url_path=r'(?P<landCode>[0-9a-f-]{36})/to-csv')
    def request_get_with_id_to_csv(self, request, landCode=None, *args, **kwargs):
        logging.debug('LandPlantListViewSet.request_get_with_id_to_csv start. landCode:' + landCode)
        if self.isGetToCsvAvailable == False:
            return Response(status=status.HTTP_501_NOT_IMPLEMENTED) 
##GENTrainingBlock[caseisGetToCsvAvailable]Start
##GENLearn[isGetToCsvAvailable=true]Start
        response = view_models.LandPlantListGetModelResponse()

        auth_dict = dict()
        if self.isPublic == False:
            token = self.get_token(request)
            auth_dict = ApiToken.validate_token(token)
            if auth_dict == None or len(auth_dict) == 0:
                return Response(json.loads(response.to_json()),status=status.HTTP_401_UNAUTHORIZED)   
            
        sid = transaction.savepoint()
        try:
            session_context = SessionContext(auth_dict)
            land_code = session_context.check_context_code("LandCode", landCode)
            logging.debug("Request:" + json.dumps(request.query_params))
            logging.debug("get schema")
            schema = marshmallow_dataclass.class_schema(view_models.LandPlantListGetModelResponse)()
            logging.debug("validating request...")
            request = schema.load(request.query_params)  
            response.request = request
            logging.debug("process request...") 
            response.process_request(
                session_context,
                landCode,
                request
            )  
        except marshmallow.exceptions.ValidationError as se:
            response.success = False
            response.message = "Schema validation error. Invalid Request"  
        except Exception as e:
            response.success = False
            traceback_string = "".join(traceback.format_tb(e.__traceback__))
            response.message = str(e) + " traceback:" + traceback_string
        finally:
            if response.success == True:
                transaction.savepoint_commit(sid)
            else:
                transaction.savepoint_rollback(sid)
        logging.debug('LandPlantListViewSet.submit get result:' + response.to_json())
        responseDict = json.loads(response.to_json())
        return Response(responseDict,status=status.HTTP_200_OK) 
##GENLearn[isGetToCsvAvailable=true]End
##GENTrainingBlock[caseisGetToCsvAvailable]End 
    def create(self, request, *args, **kwargs):
        logging.debug('LandPlantListViewSet.request_post start.')
        if self.isPostAvailable == False:
            return Response(status=status.HTTP_501_NOT_IMPLEMENTED) 
##GENTrainingBlock[caseisPostAvailable]Start
##GENLearn[isPostAvailable=false]Start
##GENLearn[isPostAvailable=false]End
##GENTrainingBlock[caseisPostAvailable]End
    @action(detail=False, methods=['post'],url_path=r'(?P<landCode>[0-9a-f-]{36})')
    def request_post_with_id(self, request, landCode=None, *args, **kwargs): 
        logging.debug('LandPlantListViewSet.request_post_with_id start. landCode:' + landCode)
        if self.isPostWithIdAvailable == False:
            return Response(status=status.HTTP_501_NOT_IMPLEMENTED) 
##GENTrainingBlock[caseisPostWithIdAvailable]Start
##GENLearn[isPostWithIdAvailable=false]Start
##GENLearn[isPostWithIdAvailable=false]End
##GENTrainingBlock[caseisPostWithIdAvailable]End
    @action(detail=False, methods=['put'])
    def request_put(self, request, landCode=None, *args, **kwargs): 
        logging.debug('LandPlantListViewSet.request_put start.')
        if self.isPutAvailable == False:
            return Response(status=status.HTTP_501_NOT_IMPLEMENTED) 
##GENTrainingBlock[caseisPutAvailable]Start
##GENLearn[isPutAvailable=false]Start
##GENLearn[isPutAvailable=false]End
##GENTrainingBlock[caseisPutAvailable]End
    @action(detail=False, methods=['delete'])
    def request_delete(self, request, landCode=None, *args, **kwargs): 
        logging.debug('LandPlantListViewSet.request_delete start.')
        if self.isDeleteAvailable == False:
            return Response(status=status.HTTP_501_NOT_IMPLEMENTED) 
##GENTrainingBlock[caseisDeleteAvailable]Start
##GENLearn[isDeleteAvailable=false]Start
##GENLearn[isDeleteAvailable=false]End
##GENTrainingBlock[caseisDeleteAvailable]End
