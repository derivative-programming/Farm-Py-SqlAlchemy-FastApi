# from django.test import TestCase
# from reports.providers import ReportProviderPacUserTriStateFilterList
# from datetime import date, datetime
# import uuid
# from decimal import Decimal
# from helpers import SessionContext,TypeConversion
# from models.factories import PacFactory
# from models import CurrentRuntime
# class ReportProviderPacUserTriStateFilterListTest(TestCase):
#     def setUp(self):
#         CurrentRuntime.initialize()
#         session_context = SessionContext(dict())
#         self.report_provider = ReportProviderPacUserTriStateFilterList(session_context)
#         self.pac = PacFactory.create()
#         self.pac_code = self.pac.code

#         self.page_number = 1
#         self.item_count_per_page = 10
#         self.order_by_column_name = ""
#         self.order_by_descending = False
#     def test_generate_list(self):
#         results = self.report_provider.generate_list(
#             self.pac_code,

#             self.page_number,
#             self.item_count_per_page,
#             self.order_by_column_name,
#             self.order_by_descending
#         )
#         self.assertIsInstance(results, list)
#         for result in results:
#             self.assertIsInstance(result, dict)
#             self.assertIn("tri_state_filter_code", result)
#             self.assertIn("tri_state_filter_description", result)
#             self.assertIn("tri_state_filter_display_order", result)
#             self.assertIn("tri_state_filter_is_active", result)
#             self.assertIn("tri_state_filter_lookup_enum_name", result)
#             self.assertIn("tri_state_filter_name", result)
#             self.assertIn("tri_state_filter_state_int_value", result)
#             # self.assertEqual(result["field_one_tri_state_filter_list_link_pac_code"], str(self.pacCode).replace('-', ''))

