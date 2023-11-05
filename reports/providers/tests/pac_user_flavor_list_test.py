# from django.test import TestCase
# from reports.providers import ReportProviderPacUserFlavorList
# from datetime import date, datetime
# import uuid
# from decimal import Decimal
# from helpers import SessionContext,TypeConversion
# from models.factories import PacFactory
# from models import CurrentRuntime
# class ReportProviderPacUserFlavorListTest(TestCase):
#     def setUp(self):
#         CurrentRuntime.initialize()
#         session_context = SessionContext(dict())
#         self.report_provider = ReportProviderPacUserFlavorList(session_context)
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
#             self.assertIn("flavor_code", result)
#             self.assertIn("flavor_description", result)
#             self.assertIn("flavor_display_order", result)
#             self.assertIn("flavor_is_active", result)
#             self.assertIn("flavor_lookup_enum_name", result)
#             self.assertIn("flavor_name", result)
#             self.assertIn("pac_name", result)
#             # self.assertEqual(result["field_one_flavor_list_link_pac_code"], str(self.pacCode).replace('-', ''))

