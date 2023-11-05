# from unittest import TestCase
# from unittest.mock import patch, MagicMock
# from reports import ReportManagerPacUserFlavorList, ReportRequestValidationError
# from reports.row_models import ReportItemPacUserFlavorList
# from datetime import date, datetime
# import uuid
# from decimal import Decimal
# from helpers import SessionContext,TypeConversion
# from models.factories import PacFactory
# from models import CurrentRuntime
# class ReportTestPacUserFlavorList(TestCase):
#     def setUp(self):
#         CurrentRuntime.initialize()
#         session_context = SessionContext(dict())
#         self.pac = PacFactory.create()
#         self.pac_code = self.pac.code

#         self.page_number = 1
#         self.item_count_per_page = 10
#         self.order_by_column_name = "code"
#         self.order_by_descending = False
#         self.report = ReportManagerPacUserFlavorList(session_context)
#     # @patch('farm.reports.providers.pac_user_flavor_list.ReportProviderPacUserFlavorList')
#     # def test_generate(self, MockProvider):
#     #     mock_provider = MockProvider.return_value
#     #     mock_provider.generate_list.return_value = [
#     #         {
#     #             "flavor_code": uuid.UUID(self.flavor_code),
#     #             "flavor_description": str(self.flavor_description),
#     #             "flavor_display_order": int(self.flavor_display_order),
#     #             "flavor_is_active": bool(self.flavor_is_active),
#     #             "flavor_lookup_enum_name": str(self.flavor_lookup_enum_name),
#     #             "flavor_name": str(self.flavor_name),
#     #             "pac_name": str(self.pac_name),
#     #         }
#     #     ]
#     #     result = self.report.generate(
#     #         self.pac_code,
#     #         self.page_number,
#     #         self.item_count_per_page,
#     #         self.order_by_column_name,
#     #         self.order_by_descending
#     #     )
#     #     self.assertIsInstance(result, list)
#     #     for item in result:
#     #         self.assertIsInstance(item, ReportItemPacUserFlavorList)
#     #         self.assertEqual(item.field_one_flavor_list_link_pac_code, self.pac_code)
#     #         self.assertEqual(item.conditional_btn_example_link_pac_code, self.pac_code)
#     #         self.assertEqual(item.is_conditional_btn_available, self.pac_code)
#     def test_generate_invalid_item_count_per_page(self):
#         with self.assertRaises(ReportRequestValidationError):
#             self.report.generate(
#                 self.pac_code,

#                 self.page_number,
#                 0,
#                 self.order_by_column_name,
#                 self.order_by_descending
#             )
#     def test_generate_invalid_page_number(self):
#         with self.assertRaises(ReportRequestValidationError):
#             self.report.generate(
#                 self.pac_code,

#                 0,
#                 self.item_count_per_page,
#                 self.order_by_column_name,
#                 self.order_by_descending
#             )

