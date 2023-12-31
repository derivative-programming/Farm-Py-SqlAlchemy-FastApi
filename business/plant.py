import random
import uuid
from typing import List
from datetime import datetime, date
from sqlalchemy import Index, event, BigInteger, Boolean, Column, Date, DateTime, Float, Integer, Numeric, String, ForeignKey, Uuid, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER 
from helpers.session_context import SessionContext 
from services.db_config import db_dialect,generate_uuid 
from managers import PlantManager
from models import Plant
import models
import managers as managers_and_enums
from .base_bus_obj import BaseBusObj
##GENINCLUDEFILE[GENVALPascalName.top.include.*]

class PlantInvalidInitError(Exception):
    pass


#Conditionally set the UUID column type
if db_dialect == 'postgresql':
    UUIDType = UUID(as_uuid=True)
elif db_dialect == 'mssql':
    UUIDType = UNIQUEIDENTIFIER
else:  #This will cover SQLite, MySQL, and other databases
    UUIDType = String(36)

class PlantBusObj(BaseBusObj):
    def __init__(self, session_context:SessionContext):
        
        if not session_context.session:
            raise ValueError("session required") 
         
        self._session_context = session_context 
        self.plant = Plant()



    @property
    def plant_id(self):
        return self.plant.plant_id

    @plant_id.setter
    def code(self, value: int):
        if not isinstance(value, int):
            raise ValueError("plant_id must be a int.")
        self.plant.plant_id = value
    
    #code
    @property
    def code(self):
        return self.plant.code

    @code.setter
    def code(self, value: UUIDType):
        #if not isinstance(value, UUIDType):
        #raise ValueError("code must be a UUID.")
        self.plant.code = value

    #last_change_code
    @property
    def last_change_code(self):
        return self.plant.last_change_code

    @last_change_code.setter
    def last_change_code(self, value: int):
        if not isinstance(value, int):
            raise ValueError("last_change_code must be an integer.")
        self.plant.last_change_code = value

    #insert_user_id
    @property
    def insert_user_id(self):
        return self.plant.insert_user_id

    @insert_user_id.setter
    def insert_user_id(self, value: uuid.UUID):
        if not isinstance(value, uuid.UUID):
            raise ValueError("insert_user_id must be a UUID.")
        self.plant.insert_user_id = value

    def set_prop_insert_user_id(self, value: uuid.UUID):
        self.insert_user_id = value
        return self

    #last_update_user_id
    @property
    def last_update_user_id(self):
        return self.plant.last_update_user_id

    @last_update_user_id.setter
    def last_update_user_id(self, value: uuid.UUID):
        if not isinstance(value, uuid.UUID):
            raise ValueError("last_update_user_id must be a UUID.")
        self.plant.last_update_user_id = value

    def set_prop_last_update_user_id(self, value: uuid.UUID):
        self.last_update_user_id = value
        return self

