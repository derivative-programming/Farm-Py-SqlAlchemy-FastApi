# from django.test import TestCase
# from reports.providers import ReportProviderPlantUserDetails
# from datetime import date, datetime
# import uuid
# from decimal import Decimal
# from helpers import SessionContext,TypeConversion
# from models.factories import PlantFactory
# from models import CurrentRuntime
# class ReportProviderPlantUserDetailsTest(TestCase):
#     def setUp(self):
#         CurrentRuntime.initialize()
#         session_context = SessionContext(dict())
#         self.report_provider = ReportProviderPlantUserDetails(session_context)
#         self.plant = PlantFactory.create()
#         self.plant_code = self.plant.code

#         self.page_number = 1
#         self.item_count_per_page = 10
#         self.order_by_column_name = ""
#         self.order_by_descending = False
#     def test_generate_list(self):
#         results = self.report_provider.generate_list(
#             self.plant_code,

#             self.page_number,
#             self.item_count_per_page,
#             self.order_by_column_name,
#             self.order_by_descending
#         )
#         self.assertIsInstance(results, list)
#         for result in results:
#             self.assertIsInstance(result, dict)
#             self.assertIn("flavor_name", result)
#             self.assertIn("is_delete_allowed", result)
#             self.assertIn("is_edit_allowed", result)
#             self.assertIn("other_flavor", result)
#             self.assertIn("some_big_int_val", result)
#             self.assertIn("some_bit_val", result)
#             self.assertIn("some_date_val", result)
#             self.assertIn("some_decimal_val", result)
#             self.assertIn("some_email_address", result)
#             self.assertIn("some_float_val", result)
#             self.assertIn("some_int_val", result)
#             self.assertIn("some_money_val", result)
#             self.assertIn("some_n_var_char_val", result)
#             self.assertIn("some_phone_number", result)
#             self.assertIn("some_text_val", result)
#             self.assertIn("some_uniqueidentifier_val", result)
#             self.assertIn("some_utc_date_time_val", result)
#             self.assertIn("some_var_char_val", result)
#             self.assertIn("phone_num_conditional_on_is_editable", result)
#             self.assertIn("n_var_char_as_url", result)
#             self.assertIn("update_button_text_link_plant_code", result)
#             self.assertIn("random_property_updates_link_plant_code", result)
#             self.assertIn("back_to_dashboard_link_tac_code", result)
#             # self.assertEqual(result["field_one__list_link_plant_code"], str(self.plantCode).replace('-', ''))

