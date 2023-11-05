# from django.test import TestCase
# from reports.providers import ReportProviderTacFarmDashboard
# from datetime import date, datetime
# import uuid
# from decimal import Decimal
# from helpers import SessionContext,TypeConversion
# from models.factories import TacFactory
# from models import CurrentRuntime
# class ReportProviderTacFarmDashboardTest(TestCase):
#     def setUp(self):
#         CurrentRuntime.initialize()
#         session_context = SessionContext(dict())
#         self.report_provider = ReportProviderTacFarmDashboard(session_context)
#         self.tac = TacFactory.create()
#         self.tac_code = self.tac.code

#         self.page_number = 1
#         self.item_count_per_page = 10
#         self.order_by_column_name = ""
#         self.order_by_descending = False
#     def test_generate_list(self):
#         results = self.report_provider.generate_list(
#             self.tac_code,

#             self.page_number,
#             self.item_count_per_page,
#             self.order_by_column_name,
#             self.order_by_descending
#         )
#         self.assertIsInstance(results, list)
#         for result in results:
#             self.assertIsInstance(result, dict)
#             self.assertIn("field_one_plant_list_link_land_code", result)
#             self.assertIn("conditional_btn_example_link_land_code", result)
#             self.assertIn("is_conditional_btn_available", result)
#             # self.assertEqual(result["field_one__list_link_tac_code"], str(self.tacCode).replace('-', ''))