#endset

    #FlvrForeignKeyID

    #IsDeleteAllowed
    @property
    def is_delete_allowed(self):
        return self.plant.is_delete_allowed

    @is_delete_allowed.setter
    def is_delete_allowed(self, value: bool):
        if not isinstance(value, bool):
            raise ValueError("is_delete_allowed must be a boolean.")
        self.plant.is_delete_allowed = value

    def set_prop_is_delete_allowed(self, value: bool):
        self.is_delete_allowed = value
        return self

    

    #IsEditAllowed
    @property
    def is_edit_allowed(self):
        return self.plant.is_edit_allowed

    @is_edit_allowed.setter
    def is_edit_allowed(self, value):
        assert isinstance(value, bool), "is_edit_allowed must be a boolean"
        self.plant.is_edit_allowed = value

    def set_prop_is_edit_allowed(self, value: bool):
        self.is_edit_allowed = value
        return self


    #OtherFlavor
    @property
    def other_flavor(self):
        return self.plant.other_flavor

    @other_flavor.setter
    def other_flavor(self, value):
        assert isinstance(value, str), "other_flavor must be a string"
        self.plant.other_flavor = value

    def set_prop_other_flavor(self, value):
        self.other_flavor = value
        return self

    #SomeBigIntVal
    @property
    def some_big_int_val(self):
        return self.plant.some_big_int_val

    @some_big_int_val.setter
    def some_big_int_val(self, value):
        assert isinstance(value, int), "some_big_int_val must be an integer"
        self.plant.some_big_int_val = value

    def set_prop_some_big_int_val(self, value):
        self.some_big_int_val = value
        return self

    #SomeBitVal
    @property
    def some_bit_val(self):
        return self.plant.some_bit_val

    @some_bit_val.setter
    def some_bit_val(self, value):
        assert isinstance(value, bool), "some_bit_val must be a boolean"
        self.plant.some_bit_val = value

    def set_prop_some_bit_val(self, value):
        self.some_bit_val = value
        return self

    #SomeDateVal
    @property
    def some_date_val(self):
        return self.plant.some_date_val

    @some_date_val.setter
    def some_date_val(self, value):
        assert isinstance(value, date), "some_date_val must be a date object"
        self.plant.some_date_val = value

    def set_prop_some_date_val(self, value):
        self.some_date_val = value
        return self

    #SomeDecimalVal
    @property
    def some_decimal_val(self):
        return self.plant.some_decimal_val

    @some_decimal_val.setter
    def some_decimal_val(self, value):
        assert isinstance(value, (int, float)), "some_decimal_val must be a number"
        self.plant.some_decimal_val = value

    def set_prop_some_decimal_val(self, value):
        self.some_decimal_val = value
        return self

    #SomeEmailAddress
    @property
    def some_email_address(self):
        return self.plant.some_email_address

    @some_email_address.setter
    def some_email_address(self, value):
        assert isinstance(value, str), "some_email_address must be a string"
        self.plant.some_email_address = value

    def set_prop_some_email_address(self, value):
        self.some_email_address = value
        return self

    #SomeFloatVal
    @property
    def some_float_val(self):
        return self.plant.some_float_val

    @some_float_val.setter
    def some_float_val(self, value):
        assert isinstance(value, float), "some_float_val must be a float"
        self.plant.some_float_val = value

    def set_prop_some_float_val(self, value):
        self.some_float_val = value
        return self

    #SomeIntVal
    @property
    def some_int_val(self):
        return self.plant.some_int_val

    @some_int_val.setter
    def some_int_val(self, value):
        assert isinstance(value, int), "some_int_val must be an integer"
        self.plant.some_int_val = value

    def set_prop_some_int_val(self, value):
        self.some_int_val = value
        return self

    #SomeMoneyVal
    @property
    def some_money_val(self):
        return self.plant.some_money_val

    @some_money_val.setter
    def some_money_val(self, value):
        assert isinstance(value, (int, float)), "some_money_val must be a number"
        self.plant.some_money_val = value

    def set_prop_some_money_val(self, value):
        self.some_money_val = value
        return self

    #SomeNVarCharVal
    @property
    def some_n_var_char_val(self):
        return self.plant.some_n_var_char_val

    @some_n_var_char_val.setter
    def some_n_var_char_val(self, value):
        assert isinstance(value, str), "some_n_var_char_val must be a string"
        self.plant.some_n_var_char_val = value

    def set_prop_some_n_var_char_val(self, value):
        self.some_n_var_char_val = value
        return self

    #somePhoneNumber
    @property
    def some_phone_number(self):
        return self.plant.some_phone_number

    @some_phone_number.setter
    def some_phone_number(self, value):
        assert isinstance(value, str), "some_phone_number must be a string"
        self.plant.some_phone_number = value

    def set_prop_some_phone_number(self, value):
        self.some_phone_number = value
        return self

    #SomeTextVal
    @property
    def some_text_val(self):
        return self.plant.some_text_val

    @some_text_val.setter
    def some_text_val(self, value):
        assert isinstance(value, str), "some_text_val must be a string"
        self.plant.some_text_val = value

    def set_prop_some_text_val(self, value):
        self.some_text_val = value
        return self

    #SomeUniqueidentifierVal
    @property
    def some_uniqueidentifier_val(self):
        return self.plant.some_uniqueidentifier_val

    @some_uniqueidentifier_val.setter
    def some_uniqueidentifier_val(self, value):
        assert isinstance(value, UUIDType), "some_uniqueidentifier_val must be a UUID"
        self.plant.some_uniqueidentifier_val = value

    def set_prop_some_uniqueidentifier_val(self, value):
        self.some_uniqueidentifier_val = value
        return self

    #SomeUTCDateTimeVal
    @property
    def some_utc_date_time_val(self):
        return self.plant.some_utc_date_time_val

    @some_utc_date_time_val.setter
    def some_utc_date_time_val(self, value):
        assert isinstance(value, datetime), "some_utc_date_time_val must be a datetime object"
        self.plant.some_utc_date_time_val = value

    def set_prop_some_utc_date_time_val(self, value):
        self.some_utc_date_time_val = value
        return self

    #SomeVarCharVal
    @property
    def some_var_char_val(self):
        return self.plant.some_var_char_val

    @some_var_char_val.setter
    def some_var_char_val(self, value):
        assert isinstance(value, str), "some_var_char_val must be a string"
        self.plant.some_var_char_val = value

    def set_prop_some_var_char_val(self, value):
        self.some_var_char_val = value
        return self

    #LandID

