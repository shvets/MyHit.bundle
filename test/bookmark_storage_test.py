# coding=utf-8

import test_helper

import unittest

import os
import json
from bookmark_storage import BookmarkStorage
from media_info import MediaInfo

class BookmarkStorageTest(unittest.TestCase):
    def setUp(self):
        self.subject = BookmarkStorage('test_storage.json')

        if os.path.exists(self.subject.file_name):
            os.remove(self.subject.file_name)

    def test_exist_if_not_exist(self):
        self.subject.exist()

        self.assertEqual(self.subject.exist(), False)


if __name__ == '__main__':
    unittest.main()
