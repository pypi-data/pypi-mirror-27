from unittest import TestCase
from ts_cli.rest_cli import RestCli


class TestRestCli(TestCase):
    def test_params_from_file(self):
        prms = RestCli.params_from_file('tests/resources/a.properties')
        self.assertEqual(prms, {'id': 'I=am Paf', 'some_num': '123456'})
