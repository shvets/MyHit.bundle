# coding=utf-8

import test_helper

import unittest

import os
import json
from file_storage import FileStorage
from media_info import MediaInfo

class FileStorageTest(unittest.TestCase):
    def setUp(self):
        self.subject = FileStorage('test_storage.json')

    def tearDown(self):
        if os.path.exists(self.subject.file_name):
            os.remove(self.subject.file_name)

    def test_exist_if_not_exist(self):
        self.subject.exist()

        self.assertEqual(self.subject.exist(), False)

    def test_exist_if_exist(self):
        open(self.subject.file_name, "w").write("")

        self.subject.exist()

        self.assertEqual(self.subject.exist(), True)

        os.remove(self.subject.file_name)

    def test_load(self):
        data = [MediaInfo(), MediaInfo()]
        open(self.subject.file_name, "w").write(json.dumps(data))

        self.subject.load()

        self.assertEqual(len(self.subject.items()), 2)

        os.remove(self.subject.file_name)

    def test_save(self):
        self.subject.add(MediaInfo())
        self.subject.add(MediaInfo())

        self.subject.save()

        self.assertEqual(len(self.subject.items()), 2)

if __name__ == '__main__':
    unittest.main()
