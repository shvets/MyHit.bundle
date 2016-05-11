# coding=utf-8

import test_helper

import unittest

from storage import Storage
from media_info import MediaInfo

class StorageTest(unittest.TestCase):
    def setUp(self):
        self.subject = Storage()

    def test_add(self):
        self.subject.add(MediaInfo())

        self.assertEqual(len(self.subject.items()), 1)

    def test_remove(self):
        self.subject.add(MediaInfo())
        self.subject.remove(MediaInfo())

        self.assertEqual(len(self.subject.items()), 0)

    def test_load(self):
        self.subject.load_storage = lambda : \
            [MediaInfo(), MediaInfo()]

        self.subject.load()

        self.assertEqual(len(self.subject.items()), 2)

    def test_save(self):
        self.subject.add(MediaInfo())
        self.subject.add(MediaInfo())

        self.subject.save_storage = lambda(items): \
            self.assertEqual(len(items), 2)

        self.subject.save()

    def test_sanitize(self):
        item = MediaInfo(season=None)

        Storage.sanitize(item)

        self.assertEqual('season' in item, False)

if __name__ == '__main__':
    unittest.main()
