'''Tests for __main__ methods'''
from unittest import TestCase, main as unit_main
from mock import patch, mock_open
import os.path as path
from os import remove
from dotapatch.__main__ import get_parser, dotapatch, main
from dotapatch.patch import Dotapatch
# from dotapatch.data import HeropediaData


class TestMain(TestCase):
    '''Tests main module'''

    def test_get_parser(self):
        '''main: assert get_parser() returns default values'''

        parser = get_parser()
        with patch('sys.argv', ['dotapatch', '706e', '707d']):
            args = parser.parse_args()

        changelog_list = args.changelogs
        template = args.template
        log_level = args.log_level
        save_log = args.save_log

        result = changelog_list == ['706e', '707d']
        result &= template == 'default'
        result &= log_level == 'INFO'
        result &= save_log is False

        self.assertTrue(result)

    def test_dotapatch(self):
        '''main: assert dotapatch() returns SUCCESS'''
        file_name = '706f'
        changelog = path.abspath(
            path.join('dotapatch', 'changelogs', file_name))
        status = dotapatch([changelog], 'default', None)
        remove(file_name + '.html')
        self.assertEqual(Dotapatch.SUCCESS, status)

    def test_main_changelog(self):
        '''main: assert main(changelog) exits with SUCCESS'''
        file_name = '706f'
        changelog = path.abspath(
            path.join('dotapatch', 'changelogs', file_name))
        with patch('sys.argv', ['dotapatch', changelog]):
            status = main(True)
        remove(file_name + '.html')
        self.assertEqual(Dotapatch.SUCCESS, status)

    def test_main_no_changelog(self):
        '''main: assert main() returns SUCCESS'''
        with patch('sys.argv', ['dotapatch']):
            status = main()
        self.assertEqual(Dotapatch.SUCCESS, status)

    # def test_update_data(self):
    #     '''main: assert dotapatch -u updates heropediadata'''

    #     # m = mock_open()
    #     with patch('sys.argv', ['dotapatch', '-u']):
    #         with patch('builtins.open', mock_open(), create=True):
    #             with patch('urllib.request.urlopen', autospec=True):
    #                 status = main(True)

    #     result = Dotapatch.SUCCESS == status
    #     # result = False

    #     # m.mock_calls

    # # item_data = path.join(HeropediaData.DATA_DIR, HeropediaData.ITEM_DATA)
    # # hero_data = path.join(HeropediaData.DATA_DIR, HeropediaData.HERO_DATA)

    #     # m.assert_called_once_with()
    #     # m.assert_called_once_with(hero_data)

    #     self.assertTrue(result)


if __name__ == '__main__':
    unit_main()
