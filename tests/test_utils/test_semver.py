from ..app_test_case import AppTestCase

from nodebin.utils.semver import (
    _remove_x_in_nodesemver, _increase_nodesemver, _padding_nodesemver,
    nodesemver2range, check_nodesemver_validness
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

    def test_check_nodesemver_validness(self):
        self.assertEqual(check_nodesemver_validness('8'), True)
        self.assertEqual(check_nodesemver_validness('8.1'), True)
        self.assertEqual(check_nodesemver_validness('8.1.1'), True)
        self.assertEqual(check_nodesemver_validness('8.1.x'), True)
        self.assertEqual(check_nodesemver_validness('8.x'), True)
        self.assertEqual(check_nodesemver_validness('8.x.x'), True)
        self.assertEqual(check_nodesemver_validness('8.x.1'), True)
        self.assertEqual(check_nodesemver_validness('8.1.1.1'), False)
        self.assertEqual(check_nodesemver_validness('8.xx'), False)
        self.assertEqual(check_nodesemver_validness('8.x.x.x'), False)
        self.assertEqual(check_nodesemver_validness('8.x.xx'), False)
