# from unittest import TestCase
# from unittest.mock import patch, MagicMock
# from reports import ReportManagerPacUserLandList, ReportRequestValidationError
# from reports.row_models import ReportItemPacUserLandList
# from datetime import date, datetime
# import uuid
# from decimal import Decimal
# from helpers import SessionContext,TypeConversion
# from models.factories import PacFactory
# from models import CurrentRuntime
# class ReportTestPacUserLandList(TestCase):
#     def setUp(self):
#         CurrentRuntime.initialize()
#         session_context = SessionContext(dict())
#         self.pac = PacFactory.create()
#         self.pac_code = self.pac.code

#         self.page_number = 1
#         self.item_count_per_page = 10
#         self.order_by_column_name = "code"
#         self.order_by_descending = False
#         self.report = ReportManagerPacUserLandList(session_context)
#     # @patch('farm.reports.providers.pac_user_land_list.ReportProviderPacUserLandList')
#     # def test_generate(self, MockProvider):
#     #     mock_provider = MockProvider.return_value
#     #     mock_provider.generate_list.return_value = [
#     #         {
#     #             "land_code": uuid.UUID(self.land_code),
#     #             "land_description": str(self.land_description),
#     #             "land_display_order": int(self.land_display_order),
#     #             "land_is_active": bool(self.land_is_active),
#     #             "land_lookup_enum_name": str(self.land_lookup_enum_name),
#     #             "land_name": str(self.land_name),
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
#     #         self.assertIsInstance(item, ReportItemPacUserLandList)
#     #         self.assertEqual(item.field_one_land_list_link_pac_code, self.pac_code)
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

