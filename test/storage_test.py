# coding=utf-8

import test_helper

import unittest

from storage import Storage
from media_info import MediaInfo

class StorageTest(unittest.TestCase):
    def setUp(self):
        self.subject = Storage()

    def test_add(self):
        self.subject.add(MediaInfo('video'))

        self.assertEqual(len(self.subject.items()), 1)

    def test_remove(self):
        self.subject.add(MediaInfo('video'))
        self.subject.remove(MediaInfo('video'))

        self.assertEqual(len(self.subject.items()), 0)

    def test_load(self):
        self.subject.load_storage = lambda : \
            [MediaInfo('video'), MediaInfo('video')]

        self.subject.load()

        self.assertEqual(len(self.subject.items()), 2)

    def test_save(self):
        self.subject.add(MediaInfo('video'))
        self.subject.add(MediaInfo('video'))

        self.subject.save_storage = lambda(items): \
            self.assertEqual(len(items), 2)

        self.subject.save()

if __name__ == '__main__':
    unittest.main()
