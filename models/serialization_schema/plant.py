# plant.py

"""
    #TODO add comment
"""

from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import Plant


class PlantSchema(SQLAlchemyAutoSchema):
    """
    #TODO add comment
    """

    class Meta:
        """
            #TODO add comment
        """

        model = Plant
        exclude = (
            "_plant_id",
            "_code",
            "_insert_user_id",
            "_last_update_user_id",
            "_last_change_code",
            "_is_delete_allowed",  # isDeleteAllowed
            "_is_edit_allowed",  # isEditAllowed
            "_other_flavor",  # otherFlavor
            "_some_big_int_val",  # someBigIntVal
            "_some_bit_val",  # someBitVal
            # someDecimalVal,
            "_some_email_address",  # someEmailAddress
            # someFloatVal,
            "_some_int_val",  # someIntVal
            # someMoneyVal,
            "_some_var_char_val",  # someVarCharVal
            # someDateVal
            # someUTCDateTimeVal
            "_flvr_foreign_key_id",  # flvrForeignKeyID
            "_land_id",  # LandID
            "_some_n_var_char_val",  # someNVarCharVal
            "_some_phone_number",  # somePhoneNumber
            "_some_uniqueidentifier_val",  # someUniqueidentifierVal
            "_some_text_val",  # someTextVal
# endset  # noqa E122
        )

    plant_id = fields.Int()
    code = fields.UUID()
    last_change_code = fields.Int()
    insert_user_id = fields.UUID()
    last_update_user_id = fields.UUID()
    flvr_foreign_key_id = fields.Int()
    is_delete_allowed = fields.Bool()
    is_edit_allowed = fields.Bool()
    land_id = fields.Int()
    other_flavor = fields.Str()
    some_big_int_val = fields.Int()
    some_bit_val = fields.Bool()
    some_date_val = fields.Date()
    some_decimal_val = fields.Decimal(as_string=True)
    some_email_address = fields.Str()
    some_float_val = fields.Float()
    some_int_val = fields.Int()
    some_money_val = fields.Decimal(as_string=True)
    some_n_var_char_val = fields.Str()
    some_phone_number = fields.Str()
    some_text_val = fields.Str()
    some_uniqueidentifier_val = fields.UUID()
    some_utc_date_time_val = fields.DateTime()  # (format="%Y-%m-%dT%H:%M:%S")
    some_var_char_val = fields.Str()
    insert_utc_date_time = fields.DateTime()
    last_update_utc_date_time = fields.DateTime()

    flvr_foreign_key_code_peek = fields.UUID()   # FlvrForeignKeyID
    land_code_peek = fields.UUID()  # LandID
# endset
