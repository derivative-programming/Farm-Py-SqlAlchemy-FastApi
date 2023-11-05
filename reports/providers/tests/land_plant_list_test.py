# from django.test import TestCase
# from reports.providers import ReportProviderLandPlantList
# from datetime import date, datetime
# import uuid
# from decimal import Decimal
# from helpers import SessionContext,TypeConversion
# from models.factories import LandFactory
# from models import CurrentRuntime

# class ReportProviderLandPlantListTest(TestCase):

#     def setUp(self):
#         CurrentRuntime.initialize()
#         session_context = SessionContext(dict())
#         self.report_provider = ReportProviderLandPlantList(session_context)
#         self.land = LandFactory.create()
#         self.land_code = self.land.code  
        
#         self.some_int_val: int = 0
#         self.some_big_int_val: int = 0
#         self.some_bit_val: bool = False
#         self.is_edit_allowed: bool = False
#         self.is_delete_allowed: bool = False
#         self.some_float_val: float = 0
#         self.some_decimal_val: Decimal = Decimal(0)
#         self.some_min_utc_date_time_val: datetime = TypeConversion.get_default_date_time()
#         self.some_min_date_val: date  = TypeConversion.get_default_date()
#         self.some_money_val: Decimal = Decimal(0)
#         self.some_n_var_char_val: str = ""
#         self.some_var_char_val: str = ""
#         self.some_text_val: str = ""
#         self.some_phone_number: str = ""
#         self.some_email_address: str = ""
#         self.flavor_code: uuid = uuid.UUID(int=0)

#         self.page_number = 1
#         self.item_count_per_page = 10
#         self.order_by_column_name = "" 
#         self.order_by_descending = False

#     def test_generate_list(self):
#         results = self.report_provider.generate_list(
#             self.land_code,  
#             self.some_int_val, 
#             self.some_big_int_val,
#             self.some_bit_val,
#             self.is_edit_allowed,
#             self.is_delete_allowed,
#             self.some_float_val,
#             self.some_decimal_val, 
#             self.some_min_utc_date_time_val,
#             self.some_min_date_val,
#             self.some_money_val, 
#             self.some_n_var_char_val,
#             self.some_var_char_val,
#             self.some_text_val,
#             self.some_phone_number,
#             self.some_email_address,
#             self.flavor_code, 
#             self.page_number,
#             self.item_count_per_page,
#             self.order_by_column_name,
#             self.order_by_descending
#         )
#         self.assertIsInstance(results, list)
#         for result in results:
#             self.assertIsInstance(result, dict)
#             self.assertIn("plant_code", result)
#             self.assertIn("some_int_val", result)
#             self.assertIn("some_big_int_val", result)
#             self.assertIn("some_bit_val", result)
#             self.assertIn("is_edit_allowed", result)
#             self.assertIn("is_delete_allowed", result)
#             self.assertIn("some_float_val", result)
#             self.assertIn("some_decimal_val", result)
#             self.assertIn("some_utc_date_time_val", result)
#             self.assertIn("some_date_val", result)
#             self.assertIn("some_money_val", result)
#             self.assertIn("some_n_var_char_val", result)
#             self.assertIn("some_var_char_val", result)
#             self.assertIn("some_text_val", result)
#             self.assertIn("some_phone_number", result)
#             self.assertIn("some_email_address", result)
#             self.assertIn("flavor_name", result)
#             self.assertIn("flavor_code", result)
#             self.assertIn("some_int_conditional_on_deletable", result)
#             self.assertIn("n_var_char_as_url", result)
#             self.assertIn("update_link_plant_code", result)
#             self.assertIn("delete_async_button_link_plant_code", result)
#             self.assertIn("details_link_plant_code", result) 
#             # self.assertEqual(result["field_one_plant_list_link_land_code"], str(self.landCode).replace('-', ''))