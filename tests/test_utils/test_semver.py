from ..app_test_case import AppTestCase

from nodebin.utils.semver import (
    _remove_x_in_nodesemver, _convert_caret_semver,
    _increase_nodesemver, _padding_nodesemver,
    nodesemver2range, is_nodesemver_valid
)


class TestSemver(AppTestCase):

    def test_remove_x_in_nodesemver(self):
        self.assertEqual(_remove_x_in_nodesemver('8.x'), '8')
        self.assertEqual(_remove_x_in_nodesemver('8.x.1'), '8')
        self.assertEqual(_remove_x_in_nodesemver('8.x.x'), '8')
        self.assertEqual(_remove_x_in_nodesemver('8'), '8')
        self.assertEqual(_remove_x_in_nodesemver('8.1.1'), '8.1.1')
        self.assertEqual(_remove_x_in_nodesemver('8.1.x'), '8.1')
        self.assertEqual(_remove_x_in_nodesemver('0.1.x'), '0.1')
        self.assertEqual(_remove_x_in_nodesemver('0.x'), '0')
        self.assertEqual(_remove_x_in_nodesemver('^1.2.x'), '^1.2')
        self.assertEqual(_remove_x_in_nodesemver('^0.0.x'), '^0.0')
        self.assertEqual(_remove_x_in_nodesemver('^1.x'), '^1')
        self.assertEqual(_remove_x_in_nodesemver('^0.x'), '^0')

    def test_convert_caret_semver(self):
        self.assertEqual(_convert_caret_semver('^1.2.3'), ('1.2.3', '1'))
        self.assertEqual(_convert_caret_semver('^0.2.3'), ('0.2.3', '0.2'))
        self.assertEqual(_convert_caret_semver('^0.0.3'), ('0.0.3', '0.0.3'))
        self.assertEqual(_convert_caret_semver('^1.2'), ('1.2', '1'))
        self.assertEqual(_convert_caret_semver('^0.0'), ('0.0', '0.0'))
        self.assertEqual(_convert_caret_semver('^1'), ('1', '1'))
        self.assertEqual(_convert_caret_semver('^0'), ('0', '0'))

    def test_increase_nodesemver(self):
        self.assertEqual(_increase_nodesemver('8.1'), '8.2')
        self.assertEqual(_increase_nodesemver('8'), '9')
        self.assertEqual(_increase_nodesemver('8.1.1'), '8.1.2')
        self.assertEqual(_increase_nodesemver('0.1'), '0.2')
        self.assertEqual(_increase_nodesemver('0'), '1')
        self.assertEqual(_increase_nodesemver('0.0'), '0.1')

    def test_padding_nodesemver(self):
        self.assertEqual(_padding_nodesemver('8'), '8.0.0')
        self.assertEqual(_padding_nodesemver('8.1'), '8.1.0')
        self.assertEqual(_padding_nodesemver('8.1.1'), '8.1.1')
        self.assertEqual(_padding_nodesemver('0.1'), '0.1.0')

    def test_nodesemver2range(self):
        self.assertEqual(nodesemver2range('8'), ('8.0.0', '9.0.0'))
        self.assertEqual(nodesemver2range('8.x'), ('8.0.0', '9.0.0'))
        self.assertEqual(nodesemver2range('8.x.1'),  ('8.0.0', '9.0.0'))
        self.assertEqual(nodesemver2range('8.1.1'), ('8.1.1', '8.1.2'))
        self.assertEqual(nodesemver2range('8.1'), ('8.1.0', '8.2.0'))
        self.assertEqual(nodesemver2range('^1.2.3'), ('1.2.3', '2.0.0'))
        self.assertEqual(nodesemver2range('^0.2.3'), ('0.2.3', '0.3.0'))
        self.assertEqual(nodesemver2range('^0.0.3'), ('0.0.3', '0.0.4'))
        self.assertEqual(nodesemver2range('^1.2.x'), ('1.2.0', '2.0.0'))
        self.assertEqual(nodesemver2range('^0.0.x'), ('0.0.0', '0.1.0'))
        self.assertEqual(nodesemver2range('^0.0'), ('0.0.0', '0.1.0'))
        self.assertEqual(nodesemver2range('^1.x'), ('1.0.0', '2.0.0'))
        self.assertEqual(nodesemver2range('^0.x'), ('0.0.0', '1.0.0'))

    def test_is_nodesemver_valid(self):
        self.assertEqual(is_nodesemver_valid('8'), True)
        self.assertEqual(is_nodesemver_valid('8.1'), True)
        self.assertEqual(is_nodesemver_valid('8.1.1'), True)
        self.assertEqual(is_nodesemver_valid('8.1.x'), True)
        self.assertEqual(is_nodesemver_valid('8.x'), True)
        self.assertEqual(is_nodesemver_valid('8.x.x'), True)
        self.assertEqual(is_nodesemver_valid('8.x.1'), True)
        self.assertEqual(is_nodesemver_valid('8.1.1.1'), False)
        self.assertEqual(is_nodesemver_valid('8.xx'), False)
        self.assertEqual(is_nodesemver_valid('8.x.x.x'), False)
        self.assertEqual(is_nodesemver_valid('8.x.xx'), False)

        self.assertEqual(is_nodesemver_valid('^1.2'), True)
        self.assertEqual(is_nodesemver_valid('^1.2.2'), True)
        self.assertEqual(is_nodesemver_valid('^1'), True)
        self.assertEqual(is_nodesemver_valid('^0'), True)
        self.assertEqual(is_nodesemver_valid('^1.x'), True)
        self.assertEqual(is_nodesemver_valid('^1.x.1'), True)
        self.assertEqual(is_nodesemver_valid('^1.x.x'), True)
        self.assertEqual(is_nodesemver_valid('^1.xx'), False)
        self.assertEqual(is_nodesemver_valid('^1.x.x.x'), False)
        self.assertEqual(is_nodesemver_valid('^1.x.xx'), False)
