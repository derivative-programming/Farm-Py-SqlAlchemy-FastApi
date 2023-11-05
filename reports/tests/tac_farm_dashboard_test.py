# from unittest import TestCase
# from unittest.mock import patch, MagicMock
# from reports import ReportManagerTacFarmDashboard, ReportRequestValidationError
# from reports.row_models import ReportItemTacFarmDashboard
# from datetime import date, datetime
# import uuid
# from decimal import Decimal
# from helpers import SessionContext,TypeConversion
# from models.factories import TacFactory
# from models import CurrentRuntime
# class ReportTestTacFarmDashboard(TestCase):
#     def setUp(self):
#         CurrentRuntime.initialize()
#         session_context = SessionContext(dict())
#         self.tac = TacFactory.create()
#         self.tac_code = self.tac.code

#         self.page_number = 1
#         self.item_count_per_page = 10
#         self.order_by_column_name = "code"
#         self.order_by_descending = False
#         self.report = ReportManagerTacFarmDashboard(session_context)
#     # @patch('farm.reports.providers.tac_farm_dashboard.ReportProviderTacFarmDashboard')
#     # def test_generate(self, MockProvider):
#     #     mock_provider = MockProvider.return_value
#     #     mock_provider.generate_list.return_value = [
#     #         {
#     #             "field_one_plant_list_link_land_code": uuid.UUID(self.field_one_plant_list_link_land_code)
#     #             "conditional_btn_example_link_land_code": uuid.UUID(self.conditional_btn_example_link_land_code)
#     #             "is_conditional_btn_available": bool(self.is_conditional_btn_available),
#     #         }
#     #     ]
#     #     result = self.report.generate(
#     #         self.tac_code,
#     #         self.page_number,
#     #         self.item_count_per_page,
#     #         self.order_by_column_name,
#     #         self.order_by_descending
#     #     )
#     #     self.assertIsInstance(result, list)
#     #     for item in result:
#     #         self.assertIsInstance(item, ReportItemTacFarmDashboard)
#     #         self.assertEqual(item.field_one__list_link_tac_code, self.tac_code)
#     #         self.assertEqual(item.conditional_btn_example_link_tac_code, self.tac_code)
#     #         self.assertEqual(item.is_conditional_btn_available, self.tac_code)
#     def test_generate_invalid_item_count_per_page(self):
#         with self.assertRaises(ReportRequestValidationError):
#             self.report.generate(
#                 self.tac_code,

#                 self.page_number,
#                 0,
#                 self.order_by_column_name,
#                 self.order_by_descending
#             )
#     def test_generate_invalid_page_number(self):
#         with self.assertRaises(ReportRequestValidationError):
#             self.report.generate(
#                 self.tac_code,

#                 0,
#                 self.item_count_per_page,
#                 self.order_by_column_name,
#                 self.order_by_descending
#             )

