# coding=utf-8

import test_helper

import unittest

from media_info import MediaInfo

class MediaInfoTest(unittest.TestCase):

    def test_create_media_info_no_params(self):
        media_info = MediaInfo()

        self.assertEqual(media_info['type'], 'movie')

    def test_create_media_info_with_params(self):
        media_info = MediaInfo(path='path', name='name')

        self.assertEqual(media_info['type'], 'movie')
        self.assertEqual(media_info['path'], 'path')
        self.assertEqual(media_info['name'], 'name')

if __name__ == '__main__':
    unittest.main()
