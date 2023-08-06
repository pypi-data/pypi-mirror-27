import unittest

from jsonschema import ValidationError

from anji_orm import ValidableJsonField, Model


class T1(Model):

    _table = 'non_table'

    c1 = ValidableJsonField({
        "type": "object",
        "properties": {
            "price": {"type": "number"},
            "name": {"type": "string"},
        }
    })


class FieldValidationTest(unittest.TestCase):

    def test_validation(self) -> None:
        t1 = T1()
        with self.assertRaises(ValidationError) as cm:
            t1.c1 = {'price': 5, 'name': 6}
            self.assertEqual(cm.exception.message, "6 is not of type 'string'")
        good_value = {'price': 5, 'name': 't1'}
        t1.c1 = good_value
        self.assertEqual(good_value, t1.c1)
