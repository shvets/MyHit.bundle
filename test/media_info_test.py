# coding=utf-8

import test_helper

import unittest

from media_info import MediaInfo

class MediaInfoTest(unittest.TestCase):

    def test_create_media_info_no_params(self):
        media_info = MediaInfo('video')

        self.assertEqual(media_info['type'], 'video')
        print(media_info)

    def test_create_media_info_with_params(self):
        media_info = MediaInfo('video', path='path', name='name')

        self.assertEqual(media_info['type'], 'video')
        self.assertEqual(media_info['path'], 'path')
        self.assertEqual(media_info['name'], 'name')
        print(media_info)

if __name__ == '__main__':
    unittest.main()