#endset

    #isDeleteAllowed,
    #isEditAllowed,
    #otherFlavor, 
    #someBigIntVal,
    #someBitVal, 
    #someDecimalVal,
    #someEmailAddress,
    #someFloatVal,
    #someIntVal,
    #someMoneyVal,
    #someNVarCharVal, 
    #someDateVal
    #someUTCDateTimeVal
    #FlvrForeignKeyID
    @property
    def flvr_foreign_key_id(self):
        return self.plant.flvr_foreign_key_id

    @flvr_foreign_key_id.setter
    def flvr_foreign_key_id(self, value: int):
        if not isinstance(value, int):
            raise ValueError("flvr_foreign_key_id must be an integer.")
        self.plant.flvr_foreign_key_id = value

    def set_prop_flvr_foreign_key_id(self, value):
        self.flvr_foreign_key_id = value
        return self

    @property 
    def flvr_foreign_key_code_peek(self):
        return self.plant.flvr_foreign_key_code_peek

    # @flvr_foreign_key_code_peek.setter
    # def flvr_foreign_key_code_peek(self, value):
    #     assert isinstance(value, UUIDType), "flvr_foreign_key_code_peek must be a UUID"
    #     self.plant.flvr_foreign_key_code_peek = value

    #LandID
    @property
    def land_id(self):
        return self.plant.land_id

    @land_id.setter
    def land_id(self, value):
        assert isinstance(value, int) or value is None, "land_id must be an integer or None"
        self.plant.land_id = value

    def set_prop_land_id(self, value):
        self.land_id = value
        return self

    @property 
    def land_code_peek(self):
        return self.plant.land_code_peek

    # @land_code_peek.setter
    # def land_code_peek(self, value):
    #     assert isinstance(value, UUIDType), "land_code_peek must be a UUID"
    #     self.plant.land_code_peek = value


    #somePhoneNumber,
    #someTextVal,
    #someUniqueidentifierVal, 
    #someVarCharVal,
    
#endset

    #insert_utc_date_time
    @property
    def insert_utc_date_time(self):
        return self.plant.insert_utc_date_time

    @insert_utc_date_time.setter
    def insert_utc_date_time(self, value):
        assert isinstance(value, datetime) or value is None, "insert_utc_date_time must be a datetime object or None"
        self.plant.insert_utc_date_time = value

    #update_utc_date_time
    @property
    def last_update_utc_date_time(self):
        return self.plant.last_update_utc_date_time

    @last_update_utc_date_time.setter
    def last_update_utc_date_time(self, value):
        assert isinstance(value, datetime) or value is None, "last_update_utc_date_time must be a datetime object or None"
        self.plant.last_update_utc_date_time = value

##GENTrainingBlock[caseLookupEnums]Start
##GENLearn[isLookup=false]Start  

    async def load(self, json_data:str=None, 
                   code:uuid.UUID=None, 
                   plant_id:int=None, 
                   plant_obj_instance:Plant=None, 
                   plant_dict:dict=None):
         
        if plant_id and self.plant.plant_id is None:
            plant_manager = PlantManager(self._session_context)
            plant_obj = await plant_manager.get_by_id(plant_id)
            self.plant = plant_obj

        if code and self.plant.plant_id is None:
            plant_manager = PlantManager(self._session_context)
            plant_obj = await plant_manager.get_by_code(code)
            self.plant = plant_obj 
            
        if plant_obj_instance and self.plant.plant_id is None: 
            plant_manager = PlantManager(self._session_context)
            plant_obj = await plant_manager.get_by_id(plant_obj_instance.plant_id)
            self.plant = plant_obj
            
        if json_data and self.plant.plant_id is None: 
            plant_manager = PlantManager(self._session_context)
            self.plant = plant_manager.from_json(json_data)  
            
        if plant_dict and self.plant.plant_id is None: 
            plant_manager = PlantManager(self._session_context)
            self.plant = plant_manager.from_dict(plant_dict)  

        return self
            
    @staticmethod
    async def get(session_context:SessionContext, 
                    json_data:str=None, 
                   code:uuid.UUID=None, 
                   plant_id:int=None, 
                   plant_obj_instance:Plant=None, 
                   plant_dict:dict=None):
        result = PlantBusObj(session_context)

        await result.load(
            json_data,
            code,
            plant_id,
            plant_obj_instance,
            plant_dict
        )
        
        return result
