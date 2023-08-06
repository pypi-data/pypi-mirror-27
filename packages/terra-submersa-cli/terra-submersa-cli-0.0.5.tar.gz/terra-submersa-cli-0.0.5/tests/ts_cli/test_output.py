from unittest import TestCase
from ts_cli.output import Output


class TestOutput(TestCase):
    list_objects_1 = [
        {'id': 1, 'text': 'abc', 'pipo': 42},
        {'id': 2334, 'text': 'abcde', 'pipo': 43444},
        {'id': 3, 'text': 'abcdefghj', 'pipo': 44},
    ]

    def test_select_fields_one(self):
        o = Output()

        sf = o.select_fields(self.list_objects_1, ['id'])

        self.assertEqual(sf, [{'id': 1}, {'id': 2334}, {'id': 3}])

    def test_select_fields_multiple(self):
        o = Output()

        sf = o.select_fields(self.list_objects_1, ['id', 'pipo'])

        self.assertEqual(sf, [{'id': 1, 'pipo': 42}, {'id': 2334, 'pipo': 43444}, {'id': 3, 'pipo': 44}])

    def test_to_text_column(self):
        o = Output()

        txt = o.to_text_column(self.list_objects_1, ['id', 'text', 'pipo'])

        self.assertEqual(txt, """1    abc       42\n2334 abcde     43444\n3    abcdefghj 44\n""")

    def test_to_text_column_max_super_large(self):
        o = Output()

        txt = o.to_text_column(self.list_objects_1, ['id', 'text', 'pipo'], max_char={'pipo': 100, 'text': 100})

        self.assertEqual(txt, """1    abc       42\n2334 abcde     43444\n3    abcdefghj 44\n""")

    def test_to_text_column_max(self):
        o = Output()

        txt = o.to_text_column(self.list_objects_1, ['id', 'text', 'pipo'], max_char={'text': 5})

        self.assertEqual(txt, """1    abc   42\n2334 abcde 43444\n3    ab... 44\n""")