##GENLearn[isLookup=false]End
##GENTrainingBlock[caseLookupEnums]End 
    
    async def refresh(self):
        plant_manager = PlantManager(self._session_context)
        self.plant = await plant_manager.refresh(self.plant)

        return self
    
    def is_valid(self):
        return (self.plant is not None)
    
    def to_dict(self):
        plant_manager = PlantManager(self._session_context)
        return plant_manager.to_dict(self.plant)
        
    def to_json(self):
        plant_manager = PlantManager(self._session_context)
        return plant_manager.to_json(self.plant)
    
    
    async def save(self):
        if self.plant.plant_id is not None and self.plant.plant_id > 0:
            plant_manager = PlantManager(self._session_context)
            self.plant = await plant_manager.update(self.plant)
        if self.plant.plant_id is None or self.plant.plant_id == 0:
            plant_manager = PlantManager(self._session_context)
            self.plant = await plant_manager.add(self.plant)

        return self
 
    
    async def delete(self):
        if self.plant.plant_id > 0:
            plant_manager = PlantManager(self._session_context)
            await plant_manager.delete(self.plant.plant_id)
            self.plant = None

    
    async def randomize_properties(self):
        self.plant.flvr_foreign_key_id =  random.choice(await managers_and_enums.FlavorManager(self._session_context).get_list()).flavor_id
        self.plant.is_delete_allowed = random.choice([True, False])
        self.plant.is_edit_allowed = random.choice([True, False])
        # self.plant.land_id = random.randint(0, 100)
        self.plant.other_flavor = "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        self.plant.some_big_int_val = random.randint(0, 1000000)
        self.plant.some_bit_val = random.choice([True, False])
        self.plant.some_date_val = date(random.randint(2000, 2023), random.randint(1, 12), random.randint(1, 28))
        self.plant.some_decimal_val = round(random.uniform(0, 100), 2)
        self.plant.some_email_address = f"user{random.randint(1, 1000)}@example.com"
        self.plant.some_float_val = random.uniform(0, 100)
        self.plant.some_int_val = random.randint(0, 100)
        self.plant.some_money_val = round(random.uniform(0, 10000), 2)
        self.plant.some_n_var_char_val = "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        self.plant.some_phone_number = f"+1{random.randint(1000000000, 9999999999)}"
        self.plant.some_text_val = "Random text"
        self.plant.some_uniqueidentifier_val = generate_uuid()
        self.plant.some_utc_date_time_val = datetime(random.randint(2000, 2023), random.randint(1, 12), random.randint(1, 28))
        self.plant.some_var_char_val = "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=10))
#endset

        return self
 
    def get_plant_obj(self) -> Plant:
        return self.plant
     
    
    def is_equal(self,plant:Plant) -> Plant:
        plant_manager = PlantManager(self._session_context)
        my_plant = self.get_plant_obj()
        return plant_manager.is_equal(plant, my_plant)
#endset

    #isDeleteAllowed,
    #isEditAllowed,
    #otherFlavor, 
    #someBigIntVal,
    #someBitVal, 
    #someDecimalVal,
    #someEmailAddress,
    #someFloatVal,
    #someIntVal,
    #someMoneyVal,
    #someNVarCharVal, 
    #someDateVal
    #someUTCDateTimeVal
    #LandID
    async def get_land_id_rel_obj(self) -> models.Land:  
        land_manager = managers_and_enums.LandManager(self._session_context)
        land_obj = await land_manager.get_by_id(self.land_id) 
        return land_obj 
    
    #FlvrForeignKeyID 
    async def get_flvr_foreign_key_id_rel_obj(self) -> models.Flavor: 
        flavor_manager = managers_and_enums.FlavorManager(self._session_context)
        flavor_obj = await flavor_manager.get_by_id(self.flvr_foreign_key_id) 
        return flavor_obj
    #somePhoneNumber,
    #someTextVal,
    #someUniqueidentifierVal, 
    #someVarCharVal,
    
#endset

    def get_obj(self) -> Plant:
        return self.plant
    
    def get_object_name(self) -> str:
        return "plant"
    
    def get_id(self) -> int:
        return self.plant_id
      
    
    #isDeleteAllowed,
    #isEditAllowed,
    #otherFlavor, 
    #someBigIntVal,
    #someBitVal, 
    #someDecimalVal,
    #someEmailAddress,
    #someFloatVal,
    #someIntVal,
    #someMoneyVal,
    #someNVarCharVal, 
    #someDateVal
    #someUTCDateTimeVal
    #FlvrForeignKeyID
    #LandID   
    async def get_parent_name(self) -> str: 
        return 'Land'
    async def get_parent_code(self) -> uuid.UUID: 
        return self.land_code_peek
    async def get_parent_obj(self) -> models.Land: 
        return self.get_land_id_rel_obj()
    #somePhoneNumber,
    #someTextVal,
    #someUniqueidentifierVal, 
    #someVarCharVal,
#endset

    @staticmethod
    async def to_bus_obj_list(session_context:SessionContext, obj_list:List[Plant]):

        result = list()

        for plant in obj_list:
            plant_bus_obj = PlantBusObj.get(session_context,plant_obj_instance=plant)
            result.append(plant_bus_obj)

        return result

          
    ##GENINCLUDEFILE[GENVALPascalName.bottom.include.*]
     
